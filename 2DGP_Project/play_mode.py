import random
from pico2d import *

import game_framework
import game_world

from girl import Girl
from boss import Boss
from stage1 import Stage1
from item import Item
from missile import Missile
from HP import Bar

girl = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            girl.handle_event(event)

def init():
    global girl

    girl = Girl()
    game_world.add_object(girl, 1)

    stage1 = Stage1()
    game_world.add_object(stage1, 0)

    stage1.set_center_object(girl)

    game_world.add_collision_pair('girl:item', girl, None)

    item1 = Item(100, 60, 0, 0)
    game_world.add_object(item1, 1)
    game_world.add_collision_pair('girl:item', None, item1)

    #boss = Boss()
    #game_world.add_object(boss, 0)

    hp = Bar('hp')
    mp = Bar('mp')
    game_world.add_object(hp, 3)
    game_world.add_object(mp, 3)

    game_world.add_collision_pair('missile:girl', None, girl)



def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass