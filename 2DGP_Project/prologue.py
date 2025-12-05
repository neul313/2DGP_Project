from pico2d import *
import game_framework
import game_world

IMAGE_FILES = ['story_image/주의.png','story_image/설명1.png', 'story_image/설명2.png']

images = []
image_index = 0
timer = 0

def init():
    global images, image_index, timer

    images = []
    for file in IMAGE_FILES:
        images.append(load_image(file))

    image_index = 0
    timer = 0
    print("프롤로그 시작")


def finish():
    global images
    for img in images:
        del img
    images = []


def update():
    global timer, image_index
    timer += game_framework.frame_time

    if timer > 2.0:
        timer = 0  # 타이머 리셋
        image_index += 1  # 다음 장으로

        if image_index >= len(images):
            import play_mode
            game_framework.change_mode(play_mode)


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
                import play_mode
                game_framework.change_mode(play_mode)


def pause():
    pass

def resume():
    pass