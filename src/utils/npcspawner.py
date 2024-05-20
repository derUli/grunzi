import logging
import random
import time

from sprites.characters.chicken import spawn_chicken
from utils.scene import get_layer


class NPCSpawner:
    def __init__(self):
        self.next_spawn = 0
        self.initial_spawn = False

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

    def spawn(self, args):

        if not any(args.state.difficulty.spawn_what):
            return

        what = random.choice(args.state.difficulty.spawn_what)
        logging.info('Spawn ' + what)

        if what == 'Skull':
            self.spawn_skull(args)

        self.next_spawn = time.time() + random.randint(1, 6)

    def spawn_skull(self, args):
        from sprites.characters.skull import spawn_skull
        spawn_skull(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def spawn_initial(self, args):

        for i in range(random.randint(1, 3)):
            logging.info(f"Spawn chicken {i}")
            spawn_chicken(args.state, args.tilemap.map, args.scene, args.physics_engine)

        self.initial_spawn = True
