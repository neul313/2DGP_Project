from pico2d import *
import random
import math
import game_framework
import game_world

TIME_PER_ACTION = 5.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

class Boss:
    images = None
    def load_images(self):
        pass

    def __init__(self):
        self.image = [load_image('boss1.png'),load_image('boss2.png')]

        self.frame =0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

    def draw(self):
        image = self.image[int(self.frame)]
        image.draw(600, 300, 400,400)

    def handle_event(self):
        pass

    def handle_collision(self):
        pass