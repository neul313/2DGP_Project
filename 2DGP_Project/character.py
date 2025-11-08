from pico2d import *

def right_down(e):
    pass

def right_up(e):
    pass

def left_down(e):
    pass

def left_up(e):
    pass


class Idle:
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
        pass
    def update(self):
        pass
    def draw(self):
        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass
