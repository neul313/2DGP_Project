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
    hp_images = None

    def load_images(self):
        pass

    def __init__(self):
        self.image = [load_image('boss1.png'),load_image('boss2.png')]
        self.frame =0.0
        self.x, self.y = 600, 230
        self.max_hp = 200 #최대
        self.hp = self.max_hp #현재 체력

        if Boss.hp_images is None:
            Boss.hp_images = {}
            # 0부터 20까지 이미지 로드
            for i in range(21):
                Boss.hp_images[i] = load_image(f'hp_boss2/{i}.png')

        #미사일 타이머
        self.missile_timer = random.uniform(1.0, 2.0)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.missile_timer -= game_framework.frame_time

        if self.missile_timer <= 0:
            self.missile_spawn()
            self.missile_timer = random.uniform(1.0, 2.0)

        if self.hp <=0:
            game_world.remove_object(self)

    def draw(self):
        cx = self.x - game_framework.camera_x
        cy = self.y - game_framework.camera_y

        image = self.image[int(self.frame)]
        image.draw(cx, cy, 400,400)

        hp_index = int(self.hp / 10)
        hp_index = clamp(0, hp_index, 20)

        Boss.hp_images[hp_index].draw(cx, cy + 250, 300, 300)

        l, b, r, t = self.get_bb()
        l -= game_framework.camera_x
        b -= game_framework.camera_y
        r -= game_framework.camera_x
        t -= game_framework.camera_y
        draw_rectangle(l, b, r, t)


    def handle_event(self,e):
        pass

    def handle_collision(self, group, other):
        if group == 'tang:boss':
            print(f"Boss Hit! HP: {self.hp}")  # 디버그용 출력
            self.hp -= 10
            if self.hp < 0:
                self.hp = 0

    # def missile_spawn(self):
    #     spawn_x = random.uniform(self.x - 400, self.x + 400)
    #
    #     missile = Missile(spawn_x, 500)
    #     game_world.add_object(missile, 1)
    #     game_world.add_collision_pair('missile:girl', missile, None)

    def missile_spawn(self):

        if 'girl' in game_framework.share:
            girl = game_framework.share['girl']
            target_x = girl.x
            spawn_range = 100
            spawn_x = random.uniform(target_x - spawn_range, target_x + spawn_range)

            spawn_y = girl.y + 600

            missile = Missile(spawn_x, spawn_y)
            game_world.add_object(missile, 1)
            game_world.add_collision_pair('missile:girl', missile, None)

        else:
            pass

    def draw_hp(self):
        bar_x = 200
        bar_y = 70
        cx = self.x - game_framework.camera_x
        cy = self.y - game_framework.camera_y
        x=cx
        y=cy + 270

        draw_rectangle(x - bar_x, y , x+bar_x, y + 25)

    def get_bb(self):
        return self.x - 170, self.y - 170, self.x + 170, self.y + 170

