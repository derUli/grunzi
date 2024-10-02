import logging

import pyglet

from constants.controls.keyboard import KEY_SELECT_INVENTORY
from constants.layers import LAYER_PLACE
from sprites.bullet.grunt import Grunt
from sprites.ui.uicontainer import UIContainer
from state.argscontainer import make_args_container
from utils.loader.loader import Loader
from utils.media.video import Video
from utils.positionalsound import PositionalSound, VOLUME_SOURCE_ATMO
from views.camera import center_camera_to_player
from views.fading import Fading
from views.menu.pausemenu import PauseMenu


class Game(Fading):
    def __init__(self, window, state, skip_intro=False):
        # Call the parent class and set up the window
        super().__init__(window)

        self.initialized = False

        self.state = state

        # Our TileMap Object
        self.tilemap = None

        # Separate variable that holds the player sprite
        self.scene.player_sprite = None

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
        self.level_completed = False

        self.astar_barrier_list = None
        self.wall_spritelist = None
        self.map_populator = None

    def setup(self):
        self.initialized = False
        self.loading_music = None

        self.ui = UIContainer()
        self.ui.setup(self.state, self.window.size)

        self.level_completed = False
        # Load map
        Loader(self).load_async()

    def on_draw(self) -> None:
        if not self.initialized or not self.ui.loading_screen.completed:
            self.ui.loading_screen.draw(time=self.time)

            return self.draw_after()

        center_camera_to_player(self.scene.player_sprite, self.camera_sprites, self.tilemap.size)

        self.camera_sprites.use()
        self.scene.draw()

        self.camera_gui.use()
        self.ui.draw()

        self.scene.player_sprite.draw_overlay(args=make_args_container(self))
        self.draw_fading()
        self.draw_after()

    @property
    def input_ready(self) -> bool:
        """ Check if the game is ready to handle input """

        if not self.initialized:
            return False

        return not self.video.active

    def on_gameover(self) -> None:
        """ Called when the player dies """

        logging.warning('TODO: implement on_gameover()')

    def on_shoot(self):
        """ Called when the player shoots """

        return self.scene.player_sprite.shoot(self.state, self.scene, self.physics_engine)

    def on_grunt(self):
        """ Called when the player grunts """

        return Grunt(8).setup(
            source=self.scene.player_sprite,
            physics_engine=self.physics_engine,
            scene=self.scene,
            state=self.state
        )

    def on_item_previous(self) -> None:
        """ Select previous item """

        self.on_select_item(index=self.ui.inventory.previous())

    def on_item_next(self) -> None:
        """ Select next item """
        self.on_select_item(index=self.ui.inventory.next())

    def on_select_item(self, key=None, index=None):
        """ Select item """
        old_item = self.scene.player_sprite.get_item()

        if old_item:
            old_item.on_unequip(make_args_container(self))

        if key:
            index = KEY_SELECT_INVENTORY.index(key)
            index -= 1

        item = self.ui.inventory.select(index)
        self.scene.player_sprite.set_item(item)

        if old_item:
            old_item.remove_from_sprite_lists()

        if not item:
            return

        self.scene.add_sprite(LAYER_PLACE, item)

        item.on_equip(make_args_container(self))

    def on_pause(self) -> None:
        """ On show pause menu """

        self.state.keypressed.reset()
        self.scene.player_sprite.reset()

        menu = PauseMenu(self.window, self.state, self)
        menu.setup()
        self.window.show_view(menu)

    def update_player_speed(self) -> None:
        """ Update player sprite """

        # Calculate speed based on the keys pressed
        self.scene.player_sprite.change_x, self.scene.player_sprite.change_y = 0, 0

        move_force = self.scene.player_sprite.move_force * self.scene.player_sprite.modifier

        force_x, force_y = 0, 0

        if self.state.keypressed.key_up and not self.state.keypressed.key_down:
            force_y = move_force
            self.scene.player_sprite.change_y = -1
        elif self.state.keypressed.key_down and not self.state.keypressed.key_up:
            force_y = -move_force
            self.scene.player_sprite.change_y = 1
        if self.state.keypressed.key_left and not self.state.keypressed.key_right:
            force_x = -move_force
            self.scene.player_sprite.change_x = -1
        elif self.state.keypressed.key_right and not self.state.keypressed.key_left:
            force_x = move_force
            self.scene.player_sprite.change_x = 1

        if force_x != 0 or force_y != 0:
            self.scene.player_sprite.start_walk(sprint=self.scene.player_sprite.sprinting)
            self.window.set_mouse_visible(False)
            self.physics_engine.apply_force(
                self.scene.player_sprite,
                (force_x, force_y)
            )
        else:
            self.scene.player_sprite.stop_walk()

    def wait_for_video(self, delta_time=0) -> None:
        """ Wait until video playback completed """

        self.window.set_mouse_visible(False)

        if not self.input_ready:
            return

        self.video = Video(None)
        self.music_queue.play()

        atmo = self.state.play_sound('atmos', self.state.map_name, loop=True)
        self.atmo = PositionalSound(
            self.scene.player_sprite,
            self.scene.player_sprite,
            atmo,
            self.state,
            volume_source=VOLUME_SOURCE_ATMO
        )

        pyglet.clock.unschedule(self.wait_for_video)

    def update_collectable(self):
        item = self.scene.get_collectable(self.scene.player_sprite)

        if not item:
            return False

        if not self.ui.inventory.has_capacity(item):
            return False

        item.remove_from_sprite_lists()
        self.ui.inventory.add_item(item)

        self.on_select_item(index=-1)

        return True
