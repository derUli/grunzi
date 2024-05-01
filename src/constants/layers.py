""" Layer constants """

from arcade import SpriteList, Scene

import sprites.decoration.car
from sprites.items.carkey import CarKey
from sprites.items.chainsaw import Chainsaw
from sprites.items.hammer import Hammer
from sprites.items.item import Fence, PiggyBank, Jeep, Water, Tree
from sprites.items.plier import Plier
from sprites.items.redherring import Feather, Vase
from sprites.sounds.beach import Beach
from sprites.sounds.highway import Highway

LAYER_WALL = 'Walls'
LAYER_PLIER = 'Plier'
LAYER_TREE = 'Tree'
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
LAYER_CAR_KEY = 'Car Key'
LAYER_CHAINSAW = 'Chainsaw'
LAYER_JEEP = 'Jeep'
LAYER_HIGHWAY = 'Sound:Highway'
LAYER_BEACH = 'Sound:Beach'
LAYER_WATER = 'Water'

ALL_LAYERS = [
    LAYER_WALL,
    LAYER_ENEMIES,
    LAYER_MOVEABLE,
    LAYER_PLAYER,
    LAYER_FENCE,
    LAYER_DECORATION,
    LAYER_SPAWN_POINT,
    LAYER_CAR_LEFT,
    LAYER_CAR_RIGHT,
    LAYER_WATER
]

WALL_LAYERS = [
    LAYER_WALL,
    LAYER_FENCE,
    LAYER_JEEP,
    LAYER_WATER
]

LAYER_OPTIONS = {
    LAYER_FENCE: {
        'custom_class': Fence
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
    LAYER_BEACH: {
        'custom_class': Beach
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
    },
    LAYER_CAR_KEY: {
        'custom_class': CarKey
    },
    LAYER_CHAINSAW: {
        'custom_class': Chainsaw
    },
    LAYER_TREE: {
        'custom_class': Tree
    },
    LAYER_JEEP: {
        'custom_class': Jeep
    },
    LAYER_WATER: {
        'custom_class': Water
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
