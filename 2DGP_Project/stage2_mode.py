import random
from pico2d import *

import game_framework
import game_world
from girl import Girl
from stage2 import Stage2
from item import Item
from inventory import Inventory
from door import Door
from HP import Bar

girl = None
door_bridge = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if 'girl' in game_framework.share:
                game_framework.share['girl'].handle_event(event)


def init():
    import play_mode

    global girl
    global door_bridge
    game_world.clear()

    if 'girl' not in game_framework.share:
        girl = Girl()
        game_framework.share['girl'] = girl
        inv = Inventory(girl)
        game_framework.share['inventory_ui'] = inv

        hp = Bar('hp')
        mp = Bar('mp')
        game_framework.share['hp'] = hp
        game_framework.share['mp'] = mp
    girl = game_framework.share['girl']

    girl.x, girl.y = 50, 230
    game_world.add_object(girl, 1)

    stage2_background = Stage2()
    game_world.add_object(stage2_background, 0)
    stage2_background.set_center_object(girl)

    game_world.add_object(game_framework.share['inventory_ui'], 3)
    game_world.add_object(game_framework.share['hp'], 3)
    game_world.add_object(game_framework.share['mp'], 3)

    game_world.add_collision_pair('girl:item', girl, None)
    game_world.add_collision_pair('missile:girl', None, girl)
    game_world.add_collision_pair('girl:door', girl, None)

    item_star = Item(300, 250, 0, 0, 'star', 10)
    game_world.add_object(item_star, 1)
    game_world.add_collision_pair('girl:item', None, item_star)

    door_bridge = Door(1500,230,2,None)
    game_world.add_object(door_bridge, 1)

    game_world.add_collision_pair('girl:door', girl, door_bridge)

    board = Item(500, 250, 0, 0, 'board', 0)
    game_world.add_object(board, 1)
    game_world.add_collision_pair('girl:item', None, board)

def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass