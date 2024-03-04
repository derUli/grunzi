from sprites.decoration.car import Car
from sprites.items.item import Fence
from sprites.items.plier import Plier

SPRITE_LIST_COINS = 'Coins'
SPRITE_LIST_WALL = 'Walls'
SPRITE_LIST_PLIER = 'Plier'
SPRITE_LIST_FENCE = 'Fence'
SPRITE_LIST_DECORATION = 'Decoration'
SPRITE_LIST_ENEMIES = 'Enemies'
SPRITE_LIST_PLAYER = 'player'
SPRITE_LIST_MOVEABLE = 'Moveable'
SPRITE_LIST_PLACE = 'Place'
SPRITE_LIST_SPAWN_POINT = 'Spawn Point'
SPRITE_LIST_CAR_RIGHT = 'Cars Right'

LAYER_OPTIONS = {
    SPRITE_LIST_PLIER: {
        'custom_class': Plier
    },
    SPRITE_LIST_FENCE: {
        'custom_class': Fence
    },
    SPRITE_LIST_CAR_RIGHT: {
        'custom_class': Car
    }
}
