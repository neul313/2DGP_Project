from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_1, SDLK_2, SDLK_3, SDLK_4, SDLK_5, SDLK_6

import random
import game_world
import game_framework
from state_machine import StateMachine

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
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('girl.png')
        self.item_collision = None

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
        #self.item_collision = None
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if self.item_collision:

                # ❗ 1. 줍는 아이템이 'bag'인지 먼저 확인
                item = self.item_collision
                if item.item_type == 'bag':
                    new_slots = item.value  # 아이템에 저장된 값 (4)
                    self.inventory_size += new_slots
                    self.is_bag = True  # ❗ 가방 플래그를 True로 변경
                    print(f"가방 업그레이드! 인벤토리 크기: {self.inventory_size}")

                    item.collect()  # 가방 월드에서 제거
                    self.item_collision = None
                    return  # 'bag'은 인벤에 넣지 않고 종료

                # ❗ 2. 'bag'가 아니면 (hp, mp 등) 인벤토리에 추가
                if len(self.inventory) < self.inventory_size:
                    self.inventory.append(item)  # 인벤에 아이템 추가
                    item.collect()  # 화면상 아이템 제거
                    self.item_collision = None
                return

            # 1번 키로 1번 슬롯 아이템 사용
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            self.use_item(0)  # 0번 아이템 사용
            return

            # 2번 키로 2번 슬롯 아이템 사용
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            self.use_item(1)
            return

        self.state_machine.handle_state_event(('INPUT', event))

    def handle_collision(self, group, other):
        if group == 'missile:girl':
            print("hit")
            #game_framework.quit()
        elif group == 'girl:item':
            print("item get")
            self.item_collision = other

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def use_item(self, index):
        # ❗ 1. 오류가 나던 'bag' 블록 완전 삭제

        # ❗ 2. 인벤토리에서 아이템을 꺼내는 로직만 남김
        if len(self.inventory) > index:
            # 인벤토리에서 아이템을 꺼냄
            item_to_use = self.inventory.pop(index)

            item_type = item_to_use.item_type
            value = item_to_use.value

            print(f"Using item from slot {index + 1} ({item_type})")

            # 아이템 효과 적용
            if item_type == 'hp':
                self.hp = min(80, self.hp + value)
            elif item_type == 'mp':
                self.mp = min(80, self.mp + value)
            # ❗ 'bag'는 인벤토리에 들어오지 않으므로, 여기서 bag 관련 로직 삭제

        else:
            print(f"Slot {index + 1} x ")  # 디버그용