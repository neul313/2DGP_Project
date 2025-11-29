from pico2d import *
import game_world
import game_framework

TANG_SPEED_PPS = 500

class Tang:
    image = None

    def __init__(self, x, y, hit):
        if Tang.image is None:
            Tang.image = load_image('tang.png')  # 총알 이미지 파일 필요
        self.x, self.y = x, y
        self.hit = hit


    def update(self):
       self.x+=self.hit * game_framework.frame_time
       if self.x < 0 or self.x > 2500 :
           game_world.remove_object(self)

    def draw(self):
        Tang.image.draw(self.x - game_framework.camera_x,
                        self.y - game_framework.camera_y, 30, 30)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15


    def handle_collision(self, group, other):
        if group == 'tang:boss':
            game_world.remove_object(self)