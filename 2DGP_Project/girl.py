from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_1, SDLK_2, SDLK_3, SDLK_4, SDLK_5, \
    SDLK_6

import random
import game_world
import game_framework
from state_machine import StateMachine
from door import Door
from item import Item
from tang import Tang

# 달리기 시간
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 액션 시간
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

# 총 속도
TANG_SPEED_PPS = 500


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class Idle:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        # 방향키가 눌려있으면(dir이 0이 아니면) RUN으로 전환
        if self.girl.dir != 0:
            self.girl.state_machine.cur_state = self.girl.RUN
            self.girl.RUN.enter(None)

    def draw(self):
        x = self.girl.x - game_framework.camera_x
        y = self.girl.y - game_framework.camera_y

        if self.girl.face_dir == 1:  # right
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 0, 48, 48, x, y, 100, 100)
        else:  # left
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 144, 48, 48, x, y, 100, 100)


class Run:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.girl.x += self.girl.dir * self.girl.speed_pps * game_framework.frame_time
        self.girl.x = clamp(25, self.girl.x, self.girl.bg_width - 30)

        # 멈췄으면(dir이 0이면) IDLE로 전환
        if self.girl.dir == 0:
            self.girl.state_machine.cur_state = self.girl.IDLE
            self.girl.IDLE.enter(None)

    def draw(self):
        x = self.girl.x - game_framework.camera_x
        y = self.girl.y - game_framework.camera_y

        if self.girl.face_dir == 1:
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 48, 48, 48, x, y, 100, 100)
        else:
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 96, 48, 48, x, y, 100, 100)


class Girl:
    def __init__(self):
        self.dir = 0
        self.face_dir = 1
        self.x, self.y = 50, 90
        self.frame = 0
        self.image = load_image('girl.png')
        self.item_collision = None
        self.door_collision = None

        self.hp = 80
        self.mp = 80
        self.mp_timer = 0
        self.no_attack_timer = 0
        self.speed_pps = RUN_SPEED_PPS

        self.bg_width = 2400

        self.key_state = {'left': False, 'right': False}

        if 'inventory' in game_framework.share:
            self.inventory = game_framework.share['inventory']
        else:
            self.inventory = []

        if 'inventory_size' in game_framework.share:
            self.inventory_size = game_framework.share['inventory_size']
        else:
            self.inventory_size = 2

        if 'is_bag' in game_framework.share:
            self.is_bag = game_framework.share['is_bag']
        else:
            self.is_bag = False

        if 'is_second_bag' in game_framework.share:
            self.is_second_bag = game_framework.share['is_second_bag']
        else:
            self.is_second_bag = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)

        # [수정] 상태 머신의 자동 전환 설정을 비웠습니다. (충돌 방지)
        # 이제 handle_event와 do 함수가 직접 상태를 관리합니다.
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {},
                self.RUN: {}
            }
        )

    def update(self):
        self.item_collision = None
        self.state_machine.update()

        if self.mp < 80:
            self.mp_timer += game_framework.frame_time
            if self.mp_timer >= 2.0:
                self.mp += 10
                if self.mp > 80: self.mp = 80
                self.mp_timer = 0
        else:
            self.mp_timer = 0

        if self.no_attack_timer > 0:
            self.no_attack_timer -= game_framework.frame_time
            if self.no_attack_timer < 0:
                self.no_attack_timer = 0

    def draw(self):
        self.state_machine.draw()
        l, b, r, t = self.get_bb()
        l -= game_framework.camera_x
        b -= game_framework.camera_y
        r -= game_framework.camera_x
        t -= game_framework.camera_y
        draw_rectangle(l, b, r, t)

    def handle_event(self, event):
        # 1. 키 입력 상태 갱신
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.key_state['right'] = True
            elif event.key == SDLK_LEFT:
                self.key_state['left'] = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.key_state['right'] = False
            elif event.key == SDLK_LEFT:
                self.key_state['left'] = False

        # 2. 방향 및 바라보는 곳 계산
        self.dir = 0
        if self.key_state['right']:
            self.dir += 1
        if self.key_state['left']:
            self.dir -= 1

        # [중요] 바라보는 방향 즉시 갱신
        if self.dir != 0:
            self.face_dir = self.dir

        # 3. 상태 머신 이벤트 전달 (공격 등 다른 키 처리용)
        self.state_machine.handle_state_event(('INPUT', event))

        # 4. 스페이스바 및 아이템 사용 등 기타 키 처리
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if self.door_collision and abs(self.x - self.door_collision.x) < 110:
                door = self.door_collision
                target_item = None

                if door.door_id == 0:
                    print("보스방 통과")
                    if door.stage:
                        game_framework.share['inventory'] = self.inventory
                        game_framework.share['inventory_size'] = self.inventory_size
                        game_framework.share['is_bag'] = self.is_bag
                        game_framework.share['is_second_bag'] = self.is_second_bag
                        game_framework.change_mode(door.stage)
                    return

                if door.door_id == 2:
                    for item in self.inventory:
                        if item.item_type == 'board':
                            target_item = item
                            break
                else:
                    for item in self.inventory:
                        if item.item_type in ['card', 'card_purple', 'card_ora']:
                            target_item = item
                            break

                if target_item:
                    print(f"아이템 사용: {target_item.item_type}")
                    self.inventory.remove(target_item)
                    door.unlock()
                    self.door_collision = None

                    if 'background' in game_framework.share:
                        game_framework.share['background'].change_background()

                    if door.stage:
                        game_framework.share['inventory'] = self.inventory
                        game_framework.share['inventory_size'] = self.inventory_size
                        game_framework.share['is_bag'] = self.is_bag
                        game_framework.share['is_second_bag'] = self.is_second_bag
                        game_framework.change_mode(door.stage)
                else:
                    print("필요한 아이템 없음")

            elif self.item_collision:
                item = self.item_collision
                special_items = ['gun', 'clothes', 'shoes']
                current_special_count = 0
                current_normal_count = 0

                for inv_item in self.inventory:
                    if inv_item.item_type in special_items:
                        current_special_count += 1
                    else:
                        current_normal_count += 1

                if item.item_type == 'bag':
                    self.inventory_size = 6
                    self.is_bag = True
                    game_framework.share['inventory_size'] = 6
                    game_framework.share['is_bag'] = True
                    item.collect()
                    self.item_collision = None
                    return

                if item.item_type in special_items:
                    if not self.is_second_bag:
                        self.is_second_bag = True
                        game_framework.share['is_second_bag'] = True

                    if current_special_count < 4:
                        self.inventory.append(item)
                        item.collect()
                        self.item_collision = None
                        if item.item_type == 'gun':
                            if 'popup' in game_framework.share:
                                game_framework.share['popup'].show('story_image/a.png', 2.0)
                        if item.item_type == 'clothes':
                            self.speed_pps = RUN_SPEED_PPS * 1.5
                        elif item.item_type == 'shoes':
                            self.speed_pps = RUN_SPEED_PPS * 2.0
                    else:
                        print("특수 아이템 슬롯 가득 참")
                    return

                if current_normal_count < self.inventory_size:
                    if item.item_type == 'board':
                        self.inventory.append(item)
                    elif item.item_type == 'card':
                        self.inventory.append(Item(0, 0, 0, 16, 'card', 20))
                    elif item.item_type == 'card_purple':
                        self.inventory.append(Item(0, 0, 16, 16, 'card_purple', 20))
                    elif item.item_type == 'card_ora':
                        self.inventory.append(Item(0, 0, 32, 16, 'card_ora', 20))
                    elif item.item_type == 'star':
                        self.inventory.append(Item(0, 0, 32, 16, 'star', 10))
                    else:
                        self.inventory.append(item)
                    item.collect()
                    self.item_collision = None
                else:
                    print(f"인벤토리 가득 참")
                return

        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            self.use_item(0)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            self.use_item(1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            self.use_item(2)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            self.use_item(3)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            self.use_item(4)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_6:
            self.use_item(5)

        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            have_gun = False
            for item in self.inventory:
                if item.item_type == 'gun':
                    have_gun = True
                    break
            if have_gun:
                if self.mp >= 10:
                    self.mp -= 10
                    tang = Tang(self.x, self.y, self.face_dir * TANG_SPEED_PPS)
                    game_world.add_object(tang, 1)

                    game_world.add_collision_pair('tang:boss', tang, None)
                else:
                    print('no mp')
            else:
                print('no gun')
                return

    def handle_collision(self, group, other):
        import stage3_mode
        import logo_mode

        if group == 'missile:girl':
            print("hit")
            self.hp -= 10
            if self.hp <= 0:
                print("Game Over")
                self.hp = 80
                game_framework.share['inventory'] = self.inventory
                game_framework.share['inventory_size'] = self.inventory_size
                game_framework.share['is_bag'] = self.is_bag
                game_framework.share['is_second_bag'] = self.is_second_bag
                if game_framework.stack[-1] == stage3_mode:
                    game_framework.change_mode(stage3_mode)
                else:
                    game_framework.change_mode(logo_mode)

        elif group == 'girl:item':
            self.item_collision = other

        elif group == 'girl:door':
            if other.door_id == 0:
                print("포탈 진입")
                if other.stage:
                    game_framework.share['inventory'] = self.inventory
                    game_framework.share['inventory_size'] = self.inventory_size
                    game_framework.share['is_bag'] = self.is_bag
                    game_framework.share['is_second_bag'] = self.is_second_bag
                    game_framework.change_mode(other.stage)
                return
            self.door_collision = other
            left, bottom, right, top = other.get_bb()
            if self.face_dir > 0:
                self.x = left - 50
            else:
                self.x = right + 50

        elif group == 'boss:girl':
            if self.no_attack_timer <= 0:
                self.hp -= 10
                self.no_attack_timer = 1.0
                if self.hp <= 0:
                    print("Game Over")
                    self.hp = 80
                    game_framework.share['inventory'] = self.inventory
                    game_framework.share['inventory_size'] = self.inventory_size
                    game_framework.share['is_bag'] = self.is_bag
                    game_framework.share['is_second_bag'] = self.is_second_bag
                    if game_framework.stack[-1] == stage3_mode:
                        game_framework.change_mode(stage3_mode)
                    else:
                        game_framework.change_mode(logo_mode)

    def get_bb(self):
        return self.x - 35, self.y - 50, self.x + 50, self.y + 50

    def use_item(self, index):
        normal_items = []
        for i, item in enumerate(self.inventory):
            if item.item_type not in ['gun', 'clothes', 'shoes']:
                normal_items.append((item, i))

        if index < len(normal_items):
            item, real_index = normal_items[index]
            if item.item_type == 'hp':
                self.hp = min(80, self.hp + item.value)
                self.inventory.pop(real_index)
            elif item.item_type == 'mp':
                self.mp = min(80, self.mp + item.value)
                self.inventory.pop(real_index)
            else:
                print(f"'{item.item_type}' 사용 불가")
        else:
            print("아이템 없음")

    def reset_collision_info(self):
        self.item_collision = None
        self.door_collision = None
        self.state_machine.cur_state = self.IDLE

    def reset_state(self):
        self.key_state = {'left': False, 'right': False}
        self.dir = 0
        self.state_machine.cur_state = self.IDLE
        self.face_dir = 1
        print("상태 리셋: IDLE")