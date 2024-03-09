""" Layer constants """

""" Layer constants """

from arcade import SpriteList, Scene

import sprites.decoration.car
from sprites.items.hammer import Hammer
from sprites.items.item import Fence, PiggyBank
from sprites.items.plier import Plier
from sprites.items.redherring import Feather, Vase
from sprites.sounds.highway import Highway

LAYER_WALL = 'Walls'
LAYER_PLIER = 'Plier'
LAYER_HAMMER = 'Hammer'
LAYER_FEATHER = 'Feathers'
LAYER_VASE = 'Vase'
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
    LAYER_WALL: {
        'use_spatial_hash': True
    },
    LAYER_FENCE: {
        'use_spatial_hash': True
    },
    LAYER_PLIER: {
        'custom_class': Plier
    },
    LAYER_HAMMER: {
        'custom_class': Hammer
    },
    LAYER_PIGGYBANK: {
        'custom_class': PiggyBank
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
    LAYER_FEATHER: {
        'custom_class': Feather
    },
    LAYER_VASE: {
        'custom_class': Vase
    }
}


def all_layers(scene: Scene, layer_names: list | None = None):
    """ Returns all layers except background and decoration
    @param scene: The scene
    @param layer_names: the layer names
    @return:
    """
    if layer_names is None:
        layer_names = ALL_LAYERS

    sprite_list = SpriteList(use_spatial_hash=False)

    for layer in scene.name_mapping:
        if layer not in layer_names:
            scene.add_sprite_list(layer)

        for sprite in scene.get_sprite_list(layer):
            sprite_list.append(sprite)

    return sprite_list
