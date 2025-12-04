import random
from pico2d import *

import game_framework
import game_world
from girl import Girl
from item import Item
from inventory import Inventory
from HP import Bar
from boss import Boss
from stage3 import Stage3
import logo_mode

girl = None
boss = None

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
    global girl

    game_world.clear()

    if 'girl' in game_framework.share:
        girl = game_framework.share['girl']
    else:
        girl = Girl()
        game_framework.share['girl'] = girl

        inv = Inventory(girl)
        game_framework.share['inventory_ui'] = inv

        hp = Bar('hp')
        mp = Bar('mp')
        game_framework.share['hp'] = hp
        game_framework.share['mp'] = mp

    girl.x, girl.y = 100, 100
    girl.face_dir = 1
    game_world.add_object(girl, 1)

    background = Stage3()
    game_world.add_object(background, 0)

    background.set_center_object(girl)

    # UI 가져오기
    if 'inventory_ui' in game_framework.share:
        game_world.add_object(game_framework.share['inventory_ui'], 3)

    if 'hp' in game_framework.share:
        game_world.add_object(game_framework.share['hp'], 3)

    if 'mp' in game_framework.share:
        game_world.add_object(game_framework.share['mp'], 3)

    game_world.add_collision_pair('girl:item', girl, None)
    game_world.add_collision_pair('missile:girl', None, girl)
    game_world.add_collision_pair('girl:door', girl, None)

    boss = Boss()
    boss.x = 800
    boss.y = 300
    game_world.add_object(boss, 1)

    game_world.add_collision_pair('tang:boss', None, boss)

def update():
    game_world.update()
    game_world.handle_collisions()

    boss_die = False
    for obj in game_world.world[1]:
        if isinstance(obj, Boss):  # 보스가 있다면
            boss_die = True
            break

    if not boss_die:
        print("clear")
        game_framework.change_mode(logo_mode)


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