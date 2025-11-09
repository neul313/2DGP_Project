from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

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
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

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
        if self.girl.face_dir == 1:  # right
            self.girl.image.clip_draw(int(self.girl.frame) * (144//3), 192//4, (144//2), 192//3, self.girl.x, self.girl.y)
        else:  # face_dir == -1: # left
            self.girl.image.clip_draw(int(self.girl.frame) * (144//3), 192//4, (144//2), 192//3, self.girl.x, self.girl.y)


class Run:
    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        pass
    def draw(self):
        pass


class Girl:
    def __init__(self):
        self.face_dir = 1
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('girl.png')

        self.IDLE = Idle(self)
        self.state_machine = StateMachine(self.IDLE, {})

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def handle_collision(self, group, other):
        pass
