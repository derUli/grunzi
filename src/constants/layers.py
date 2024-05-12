""" Layer constants """
import arcade
from arcade import Scene

import sprites.decoration.car
from sprites.characters.duck import Duck
from sprites.decoration.cloud import Cloud
from sprites.decoration.sun import Sun
from sprites.items.Cone import Cone
from sprites.items.carkey import CarKey
from sprites.items.chainsaw import Chainsaw
from sprites.items.hammer import Hammer
from sprites.items.item import Fence, PiggyBank, Jeep, Water, Tree, Electric
from sprites.items.plier import Plier
from sprites.items.redherring import Feather, Vase
from sprites.sounds.beach import Beach
from sprites.sounds.highway import Highway

LAYER_WALL = 'Wall'
LAYER_PLIER = 'Plier'
LAYER_TREE = 'Tree'
LAYER_HAMMER = 'Hammer'
LAYER_FEATHER = 'Feather'
LAYER_VASE = 'Vase'
LAYER_FENCE = 'Fence'
LAYER_PIGGYBANK = 'PiggyBank'
LAYER_DECORATION = 'Decoration'
LAYER_ENEMIES = 'Enemies'
LAYER_PLAYER = 'Player'
LAYER_MOVEABLE = 'Moveable'
LAYER_PLACE = 'Place'
LAYER_SPAWN_POINT = 'Spawn Point'
LAYER_CAR_LEFT = 'CarLeft'
LAYER_CAR_RIGHT = 'CarRight'
LAYER_CAR_KEY = 'CarKey'
LAYER_CHAINSAW = 'Chainsaw'
LAYER_DUCK = 'Duck'
LAYER_JEEP = 'Jeep'
LAYER_HIGHWAY = 'Highway'
LAYER_BEACH = 'Beach'
LAYER_WATER = 'Water'
LAYER_CONES = 'Cone'
LAYER_CLOUDS = 'Clouds'
LAYER_SKY = 'Sky'
LAYER_SUN = 'Sun'
LAYER_ELECTRIC = 'Electric'

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
    LAYER_WATER,
    LAYER_SKY,
    LAYER_SUN,
    LAYER_ELECTRIC
]

WALL_LAYERS = [
    LAYER_WALL,
    LAYER_FENCE,
    LAYER_JEEP,
    LAYER_WATER,
    LAYER_SKY
]

SKY_LAYERS = [
    LAYER_CLOUDS,
    LAYER_SUN
]

TRAFFIC_LAYERS = [
    LAYER_CAR_LEFT,
    LAYER_CAR_RIGHT
]

ANIMATED_LAYERS = [
    LAYER_WATER,
    LAYER_ELECTRIC
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
    LAYER_CONES: {
        'custom_class': Cone
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
    },
    LAYER_DUCK: {
        'custom_class': Duck
    },
    LAYER_CLOUDS: {
        'custom_class': Cloud
    },
    LAYER_SUN: {
        'custom_class': Sun
    },
    LAYER_ELECTRIC: {
        'custom_class': Electric
    }
}


def check_collision_with_layers(scene: Scene, sprite, layer_names: list | None = None):
    """ Returns all layers except background and decoration
       @param scene: The scene
       @param sprite: The sprite
       @param layer_names: the layer names
       @return:
       """
    if layer_names is None:
        layer_names = ALL_LAYERS

    for layer in layer_names:
        if layer not in scene.name_mapping:
            continue

        if arcade.check_for_collision_with_list(sprite, scene[layer]):
            return True

    return False
