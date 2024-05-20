import random
import time

import logging

from sprites.characters.chicken import spawn_chicken
from utils.scene import get_layer


class NPCSpawner:
    def __init__(self):
        self.next_spawn = 0
        self.initial_spawn = False

    def setup(self):
        self.next_spawn = 0
        self.initial_spawn = False

        return self

    def update(self, args):
        if time.time() <= self.next_spawn:
            return

        if not self.initial_spawn:
            self.spawn_initial(args)

        from constants.layers import LAYER_NPC

        enemies = get_layer(LAYER_NPC, args.scene)

        if len(enemies) >= args.state.difficulty.max_npcs:
            return

        self.spawn(args)

        self.next_spawn = time.time() + random.randint(1, 6)

    def spawn(self, args):
        what = random.choice([
            'skull'
        ])

        logging.info('Spawn ' + what)

        if what == 'skull':
            self.spawn_skull(args)

    def spawn_skull(self, args):
        from sprites.characters.skull import spawn_skull
        spawn_skull(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def spawn_initial(self, args):

        for i in range(random.randint(1, 3)):
            logging.info(f"Spawn chicken {i}")
            spawn_chicken(args.state, args.tilemap.map, args.scene, args.physics_engine)

        self.initial_spawn = True
