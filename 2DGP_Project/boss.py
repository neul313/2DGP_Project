from pico2d import *
import random
import math
import game_framework
import game_world
from missile import Missile


TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2.0

class Boss:
    images = None
    def load_images(self):
        pass

    def __init__(self):
        self.image = [load_image('boss1.png'),load_image('boss2.png')]
        self.frame =0.0
        self.x, self.y = 600, 300
        self.max_hp = 100 #최대
        self.hp = self.max_hp #현재 체력

        #미사일 타이머
        self.missile_timer = random.uniform(3.0, 5.0)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.missile_timer -= game_framework.frame_time

        if self.missile_timer <= 0:
            self.missile_spawn()
            self.missile_timer = random.uniform(3.0, 5.0)

        if self.hp <=0:
            game_world.remove_object(self)

    def draw(self):
        image = self.image[int(self.frame)]
        image.draw(self.x, self.y, 400,400)

    def handle_event(self,e):
        pass

    def handle_collision(self, group, other):
        pass

    def missile_spawn(self):
        x = random.uniform(200,1000)

        missile = Missile(x,500)
        game_world.add_object(missile,1)
        game_world.add_collision_pair('missile:girl', missile, None)

    def hp(self):
        pass

    def hp_min(self, n):
        pass
