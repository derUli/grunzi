"""
Platformer Template

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.template_platformer
"""
import logging
import os
import random

import arcade
from arcade import SpriteList, PymunkPhysicsEngine

import constants.controls.keyboard
import sprites.characters.playersprite
import utils.audio
from sprites.bullet.bullet import Bullet
from sprites.bullet.grunt import Grunt
from sprites.characters.enemysprite import EnemySprite
from sprites.characters.playersprite import PlayerSprite
from sprites.characters.skullsprite import SkullSprite
from utils.physics import make_physics_engine
from utils.sprite import random_position
from views.fading import Fading
from views.mainmenu import MainMenu
from views.pausemenu import PauseMenu

# Constants used to scale our sprites from their original size
TILE_SCALING = 1.0

SPRITE_LIST_COINS = 'Coins'
SPRITE_LIST_WALL = 'Walls'
SPRITE_LIST_ENEMIES = 'enemies'
SPRITE_LIST_PLAYER = 'player'
SPRITE_LIST_MOVEABLE = 'Moveable'
TOTAL_COINS = 100

START_POS_X = 474
START_POS_Y = 226


class Game(Fading):
    """
    Main application class.
    """

    def __init__(self, window, state):

        # Call the parent class and set up the window
        super().__init__(window)

        self.state = state

        # Our TileMap Object
        self.tile_map = None

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

        self.initialized = False

    def on_show_view(self):
        super().on_show_view()

        self.window.set_mouse_visible(False)

        if self.initialized:
            self.music_queue.play()
            return

        self.setup()

    def setup(self):

        # Set up the Cameras
        self.camera_sprites = arcade.Camera()

        # Name of map file to load
        map_name = os.path.join(self.state.map_dir, f"{self.state.map_name}.tmx")

        layer_options = {
            "Walls": {
                "use_spatial_hash": True,
            }
        }

        # Read in the tiled map
        try:
            self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        except FileNotFoundError as e:
            logging.error(e)
            arcade.exit()
            return

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player, specifically placing it at these coordinates.
        filename = os.path.join(self.state.sprite_dir, 'pig.png')
        self.player_sprite = PlayerSprite(filename)
        self.player_sprite.center_x = START_POS_X
        self.player_sprite.center_y = START_POS_Y
        self.scene.add_sprite(SPRITE_LIST_PLAYER, self.player_sprite)

        # Create the physics engine
        self.physics_engine = make_physics_engine(self.player_sprite, self.scene)

        # Create the music queue
        self.music_queue = utils.audio.MusicQueue(state=self.state)
        self.music_queue.from_directory(os.path.join(self.state.music_dir, self.state.map_name))
        self.music_queue.play()

        # Place coins
        for i in range(TOTAL_COINS):
            self.make_coin()

        self.initialized = True

    def on_hide_view(self):

        self.window.set_mouse_visible(True)
        self.music_queue.pause()

    def on_draw(self):
        """Render the screen."""

        self.clear()
        self.camera_sprites.use()

        # Draw our Scene
        # Note, if you a want pixelated look, add pixelated=True to the parameters
        self.scene.draw()

        try:
            enemies = self.scene[SPRITE_LIST_ENEMIES]
        except KeyError:
            enemies = []
        for sprite in enemies:

            if self.window.debug:
                sprite.draw_debug()

            sprite.draw_overlay()

        self.camera_gui.use()

        utils.text.draw_coins(self.state.coins)

        self.player_sprite.draw_overlay()

        self.draw_fading()
        self.draw_debug(self.player_sprite)

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0

        move_force = self.player_sprite.move_force * self.player_sprite.modifier

        force_x, force_y = 0, 0

        if self.up_key_pressed and not self.down_key_pressed:
            force_y = move_force
        elif self.down_key_pressed and not self.up_key_pressed:
            force_y = -move_force
        if self.left_key_pressed and not self.right_key_pressed:
            force_x = -move_force
            self.player_sprite.change_x = -1
        elif self.right_key_pressed and not self.left_key_pressed:
            force_x = move_force
            self.player_sprite.change_x = 1

        self.physics_engine.apply_force(self.player_sprite, (force_x, force_y))

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)

        """Called whenever a key is pressed."""
        if key in constants.controls.keyboard.KEY_PAUSE:
            self.reset_keys()

            if not self.player_sprite.dead():
                self.window.show_view(
                    PauseMenu(self.window, self.state, self)
                )
            else:
                self.next_view = MainMenu(self.window, self.state)
                self.fade_out()
                return

        if key in constants.controls.keyboard.KEY_SPRINT:
            self.player_sprite.modifier = sprites.characters.playersprite.MODIFIER_SPRINT

        if key in constants.controls.keyboard.KEY_USE:
            self.on_use()

        if key in constants.controls.keyboard.KEY_SHOOT:
            self.on_shoot()

        if key in constants.controls.keyboard.KEY_GRUNT:
            self.on_grunt()

        if key in constants.controls.keyboard.KEY_MOVE_LEFT:
            self.left_key_pressed = True
        elif key in constants.controls.keyboard.KEY_MOVE_RIGHT:
            self.right_key_pressed = True
        elif key in constants.controls.keyboard.KEY_MOVE_UP:
            self.up_key_pressed = True
        elif key in constants.controls.keyboard.KEY_MOVE_DOWN:
            self.down_key_pressed = True

    def reset_keys(self):
        # What key is pressed down?
        self.up_key_pressed = False
        self.right_key_pressed = False
        self.down_key_pressed = False
        self.left_key_pressed = False
        self.player_sprite.reset()

    def on_key_release(self, key, modifiers):
        super().on_key_release(key, modifiers)
        """Called when the user releases a key."""

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

    def on_shoot(self):
        bullet = Bullet(4, color=arcade.csscolor.HOTPINK)
        bullet.setup(
            source=self.player_sprite,
            physics_engine=self.physics_engine,
            scene=self.scene,
            state=self.state
        )

    def on_grunt(self):
        if self.state.is_silent():
            return

        bullet = Grunt(8)
        bullet.setup(
            source=self.player_sprite,
            physics_engine=self.physics_engine,
            scene=self.scene,
            state=self.state
        )

    def on_use(self):
        self.state.sounds['beep'].play()
        logging.info('"Use" not implemented yet')

    def center_camera_to_player(self):
        # Find where player is, then calculate lower left corner from that
        screen_center_x = self.player_sprite.center_x - (self.camera_sprites.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera_sprites.viewport_height / 2)

        # Set some limits on how far we scroll
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Here's our center, move to it
        player_centered = screen_center_x, screen_center_y
        self.camera_sprites.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.update_player()
        self.physics_engine.step()
        self.update_collectable()
        self.update_enemies()
        self.center_camera_to_player()

        self.update_fade(self.next_view)

    def update_player(self):
        self.update_player_speed()
        self.player_sprite.update()

    def update_enemies(self):
        try:
            enemies = self.scene[SPRITE_LIST_ENEMIES]
        except KeyError:
            enemies = []

        for sprite in enemies:
            if not isinstance(sprite, EnemySprite):
                continue
            sprite.update(
                player=self.player_sprite,
                scene=self.scene,
                physics_engine=self.physics_engine,
                state=self.state
            )

            if arcade.check_for_collision(sprite, self.player_sprite):
                self.player_sprite.hurt(sprite.damage)

        if len(enemies) < 100:
            if random.randint(1, 80) == 1:
                self.spawn_skull()
                logging.info(f'Spawn enemy, new total enemy count: {len(self.scene[SPRITE_LIST_ENEMIES])}')

    def static_layers(self):
        sprite_list = SpriteList(is_static=True)

        layer_names = [
            SPRITE_LIST_WALL,
            SPRITE_LIST_COINS,
            SPRITE_LIST_ENEMIES,
            SPRITE_LIST_PLAYER,
            SPRITE_LIST_MOVEABLE,
        ]

        layers = []

        for layer_name in layer_names:
            try:
                layers.append(self.scene[layer_name])
            except KeyError:
                pass

        for layer in layers:
            for sprite in layer:
                sprite_list.append(sprite)

        return sprite_list

    def make_coin(self):
        rand_x, rand_y = random_position(self.tile_map)
        coin = arcade.sprite.Sprite(
            filename=os.path.join(self.state.sprite_dir, 'coin.png'),
            center_x=rand_x,
            center_y=rand_y,
            scale=0.6
        )

        if arcade.check_for_collision_with_list(coin, self.static_layers()):
            return self.make_coin()

        self.scene.add_sprite(SPRITE_LIST_COINS, coin)

        return

    def spawn_skull(self):
        rand_x, rand_y = random_position(self.tile_map)

        skull = SkullSprite(filename=os.path.join(self.state.sprite_dir, 'skull.png'), center_x=rand_x, center_y=rand_y)

        if arcade.check_for_collision_with_list(skull, self.static_layers()):
            return self.spawn_skull()

        self.scene.add_sprite(SPRITE_LIST_ENEMIES, skull)

        self.physics_engine.add_sprite(skull,
                                       friction=skull.friction,
                                       moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="enemy",
                                       max_velocity=200,
                                       damping=skull.damping
                                       )

        return

    def update_collectable(self):
        coins = arcade.check_for_collision_with_list(self.player_sprite, self.scene[SPRITE_LIST_COINS])
        collected = False

        for coin in coins:
            coin.remove_from_sprite_lists()
            self.state.coins += 1
            self.state.play_sound('coin')
            collected = True

        if collected:
            total_coins = len(self.scene[SPRITE_LIST_COINS])
            logging.info(f'Collected coins {self.state.coins} | coins in scene {total_coins}')
