from pico2d import *
import game_framework
from item import Item


class Inventory:
    def __init__(self, girl):
        self.girl = girl
        self.inven1 = load_image('inven1.png')
        self.inven2 = load_image('inven2.png')
        self.item_image = load_image('items.png')
        self.bag_image = load_image('bag.png')

    def update(self):
        pass

    def draw(self):
        if self.girl.is_bag:
            self.inven1.draw(400, 590)
            self.inven2.draw(530, 654)
        else:
            self.inven1.draw(400, 590)

        for i, item in enumerate(self.girl.inventory):
            draw_x = 317 + i * 67
            draw_y = 645

            if item.item_type == 'clothes':
                Item.cloth.draw(draw_x, draw_y, 60, 60)

            else:
                clip_bottom = self.item_image.h - item.clip_y - item.size
                self.item_image.clip_draw(
                    item.clip_x, clip_bottom, item.size, item.size,
                    draw_x, draw_y, 40, 40)
