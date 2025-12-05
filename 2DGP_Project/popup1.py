from pico2d import *
import game_framework

class Popup:
    def __init__(self):
        self.image = None
        self.play_time = 0
        self.visible = False

    def update(self):
        pass

    def draw(self):
        pass

    def show(self, image_file, time=2.0):
        pass