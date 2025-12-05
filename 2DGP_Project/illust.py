from pico2d import *
import game_framework
import game_world

image = None
timer = 0

def init():
    global image, timer
    image = load_image('story/bus.png')
    timer = 0


def finish():
    global image
    del image


def update():
    global timer
    timer += game_framework.frame_time

    if timer > 3.0:
        import stage2_mode
        game_framework.change_mode(stage2_mode)


def draw():
    clear_canvas()
    image.draw(600, 350)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        # 스페이스바를 누르면 바로 스킵하고 넘어가기
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            import stage2_mode
            game_framework.change_mode(stage2_mode)


def pause(): pass


def resume(): pass