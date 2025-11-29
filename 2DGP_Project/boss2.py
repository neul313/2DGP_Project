import pygame
from pico2d import *
import random
import math
import game_framework
import game_world
from tang import Tang

# 곰 행동
ACTION_IDLE = 0
ACTION_WALK = 1
#2은 뭔가 좀 애매
ACTION_ATTACK = 3  # 3번째 줄이 서서 공격하는 모션
ACTION_DEAD = 4

TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Boss:
    image = None
    def __init__(self,x, y):
        if self.image is None:
            self.image = load_image('Bear.png')

        self.x, self.y = x, y

        self.frame_width = 621 // 6
        self.frame_height = 380 // 5

        self.hp = 100 #총알 1대당 10대미지로 설정 예정
        self.dir = -1
        self.frame = 0
        self.action = ACTION_IDLE
        self.timer = 0

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self,e):
        pass

    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        pass