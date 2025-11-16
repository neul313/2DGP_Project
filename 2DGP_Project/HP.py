from pico2d import *
import play_mode

class Bar:
    def __init__(self):
        self.image = load_image('hp.png')
        self.x = 10
        self.y = 390
        self.width = 400
        self.height = 400

        self.max_hp=100
        self.max_mp=100
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp

        # hp 표시 직사각형 두께
        self.offset_x = 5  # 왼쪽 테두리 두께
        self.offset_y = 5  # 아래쪽 테두리 두께

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, self.image.w, self.image.h,self.x, self.y,self.width, self.height)


    def update(self):
        if play_mode.girl:
            # girl.py에 self.hp가 정의되어 있다고 가정
            if hasattr(play_mode.girl, 'hp'):
                self.current_hp = play_mode.girl.hp
        self.current_hp = clamp(0, self.current_hp, self.max_hp)

    def handle_event(self, event):
        pass
