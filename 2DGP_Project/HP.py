from pico2d import *
import game_framework  # play_mode 대신 game_framework만 import


class Bar:
    images = None

    def __init__(self, bar):
        self.bar = bar

        if Bar.images == None:
            Bar.images = {}
            Bar.images['hp'] = {}
            Bar.images['mp'] = {}

            for i in range(9):
                Bar.images['hp'][i] = load_image(f'hp/{i}.png')

            for i in range(9):
                Bar.images['mp'][i] = load_image(f'mp/{i}.png')

        self.images = Bar.images

        self.x = 130
        self.y = 590
        self.width = 400
        self.height = 400

        if self.bar == 'hp':
            self.max_hp = 80
            self.current_hp = self.max_hp
        elif self.bar == 'mp':
            self.max_mp = 80
            self.current_mp = self.max_mp
            self.y = 588

    def draw(self):
        index = 0
        image_set = None

        if self.bar == 'hp':
            if self.max_hp > 0:
                ratio = self.current_hp / self.max_hp
                index = int(ratio * 8)
            image_set = self.images['hp']

        elif self.bar == 'mp':
            if self.max_mp > 0:
                ratio = self.current_mp / self.max_mp
                index = int(ratio * 8)
            image_set = self.images['mp']

        index = clamp(0, index, 8)

        if image_set:
            image_set[index].draw(self.x, self.y, self.width, self.height)

    def update(self):
        if 'girl' in game_framework.share:
            girl = game_framework.share['girl']

            if self.bar == 'hp':
                if hasattr(girl, 'hp'):
                    self.current_hp = girl.hp
                self.current_hp = clamp(0, self.current_hp, self.max_hp)

            elif self.bar == 'mp':
                if hasattr(girl, 'mp'):
                    self.current_mp = girl.mp
                self.current_mp = clamp(0, self.current_mp, self.max_mp)

    def handle_event(self, event):
        pass