from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_1, SDLK_2, SDLK_3, SDLK_4, SDLK_5, SDLK_6

import random
import game_world
import game_framework
from state_machine import StateMachine
from door import Door
from item import Item
from tang import Tang

# 달리기 시간
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
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

    def draw(self):
        x = self.girl.x - game_framework.camera_x
        y = self.girl.y - game_framework.camera_y

        if self.girl.face_dir == 1:  # right
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 0, 48, 48, x, y,100,100)
        else:  # face_dir == -1: # left
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 144, 48, 48, x, y,100,100)


class Run:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.girl.dir = self.girl.face_dir = 1
        elif left_down(e) or right_up(e):
            self.girl.dir = self.girl.face_dir = -1

    def exit(self, e):
        pass
    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.girl.x += self.girl.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.girl.x = clamp(25, self.girl.x, 2400 - 30)

    def draw(self):
        x = self.girl.x - game_framework.camera_x
        y = self.girl.y - game_framework.camera_y

        if self.girl.face_dir == 1:  # right
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 48, 48, 48, x, y,100,100)
        else:  # face_dir == -1: # left
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 96, 48, 48, x, y,100,100)



class Girl:
    def __init__(self):
        self.face_dir = 1
        self.x, self.y = 50, 90
        self.frame = 0
        self.image = load_image('girl.png')
        self.item_collision = None
        self.door_collision = None

        self.hp = 40
        self.mp = 80

        self.inventory = []
        self.inventory_size = 2

        self.is_bag = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.RUN, left_down: self.RUN,
                            right_up: self.RUN, left_up: self.RUN},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE,
                           left_down: self.IDLE}
            }
        )
    def update(self):
        self.item_collision = None
        #self.door_collision = None
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if self.door_collision and abs(self.x - self.door_collision.x) < 110:
                door = self.door_collision
                target_item = None
                #2스테이지 로직
                if door.door_id == 2:
                    for item in self.inventory:
                        if item.item_type == 'board':
                            target_item = item
                            break
                else:
                    #1스테이지 로직
                    for item in self.inventory:
                        if (item.item_type == 'card' or item.item_type == 'card_purple'
                                or item.item_type == 'card_ora'):
                            target_item = item
                            break
                if target_item:
                    print(f"아이템 사용: {target_item.item_type}")
                    self.inventory.remove(target_item)  # 아이템 사용
                    door.unlock()  # 문 열기
                    self.door_collision = None  # 상호작용 종료

                    #문?을 열면 배경이 바뀜.
                    if 'background' in game_framework.share:
                        game_framework.share['background'].change_background()
                        print("배경 변경")

                    # 다음 스테이지로 이동
                    if door.stage:
                        game_framework.change_mode(door.stage)
                else:
                    print("필요한 아이템 없음")

            elif self.item_collision:
                item = self.item_collision
                if item.item_type == 'bag':
                    new_slots = item.value  # 아이템에 저장된 값 (4)
                    self.inventory_size += new_slots
                    self.is_bag = True
                    print("인벤토리 증가")

                    item.collect()  # 가방 월드에서 제거
                    self.item_collision = None
                    return

                if len(self.inventory) < self.inventory_size:
                    print(f"{item.item_type} 획득")

                    # 아이템 타입별로 인벤토리에 넣기
                    if item.item_type == 'board':
                        self.inventory.append(item)
                    elif item.item_type == 'card':
                        self.inventory.append(Item(0, 0, 0, 16, 'card', 20))
                    elif item.item_type == 'card_purple':
                        self.inventory.append(Item(0, 0, 16, 16, 'card_purple', 20))
                    elif item.item_type == 'card_ora':
                        self.inventory.append(Item(0, 0, 32, 16, 'card_ora', 20))
                    elif item.item_type == 'clothes':
                        self.inventory.append(Item(0, 0, 0, 0, 'clothes', 20))
                    elif item.item_type == 'star':
                        self.inventory.append(Item(0, 0, 32, 16, 'star', 10))
                    elif item.item_type == 'gun':
                        self.inventory.append(item)
                    else:
                        self.inventory.append(item)

                    item.collect()
                    self.item_collision = None
                else:
                    print("인벤토리 가득 참")

                return

        # 1번 키로 1번 슬롯 아이템 사용
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            self.use_item(0)  # 0번 아이템 사용
            return

        # 2번 키로 2번 슬롯 아이템 사용
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            self.use_item(1)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            self.use_item(2)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            self.use_item(3)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            self.use_item(4)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_6:
            self.use_item(5)
            return
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            have_gun = False
            for item in self.inventory:
                if item.item_type == 'gun':
                    have_gun = True
                    break

            if have_gun:
                print('yes gun')
                tang = Tang(self.x, self.y, self.face_dir*TANG_SPEED_PPS)
                game_world.add_object(tang,1)

                game_world.add_collision_pair('tang:boss', tang, None)
            else:
                print('no gun')
                return



        self.state_machine.handle_state_event(('INPUT', event))

    def handle_collision(self, group, other):
        if group == 'missile:girl':
            print("hit")
            #game_framework.quit()
        elif group == 'girl:item':
            #print("item get")
            self.item_collision = other

        elif group == 'girl:door':
            print("door close")
            self.door_collision = other

            left, bottom, right, top = other.get_bb()
            cur_dir = self.face_dir
            if cur_dir > 0:
                self.x = left -50
            else:
                self.x = right + 50


    def get_bb(self):
        return self.x - 35, self.y - 50, self.x + 50, self.y + 50

    def use_item(self, index):

        if len(self.inventory) > index:
            item_to_check = self.inventory[index]

            if (item_to_check.item_type == 'card' or item_to_check.item_type == 'clothes'
                    or item_to_check.item_type == 'card_purple'
                    or item_to_check.item_type == 'card_ora'
                    or item_to_check.item_type == 'star'
                    or item_to_check.item_type == 'board'
                    or item_to_check.item_type == 'gun'):
                return

            item_to_use = self.inventory.pop(index)
            item_type = item_to_use.item_type
            value = item_to_use.value

            print(f"Using item slot {index + 1} ({item_type})")

            if item_type == 'hp':
                self.hp = min(80, self.hp + value)
            elif item_type == 'mp':
                self.mp = min(80, self.mp + value)

        else:
            print(f"Slot {index + 1} x ")  # 디버그용