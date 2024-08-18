import logging
import os
import sys
import threading
import time

import pyglet.clock
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

import constants.controls.controller
import constants.controls.keyboard
import utils.media.audio
from constants.layers import *
from constants.mapconfig import MapConfig
from constants.maps import MAPS
from sprites.bullet.grunt import Grunt
from sprites.characters.player import Player, MODIFIER_SPRINT, MODIFIER_DEFAULT
from sprites.items.item import Useable
from sprites.ui.uicontainer import UIContainer
from state.argscontainer import make_args_container
from state.savegamestate import SaveGameState
from utils.callbackhandler import CallbackHandler
from utils.mappopulator import MapPopulator
from utils.media.video import load_video, Video
from utils.physics import make_physics_engine
from utils.positionalsound import PositionalSound, VOLUME_SOURCE_ATMO
from utils.scene import Scene
from utils.tilemap import TileMap
from views.camera import center_camera_to_player
from views.fading import Fading
from views.menu.mainmenu import MainMenu
from views.menu.pausemenu import PauseMenu
from window.gamewindow import UPDATE_RATE


class Game(Fading):
    """
    Main application class.
    """

    def __init__(self, window, state, skip_intro=False):

        # Call the parent class and set up the window
        super().__init__(window)

        self.initialized = False

        self.state = state

        # Our TileMap Object
        self.tilemap = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera_sprites = None

        # Music queue
        self.music_queue = None
        self.atmo = None
        self.loading_music = None

        # This method is called in next call of on_update
        self._call_method = None

        self.video = Video(None)
        self.skip_intro = skip_intro

        self.ui = None

        self.astar_barrier_list = None
        self.wall_spritelist = None
        self.map_populator = None
        self.measurements = []

    def on_show_view(self) -> None:
        """ On show view """
        super().on_show_view()

        self.window.set_mouse_visible(False)
        self.push_controller_handlers()
        self.state.settings.unmute()

        if self.initialized:
            self.music_queue.play()
            self.atmo.play()
            return

        self.setup()

    def on_hide_view(self) -> None:
        """ On hide view """
        super().on_hide_view()

        if self.player_sprite:
            self.player_sprite.stop_walk()

        self.window.set_mouse_visible(True)
        self.music_queue.pause()
        self.pop_controller_handlers()
        self.atmo.pause()
        self.state.settings.mute()
        self.scene.update_scene(0, make_args_container(self))

    def setup(self) -> None:
        """ Setup game """

        self.initialized = False
        video_file = os.path.join(self.state.video_dir, 'splash', f"{self.state.map_name}.webm")

        if not self.state.settings.videos:
            self.skip_intro = True

        if not self.skip_intro:
            self.video = load_video(
                video_file,
                self.window.size,
                self.state.settings.music_volume
            )

        self.loading_music = None

        self.ui = UIContainer()
        self.ui.setup(self.state, self.window.size)

        # Load map
        threading.Thread(target=self.async_load).start()

    def async_load(self) -> None:
        """ Async load map """

        start_time = time.time()

        self.ui.loading_screen.show = True
        self.ui.loading_screen.percent = 0

        savegame = SaveGameState.load()
        savegame.current = self.state.map_name
        savegame.save()

        # Set up the Cameras
        self.camera_sprites = arcade.camera.Camera2D()
        self.state.reset()
        self.state.difficulty = MapConfig(savegame.difficulty, self.state.map_name, self.state.map_dir)

        self.ui.loading_screen.percent = 10

        # Name of map file to load
        map_name = os.path.join(self.state.map_dir, f"{self.state.map_name}.tmx")

        # Read in the tiled map
        try:
            self.tilemap = TileMap(
                map_name,
                layer_options=LAYER_OPTIONS
            )
        except FileNotFoundError as e:
            logging.error(e)
            sys.exit(1)

        self.ui.loading_screen.percent = 25

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = Scene.from_tilemap(self.tilemap.map)

        self.ui.loading_screen.percent = 50

        self.map_populator = MapPopulator()
        self.map_populator.spawn_initial(make_args_container(self))

        # Set up the player, specifically placing it at these coordinates.
        filename = os.path.join(self.state.sprite_dir, 'char', 'pig.png')
        self.player_sprite = Player(filename)

        self.player_sprite.setup(
            state=self.state,
            scene=self.scene,
            callbacks=CallbackHandler(
                on_complete=self.on_next_level
            ),
            controllers=self.window.controllers
        )

        # Create the physics engine
        self.physics_engine = make_physics_engine(self.player_sprite, self.scene)

        self.map_populator.spawn_npcs(make_args_container(self))

        self.ui.loading_screen.percent = 60

        self.wall_spritelist = self.scene.make_wall_spritelist()

        sprite = arcade.SpriteSolidColor(
            width=64,
            height=64,
            color=arcade.color.BLACK
        )

        self.astar_barrier_list = arcade.AStarBarrierList(
            moving_sprite=sprite,
            blocking_sprites=self.wall_spritelist,
            grid_size=64,
            left=0,
            right=self.tilemap.width,
            top=self.tilemap.height,  # FIXME: Top and bottom is switched in this dev version of arcade
            bottom=0
        )

        self.ui.loading_screen.percent = 80

        # Create the music queue
        self.music_queue = utils.media.audio.MusicQueue(state=self.state)
        self.music_queue.from_directory(os.path.join(self.state.music_dir, str(self.state.map_name)))

        self.ui.loading_screen.percent = 100

        pyglet.clock.schedule_interval_soft(self.wait_for_video, interval=UPDATE_RATE)

        # Sleep some seconds to wait until the 100 Percent is shown
        while not self.ui.loading_screen.completed:
            time.sleep(0.0001)

        self.ui.loading_screen.show = False
        self.initialized = True

        logging.info(f"Map {self.state.map_name} loaded in {time.time() - start_time} seconds")

    def wait_for_video(self, delta_time=0) -> None:
        """ Wait until video playback completed """

        self.window.set_mouse_visible(False)

        if not self.input_ready:
            return

        self.video = Video(None)
        self.music_queue.play()

        atmo = self.state.play_sound('atmos', self.state.map_name, loop=True)
        self.atmo = PositionalSound(
            self.player_sprite,
            self.player_sprite,
            atmo,
            self.state,
            volume_source=VOLUME_SOURCE_ATMO
        )

        pyglet.clock.unschedule(self.wait_for_video)

    def on_update(self, delta_time: float) -> None:
        """Movement and game logic"""

        super().on_update(delta_time)

        self.ui.loading_screen.update(delta_time)

        if not self.initialized:
            if not self.video.active and not self.loading_music:
                self.loading_music = self.state.play_sound(
                    'loading',
                    loop=True,
                    volume=self.state.settings.music_volume,
                )
            return

        if self.video.active:
            return

        if self.loading_music:
            self.loading_music.pause()
            self.loading_music = None

        if self.atmo:
            self.atmo.update()

        if self.music_queue:
            self.music_queue.update()

        # There is an OpenGL error happening when a sprite is added by an controller event handler
        # which seems to happen because the controller events are handled in a different thread.
        # To work around this we have the _call_method class variable which can be set to a class method
        # Which is called in next execution of on_update
        if self._call_method:
            self._call_method()
            self._call_method = None

        if self.player_sprite.dead:
            self.player_sprite.update(delta_time, make_args_container(self))
            self.player_sprite.reset()

            if not self.player_sprite.bloody_screen.shown:
                self.scene.update_scene(
                    delta_time,
                    make_args_container(self)
                )

            return self.update_fade(self.next_view)

        # Move the player with the physics engine
        self.update_player_speed()
        self.physics_engine.step(delta_time)

        self.scene.update_scene(
            delta_time,
            make_args_container(self)
        )

        self.map_populator.update(make_args_container(self))
        self.update_fade(self.next_view)

    def on_draw(self) -> None:
        """Render the screen."""

        self.clear()

        if self.video.active:
            # Loading a video will open a ffmpeg console window.
            # Which will disappear after a second.
            # The game window lose it's focus.
            # Activate the window again.
            self.window.activate()
            self.video.draw((0, 0), force_draw=True)
            return self.draw_after()

        if not self.initialized or not self.ui.loading_screen.completed:
            self.ui.loading_screen.draw(self.time)

            return self.draw_after()

        center_camera_to_player(self.player_sprite, self.camera_sprites, self.tilemap.size)

        self.camera_sprites.use()
        self.scene.draw()

        self.camera_gui.use()
        self.ui.draw()

        self.player_sprite.draw_overlay(args=make_args_container(self))
        self.draw_fading()
        self.draw_after()

    def update_player_speed(self) -> None:
        """ Update player sprite """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x, self.player_sprite.change_y = 0, 0

        move_force = self.player_sprite.move_force * self.player_sprite.modifier

        force_x, force_y = 0, 0

        if self.state.keypressed.key_up and not self.state.keypressed.key_down:
            force_y = move_force
            self.player_sprite.change_y = -1
        elif self.state.keypressed.key_down and not self.state.keypressed.key_up:
            force_y = -move_force
            self.player_sprite.change_y = 1
        if self.state.keypressed.key_left and not self.state.keypressed.key_right:
            force_x = -move_force
            self.player_sprite.change_x = -1
        elif self.state.keypressed.key_right and not self.state.keypressed.key_left:
            force_x = move_force
            self.player_sprite.change_x = 1

        if force_x != 0 or force_y != 0:
            self.player_sprite.start_walk(sprint=self.player_sprite.sprinting)
            self.window.set_mouse_visible(False)
            self.physics_engine.apply_force(
                self.player_sprite,
                (force_x, force_y)
            )
        else:
            self.player_sprite.stop_walk()

    def on_button_press(self, controller, key):
        """ On button press """
        if self.video.active and key in constants.controls.controller.KEY_DISCARD:
            return self.video.stop()

        if not self.initialized:
            return

        if self.player_sprite.dead:
            if key in constants.controls.controller.KEY_DISCARD:
                self._call_method = self.on_gameover
            return

        if key in constants.controls.controller.KEY_PAUSE:
            self._call_method = self.on_pause
        if key in constants.controls.controller.KEY_USE:
            self._call_method = self.on_use
        if key in constants.controls.controller.KEY_DROP:
            self._call_method = self.on_drop
        if key in constants.controls.controller.KEY_SHOOT:
            self._call_method = self.on_shoot
        if key in constants.controls.controller.KEY_GRUNT:
            self._call_method = self.on_grunt
        if key in constants.controls.controller.PREVIOUS_ITEM:
            self._call_method = self.on_item_previous
        if key in constants.controls.controller.NEXT_ITEM:
            self._call_method = self.on_item_next
        if key in constants.controls.controller.KEY_SPRINT:
            self.player_sprite.modifier = MODIFIER_SPRINT

    def on_button_release(self, controller, key):

        if self.player_sprite and key in constants.controls.controller.KEY_SPRINT:
            self.player_sprite.modifier = MODIFIER_DEFAULT

    def on_item_previous(self) -> None:
        """ Select previous item """
        self.on_select_item(index=self.ui.inventory.previous())

    def on_item_next(self):
        self.on_select_item(index=self.ui.inventory.next())

    def on_main_menu(self):
        self.fade_to_view(MainMenu(self.window, self.state))

    def on_gameover(self):
        self.on_next_level(same=True)

    def on_next_level(self, same=False):
        if self.next_view:
            return

        self.player_sprite.reset()

        old_map = self.state.map_name
        next_map = old_map
        index = MAPS.index(old_map)

        if not same:
            index += 1

        completed = False

        try:
            next_map = MAPS[index]
        except IndexError as e:
            logging.error(e)
            completed = True

        self.state.map_name = next_map

        savegame = SaveGameState.load()
        savegame.current = next_map

        if old_map not in savegame.completed:
            savegame.completed += [old_map]

        savegame.score[old_map] = self.state.score
        savegame.save()

        if completed:
            logging.info('Game Completed')
            from views.highscore.highscoreadd import HighscoreAdd
            self.fade_to_view(HighscoreAdd(self.window, self.state))
            return

        self.fade_to_view(Game(self.window, self.state, skip_intro=same))

    def on_stick_motion(self, controller, stick_name, x_value, y_value):
        if not self.input_ready:
            return

        x_value, y_value = round(x_value), round(y_value)

        if stick_name == constants.controls.controller.LEFTSTICK:
            if x_value == constants.controls.controller.AXIS_RIGHT:
                self.state.keypressed.key_right = True
            elif x_value == constants.controls.controller.AXIS_LEFT:
                self.state.keypressed.key_left = True
            else:
                self.state.keypressed.key_right = False
                self.state.keypressed.key_left = False

            if y_value == constants.controls.controller.AXIS_DOWN:
                self.state.keypressed.key_down = True
            elif y_value == constants.controls.controller.AXIS_UP:
                self.state.keypressed.key_up = True
            else:
                self.state.keypressed.key_down = False
                self.state.keypressed.key_up = False

        if stick_name == constants.controls.controller.RIGHTSTICK:
            face = self.player_sprite.face
            if x_value == constants.controls.controller.AXIS_RIGHT:
                face = FACE_RIGHT
            if x_value == constants.controls.controller.AXIS_LEFT:
                face = FACE_LEFT
            if y_value == constants.controls.controller.AXIS_DOWN:
                face = FACE_DOWN
            if y_value == constants.controls.controller.AXIS_UP:
                face = FACE_UP

            self.player_sprite.set_face(face)

    def on_key_press(self, key: int, modifiers: int):
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if self.video.active and key in constants.controls.keyboard.KEY_DISCARD:
            return self.video.stop()

        if not self.initialized:
            return

        if self.player_sprite.dead:
            if key in constants.controls.keyboard.KEY_DISCARD:
                return self.on_gameover()

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_pause()
        if key in constants.controls.keyboard.KEY_SPRINT:
            self.player_sprite.modifier = MODIFIER_SPRINT
        if key in constants.controls.keyboard.KEY_USE:
            self.on_use()
        if key == arcade.key.F7:
            self.on_next_level()
        if key in constants.controls.keyboard.KEY_DROP:
            self.on_drop()
        if key in constants.controls.keyboard.KEY_SHOOT:
            self.on_shoot()
        if key in constants.controls.keyboard.KEY_GRUNT:
            self.on_grunt()
        if key in constants.controls.keyboard.KEY_MOVE_LEFT:
            self.state.keypressed.key_left = True
        elif key in constants.controls.keyboard.KEY_MOVE_RIGHT:
            self.state.keypressed.key_right = True
        elif key in constants.controls.keyboard.KEY_MOVE_UP:
            self.state.keypressed.key_up = True
        elif key in constants.controls.keyboard.KEY_MOVE_DOWN:
            self.state.keypressed.key_down = True
        if key in constants.controls.keyboard.KEY_SELECT_INVENTORY:
            self.on_select_item(key=key)

    def on_key_release(self, key: int, modifiers: int):
        """Called when the user releases a key."""
        super().on_key_release(key, modifiers)

        if not self.input_ready:
            return

        if key in constants.controls.keyboard.KEY_SPRINT:
            self.player_sprite.modifier = MODIFIER_DEFAULT

        movement = True

        if key in constants.controls.keyboard.KEY_MOVE_LEFT:
            self.state.keypressed.key_left = False
        elif key in constants.controls.keyboard.KEY_MOVE_RIGHT:
            self.state.keypressed.key_right = False
        elif key in constants.controls.keyboard.KEY_MOVE_UP:
            self.state.keypressed.key_up = False
        elif key in constants.controls.keyboard.KEY_MOVE_DOWN:
            self.state.keypressed.key_down = False
        else:
            movement = False

        if movement:
            self.update_player_speed()
        else:
            self.player_sprite.stop_walk()

    def on_select_item(self, key=None, index=None):
        old_item = self.player_sprite.get_item()

        if old_item:
            old_item.on_unequip(make_args_container(self))

        if key:
            index = constants.controls.keyboard.KEY_SELECT_INVENTORY.index(key)
            index -= 1

        item = self.ui.inventory.select(index)
        self.player_sprite.set_item(item)

        if old_item:
            old_item.remove_from_sprite_lists()

        if not item:
            return

        self.scene.add_sprite(LAYER_PLACE, item)

        item.on_equip(make_args_container(self))

    def on_shoot(self):
        return self.player_sprite.shoot(self.state, self.scene, self.physics_engine)

    def on_grunt(self):
        return Grunt(8).setup(
            source=self.player_sprite,
            physics_engine=self.physics_engine,
            scene=self.scene,
            state=self.state
        )

    def on_drop(self):
        item = self.player_sprite.get_item()
        selected, index = self.ui.inventory.get_selected()

        if not item:
            logging.info('No item selected')
            return self.state.noaction()

        new_item = item.copy()
        layer = new_item.__class__.__name__

        if hasattr(new_item, 'layer_name'):
            layer = new_item.layer_name

        if check_collision_with_layers(self.scene, new_item, WALL_LAYERS):
            logging.info("Can't drop item on wall.")
            return self.state.noaction()

        if selected:
            quantity = selected.pop()

            if quantity == 0:
                self.player_sprite.set_item(None)
                self.ui.inventory.unselect()

        self.scene.add_sprite(layer, new_item)

    def on_pause(self) -> None:
        """
        On show pause menu
        """

        self.state.keypressed.reset()
        self.player_sprite.reset()

        menu = PauseMenu(self.window, self.state, self)
        menu.setup()
        self.window.show_view(menu)

    def on_use(self):

        item = self.player_sprite.get_item()
        if not item:
            if self.update_collectable():
                self.state.play_sound('coin')
                return
            else:
                interactable = self.scene.get_next_interactable()
                if interactable:
                    interactable.on_interact(args=make_args_container(self))
                    return

            self.state.noaction()
            return

        args = make_args_container(self)

        for sprite in self.scene.get_next_sprites():
            if isinstance(sprite, Useable):
                return item.on_use_with(
                    sprite,
                    args=args
                )

        item.on_use(
            args=make_args_container(self)
        )

    def update_collectable(self):
        item = self.scene.get_collectable(self.player_sprite)

        if not item:
            return False

        if not self.ui.inventory.has_capacity(item):
            return False

        item.remove_from_sprite_lists()
        self.ui.inventory.add_item(item)

        self.on_select_item(index=-1)

        return True

    @property
    def input_ready(self) -> bool:
        """ Check if the game is ready to handle input """
        if not self.initialized:
            return False

        return not self.video.active
