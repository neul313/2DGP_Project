from pico2d import *
import game_framework
import play_mode

class Stage1:
    def __init__(self):
        self.image = load_image('stage_1.png')

        self.canvas_width = 1200
        self.canvas_height = 700
        self.image_width = self.image.w
        self.image_height = self.image.h

        self.window_left = 0
        self.window_bottom = 0

        game_framework.camera_x = 0
        game_framework.camera_y = 0

        self.center_object = None


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