from pico2d import *
import game_framework
import play_mode

class Stage2:
    def __init__(self):
        self.images = ['stage2/stage2_1.png','stage2/stage2_2.png',
                       'stage2/stage2_3.png','stage2/stage2_4.png',]
        self.images_index = 0

        self.image = load_image(self.images[self.images_index])

        self.canvas_width = 1200
        self.canvas_height = 700
        self.image_width = self.image.w
        self.image_height = self.image.h

        self.window_left = 0
        self.window_bottom = 0

        game_framework.camera_x = 0
        game_framework.camera_y = 0

        self.center_object = None

    def change_background(self):
        # 인덱스를 1 증가 (다음 번호로)
        self.images_index += 1

        # 준비된 이미지 개수보다 작을 때만 변경 (에러 방지)
        if self.images_index < len(self.images):
            # 새로운 이미지 로딩
            self.image = load_image(self.images[self.images_index])
            print(f"배경 변경됨: {self.images[self.images_index]}")
        else:
            print("더 이상 바꿀 배경이 없습니다.")


    def update(self):
        if self.center_object is None:
            return
        #clamp는 입려으로 들어오는 모든 값들을 [min,max]범위 안으로 조정하는 역할
        self.window_left = clamp(0, int(self.center_object.x) - self.canvas_width // 2,
                                 self.image_width - self.canvas_width)

        game_framework.camera_x = self.window_left
        game_framework.camera_y = self.window_bottom


    def draw(self):
        self.image.clip_draw_to_origin( self.window_left, self.window_bottom,
            self.canvas_width, self.canvas_height,0, 0)

    def get_bb(self):
            pass

    def handle_collision(self, group, other):
        pass

    def set_center_object(self, obj):
        self.center_object = obj