from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_1, SDLK_2, SDLK_3, SDLK_4, SDLK_5, SDLK_6

import random
import game_world
import game_framework
from state_machine import StateMachine
from door import Door
from item import Item

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
        self.door_collision = None
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if self.door_collision:
                door = self.door_collision

                # 인벤토리에서 card 아이템 검색
                card_found = None
                for item_in_inventory in self.inventory:
                    if item_in_inventory.item_type == 'card':
                        card_found = item_in_inventory
                        break  # 카드 찾음

                if card_found:
                    print("Card use.")
                    self.inventory.remove(card_found)

                    door.unlock()
                    self.door_collision = None  # 상호작용 완료
                else:
                    print("lock.")

                return

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

                if item.item_type == 'card':
                    if len(self.inventory) < self.inventory_size:
                        print("반짝이")

                        item.collect()
                        self.item_collision = None

                        # 새로운 'card' 아이템을 생성하여 인벤토리에 추가
                        new_card = Item(0, 0, 0, 16, 'card', 20)
                        self.inventory.append(new_card)
                        return
                    else:
                        return

                elif item.item_type == 'clothes':
                    if len(self.inventory) < self.inventory_size:
                        print("반짝이")

                        item.collect()
                        self.item_collision = None

                        new_cloth = Item(0, 0, 0, 0, 'clothes', 20)
                        self.inventory.append(new_cloth)
                        return
                    else:
                        return

                if len(self.inventory) < self.inventory_size:
                    self.inventory.append(item)
                    item.collect()
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
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def use_item(self, index):

        if len(self.inventory) > index:
            item_to_check = self.inventory[index]

            if item_to_check.item_type == 'card' or item_to_check.item_type == 'clothes':
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