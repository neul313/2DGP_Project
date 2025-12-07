import pygame
from pico2d import *
import random
import math
import game_framework
import game_world

# 상태 상수
ACTION_IDLE = 0
ACTION_WALK = 1
ACTION_ATTACK = 2
ACTION_DEAD = 3

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Boss:
    image = None
    hp_images = None

    def __init__(self, x, y):
        if self.image is None:
            self.image = load_image('Bear.png')
        if Boss.hp_images is None:
            Boss.hp_images = {}
            for i in range(11):
                Boss.hp_images[i] = load_image(f'hp_boss1/{i}.png')
        global bgm

        bgm = load_music('sound/2챕터 bgm.ogg')
        bgm.set_volume(32)
        bgm.repeat_play()

        self.x, self.y = x, y


        # 화면에 그려질 크기
        self.draw_width = 150
        self.draw_height = 150

        self.hp = 100
        self.dir = -1
        self.frame = 0
        self.action = ACTION_IDLE


        self.frames = [
            # 1번째 줄 (서 있는 모습) - IDLE
            (21, 316, 76, 52), (105, 316, 78, 52), (188, 316, 79, 52), (273, 316, 78, 51),
            (355, 316, 79, 51), (440, 316, 79, 51),

            # 2번째 줄 (걷기) - WALK
            (21, 247, 76, 51), (104, 247, 79, 50), (188, 247, 78, 52), (273, 247, 80, 51),
            (355, 247, 80, 49), (440, 247, 80, 50),

            # 3번째 줄 (포효/공격 준비) - 미사용 예정
            (20, 179, 77, 51), (103, 179, 79, 50), (187, 179, 79, 50), (273, 179, 73, 47),
            (353, 179, 76, 50), (436, 179, 78, 50),

            # 4번째 줄 (공격) - ATTACK
            (20, 103, 71, 55), (103, 103, 68, 67), (181, 103, 95, 60), (288, 103, 63, 64),
            (361, 103, 70, 57), (443, 103, 73, 50),

            # 5번째 줄 (피격/쓰러짐) - DEAD
            (20, 25, 60, 54), (103, 25, 68, 52), (181, 25, 95, 42), (288, 25, 380, 40)
        ]

        self.timer = 0
        self.dead_timer = 0

        # 현재 그려야 할 리스트의 인덱스 번호
        self.current_draw_index = 0

    def update(self):
        # 현재 행동에 따라 사용할 프레임 범위 설정
        start_index = 0
        frame_count = 0

        if self.action == ACTION_IDLE:
            start_index = 0
            frame_count = 6
        elif self.action == ACTION_WALK:
            start_index = 6
            frame_count = 6
        elif self.action == ACTION_ATTACK:
            start_index = 18  # 4번째 줄 사용
            frame_count = 6
        elif self.action == ACTION_DEAD:
            start_index = 24
            frame_count = 4

        # 프레임 갱신
        self.frame = (self.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count

        # 죽음 처리 (마지막 프레임 고정)
        if self.action == ACTION_DEAD:
            self.dead_timer += game_framework.frame_time
            if int(self.frame) >= 3:  # 4개니까 인덱스는 0,1,2,3
                self.frame = 3
            if self.dead_timer >= 3.0:
                game_world.remove_object(self)

        # 실제 그려질 리스트 인덱스 계산
        self.current_draw_index = start_index + int(self.frame)

        #플레이어가 가까이 있으면 공격
        if self.action != ACTION_DEAD and 'girl' in game_framework.share:
            girl = game_framework.share['girl']
            distance = math.sqrt((girl.x - self.x) ** 2 + (girl.y - self.y) ** 2)

            if girl.x > self.x:
                self.dir = 1
            else:
                self.dir = -1

            if distance < 50:
                self.action = ACTION_ATTACK
            elif distance < 100:
                self.action = ACTION_WALK
                self.x += self.dir * 100 * game_framework.frame_time
            else:
                self.action = ACTION_IDLE

        self.x = clamp(50, self.x, 2400 - 50)

    def draw(self):
        cx = self.x - game_framework.camera_x
        cy = self.y - game_framework.camera_y

        safe_index = clamp(0, self.current_draw_index, len(self.frames) - 1)

        x, y, w, h = self.frames[safe_index]

        if self.dir == 1:
            self.image.clip_draw(x, y, w, h, cx, cy, self.draw_width, self.draw_height)
        else:
            self.image.clip_composite_draw(x, y, w, h, 0, 'h', cx, cy, self.draw_width, self.draw_height)

        # 보스 체력바 그리기

        hp_index = int(self.hp / 10)
        hp_index = clamp(0, hp_index, 10)
        Boss.hp_images[hp_index].draw(self.x, self.y + 100, 300, 300)

        # 디버그 박스
        l, b, r, t = self.get_bb()
        l -= game_framework.camera_x
        b -= game_framework.camera_y
        r -= game_framework.camera_x
        t -= game_framework.camera_y
        #draw_rectangle(l, b, r, t)

    def handle_collision(self, group, other):
        if group == 'tang:boss':
            if self.action != ACTION_DEAD:
                print(f"Boss Hit, HP: {self.hp}")
                self.hp -= 10
                if self.hp <= 0:
                    self.hp = 0
                    self.action = ACTION_DEAD
                    self.frame = 0  # 죽는 모션 처음부터 시작

    def get_bb(self):
        half_w = self.draw_width // 3
        half_h = self.draw_height // 2
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_event(self, e):
        pass