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

    """ Async load map """

    def run(self, klaas) -> None:
        self.threads = []

        self.threads.append(threading.Thread(target=self.async_load, args=(klaas,)))

        for thread in self.threads:
            thread.start()

    def async_load(self, klaas):
        klaas.ui.loading_screen.show = True
        klaas.ui.loading_screen.percent = 0

        savegame = SaveGameState.load()
        savegame.current = klaas.state.map_name
        savegame.save()

        # Set up the Cameras
        klaas.camera_sprites = arcade.Camera()
        klaas.state.reset()
        klaas.state.difficulty = MapConfig(savegame.difficulty, klaas.state.map_name, klaas.state.map_dir)

        klaas.ui.loading_screen.percent = 10

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

        klaas.ui.loading_screen.percent = 25

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        klaas.scene = Scene.from_tilemap(klaas.tilemap.map)

        klaas.ui.loading_screen.percent = 50

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

        klaas.ui.loading_screen.percent = 60

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

        klaas.ui.loading_screen.percent = 80

        # Create the music queue
        klaas.music_queue = MusicQueue(state=klaas.state)
        klaas.music_queue.from_directory(os.path.join(klaas.state.music_dir, str(klaas.state.map_name)))

        klaas.ui.loading_screen.percent = 100

        pyglet.clock.schedule_interval_soft(klaas.wait_for_video, interval=UPDATE_RATE)

        # Sleep some seconds to wait until the 100 Percent is shown
        while not klaas.ui.loading_screen.completed:
            time.sleep(0.0001)

        klaas.ui.loading_screen.show = False

    @property
    def initialized(self):
        if len(self.threads) == 0:
            return False

        for thread in self.threads:
            if thread.is_alive():
                return False

        return True
