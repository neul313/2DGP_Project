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
    image = None
    def load_images(self):
        pass

    def __init__(self):
        self.image = [load_image('boss1.png'),load_image('boss2.png')]
        self.frame =0.0
        self.x, self.y = 600, 100
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
        cx = self.x - game_framework.camera_x
        cy = self.y - game_framework.camera_y

        image = self.image[int(self.frame)]
        image.draw(cx, cy, 400,400)
        self.draw_hp()

    def handle_event(self,e):
        pass

    def handle_collision(self, group, other):
        if group == 'tang:boss':
            print(f"Boss Hit! HP: {self.hp}")  # 디버그용 출력
            self.hp -= 10
            if self.hp < 0:
                self.hp = 0

    def missile_spawn(self):
        spawn_x = random.uniform(self.x - 400, self.x + 400)

        missile = Missile(spawn_x, 500)
        game_world.add_object(missile, 1)
        game_world.add_collision_pair('missile:girl', missile, None)

    def draw_hp(self):
        bar_x = 200
        bar_y = 70
        cx = self.x - game_framework.camera_x
        cy = self.y - game_framework.camera_y
        x=cx
        y=cy + 270

        draw_rectangle(x - bar_x, y , x+bar_x, y + 25)

