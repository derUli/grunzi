import arcade

import constants.controls.keyboard
from utils.screenshot import make_screenshot


class View(arcade.View):

    def __init__(self, window):
        # Call the parent class and set up the window
        super().__init__(window)

        self.state = None
        self.scene = arcade.Scene()

        # Initialize the camera for static GUI elements
        self.camera_gui = arcade.Camera()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        if key in constants.controls.keyboard.KEY_SCREENSHOT:
            make_screenshot()
            self.state.play_sound('screenshot')

    def on_show_view(self):
        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
