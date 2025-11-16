from pico2d import *
import game_world
import game_framework

class Item:
    image = None

    def __init__(self, x, y, cx, cy, item_type = 'hp', value = 20):
        if Item.image is None:
            Item.image = load_image('items.png')
        self.x, self.y = x, y
        self.clip_x = cx
        self.clip_y = cy
        self.size = 15

        self.item_type = item_type
        self.value = value
    def update(self):
        pass

    def draw(self):
        draw_x = self.x - game_framework.camera_x
        draw_y = self.y - game_framework.camera_y

        clip_bottom = self.image.h - self.clip_y - self.size

        self.image.clip_draw(self.clip_x, clip_bottom, self.size, self.size,
                            draw_x, draw_y, 50,50)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'girl:item':
            pass

    def collect(self):
        game_world.remove_object(self)