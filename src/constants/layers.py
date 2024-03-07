""" Layer constants """
from arcade import SpriteList

import sprites.decoration.car
from sprites.items.hammer import Hammer
from sprites.items.item import Fence
from sprites.items.plier import Plier

LAYER_WALL = 'Walls'
LAYER_PLIER = 'Plier'
LAYER_HAMMER = 'Hammer'
LAYER_FENCE = 'Fence'
LAYER_DECORATION = 'Decoration'
LAYER_ENEMIES = 'Enemies'
LAYER_PLAYER = 'player'
LAYER_MOVEABLE = 'Moveable'
LAYER_PLACE = 'Place'
LAYER_SPAWN_POINT = 'Spawn Point'
LAYER_CAR_LEFT = 'Cars Left'
LAYER_CAR_RIGHT = 'Cars Right'

ALL_LAYERS = [
    LAYER_WALL,
    LAYER_ENEMIES,
    LAYER_MOVEABLE,
    LAYER_PLAYER,
    LAYER_FENCE,
    LAYER_DECORATION,
    LAYER_SPAWN_POINT,
    LAYER_CAR_LEFT,
    LAYER_CAR_RIGHT
]

LAYER_OPTIONS = {
    LAYER_PLIER: {
        'custom_class': Plier
    },
    LAYER_HAMMER: {
        'custom_class': Hammer
    },
    LAYER_FENCE: {
        'custom_class': Fence
    },
    LAYER_CAR_RIGHT: {
        'custom_class': sprites.decoration.car.CarRight
    },
    LAYER_CAR_LEFT: {
        'custom_class': sprites.decoration.car.CarLeft
    }
}


def all_layers(scene):
    """ Returns all layers except background and decoration"""
    sprite_list = SpriteList(use_spatial_hash=False)

    layer_names = ALL_LAYERS

    for layer in scene.name_mapping:
        if layer not in layer_names:
            scene.add_sprite_list(layer)

        for sprite in scene.get_sprite_list(layer):
            sprite_list.append(sprite)

    return sprite_list
