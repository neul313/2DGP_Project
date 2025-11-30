import random
from pico2d import *
import game_framework
import game_world
import play_mode
from boss2 import Boss  # boss2.py에서 Boss 클래스 가져오기

# 모듈 단위 변수 (전역 변수)
image = None


# ▼▼▼ self 제거 (모듈 함수이므로) ▼▼▼
def init():
    global image  # 전역 변수 image를 사용하겠다고 선언

    print("Stage 2 Boss 진입")

    # 1. 배경 이미지 로드
    # 실제 존재하는 이미지 파일명으로 바꿔주세요! (예: 'stage_1.png')
    image = load_image('임시.jpg')

    game_framework.camera_x = 0
    game_framework.camera_y = 0

    # 2. 보스 생성
    boss = Boss(800, 100)
    game_world.add_object(boss, 1)

    # 3. 플레이어 및 충돌 처리
    if 'girl' in game_framework.share:
        girl = game_framework.share['girl']
        game_world.add_object(girl, 1)  # 플레이어도 화면에 추가

        girl.x = 100  # 왼쪽에서 시작
        girl.y = 100  # 바닥 높이 (이 값을 조절하세요!)

        # 충돌 쌍 등록
        game_world.add_collision_pair('tang:boss', None, boss)
        game_world.add_collision_pair('missile:girl', None, girl)


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


def draw():
    clear_canvas()

    # ▼▼▼ 배경 먼저 그리기 ▼▼▼
    if image:
        # 화면 크기(1200x700)에 맞춰 중앙이나 적절한 위치에 그림
        image.draw(600, 350)

    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    global image
    del image  # 메모리 해제


def pause(): pass


def resume(): pass