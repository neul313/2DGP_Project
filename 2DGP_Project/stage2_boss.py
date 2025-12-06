import random
from pico2d import *
import game_framework
import game_world
import play_mode
from boss2 import Boss  # 2스테이지 보스 (곰)
import stage3_mode  # 3스테이지 (공장)
from door import Door

image = None
boss = None  # 보스 객체를 담을 변수

def init():
    global image, boss

    print("[DEBUG] 2스테이지 보스전(곰)시작")

    # 1. 게임 월드 초기화
    game_world.clear()
    # 배경 이미지 (3스테이지와 같아서 헷갈릴 수 있음)
    image = load_image('stage3.png')

    game_framework.camera_x = 0
    game_framework.camera_y = 0

    # 2. 보스 생성 (전역 변수에 저장)
    boss = Boss(800, 100)
    game_world.add_object(boss, 1)

    print(f"[DEBUG] 곰 보스 생성 완료. 초기 HP: {boss.hp}")
    # 3. 플레이어 및 충돌 처리
    if 'girl' in game_framework.share:
        girl = game_framework.share['girl']
        game_world.add_object(girl, 1)

        # 위치 조정
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

    # 시작하자마자 있는 포탈 제거 (안전장치)
    for layer in game_world.world:
        for obj in layer:
            if isinstance(obj, Door):
                print("[DEBUG] 경고: 2스테이지 보스전에 남아있는 포탈 제거")
                game_world.remove_object(obj)

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

    # [핵심 수정] 리스트 검사가 아닌, 보스 객체의 HP를 직접 확인
    if boss:
        if boss.hp <= 0:
            # 보스 HP가 0 이하일 때만 문 생성

            door_exists = False
            for obj in game_world.world[1]:
                if isinstance(obj, Door):
                    door_exists = True
                    break

            if not door_exists:
                print(f"[DEBUG] 곰 보스 사망(HP:{boss.hp}) -> 3스테이지행 포탈 생성!")

                # 3스테이지로 이동하는 문 생성
                exit_door = Door(1100, 100, 0, stage3_mode)
                game_world.add_object(exit_door, 1)

                if 'girl' in game_framework.share:
                    girl = game_framework.share['girl']
                    game_world.add_collision_pair('girl:door', girl, exit_door)


def draw():
    clear_canvas()
    if image:
        image.draw(600, 350)
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    global image, boss
    image = None
    boss = None


def pause():
    pass

def resume():
    pass