import logging
import random
import time

import pyglet.clock
from arcade import SpriteList

from constants.layers import LAYER_SNOW
from sprites.characters.chicken import spawn_chicken
from sprites.decoration.hellparticle import HELL_PARTICLE_COLORS, HellParticle
from sprites.decoration.snow import Snow, SNOW_COLORS
from sprites.items.food import spawn_food
from sprites.items.landmine import spawn_landmine
from state.argscontainer import ArgsContainer
from utils.performance import chunk
from utils.text import label_value

SPAWN_CHICKEN = 'chicken'
SPAWN_HELL_PARTICLE = 'hell_particle'
SPAWN_SNOW = 'snow'
SPAWN_FOOD = 'food'
SPAWN_LANDMINE = 'landmine'

SPAWN_INTERVAL = 1 / 36
CHUNK_SIZE = 50


class MapPopulator:
    def __init__(self, benchmark_mode: bool = False):
        """ Constructor """

        self.next_spawn = 0
        self.enabled = True
        self.spawn_what = []
        self.spawn_what_chunks = None
        self.initialized = None
        self.benchmark_mode = benchmark_mode

    def update(self, args: ArgsContainer) -> None:
        logging.error('MapPopulator update() not implemented')

    def spawn_next_initial(self, dt, args):
        if not self.initialized:
            self.initialized = time.time()

        if not self.spawn_what_chunks:
            self.spawn_what_chunks = list(chunk(self.spawn_what, CHUNK_SIZE))

        items = self.spawn_what_chunks.pop()

        for item in items:
            logging.debug('Initial spawn ' + item)

            if item == SPAWN_CHICKEN:
                spawn_chicken(args.state, args.map_size, args.scene, args.physics_engine)
            if item == SPAWN_HELL_PARTICLE:
                self.spawn_hell_particles(args)
            if item == SPAWN_SNOW:
                self.spawn_snow(args)
            if item == SPAWN_FOOD:
                self.spawn_food(args)
            if item == SPAWN_LANDMINE:
                self.spawn_landmine(args)

        if not any(self.spawn_what_chunks):
            logging.info('MapPopulator initialized in ' + str(time.time() - self.initialized) + ' seconds')
            return

        pyglet.clock.schedule_once(self.spawn_next_initial, SPAWN_INTERVAL, args)

    def spawn(self, args: ArgsContainer) -> None:

        # Don't spawn enemies in benchmark mode
        if self.benchmark_mode:
            return

        if not self.enabled:
            return

        if not any(args.state.difficulty.spawn_what):
            return

        what = random.choice(args.state.difficulty.spawn_what)
        logging.info('Spawn ' + what)

        if what == 'Skull':
            self.spawn_skull(args)
        elif what == 'Slimer':
            self.spawn_slimer(args)
        elif what == 'Barrel':
            self.spawn_barrel(args)

        self.next_spawn = time.time() + random.randint(1, 6)

    def spawn_skull(self, args: ArgsContainer) -> None:
        """
        Spawn a skull
        
        @param: ArgsContainer
        """
        from sprites.characters.skull import spawn_skull
        spawn_skull(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def spawn_slimer(self, args: ArgsContainer) -> None:
        """
        Spawn a slimer

        @param: ArgsContainer
        """
        from sprites.characters.slimer import spawn_slimer
        spawn_slimer(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def spawn_barrel(self, args: ArgsContainer) -> None:
        """
        Spawn a slimer

        @param: ArgsContainer
        """
        from sprites.characters.barrel import spawn_barrel
        spawn_barrel(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def spawn_npcs(self, args: ArgsContainer) -> None:
        """ Spawn some sprites on level load """

        if not self.enabled:
            return

        self.schedule_chicken(args)

    def spawn_initial(self, args: ArgsContainer) -> None:
        """ Spawn some sprites on level load """

        logging.error('MapPopulator spawn_initial() not implemented')

    def init_npc_spritelist(self, args):
        from constants.layers import LAYER_NPC, LAYER_FOOD

        args.scene.add_sprite_list(LAYER_FOOD, SpriteList(lazy=True, use_spatial_hash=True))
        args.scene.add_sprite_list(LAYER_NPC, SpriteList(lazy=True, use_spatial_hash=True))

    def schedule_landmine(self, args):
        if not args.state.difficulty.options['landmines']:
            return

        x = range(random.randint(1, 4))

        if self.benchmark_mode:
            x = range(5)

        for i in x:
            self.spawn_what.append(SPAWN_LANDMINE)

    def spawn_landmine(self, args: ArgsContainer) -> None:
        spawn_landmine(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def schedule_chicken(self, args: ArgsContainer) -> None:
        if not args.state.difficulty.options['chicken']:
            return

        x = range(random.randint(2, 5))

        if self.benchmark_mode:
            x = range(500)

        for i in x:
            self.spawn_what.append(SPAWN_CHICKEN)

    def schedule_food(self, args: ArgsContainer):

        x = range(random.randint(1, 10))

        if self.benchmark_mode:
            x = range(5)

        for i in x:
            self.spawn_what.append(SPAWN_FOOD)

    def spawn_food(self, args: ArgsContainer) -> None:
        spawn_food(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def schedule_snow(self, args: ArgsContainer) -> None:
        if not args.state.difficulty.options['snow']:
            return

        if not args.state.settings.weather:
            return

        for i in range(1, 1000):
            self.spawn_what.append(SPAWN_SNOW)

    def spawn_snow(self, args: ArgsContainer) -> None:
        snow = Snow(radius=8, color=random.choice(SNOW_COLORS), soft=True)
        snow.center_x = random.randint(0, args.tilemap.width)
        snow.center_y = random.randint(0, args.tilemap.height)

        args.scene.add_sprite(LAYER_SNOW, snow)

    def schedule_hell_particles(self, args):
        if not args.state.difficulty.options['hellParticles']:
            return

        if not args.state.settings.weather:
            return

        for i in range(1, 500):
            self.spawn_what.append(SPAWN_HELL_PARTICLE)

    def spawn_hell_particles(self, args: ArgsContainer) -> None:
        radius = random.randint(1, 14)
        particle = HellParticle(radius=radius, color=random.choice(HELL_PARTICLE_COLORS), soft=True)
        particle.center_x = random.randint(0, args.tilemap.width)
        particle.center_y = random.randint(0, args.tilemap.height)

        args.scene.add_sprite(LAYER_SNOW, particle)


def init_map_populator(gamemode: str, benchmark_mode: bool = False) -> MapPopulator:
    from constants.gamemode import GAMEMODE_CAMPAIGN

    if gamemode == GAMEMODE_CAMPAIGN:
        from utils.mappopulator.campaignmappopulator import CampaignMapPopulator
        return CampaignMapPopulator(benchmark_mode)
    else:
        gamemode = 'Unknown'

    logging.error(label_value('MapPopulator', gamemode))
