from pico2d import *
import game_framework
import logo_mode

IMAGE_FILES = ['story_image/설명3.png', 'story/last1.png',
               'story/last2.png', 'story_image/인사.png']

images = []
image_index = 0
timer = 0

def init():
    global images, image_index, timer, bgm
    bgm = load_music('sound/크레딧 bgm.ogg')
    bgm.set_volume(32)
    bgm.repeat_play()

    images = []
    for file in IMAGE_FILES:
        images.append(load_image(file))

    image_index = 0
    timer = 0
    print("프롤로그 시작")


def finish():
    global images, bgm
    for img in images:
        del img
    images = []

    if bgm:
        bgm.stop()
        del bgm


def update():
    global timer, image_index
    timer += game_framework.frame_time

    if timer > 2.0:
        timer = 0  # 타이머 리셋
        image_index += 1  # 다음 장으로

        if image_index >= len(images):
            game_framework.change_mode(logo_mode)


def draw():
    clear_canvas()
    if image_index < len(images):
        images[image_index].draw(600, 350)

    update_canvas()


def handle_events():
    global image_index, timer
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        # 스페이스바를 누르면 다음 장으로
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            timer = 0
            image_index += 1
            if image_index >= len(images):
                game_framework.change_mode(logo_mode)


def pause():
    pass

def resume():
    pass