from pico2d import *
import game_world
import game_framework

class Item:
    image = None
    bag  = None
    sparkle = None

    def __init__(self, x, y, cx, cy, item_type = 'hp', value = 20):
        if Item.image is None:
            Item.image = load_image('items.png')

        if Item.bag is None:
            Item.bag = load_image('bag.png')

        if Item.sparkle is None:
            Item.sparkle = load_image('sparkle.png')

        self.x, self.y = x, y
        self.clip_x = cx
        self.clip_y = cy
        self.size = 15

        self.item_type = item_type
        self.value = value

        if self.item_type == 'bag':
            self.image = Item.bag
        elif self.item_type == 'sparkle':
            self.image = Item.sparkle
        else:
            self.image = Item.image

    def update(self):
        pass

    def draw(self):
        draw_x = self.x - game_framework.camera_x
        draw_y = self.y - game_framework.camera_y

        if self.item_type == 'bag':
            self.image.draw(draw_x, draw_y, 130, 130)
        elif self.item_type == 'sparkle':
            self.image.draw(draw_x, draw_y, 200, 200)
            #self.image.clip_draw(0, 233, 233, 233, draw_x, draw_y, 150, 150)
        else:
            clip_bottom = self.image.h - self.clip_y - self.size
            self.image.clip_draw(self.clip_x, clip_bottom, self.size, self.size,draw_x, draw_y, 50, 50)

        if self.item_type == 'bag':
            center_x = draw_x
            center_y = draw_y
            half_w = 40
            half_h = 40
            draw_rectangle (center_x - half_w, center_y - half_h, center_x + half_w, center_y + half_h)
        else:
            center_x = draw_x
            center_y = draw_y
            half_w = 50 / 2
            half_h = 50 / 2
            draw_rectangle (center_x - half_w, center_y - half_h, center_x + half_w, center_y + half_h)



    def handle_collision(self, group, other):
        if group == 'girl:item':
            pass

    def collect(self):
        game_world.remove_object(self)

    def get_bb(self):
        if self.item_type == 'bag':
            center_x = self.x
            center_y = self.y
            half_w = 40
            half_h = 40
            return center_x - half_w, center_y - half_h, center_x + half_w, center_y + half_h
        else:
            center_x = self.x
            center_y = self.y
            half_w = 50 / 2
            half_h = 50 / 2
            return center_x - half_w, center_y - half_h, center_x + half_w, center_y + half_h
