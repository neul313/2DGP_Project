from pico2d import *
import game_world
import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class Item:
    image = None
    bag  = None
    sparkle = None
    cloth = None

    def __init__(self, x, y, cx, cy, item_type = 'hp', value = 20):
        if Item.image is None:
            Item.image = load_image('items.png')

        if Item.bag is None:
            Item.bag = load_image('bag.png')

        if Item.sparkle is None:
            Item.sparkle = load_image('twinkle.png')

        if Item.cloth is None:
            Item.cloth = load_image('item/패딩.png')

        self.x, self.y = x, y
        self.clip_x = cx
        self.clip_y = cy
        self.size = 15

        self.item_type = item_type
        self.value = value

        if self.item_type == 'bag':
            self.image = Item.bag
        elif self.item_type == 'card' or self.item_type == 'clothes':
            self.image = Item.sparkle
            self.frame = 0
            self.max_frame = 3
            self.f_w = 300
            self.f_h = 300
        else:
            self.image = Item.image

    def update(self):
        if self.item_type == 'card' or self.item_type == 'clothes':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.max_frame

    def draw(self):
        draw_x = self.x - game_framework.camera_x
        draw_y = self.y - game_framework.camera_y

        if self.item_type == 'bag':
            self.image.draw(draw_x, draw_y, 130, 130)

        elif self.item_type == 'card':
            self.image.clip_draw(int(self.frame) * self.f_w, 0, self.f_w, self.f_h,
                                 draw_x, draw_y, 130, 90)

        elif self.item_type == 'clothes':
            self.image.clip_draw(int(self.frame) * self.f_w, 0, self.f_w, self.f_h,
                                 draw_x, draw_y, 130, 90)
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
