from pico2d import *
import game_framework

class Popup:
    def __init__(self):
        self.image = None
        self.play_time = 0
        self.visible = False

    def update(self):
        if self.play_time > 0:
            self.play_time -= game_framework.frame_time
            if self.play_time <= 0:
                self.visible = False
                self.image = None # 이미지 해제

    def draw(self):
        if self.visible and self.image:
            self.image.draw(600, 300, 300, 200)

    def show(self, image_file, time=2.0):
        self.image = load_image(image_file)
        self.play_time = time
        self.visible = True