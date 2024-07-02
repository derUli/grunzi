""" Map config class """

import os

import orjson

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3


class MapConfig:
    """ map config class"""

    def __init__(self, difficulty, map_name, level_dir):
        """ Constructor """

        self.max_npcs = 0
        self.skull_hurt = 0
        self.slimer_hurt = 0
        self.spawn_what = []
        self.options = {}

        self.setup(difficulty, map_name, level_dir)

    def reset(self):
        """ Reset values """

        self.max_npcs = 0
        self.skull_hurt = 0
        self.slimer_hurt = 0
        self.spawn_what = []
        self.options = {
            'chicken': False,
            'fog': False,
            'sun': False,
            'lighting': None,
            'landmines': False,
        }

    def setup(self, difficulty, map_name, level_dir) -> None:
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

        map_data = {}

        if map_name in jsond:
            map_data = jsond[map_name]
            difficulty_data = map_data[str(difficulty)]

        if 'options' in map_data:
            for key in map_data['options'].keys():
                self.options[key] = map_data['options'][key]

        if 'spawnWhat' in map_data:
            self.spawn_what = map_data['spawnWhat']

        if 'maxNPCs' in difficulty_data:
            self.max_npcs = difficulty_data['maxNPCs']
