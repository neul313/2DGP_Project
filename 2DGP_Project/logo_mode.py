import game_framework
from pico2d import *
import prologue

def init():
    global image
    image = load_image('logo.png')

def finish():
    global image
    del image

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(prologue)

def draw():
    clear_canvas()
    image.draw(600,350)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass
