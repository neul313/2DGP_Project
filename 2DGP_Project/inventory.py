from pico2d import *
import game_framework
from item import Item


class Inventory:
    def __init__(self, girl):
        self.girl = girl
        self.inven1 = load_image('inven1.png')
        self.inven2 = load_image('inven2.png')
        self.inven3 = load_image('inven3.png')

        self.item_image = load_image('items.png')
        self.bag_image = load_image('bag.png')
        self.gun_image = load_image('gun.png')

    def update(self):
        pass

    def draw(self):
        if self.girl.is_bag:
            self.inven1.draw(400, 590)
            self.inven2.draw(530, 654)
            self.inven3.draw(400, 590)

        else:
            self.inven1.draw(400, 590)
            self.inven3.draw(400, 590)

        normal_index = 0  # 일반 아이템
        special_index = 0 # 특수 아이템

        for item in self.girl.inventory:

            # 특수 아이템
            if item.item_type in ['gun', 'clothes']:
                draw_x = 317 + special_index * 67
                draw_y = 575

                if item.item_type == 'clothes':
                    Item.cloth.draw(draw_x, draw_y, 60, 60)
                elif item.item_type == 'gun':
                    Item.gun.draw(draw_x, draw_y, 60, 60)

                special_index += 1

            # 일반 아이템
            else:
                draw_x = 317 + normal_index * 67
                draw_y = 645

                if item.item_type == 'board':
                    Item.board.draw(draw_x, draw_y, 50, 40)
                else:
                    clip_bottom = self.item_image.h - item.clip_y - item.size
                    self.item_image.clip_draw(
                        item.clip_x, clip_bottom, item.size, item.size,
                        draw_x, draw_y, 40, 40)

                normal_index += 1
