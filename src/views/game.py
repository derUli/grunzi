"""
Platformer Template

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.template_platformer
"""
import logging
import os
import random
import threading
import time

import arcade
import pyglet.clock
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

import constants.controls.controller
import constants.controls.keyboard
import sprites.characters.playersprite
import utils.audio
from constants.layers import *
from sprites.bullet.bullet import Bullet
from sprites.bullet.grunt import Grunt
from sprites.characters.enemysprite import EnemySprite
from sprites.characters.ferret import spawn_ferret
from sprites.characters.playersprite import PlayerSprite
from sprites.characters.skullsprite import spawn_skull
from sprites.items.item import Item, Useable
from sprites.sprite import Sprite
from sprites.ui.inventorycontainer import InventoryContainer
from utils.physics import make_physics_engine
from utils.positioned_sound import PositionedSound
from utils.scene import get_layer
from utils.sprite import tilemap_size
from utils.video import load_video
from views.camera import center_camera_to_player
from views.fading import Fading
from views.mainmenu import MainMenu
from views.pausemenu import PauseMenu
from window.gamewindow import UPDATE_RATE


class Game(Fading):
    """
    Main application class.
    """

    def __init__(self, window, state):

        # Call the parent class and set up the window
        super().__init__(window)

        self.state = state

        # Our TileMap Object
        self.tilemap = None
        self.tilemap_size = (0, 0)

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera_sprites = None

        # What key is pressed down?
        self.up_key_pressed = False
        self.right_key_pressed = False
        self.down_key_pressed = False
        self.left_key_pressed = False

        # Music queue
        self.music_queue = None
        self.atmo = None

        # Inventory
        self.inventory = None

        self.initialized = False

        self.scene = None

        self.message_box = None

        # This method is called in next call of on_update
        self._call_method = None

        self.video = None

    def on_show_view(self):
        super().on_show_view()
        self.window.set_mouse_visible(False)

        self.push_controller_handlers()

        self.state.unmute()

        if self.initialized:
            self.music_queue.play()
            self.atmo.play()
            return

        self.setup()

    def on_hide_view(self):
        self.window.set_mouse_visible(True)
        self.music_queue.pause()
        self.pop_controller_handlers()

        self.state.mute()
        self.on_update(0)

    def setup(self):
        video_file = os.path.join(self.state.video_dir, 'splash', f"{self.state.map_name}.webm")
        self.video = load_video(
            video_file,
            self.window.size,
            self.state.sound_volume
        )

        threading.Thread(target=self.async_load).start()

    def async_load(self):
        start_time = time.time()
        # Set up the Cameras
        self.camera_sprites = arcade.Camera()

        # Name of map file to load
        map_name = os.path.join(self.state.map_dir, f"{self.state.map_name}.tmx")

        # Read in the tiled map
        try:
            self.tilemap = arcade.load_tilemap(
                map_name,
                layer_options=LAYER_OPTIONS,
                use_spatial_hash=True
            )

            self.tilemap_size = tilemap_size(self.tilemap)
        except FileNotFoundError as e:
            logging.error(e)
            return arcade.exit()

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tilemap)

        # Set up the player, specifically placing it at these coordinates.
        filename = os.path.join(self.state.sprite_dir, 'char', 'pig.png')
        self.player_sprite = PlayerSprite(filename)
        self.player_sprite.setup(state=self.state, scene=self.scene)

        # Create the physics engine
        self.physics_engine = make_physics_engine(self.player_sprite, self.scene)

        # Create the music queue
        self.music_queue = utils.audio.MusicQueue(state=self.state)
        self.music_queue.from_directory(os.path.join(self.state.music_dir, str(self.state.map_name)))
        spawn_ferret(self.state, self.tilemap, self.scene, self.physics_engine)
        self.inventory = InventoryContainer()
        self.inventory.setup(state=self.state, size=self.window.size)
        pyglet.clock.schedule_interval_soft(self.wait_for_video, interval=UPDATE_RATE)

        self.initialized = True

        logging.info(f"Map {self.state.map_name} loaded in {time.time() - start_time} seconds")

    def wait_for_video(self, delta_time=0):

        if not self.initialized:
            return

        # Wait until video is completed until playing music
        if self.video and self.video.active:
            return

        self.video = None

        self.music_queue.play()

        atmo = self.state.play_sound('atmos', 'world', loop=True)
        self.atmo = PositionedSound(self.player_sprite, self.player_sprite, atmo, self.state)

        pyglet.clock.unschedule(self.wait_for_video)

    def on_draw(self):
        """Render the screen."""

        if self.video and self.video.active:
            self.video.draw((0, 0), force_draw=False)
            return self.draw_debug()

        self.clear()

        if not self.initialized:
            # Loading screen fallback if there is no intro video
            # or the intro video is already completed
            utils.text.create_text(
                _("Loading..."),
                width=self.window.width - (utils.text.MARGIN * 2),
                align='left').draw()
            return self.draw_debug()

        self.camera_sprites.use()
        self.scene.draw()

        for sprite in get_layer(LAYER_ENEMIES, self.scene):
            if self.window.debug:
                sprite.draw_debug()

            sprite.draw_overlay()

        self.camera_gui.use()
        self.inventory.draw()
        self.player_sprite.draw_overlay()
        self.draw_fading()
        self.draw_debug()

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        move_force = self.player_sprite.move_force * self.player_sprite.modifier

        force_x, force_y = 0, 0

        if self.up_key_pressed and not self.down_key_pressed:
            force_y = move_force
            self.player_sprite.change_y = -1
        elif self.down_key_pressed and not self.up_key_pressed:
            force_y = -move_force
            self.player_sprite.change_y = 1
        if self.left_key_pressed and not self.right_key_pressed:
            force_x = -move_force
            self.player_sprite.change_x = -1
        elif self.right_key_pressed and not self.left_key_pressed:
            force_x = move_force
            self.player_sprite.change_x = 1

        self.physics_engine.apply_force(self.player_sprite, (force_x, force_y))

    def reset_keys(self):
        # What key is pressed down?
        self.up_key_pressed = False
        self.right_key_pressed = False
        self.down_key_pressed = False
        self.left_key_pressed = False
        self.player_sprite.reset()

    def on_button_press(self, controller, key):
        logging.info(f"Controller button {key} pressed")

        if not self.initialized:
            return

        if self.video and self.video.active:
            if key in constants.controls.controller.KEY_DISCARD:
                self.video.stop()
            return

        if self.player_sprite.dead:
            if key in constants.controls.controller.KEY_DISCARD:
                self._call_method = self.on_main_menu
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

    def on_item_previous(self):
        self.on_select_item(index=self.inventory.previous())

    def on_item_next(self):
        self.on_select_item(index=self.inventory.next())

    def on_main_menu(self):
        self.next_view = MainMenu(self.window, self.state)
        self.fade_out()

    def on_stick_motion(self, controller, stick_name, x_value, y_value):
        logging.info(f"Stick motion {stick_name}, {x_value}, {y_value}")

        if not self.initialized:
            return

        x_value = round(x_value)
        y_value = round(y_value)

        if stick_name == constants.controls.controller.LEFTSTICK:
            if x_value == constants.controls.controller.AXIS_RIGHT:
                self.right_key_pressed = True
            elif x_value == constants.controls.controller.AXIS_LEFT:
                self.left_key_pressed = True
            else:
                self.right_key_pressed = False
                self.left_key_pressed = False

            if y_value == constants.controls.controller.AXIS_DOWN:
                self.down_key_pressed = True
            elif y_value == constants.controls.controller.AXIS_UP:
                self.up_key_pressed = True
            else:
                self.down_key_pressed = False
                self.up_key_pressed = False

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

    def on_trigger_motion(self, controller, trigger_name, value):
        logging.info(f"{trigger_name}, {value}")

        if not self.initialized:
            return

        value = round(value)

        if trigger_name in constants.controls.controller.LEFT_TRIGGER:
            if value == constants.controls.controller.TRIGGER_ON:
                self.player_sprite.modifier = sprites.characters.playersprite.MODIFIER_SPRINT
            if value == constants.controls.controller.TRIGGER_OFF:
                self.player_sprite.modifier = sprites.characters.playersprite.MODIFIER_DEFAULT

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if not self.initialized:
            return

        if self.video and self.video.active:
            if key in constants.controls.keyboard.KEY_DISCARD:
                return self.video.stop()

        if self.player_sprite.dead:
            if key in constants.controls.keyboard.KEY_DISCARD:
                return self.on_main_menu()

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_pause()
        if key in constants.controls.keyboard.KEY_SPRINT:
            self.player_sprite.modifier = sprites.characters.playersprite.MODIFIER_SPRINT
        if key in constants.controls.keyboard.KEY_USE:
            self.on_use()
        if key in constants.controls.keyboard.KEY_DROP:
            self.on_drop()
        if key in constants.controls.keyboard.KEY_SHOOT:
            self.on_shoot()
        if key in constants.controls.keyboard.KEY_GRUNT:
            self.on_grunt()
        if key in constants.controls.keyboard.KEY_SPAWN_FERRET:
            spawn_ferret(self.state, self.tilemap, self.scene, self.physics_engine)
        if key in constants.controls.keyboard.KEY_MOVE_LEFT:
            self.left_key_pressed = True
        elif key in constants.controls.keyboard.KEY_MOVE_RIGHT:
            self.right_key_pressed = True
        elif key in constants.controls.keyboard.KEY_MOVE_UP:
            self.up_key_pressed = True
        elif key in constants.controls.keyboard.KEY_MOVE_DOWN:
            self.down_key_pressed = True
        if key in constants.controls.keyboard.KEY_SELECT_INVENTORY:
            self.on_select_item(key=key)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        super().on_key_release(key, modifiers)

        if not self.initialized:
            return

        if key in constants.controls.keyboard.KEY_SPRINT:
            self.player_sprite.modifier = sprites.characters.playersprite.MODIFIER_DEFAULT

        movement = True

        if key in constants.controls.keyboard.KEY_MOVE_LEFT:
            self.left_key_pressed = False
        elif key in constants.controls.keyboard.KEY_MOVE_RIGHT:
            self.right_key_pressed = False
        elif key in constants.controls.keyboard.KEY_MOVE_UP:
            self.up_key_pressed = False
        elif key in constants.controls.keyboard.KEY_MOVE_DOWN:
            self.down_key_pressed = False
        else:
            movement = False

        if movement:
            self.update_player_speed()

    def on_select_item(self, key=None, index=None):
        old_item = self.player_sprite.get_item()

        if key:
            index = constants.controls.keyboard.KEY_SELECT_INVENTORY.index(key)
            index -= 1

        item = self.inventory.select(index)
        self.player_sprite.set_item(item)

        if old_item:
            old_item.remove_from_sprite_lists()

        if not item:
            return

        self.scene.add_sprite(LAYER_PLACE, item)

    def on_shoot(self):
        return Bullet(6, color=arcade.csscolor.HOTPINK).setup(
            source=self.player_sprite,
            physics_engine=self.physics_engine,
            state=self.state,
            scene=self.scene
        )

    def on_grunt(self):
        return Grunt(8).setup(
            source=self.player_sprite,
            physics_engine=self.physics_engine,
            scene=self.scene,
            state=self.state
        )

    def on_drop(self):
        item = self.player_sprite.get_item()
        selected, index = self.inventory.get_selected()
        if not item:
            logging.info('No item selected')
            return self.state.beep()

        klass = item.__class__
        layer = klass.__name__ + 's'
        new_item = item.copy()

        if selected:
            quantity = selected.pop()

            if quantity == 0:
                self.player_sprite.set_item(None)
                self.inventory.unselect()

        self.scene.add_sprite(layer, new_item)

    def on_pause(self) -> None:
        """
        On show pause menu
        """
        self.reset_keys()
        self.window.show_view(PauseMenu(self.window, self.state, self))

    def on_use(self):
        if not self.player_sprite.get_item():
            return self.update_collectable()

        item = self.player_sprite.get_item()
        sprites = arcade.check_for_collision_with_lists(self.player_sprite.get_item(), self.scene.sprite_lists)

        for sprite in sprites:
            if isinstance(sprite, Useable):
                item.on_use(sprite, state=self.state)
                return

        self.state.beep()
        logging.info('Nothing to use at ' + str(self.player_sprite.get_item().position))

    def on_update(self, delta_time):
        """Movement and game logic"""
        if not self.initialized:
            return

        super().on_update(delta_time)

        if self.video and self.video.active:
            return

        if self.atmo:
            self.atmo.update()

        # There is an OpenGL error happens when a sprite is added by an controller event handler
        # which seems to happen because the controller events are handled in a different thread.
        # To work around this we have the _call_method class variable which can be set to a class method
        # Which is called in next execution of on_update
        if self._call_method:
            self._call_method()
            self._call_method = None

        if self.player_sprite.dead:
            return self.update_fade(self.next_view)

        # Move the player with the physics engine
        self.update_player()
        self.physics_engine.step()

        for sprite_list in self.scene.sprite_lists:
            for sprite in sprite_list:
                if not isinstance(sprite, Sprite):
                    continue

                sprite.update(
                    player=self.player_sprite,
                    scene=self.scene,
                    physics_engine=self.physics_engine,
                    state=self.state,
                    delta_time=delta_time,
                    map_size=self.tilemap_size
                )

        self.update_enemies(delta_time)
        center_camera_to_player(self.player_sprite, self.camera_sprites)
        self.update_fade(self.next_view)

    def update_player(self):
        self.update_player_speed()
        self.player_sprite.update()

    def update_enemies(self, delta_time):
        enemies = get_layer(LAYER_ENEMIES, self.scene)

        for sprite in enemies:
            if not isinstance(sprite, EnemySprite):
                continue

            if arcade.check_for_collision(sprite, self.player_sprite):
                self.player_sprite.hurt(sprite.damage)

        if len(enemies) < 10:
            if random.randint(1, 150) == 50:
                spawn_skull(self.state, self.tilemap, self.scene, self.physics_engine)
                logging.info(f'Spawn enemy, new total enemy count: {len(self.scene[LAYER_ENEMIES])}')

    def update_collectable(self):
        items = arcade.check_for_collision_with_lists(self.player_sprite, self.scene.sprite_lists)
        for item in items:
            if isinstance(item, Item):
                item.remove_from_sprite_lists()

                self.inventory.add_item(item)
                self.state.play_sound('coin')
                self.on_select_item(index=-1)
                return True

        self.state.beep()
        return False
