import logging
import os
import sys
import threading
import time

import arcade
import pyglet

from constants.layers import LAYER_OPTIONS
from constants.mapconfig import MapConfig
from sprites.characters.player import Player
from state.argscontainer import make_args_container
from state.savegamestate import SaveGameState
from utils.callbackhandler import CallbackHandler
from utils.mappopulator import MapPopulator
from utils.media.audio import MusicQueue
from utils.physics import make_physics_engine
from utils.scene import Scene
from utils.tilemap import TileMap
from window.gamewindow import UPDATE_RATE


class Loader:
    def __init__(self):
        self.threads = []
        self.started_at = None
        self.completed_at = None

    """ Async load map """

    def run(self, klaas) -> None:
        self.started_at = time.time()
        self.completed_at = None
        self.threads = []

        self.threads.append(threading.Thread(target=self.init_level, args=(klaas,)))
        self.threads.append(threading.Thread(target=self.init_music_queue, args=(klaas,)))

        for thread in self.threads:
            thread.start()

    @staticmethod
    def init_level(klaas):
        klaas.ui.loading_screen.show = True

        savegame = SaveGameState.load()
        savegame.current = klaas.state.map_name
        savegame.save()

        # Set up the Cameras
        klaas.camera_sprites = arcade.Camera()
        klaas.state.reset()
        klaas.state.difficulty = MapConfig(savegame.difficulty, klaas.state.map_name, klaas.state.map_dir)

        # Name of map file to load
        map_name = os.path.join(klaas.state.map_dir, f"{klaas.state.map_name}.tmx")

        # Read in the tiled map
        try:
            klaas.tilemap = TileMap(
                map_name,
                layer_options=LAYER_OPTIONS
            )
        except FileNotFoundError as e:
            logging.error(e)
            sys.exit(1)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        klaas.scene = Scene.from_tilemap(klaas.tilemap.map)

        klaas.map_populator = MapPopulator()
        klaas.map_populator.spawn_initial(make_args_container(klaas))

        # Set up the player, specifically placing it at these coordinates.
        filename = os.path.join(klaas.state.sprite_dir, 'char', 'pig.png')
        klaas.player_sprite = Player(filename)

        klaas.player_sprite.setup(
            state=klaas.state,
            scene=klaas.scene,
            callbacks=CallbackHandler(
                on_complete=klaas.on_next_level
            ),
            controllers=klaas.window.controllers
        )

        # Create the physics engine
        klaas.physics_engine = make_physics_engine(klaas.player_sprite, klaas.scene)

        klaas.map_populator.spawn_npcs(make_args_container(klaas))

        klaas.wall_spritelist = klaas.scene.make_wall_spritelist()

        sprite = arcade.SpriteSolidColor(
            width=64,
            height=64,
            color=arcade.color.BLACK
        )

        klaas.astar_barrier_list = arcade.AStarBarrierList(
            moving_sprite=sprite,
            blocking_sprites=klaas.wall_spritelist,
            grid_size=64,
            left=0,
            right=klaas.tilemap.width,
            top=klaas.tilemap.height,  # FIXME: Top and bottom is switched in this dev version of arcade
            bottom=0
        )

        pyglet.clock.schedule_interval_soft(klaas.wait_for_video, interval=UPDATE_RATE)

    @staticmethod
    def init_music_queue(klaas):

        # Create the music queue
        klaas.music_queue = MusicQueue(state=klaas.state)
        klaas.music_queue.from_directory(os.path.join(klaas.state.music_dir, str(klaas.state.map_name)))

    @property
    def execution_time(self):
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at

        return None

    @property
    def initialized(self):
        return self.completed_at is not None

    def complete(self):
        if not self.completed_at:
            self.completed_at = time.time()

            logging.info(f"Map loaded in {self.execution_time} seconds")

    @property
    def percentage(self):
        finished = 0
        for thread in self.threads:
            if not thread.is_alive():
                finished += 1

        if finished == 0:
            return 0

        return 100 / len(self.threads) * finished

    def check_completed(self):
        if self.percentage == 100:
            self.complete()
    def wait_for(self):
        for thread in self.threads:
            thread.join()

        self.complete()


