from pico2d import *
import game_framework


class Inventory:
    def __init__(self, girl):
        self.girl = girl  # girl의 인벤토리 정보에 접근하기 위함
        self.inventory_image = load_image('inven1.png')  # 인벤토리 '배경'
        self.item_image = load_image('items.png')  # 인벤토리 '아이템'

    def update(self):
        pass

    def draw(self):
        self.inventory_image.draw(400, 590)

        for i, item in enumerate(self.girl.inventory):
            draw_x = 50 + i * 60
            draw_y = 650

            clip_bottom = self.item_image.h - item.clip_y - item.size
            self.item_image.clip_draw(
                item.clip_x, clip_bottom, item.size, item.size,
                draw_x, draw_y, 50, 50 )