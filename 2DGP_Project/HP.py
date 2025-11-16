from pico2d import *
import play_mode

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
            self.max_hp=80
            self.current_hp = self.max_hp
        elif self.bar == 'mp':
            self.max_mp=80
            self.current_mp = self.max_mp
            self.y = 588


    def draw(self):
        index = 0
        image_set = None

        if self.bar == 'hp':
            index = (self.current_hp/10)
            image_set = self.images['hp']

        elif self.bar == 'mp':
            index = (self.current_mp/10)
            image_set = self.images['mp']

        index = clamp(0, index, 8)

        if image_set:
            image_set[index].draw(self.x, self.y, self.width, self.height)

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
                else:
                    self.current_mp = 80  # mp가 없으면 테스트용으로 80
            self.current_mp = clamp(0, self.current_mp, self.max_mp)

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
