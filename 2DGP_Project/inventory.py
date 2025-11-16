from pico2d import *
import game_framework


class Inventory:
    def __init__(self, girl):
        self.girl = girl
        self.inventory_image = load_image('inven1.png')
        self.item_image = load_image('items.png')

    def update(self):
        pass

    def draw(self):
        self.inventory_image.draw(400, 590)

        for i, item in enumerate(self.girl.inventory):
            draw_x = 317
            draw_y = 645

            clip_bottom = self.item_image.h - item.clip_y - item.size
            self.item_image.clip_draw(
                item.clip_x, clip_bottom, item.size, item.size,
                draw_x, draw_y, 40, 40 )


