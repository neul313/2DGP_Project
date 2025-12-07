from pico2d import *
import game_framework
import game_world

class Door:
    def __init__(self,x,y,door_id =1,stage = None):
        self.x = x
        self.y = y
        self.door_id = door_id

        self.width = 50
        self.height = 400

        self.stage = stage

    def update(self):
        pass

    def draw(self):
        draw_x = self.x - game_framework.camera_x
        draw_y = self.y - game_framework.camera_y
        #draw_rectangle(draw_x - 50, draw_y - 50, draw_x +50, draw_y+300)

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 300

    def handle_collision(self,group, other):
        pass

    def unlock(self):
        game_world.remove_object(self)