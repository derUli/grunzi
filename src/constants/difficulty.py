""" Difficulty constants """

import json
import os

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3


class Difficulty:
    """ Difficulty class"""

    def __init__(self, difficulty, map_name, level_dir):
        """ Constructor """

        self.max_skulls = 0
        self.skull_spawn_range = 0
        self.skull_hurt = 0

        self.setup(difficulty, map_name, level_dir)

    def reset(self):
        """ Reset values """

        self.max_skulls = 0
        self.skull_spawn_range = 0
        self.skull_hurt = 0

    def setup(self, difficulty, map_name, level_dir) -> None:
        """ Setup difficulty """

        maps = os.path.join(level_dir, 'maps.json')

        with open(maps, 'r', encoding='utf-8') as f:
            jsond = json.load(f)

        difficulty_data = jsond['default'][str(difficulty)]

        if map_name in jsond:
            difficulty_data = jsond[map_name][str(difficulty)]

        self.reset()

        if 'maxSkulls' in difficulty_data:
            self.max_skulls = difficulty_data['maxSkulls']

        if 'skullSpawnRange' in difficulty_data:
            self.skull_spawn_range = tuple(difficulty_data['skullSpawnRange'])

        if 'skullHurt' in difficulty_data:
            self.skull_hurt = difficulty_data['skullHurt']
