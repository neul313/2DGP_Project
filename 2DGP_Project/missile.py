from pico2d import *
import game_world
import game_framework

MISSILE_SPEED_PPS = 300

class Missile:
    image = None

    def __init__(self,x,y):
        if self.image is None:
            self.image = load_image('attack.png')

        self.x, self.y = x,y


    def update(self):
        self.y -= MISSILE_SPEED_PPS * game_framework.frame_time
        # 임시로 90으로 설정
        if self.y < 90:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y, 100,100)

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        if group == 'missle:girl':
            game_world.remove_object(self)