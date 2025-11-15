from pico2d import *

class Stage1:
    def __init__(self):
        self.image = load_image('st1.png')

        self.canvas_width = 1200
        self.canvas_height = 700
        self.image_width = self.image.w
        self.image_height = self.image.h

        self.window_left = 0
        self.window_bottom = 50

        self.center_object = None


    def update(self):
        if self.center_object is None:
            return
        self.window_left = clamp(0,
                                 int(self.center_object.x) - self.canvas_width // 2,
                                 self.image_width - self.canvas_width)

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.canvas_width, self.canvas_height,
            0, 0
        )

    def get_bb(self):
            pass

    def handle_collision(self, group, other):
        pass

    def set_center_object(self, obj):
        self.center_object = obj