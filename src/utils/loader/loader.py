import logging
import os
import sys
import threading
import time

import arcade
import pyglet

import utils.media.audio
from constants.collisions import GRID_SIZE
from constants.gamemode import GAMEMODE_CAMPAIGN
from constants.layers import LAYER_OPTIONS
from constants.mapconfig import MapConfig
from sprites.characters.player import Player
from state.argscontainer import make_args_container
from state.savegamestate import SaveGameState
from utils.callbackhandler import CallbackHandler
from utils.mappopulator.mappopulator import init_map_populator
from utils.physics import make_physics_engine
from utils.scene import Scene
from utils.tilemap import TileMap
from window.gamewindow import UPDATE_RATE


class Loader:
    def __init__(self, parent):
        self.parent = parent

    def load_async(self) -> None:
        threading.Thread(target=self.load).start()

    def load(self):

        start_time = time.time()

        self.parent.ui.loading_screen.show = True
        self.parent.ui.loading_screen.percent = 0

        savegame = SaveGameState.load()
        savegame.current = self.parent.state.map_name
        savegame.save()

        # Set up the Cameras
        self.parent.camera_sprites = arcade.Camera()
        self.parent.state.reset()
        self.parent.state.difficulty = MapConfig(
            savegame.difficulty,
            self.parent.state.map_name,
            self.parent.state.map_dir
        )

        # Name of map file to load
        map_name = os.path.join(self.parent.state.map_dir, f"{self.parent.state.map_name}.tmx")

        # Read in the tiled map
        try:
            self.parent.tilemap = TileMap(
                map_name,
                layer_options=LAYER_OPTIONS,
            )
        except FileNotFoundError as e:
            logging.error(e)
            sys.exit(1)

        self.parent.ui.loading_screen.percent = 25

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.parent.scene = Scene.from_tilemap(self.parent.tilemap.map)

        if 'weatherLayers' in self.parent.state.difficulty.options and not self.parent.state.settings.weather:
            for layer in self.parent.state.difficulty.options['weatherLayers']:
                try:
                    self.parent.scene[layer].clear()
                except KeyError:
                    pass

        self.parent.ui.loading_screen.percent = 50

        # Set up the player, specifically placing it at these coordinates.
        filename = os.path.join(self.parent.state.sprite_dir, 'char', 'pig.png')
        self.parent.scene.player_sprite = Player(filename)

        self.parent.map_populator = init_map_populator(GAMEMODE_CAMPAIGN)
        self.parent.map_populator.spawn_initial(make_args_container(self.parent))

        self.parent.scene.player_sprite.setup(
            state=self.parent.state,
            scene=self.parent.scene,
            callbacks=CallbackHandler(
                on_complete=self.parent.on_next_level
            ),
            controllers=self.parent.window.controllers,
            bullet_size=savegame.bullet_size
        )

        # Create the physics engine
        self.parent.physics_engine = make_physics_engine(self.parent.scene.player_sprite, self.parent.scene)

        self.parent.map_populator.spawn_npcs(make_args_container(self.parent))

        self.parent.ui.loading_screen.percent = 75

        self.parent.wall_spritelist = self.parent.scene.make_wall_spritelist()

        sprite = arcade.SpriteSolidColor(
            width=GRID_SIZE,
            height=GRID_SIZE,
            color=arcade.color.BLACK
        )

        self.parent.astar_barrier_list = arcade.AStarBarrierList(
            moving_sprite=sprite,
            blocking_sprites=self.parent.wall_spritelist,
            grid_size=GRID_SIZE,
            left=0,
            right=self.parent.tilemap.width,
            top=self.parent.tilemap.height,  # FIXME: Top and bottom is switched in this dev version of arcade
            bottom=0
        )

        # Create the music queue
        self.parent.music_queue = utils.media.audio.MusicQueue(state=self.parent.state)
        self.parent.music_queue.from_directory(
            os.path.join(self.parent.state.music_dir, str(self.parent.state.map_name))
        )

        self.parent.ui.loading_screen.percent = 100

        pyglet.clock.schedule_interval_soft(self.parent.wait_for_video, interval=UPDATE_RATE)

        # Sleep some seconds to wait until the 100 Percent is shown
        while not self.parent.ui.loading_screen.completed:
            time.sleep(0.000001)

        self.parent.ui.loading_screen.show = False
        self.parent.initialized = True

        logging.info(f"Map {self.parent.state.map_name} loaded in {time.time() - start_time} seconds")
