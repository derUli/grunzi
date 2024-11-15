""" Map config class """

import os

import orjson

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3


class MapConfig:
    """ map config class"""

    def __init__(self, difficulty: int, map_name: str, level_dir: str):
        """ Constructor """

        self.max_npcs = 0
        self.skull_hurt = 0
        self.slimer_hurt = 0
        self.barrel_hurt = 0
        self.boss_laser_hurt = 0

        self.health_regeneration_speed = 0

        self.spawn_what = []
        self.options = {}

        self.setup(difficulty, map_name, level_dir)

    def setup(self, difficulty: int, map_name: str, level_dir: str) -> None:
        """ Setup difficulty """

        self.reset()

        maps = os.path.join(level_dir, 'maps.json')

        with open(maps, 'r', encoding='utf-8') as f:
            jsond = orjson.loads(f.read())

        difficulty_data = jsond['default'][str(difficulty)]

        if 'skullHurt' in difficulty_data:
            self.skull_hurt = difficulty_data['skullHurt']
        if 'slimerHurt' in difficulty_data:
            self.slimer_hurt = difficulty_data['slimerHurt']
        if 'barrelHurt' in difficulty_data:
            self.barrel_hurt = difficulty_data['barrelHurt']
        if 'bossLaserHurt' in difficulty_data:
            self.boss_laser_hurt = difficulty_data['bossLaserHurt']
        if 'healthRegenerationSpeed' in difficulty_data:
            self.health_regeneration_speed = difficulty_data['healthRegenerationSpeed']

        map_data = {}

        if map_name in jsond:
            map_data = jsond[map_name]
            try:
                difficulty_data = map_data[str(difficulty)]
            except KeyError:
                pass

        if 'options' in map_data:
            for key in map_data['options'].keys():
                self.options[key] = map_data['options'][key]

        if 'spawnWhat' in map_data:
            self.spawn_what = map_data['spawnWhat']

        if 'maxNPCs' in difficulty_data:
            self.max_npcs = difficulty_data['maxNPCs']

    def reset(self) -> None:
        """ Reset values """

        self.max_npcs = 0
        self.skull_hurt = 0
        self.slimer_hurt = 0
        self.barrel_hurt = 0
        self.spawn_what = []
        self.options = {
            'chicken': False,
            'fog': False,
            'lighting': None,
            'landmines': False,
            'snow': False,
            'hellParticles': False
        }
