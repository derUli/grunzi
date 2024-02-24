"""
Platformer Template

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.template_platformer
"""
import os
import arcade
from arcade import SpriteList, PymunkPhysicsEngine

import utils.audio
from sprites.characters.playersprite import PlayerSprite
from sprites.characters.skullsprite import SkullSprite
from utils.physics import make_physics_engine
from utils.sprite import random_position
from views.fadingview import FadingView
from views.pausemenuview import PauseMenuView

# Constants used to scale our sprites from their original size
TILE_SCALING = 1.0

SPRITE_LIST_COINS = 'Coins'
SPRITE_LIST_WALL = 'Walls'
SPRITE_LIST_ENEMIES = 'enemies'
SPRITE_LIST_PLAYER = 'player'
SPRITE_LIST_MOVEABLE = 'Moveable'
TOTAL_COINS = 100

class GameView(FadingView):
    """
    Main application class.
    """

    def __init__(self, window, state):

        # Call the parent class and set up the window
        super().__init__(window)

        self.state = state

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera_sprites = None

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False
        self.down_key_down = False
        self.up_key_down = False

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
        map_name = os.path.join(self.state.map_dir, 'world.tmx')

        layer_options = {
            "Walls": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player, specifically placing it at these coordinates.
        filename = os.path.join(self.state.sprite_dir, 'pig.png')
        self.player_sprite = PlayerSprite(filename)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 128
        self.scene.add_sprite(SPRITE_LIST_PLAYER, self.player_sprite)

        # Create the physics engine
        self.physics_engine = make_physics_engine(self.player_sprite, self.scene)

        # Create the music queue
        self.music_queue = utils.audio.MusicQueue()
        self.music_queue.from_directory(os.path.join(self.state.music_dir, 'level1'))
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

        # Activate the game camera
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


        self.camera_gui.use()

        utils.text.draw_coins(self.state.coins)

        if self.window.debug:
            utils.text.draw_debug(self.player_sprite, self.window)

        self.draw_fading()

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0

        move_force = self.player_sprite.move_force

        force_x, force_y = 0, 0

        if self.up_key_down and not self.down_key_down and self:
            force_y = move_force
        elif self.down_key_down and not self.up_key_down:
            force_y = -move_force
        if self.left_key_down and not self.right_key_down:
            force_x = -move_force
            self.player_sprite.change_x = -1
        elif self.right_key_down and not self.left_key_down:
            force_x = move_force
            self.player_sprite.change_x = 1

        self.physics_engine.apply_force(self.player_sprite, (force_x, force_y))

        # --- Move items in the physics engine
        self.player_sprite.update()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)

        """Called whenever a key is pressed."""
        if key == arcade.key.ESCAPE:
            pause_view = PauseMenuView(self.window, self.state, self)
            self.window.show_view(pause_view)

        if key == arcade.key.F1:
            self.join_skull()

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_key_down = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_key_down = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
            self.update_player_speed()
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
            self.update_player_speed()
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_key_down = False
            self.update_player_speed()
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down_key_down = False
            self.update_player_speed()

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
        self.camera_sprites.move_to(player_centered, speed=0.8)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.update_player_speed()
        self.physics_engine.step()
        self.update_collectable()

        # Position the camera
        self.center_camera_to_player()
        self.update_fade()

        try:
            enemies = self.scene[SPRITE_LIST_ENEMIES]
        except KeyError:
            return

        for sprite in enemies:
            sprite.update(
                player=self.player_sprite,
                walls = self.scene[SPRITE_LIST_WALL],
                scene=self.scene,
                physics_engine=self.physics_engine
            )

    def static_layers(self):
        sprite_list = SpriteList()

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
            center_x = rand_x,
            center_y = rand_y
        )

        if arcade.check_for_collision_with_list(coin, self.static_layers()):
            return self.make_coin()

        self.scene.add_sprite(SPRITE_LIST_COINS, coin)

        return

    def join_skull(self):
        rand_x, rand_y = random_position(self.tile_map)

        rand_x, rand_y = 680, 500

        skull = SkullSprite(filename=os.path.join(self.state.sprite_dir, 'skull.png'), center_x = rand_x, center_y = rand_y)

        if arcade.check_for_collision_with_list(skull, self.static_layers()):
            return self.join_skull()

        self.scene.add_sprite(SPRITE_LIST_ENEMIES, skull)

        self.physics_engine.add_sprite(skull,
                                  friction=skull.friction,
                                  moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                                  collision_type="player",
                                  max_velocity=400,
                                  damping=skull.damping
                                  )

        return

    def update_collectable(self):
        coins = arcade.check_for_collision_with_list(self.player_sprite, self.scene[SPRITE_LIST_COINS])
        for coin in coins:
            coin.remove_from_sprite_lists()
            self.state.coins += 1

            self.state.play_sound('coin')