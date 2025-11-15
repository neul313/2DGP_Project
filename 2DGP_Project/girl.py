from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

import random
import game_world
import game_framework
from state_machine import StateMachine

# 달리기 시간
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 액션 시간
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT



class Idle:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    def draw(self):
        x = self.girl.x - game_framework.camera_x
        y = self.girl.y - game_framework.camera_y

        if self.girl.face_dir == 1:  # right
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 0, 48, 48, x, y,100,100)
        else:  # face_dir == -1: # left
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 144, 48, 48, x, y,100,100)


class Run:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.girl.dir = self.girl.face_dir = 1
        elif left_down(e) or right_up(e):
            self.girl.dir = self.girl.face_dir = -1

    def exit(self, e):
        pass
    def do(self):
        self.girl.frame = (self.girl.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.girl.x += self.girl.dir * RUN_SPEED_PPS * game_framework.frame_time


    def draw(self):
        x = self.girl.x - game_framework.camera_x
        y = self.girl.y - game_framework.camera_y

        if self.girl.face_dir == 1:  # right
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 48, 48, 48, x, y,100,100)
        else:  # face_dir == -1: # left
            self.girl.image.clip_draw(int(self.girl.frame) * 48, 96, 48, 48, x, y,100,100)


class Girl:
    def __init__(self):
        self.face_dir = 1
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('girl.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.RUN, left_down: self.RUN,
                            right_up: self.RUN, left_up: self.RUN},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE,
                           left_down: self.IDLE}
            }
        )
    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50
