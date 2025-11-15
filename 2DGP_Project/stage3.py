import random
from pico2d import *
import play_mode
import game_framework
import game_world

from boss import Boss


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if play_mode.girl:
                play_mode.girl.handle_event(event)


def init():
    print("Stage 3 Mode 진입")
    boss = Boss()
    game_world.add_object(boss, 0)

    if play_mode.girl:
        game_world.add_collision_pair('missile:girl', None, play_mode.girl)


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass


def pause(): pass
def resume(): pass