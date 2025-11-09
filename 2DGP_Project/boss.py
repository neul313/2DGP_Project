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
        self.frame =0
        self.x, self.y = 600, 300

        #미사일 타이머
        self.missile_timer = random.randint(3, 5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.missile_timer -= game_framework.frame_time

        if self.missile_timer <= 0:
            self.missle_spawn()
            self.missile_timer = random.randint(3, 5)

    def draw(self):
        image = self.image[int(self.frame)]
        image.draw(600, 300, 400,400)

    def handle_event(self):
        pass

    def handle_collision(self):
        pass

    def missle_spawn(self):
        missile = Missile(self.x, self.y)
        game_world.add_object(missile,1)
