from pico2d import *
import game_world
import game_framework

MISSILE_SPEED_PPS = 400
size = 100

class Missile:
    image = None

    def __init__(self,x,y):
        if Missile.image is None:
            Missile.image = load_image('attack.png')

        self.x, self.y = x,y


    def update(self):
        self.y -= MISSILE_SPEED_PPS * game_framework.frame_time
        # 임시로 90으로 설정
        if self.y < 90:
            game_world.remove_object(self)

    def draw(self):
        sx = self.x - game_framework.camera_x
        sy = self.y - game_framework.camera_y
        Missile.image.draw(sx, sy, size,size)

    def get_bb(self):
        bb=size//2
        return self.x - bb, self.y - bb, self.x + bb, self.y + bb

    def handle_collision(self, group, other):
        if group == 'missile:girl':
            game_world.remove_object(self)