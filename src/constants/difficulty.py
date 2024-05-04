""" Difficulty constants """
import json
import os

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3


class Difficulty:
    def __init__(self, difficulty, map, level_dir):
        maps = os.path.join(level_dir, 'maps.json')

        with open(maps, 'r') as f:
            jsond = json.load(f)

        difficulty_data = jsond['default'][str(difficulty)]

        if map in jsond:
            difficulty_data = jsond[map][str(difficulty)]

        self.max_skulls = 0
        self.skull_spawn_range = 0
        self.skull_hurt = 0

        if 'maxSkulls' in difficulty_data:
            self.max_skulls = difficulty_data['maxSkulls']

        if 'skullSpawnRange' in difficulty_data:
            self.skull_spawn_range = tuple(difficulty_data['skullSpawnRange'])

        if 'skullHurt' in difficulty_data:
            self.skull_hurt = difficulty_data['skullHurt']
