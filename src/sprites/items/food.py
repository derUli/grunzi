import logging
import os

from constants.layers import check_collision_with_layers, LAYER_FOOD
from sprites.items.item import Item
from utils.sprite import random_position


class Food(Item):
    def eat(self, state, args, bullet_size):
        args.player.bullet_size += bullet_size

        state.play_sound('smacks')

        selected, index = args.inventory.get_selected()
        quantity = selected.pop()

        if quantity == 0:
            args.player.set_item(None)

        return True

    @property
    def layer_name(self):
        return LAYER_FOOD

class Apple(Food):
    def copy(self):
        """ Copy item """
        return Apple(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )

    def on_use(self, state, args):
        return self.eat(state, args, 2)

def spawn_food(state, tilemap, scene, physics_engine):
    rand_x, rand_y = random_position(tilemap)

    food = Apple(
        filename=os.path.join(state.sprite_dir, 'food', 'apple.png'),
        center_x=rand_x,
        center_y=rand_y
    )

    try:
        if check_collision_with_layers(scene, food):
            return spawn_food(state, tilemap, scene, physics_engine)
    except AttributeError as e:
        logging.error(e)
        return

    scene.add_sprite(LAYER_FOOD, food)
