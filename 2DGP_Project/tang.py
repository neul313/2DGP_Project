from pico2d import *
import game_world
import game_framework


class Tang:
    image = None

    def __init__(self, x, y, hit):
        if Tang.image is None:
            Tang.image = load_image('tang.png')  # 총알 이미지 파일 필요
        self.x, self.y = x, y


    def update(self):
       pass

    def draw(self):
        pass
    def get_bb(self):
        pass


    def handle_collision(self, group, other):
        pass