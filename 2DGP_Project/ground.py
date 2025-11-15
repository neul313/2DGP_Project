from pico2d import *

class Land:
    def __init__(self):
        self.image = load_image('land.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 50)
        self.image.draw(1200, 50)

    def get_bb(self):
        return 0, 0, 1600, 60

    def handle_collision(self, group, other):
        pass