from pico2d import *
import play_mode

class Bar:
    images = None
    def __init__(self, bar):
        self.bar = bar

        if Bar.images == None:
            Bar.images = {}  # 딕셔너리로 만듦

            for i in range(7):
                Bar.images[i] = load_image(f'hp_mp/{i + 1}.png')

        self.images = Bar.images

        self.x = -50
        self.y = 390
        self.width = 400
        self.height = 400

        if self.bar == 'hp':
            self.max_hp=80
            self.current_hp = self.max_hp
        elif self.bar == 'mp':
            self.max_mp=80
            self.current_mp = self.max_mp


    def draw(self):
       pass


    def update(self):
        if self.bar == 'hp':
            if play_mode.girl:
                if hasattr(play_mode.girl, 'hp'):
                    self.current_hp = play_mode.girl.hp
            self.current_hp = clamp(0, self.current_hp, self.max_hp)

        elif self.bar == 'mp':
            if play_mode.girl:
                if hasattr(play_mode.girl, 'mp'):
                    self.current_mp = play_mode.girl.mp
            self.current_mp = clamp(0, self.current_mp, self.max_mp)

    def handle_event(self, event):
        pass
