import random
from pico2d import *
import game_framework
import game_world
import play_mode
from boss2 import Boss
import stage3_mode

image = None

def init():
    global image

    print("Stage 2 Boss 진입")
    game_world.clear()
    image = load_image('stage3.png')

    game_framework.camera_x = 0
    game_framework.camera_y = 0

    # 2. 보스 생성
    boss = Boss(800, 100)
    game_world.add_object(boss, 1)

    # 3. 플레이어 및 충돌 처리
    if 'girl' in game_framework.share:
        girl = game_framework.share['girl']
        game_world.add_object(girl, 1)

        girl.x = 100
        girl.y = 100

        game_world.add_collision_pair('tang:boss', None, boss)
        game_world.add_collision_pair('boss:girl', boss, girl)

        if 'inventory_ui' in game_framework.share:
            game_world.add_object(game_framework.share['inventory_ui'], 3)
        if 'hp' in game_framework.share:
            game_world.add_object(game_framework.share['hp'], 3)
        if 'mp' in game_framework.share:
            game_world.add_object(game_framework.share['mp'], 3)

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

    boss_die = False
    for obj in game_world.world[1]:
        if isinstance(obj, Boss): # 보스가 있다면
            boss_die = True
            break

    # 보스가 없으면 -> 3스테이지로 이동
    if not boss_die:
        print("clear")
        game_framework.change_mode(stage3_mode)


def draw():
    clear_canvas()
    if image:
        image.draw(600, 350)
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    global image
    image = None


def pause():
    pass

def resume():
    pass