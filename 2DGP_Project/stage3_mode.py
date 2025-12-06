import random
from pico2d import *

import game_framework
import game_world
from girl import Girl
from item import Item
from inventory import Inventory
from HP import Bar
from boss import Boss  # 3스테이지 보스 (공장)
from stage3 import Stage3
import logo_mode
from door import Door
import last

girl = None
boss = None


def init():
    global girl, boss

    print("[DEBUG] 3스테이지(공장) init() 시작")

    # 1. 게임 월드 초기화
    game_world.clear()

    # 2. 플레이어 설정
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

    girl.reset_collision_info()
    girl.reset_state()
    girl.bg_width = 1200

    girl.x, girl.y = 100, 100
    girl.face_dir = 1
    game_world.add_object(girl, 1)

    # 3. 배경 설정
    background = Stage3()
    game_world.add_object(background, 0)
    background.set_center_object(girl)

    # 4. UI 설정
    if 'inventory_ui' in game_framework.share:
        game_world.add_object(game_framework.share['inventory_ui'], 3)
    if 'hp' in game_framework.share:
        game_world.add_object(game_framework.share['hp'], 3)
    if 'mp' in game_framework.share:
        game_world.add_object(game_framework.share['mp'], 3)

    # 5. 충돌 설정
    game_world.add_collision_pair('girl:item', girl, None)
    game_world.add_collision_pair('missile:girl', None, girl)
    game_world.add_collision_pair('girl:door', girl, None)

    # 6. 보스 생성
    boss = Boss()
    game_world.add_object(boss, 1)
    game_world.add_collision_pair('tang:boss', None, boss)
    # game_world.add_collision_pair('boss:girl', boss, girl)

    print(f"[DEBUG] 보스 생성 완료. 초기 HP: {boss.hp}")
    doors_removed = 0
    for layer in game_world.world:
        for obj in layer:
            if isinstance(obj, Door):
                game_world.remove_object(obj)
                doors_removed += 1

    if doors_removed > 0:
        print(f"[DEBUG] 경고: 시작 시 {doors_removed}개의 포탈이 발견되어 강제로 삭제했습니다.")


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

def update():
    game_world.update()
    game_world.handle_collisions()

    global boss

    if boss:
        if boss.hp <= 0:
            # 보스 HP가 0 이하일 때만
            # 문이 이미 있는지 확인 (중복 생성 방지)
            door_exists = False
            for obj in game_world.world[1]:
                if isinstance(obj, Door):
                    door_exists = True
                    break

            if not door_exists:
                print(f"[DEBUG] 보스 사망(HP:{boss.hp}) -> 엔딩 포탈 생성!")
                portal = Door(1100, 100, 0, last)
                game_world.add_object(portal, 1)

                # 플레이어와 충돌 등록
                if 'girl' in game_framework.share:
                    game_world.add_collision_pair('girl:door', game_framework.share['girl'], portal)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    global boss
    boss = None

def pause():
    pass

def resume():
    pass