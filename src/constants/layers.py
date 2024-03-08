""" Layer constants """

from arcade import SpriteList

import sprites.decoration.car
from sprites.items.hammer import Hammer
from sprites.items.item import Fence, PiggyBank
from sprites.items.plier import Plier
from sprites.items.redherring import RedHerring
from sprites.sounds.highway import Highway

LAYER_WALL = 'Walls'
LAYER_PLIER = 'Plier'
LAYER_HAMMER = 'Hammer'
LAYER_RED_HERRINGS = 'Red Herrings'
LAYER_FENCE = 'Fence'
LAYER_PIGGYBANK = 'Piggybanks'
LAYER_DECORATION = 'Decoration'
LAYER_ENEMIES = 'Enemies'
LAYER_PLAYER = 'player'
LAYER_MOVEABLE = 'Moveable'
LAYER_PLACE = 'Place'
LAYER_SPAWN_POINT = 'Spawn Point'
LAYER_CAR_LEFT = 'Cars Left'
LAYER_CAR_RIGHT = 'Cars Right'

LAYER_HIGHWAY = 'Highway'

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

WALL_LAYERS = [
    LAYER_WALL,
    LAYER_FENCE
]

LAYER_OPTIONS = {
    LAYER_PLIER: {
        'custom_class': Plier
    },
    LAYER_HAMMER: {
        'custom_class': Hammer
    },
    LAYER_PIGGYBANK: {
        'custom_class': PiggyBank
    },
    LAYER_FENCE: {
        'custom_class': Fence
    },
    LAYER_HIGHWAY: {
        'custom_class': Highway
    },
    LAYER_CAR_RIGHT: {
        'custom_class': sprites.decoration.car.CarRight
    },
    LAYER_CAR_LEFT: {
        'custom_class': sprites.decoration.car.CarLeft
    },
    LAYER_RED_HERRINGS: {
        'custom_class': RedHerring
    }
}


def all_layers(scene, layer_names=None):
    """ Returns all layers except background and decoration"""
    if layer_names is None:
        layer_names = ALL_LAYERS

    sprite_list = SpriteList(use_spatial_hash=False)

    for layer in scene.name_mapping:
        if layer not in layer_names:
            scene.add_sprite_list(layer)

        for sprite in scene.get_sprite_list(layer):
            sprite_list.append(sprite)

    return sprite_list
