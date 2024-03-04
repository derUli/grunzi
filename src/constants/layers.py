""" Layer constants """

from sprites.decoration.car import Car
from sprites.items.item import Fence
from sprites.items.plier import Plier

LAYER_COINS = 'Coins'
LAYER_WALL = 'Walls'
LAYER_PLIER = 'Plier'
LAYER_FENCE = 'Fence'
LAYER_DECORATION = 'Decoration'
LAYER_ENEMIES = 'Enemies'
LAYER_PLAYER = 'player'
LAYER_MOVEABLE = 'Moveable'
LAYER_PLACE = 'Place'
LAYER_SPAWN_POINT = 'Spawn Point'
LAYER_CAR_RIGHT = 'Cars Right'

LAYER_OPTIONS = {
    LAYER_PLIER: {
        'custom_class': Plier
    },
    LAYER_FENCE: {
        'custom_class': Fence
    },
    LAYER_CAR_RIGHT: {
        'custom_class': Car
    }
}
