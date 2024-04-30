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

        difficulty = jsond['default'][str(difficulty)]

        if map in jsond:
            difficulty = jsond[map][str(difficulty)]

        self.max_skulls = difficulty['maxSkulls']
        self.skull_spawn_range = tuple(difficulty['skullSpawnRange'])
        self.skull_hurt = difficulty['skullHurt']
