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

        self.max_npcs = 0
        self.skull_hurt = 0
        self.spawn_what = []

        self.setup(difficulty, map_name, level_dir)

    def reset(self):
        """ Reset values """

        self.max_npcs = 0
        self.skull_hurt = 0
        self.spawn_what = []

    def setup(self, difficulty, map_name, level_dir) -> None:
        """ Setup difficulty """

        self.reset()

        maps = os.path.join(level_dir, 'maps.json')

        with open(maps, 'r', encoding='utf-8') as f:
            jsond = json.load(f)

        difficulty_data = jsond['default'][str(difficulty)]

        if 'skullHurt' in difficulty_data:
            self.skull_hurt = difficulty_data['skullHurt']

        map_data = {}

        if map_name in jsond:
            map_data = jsond[map_name]
            difficulty_data = map_data[str(difficulty)]

        if 'spawnWhat' in map_data:
            self.spawn_what = map_data['spawnWhat']

        if 'maxNPCs' in difficulty_data:
            self.max_npcs = difficulty_data['maxNPCs']
