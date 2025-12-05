from pico2d import *

import game_framework
import game_world

from girl import Girl
from stage1 import Stage1
from item import Item
from HP import Bar
from inventory import Inventory
from door import Door
from popup1 import Popup


girl = None
inventory_ui = None
hp = None
mp = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            game_framework.share['girl'].handle_event(event)

def init():
    global girl
    #import stage2_mode
    import illust

    popup = Popup()
    game_framework.share['popup'] = popup
    game_world.add_object(popup, 3)

    popup.show('story_image/space.png', 2.0)

    girl = Girl()
    game_framework.share['girl'] = girl
    game_world.add_object(girl, 1)

    girl.reset_collision_info()
    girl.reset_state()

    stage1 = Stage1()
    game_world.add_object(stage1, 0)
    stage1.set_center_object(girl)

    game_world.add_collision_pair('girl:item', girl, None)

    door = Door(1020,60,1)
    game_world.add_object(door, 1)
    game_world.add_collision_pair('girl:door', girl, door)

    door2 = Door(1720, 60, 1)
    game_world.add_object(door2, 1)
    game_world.add_collision_pair('girl:door', girl, door2)

    door3 = Door(2300, 60, 1, illust)
    game_world.add_object(door3, 1)
    game_world.add_collision_pair('girl:door', girl, door3)


    item1 = Item(600, 60, 0, 0, 'hp', 20)
    game_world.add_object(item1, 1)
    game_world.add_collision_pair('girl:item', None, item1)

    item_bag = Item(450,60,30,0,'bag',4)
    game_world.add_object(item_bag, 1)
    game_world.add_collision_pair('girl:item', None, item_bag)

    item_shoes = Item(900, 60, 30, 0, 'shoes', 4)
    game_world.add_object(item_shoes, 1)
    game_world.add_collision_pair('girl:item', None, item_shoes)

    item2 = Item(1500, 60, 18, 0, 'hp', 20)
    game_world.add_object(item2, 1)
    game_world.add_collision_pair('girl:item', None, item2)

    # item_card = Item(300, 60, 0, 16, 'card', 20)
    # game_world.add_object(item_card, 1)
    # game_world.add_collision_pair('girl:item', None, item_card)

    item_sparkle = Item(310, 80, 0, 0, 'card', 20)
    game_world.add_object(item_sparkle, 1)
    game_world.add_collision_pair('girl:item', None, item_sparkle)

    item_sparkle3 = Item(1200, 80, 0, 0, 'card_purple', 20)
    game_world.add_object(item_sparkle3, 1)
    game_world.add_collision_pair('girl:item', None, item_sparkle3)

    item_sparkle4 = Item(1900, 80, 0, 0, 'card_ora', 20)
    game_world.add_object(item_sparkle4, 1)
    game_world.add_collision_pair('girl:item', None, item_sparkle4)

    item_sparkle2 = Item(180, 80, 0, 0, 'clothes', 20)
    game_world.add_object(item_sparkle2, 1)
    game_world.add_collision_pair('girl:item', None, item_sparkle2)

    inventory_ui = Inventory(girl)
    game_framework.share['inventory_ui'] = inventory_ui
    game_world.add_object(inventory_ui, 3)

    #boss = Boss()
    #game_world.add_object(boss, 0)

    hp = Bar('hp')
    mp = Bar('mp')
    game_framework.share['hp'] = hp
    game_framework.share['mp'] = mp
    game_world.add_object(hp, 3)
    game_world.add_object(mp, 3)

    game_world.add_collision_pair('missile:girl', None, girl)



def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    pass

def pause(): pass
def resume(): pass