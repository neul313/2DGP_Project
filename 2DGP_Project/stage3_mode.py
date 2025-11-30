import random
from pico2d import *

import game_framework
import game_world
import play_mode
from girl import Girl
from stage2 import Stage2
from item import Item
from inventory import Inventory
from HP import Bar
from boss import Boss
import stage3
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

    # 2스테이지 시작 좌표 설정
    girl.x, girl.y = 50, 100
    girl.face_dir = 1
    game_world.add_object(girl, 1)

    background = stage3()
    game_world.add_object(background, 0)

    game_framework.camera_x = 0
    game_framework.camera_y = 0

    stage2_background = Stage2()
    game_world.add_object(stage2_background, 0)
    game_framework.share['background'] = stage2_background
    stage2_background.set_center_object(girl)  # 배경이 소녀를 따라다니게 설정

    game_world.add_object(game_framework.share['inventory_ui'], 3)
    game_world.add_object(game_framework.share['hp'], 3)
    game_world.add_object(game_framework.share['mp'], 3)

    game_world.add_collision_pair('girl:item', girl, None)
    game_world.add_collision_pair('missile:girl', None, girl)
    game_world.add_collision_pair('girl:door', girl, None)

    item_gun = Item(555, 270, 0, 0, 'gun', 10)
    game_world.add_object(item_gun, 1)
    game_world.add_collision_pair('girl:item', None, item_gun)

    boss = Boss()
    game_world.add_object(boss, 1)

    # 총알과 보스의 충돌 처리
    game_world.add_collision_pair('tang:boss', None, boss)
    game_world.add_collision_pair('missile:girl', None, girl)
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