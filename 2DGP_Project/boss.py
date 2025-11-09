from pico2d import *
import random
import math
import game_framework
import game_world

TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

class Boss:
    images = None
    def load_images(self):
        pass

    def __init__(self):
        self.boss = Boss
        self.image = load_image('boss1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(600, 300, 400,400)

    def handle_event(self):
        pass

    def handle_collision(self):
        pass