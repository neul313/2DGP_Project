from pico2d import *
import play_mode

class Bar:
    def __init__(self):
        self.image = load_image('hp.png')
        self.x = -50
        self.y = 390
        self.width = 400
        self.height = 400

        self.max_hp=100
        self.max_mp=100
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, self.image.w, self.image.h,self.x, self.y,self.width, self.height)

    def update(self):
        if play_mode.girl:
            # girl.py에 self.hp 정의함
            if hasattr(play_mode.girl, 'hp'):
                self.current_hp = play_mode.girl.hp
        self.current_hp = clamp(0, self.current_hp, self.max_hp)

    def handle_event(self, event):
        pass
