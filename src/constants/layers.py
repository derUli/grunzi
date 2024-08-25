""" Layer constants """

import arcade
from arcade import Scene

import sprites.decoration.car
from sprites.characters.duck import Duck
from sprites.characters.fish import Fish
from sprites.decoration.cloud import Cloud
from sprites.decoration.fire import Fire
from sprites.decoration.moon import Moon
from sprites.decoration.river import River, RiverSound
from sprites.decoration.ship import Ship, Steam
from sprites.decoration.sun import Sun
from sprites.decoration.water import Water
from sprites.items.Cone import Cone
from sprites.items.cactus import Cactus
from sprites.items.carkey import CarKey
from sprites.items.chainsaw import Chainsaw
from sprites.items.electric import Electric
from sprites.items.electricswitch import ElectricSwitch
from sprites.items.fence import Fence
from sprites.items.hammer import Hammer
from sprites.items.jeep import Jeep
from sprites.items.levelexit import LevelExit
from sprites.items.piggybank import PiggyBank
from sprites.items.plier import Plier
from sprites.items.portal import Portal
from sprites.items.redherring import Feather, Vase
from sprites.items.switch import Switch
from sprites.items.tree import Tree
from sprites.items.valve import Valve
from sprites.items.valvetarget import ValveTarget
from sprites.sounds.beach import Beach
from sprites.sounds.highway import Highway
from sprites.sprite import AlphaWall

LAYER_WALL = 'Wall'
LAYER_ALPHA_WALL = 'AlphaWall'
LAYER_PLIER = 'Plier'
LAYER_TREE = 'Tree'
LAYER_HAMMER = 'Hammer'
LAYER_FEATHER = 'Feather'
LAYER_VASE = 'Vase'
LAYER_FENCE = 'Fence'
LAYER_PIGGYBANK = 'PiggyBank'
LAYER_DECORATION = 'Decoration'
LAYER_NPC = 'NPC'
LAYER_PLAYER = 'Player'
LAYER_MOVEABLE = 'Moveable'
LAYER_PLACE = 'Place'
LAYER_SPAWN_POINT = 'SpawnPoint'
LAYER_CAR_LEFT = 'CarLeft'
LAYER_CAR_RIGHT = 'CarRight'
LAYER_CAR_KEY = 'CarKey'
LAYER_VALVE = 'Valve'
LAYER_VALVE_TARGET = 'ValveTarget'
LAYER_CHAINSAW = 'Chainsaw'
LAYER_DUCK = 'Duck'
LAYER_JEEP = 'Jeep'
LAYER_HIGHWAY = 'Highway'
LAYER_BEACH = 'Beach'
LAYER_WATER = 'Water'
LAYER_FIRE = 'Fire'
LAYER_CONES = 'Cone'
LAYER_CLOUDS = 'Cloud'
LAYER_SKY = 'Sky'
LAYER_SUN = 'Sun'
LAYER_MOON = 'Moon'
LAYER_ELECTRIC = 'Electric'
LAYER_ELECTRIC_SWITCH = 'ElectricSwitch'
LAYER_LEVEL_EXIT = 'LevelExit'
LAYER_RIVER = 'River'
LAYER_RIVER_SOUND = 'RiverSound'
LAYER_FISH = 'Fish'
LAYER_FOOD = 'Food',
LAYER_CACTUS = 'Cactus'
LAYER_SHIP = 'Ship'
LAYER_STEAM = 'Steam'
LAYER_SNOW = 'Snow'
LAYER_PORTAL = 'Portal'
LAYER_SWITCH = 'Switch'

ALL_LAYERS = [
    LAYER_WALL,
    LAYER_NPC,
    LAYER_MOVEABLE,
    LAYER_PLAYER,
    LAYER_FENCE,
    LAYER_DECORATION,
    LAYER_SPAWN_POINT,
    LAYER_CAR_LEFT,
    LAYER_CAR_RIGHT,
    LAYER_WATER,
    LAYER_FIRE,
    LAYER_SKY,
    LAYER_SUN,
    LAYER_MOON,
    LAYER_ELECTRIC,
    LAYER_ELECTRIC_SWITCH,
    LAYER_RIVER,
    LAYER_FOOD,
    LAYER_CACTUS,
]

WALL_LAYERS = [
    LAYER_WALL,
    LAYER_FENCE,
    LAYER_JEEP,
    LAYER_WATER,
    LAYER_SKY,
    LAYER_TREE,
    LAYER_RIVER,
    LAYER_CACTUS
]

ANIMATED_LAYERS = [
    LAYER_WATER,
    LAYER_FIRE,
    LAYER_ELECTRIC,
    LAYER_STEAM,
    LAYER_PORTAL
]

PASSIVE_LAYERS = WALL_LAYERS + ANIMATED_LAYERS + [
    LAYER_CAR_LEFT,
    LAYER_CAR_RIGHT,
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
    LAYER_VALVE: {
        'custom_class': Valve
    },
    LAYER_VALVE_TARGET: {
        'custom_class': ValveTarget
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
    LAYER_FIRE: {
        'custom_class': Fire
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
    LAYER_MOON: {
        'custom_class': Moon
    },
    LAYER_ELECTRIC: {
        'custom_class': Electric
    },
    LAYER_ELECTRIC_SWITCH: {
        'custom_class': ElectricSwitch
    },
    LAYER_LEVEL_EXIT: {
        'custom_class': LevelExit
    },
    LAYER_RIVER: {
        'custom_class': River
    },
    LAYER_RIVER_SOUND: {
        'custom_class': RiverSound
    },
    LAYER_FISH: {
        'custom_class': Fish
    },
    LAYER_CACTUS: {
        'custom_class': Cactus
    },
    LAYER_ALPHA_WALL: {
        'custom_class': AlphaWall
    },
    LAYER_SHIP: {
        'custom_class': Ship
    },
    LAYER_STEAM: {
        'custom_class': Steam
    },
    LAYER_SWITCH: {
        'custom_class': Switch
    },
    LAYER_PORTAL: {
        'custom_class': Portal
    }
}


def check_collision_with_layers(scene: Scene, sprite, layer_names: list | None = None) -> bool:
    """
    Returns all layers except background and decoration
    @param scene: The scene
    @param sprite: The sprite
    @param layer_names: the layer names
    @return: Boolean
    """

    if layer_names is None:
        layer_names = ALL_LAYERS

    for layer in layer_names:
        if layer not in scene.name_mapping:
            continue

        if arcade.check_for_collision_with_list(sprite, scene[layer]):
            return True

    return False
