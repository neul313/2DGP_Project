import pygame
from pico2d import *
import game_world
import game_framework

MISSILE_SPEED_PPS = 300

class Missile:
    image = None

    def __init__(self):
        if self.image is None:
            self.image = load_image('attack.png')

        self.x, self.y = x,y


    def update(self):
        self.y -= MISSILE_SPEED_PPS * game_framework.frame_time
        # 임시로 90으로 설정
        if self.y < 90:
            game_world.remove_object(self)

    def draw(self):
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass