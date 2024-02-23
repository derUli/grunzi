"""
Platformer Template

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.template_platformer
"""
import os

import arcade

import utils.audio
from sprites.characters.playersprite import PlayerSprite
from views.fadingview import FadingView

# Constants used to scale our sprites from their original size
TILE_SCALING = 1.0

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10


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

        self.music_queue = None

    def on_show_view(self):
        """Set up the game here. Call this function to restart the game."""

        # Setup the Cameras
        self.camera_sprites = arcade.Camera()

        # Name of map file to load
        map_name = os.path.join(self.state.map_dir, 'world.tmx')

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            # "Platforms": {
            #    "use_spatial_hash": True,
            # },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set the background color
        if self.tile_map.background_color:
            self.background_color = self.tile_map.background_color

        # Set up the player, specifically placing it at these coordinates.
        filename = os.path.join(self.state.sprite_dir, 'pig.png')
        self.player_sprite = PlayerSprite(filename)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # --- Other stuff
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, walls=self.scene["Walls"]
        )

        self.music_queue = utils.audio.MusicQueue()

        self.music_queue.from_directory(os.path.join(self.state.music_dir, 'level1'))
        self.music_queue.play()

    def on_draw(self):
        """Render the screen."""

        # Activate the game camera
        self.camera_sprites.use()

        # Draw our Scene
        # Note, if you a want pixelated look, add pixelated=True to the parameters
        self.scene.draw()

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.left_key_down and not self.right_key_down:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_key_down and not self.left_key_down:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        if self.down_key_down and not self.up_key_down:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif self.up_key_down and not self.down_key_down:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED

        self.player_sprite.update()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:
            arcade.close_window()  # TODO: Return to main Menu

        """Called whenever a key is pressed."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True
            self.update_player_speed()

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_key_down = True
            self.update_player_speed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_key_down = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
            self.update_player_speed()

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_key_down = False
            self.update_player_speed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
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
        self.camera_sprites.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()
