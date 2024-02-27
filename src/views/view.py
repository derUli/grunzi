import os

import arcade

import constants.controls.keyboard
from utils.screenshot import make_screenshot
from utils.text import MARGIN, create_text
from utils.text import draw_debug

class View(arcade.View):

    def __init__(self, window):
        # Call the parent class and set up the window
        super().__init__(window)

        self.state = None
        self.scene = arcade.Scene()
        self.build_version = ''
        # Initialize the camera for static GUI elements
        self.camera_gui = arcade.Camera()

        self.alt_key_pressed = False

    def on_key_press(self, key, modifiers):

        super().on_key_press(key, modifiers)
        if key == arcade.key.LALT:
            self.alt_key_pressed = True
        if self.alt_key_pressed and key == arcade.key.ENTER:
            self.on_toggle_fullscreen()

        if key in constants.controls.keyboard.KEY_TOGGLE_FPS:
            self.on_toggle_fps()
        if key in constants.controls.keyboard.KEY_SCREENSHOT:
            self.on_make_screenshot()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LALT:
            self.alt_key_pressed = False

    def on_show_view(self):
        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_toggle_fullscreen(self):
        self.window.set_fullscreen(not self.window.fullscreen)

    def on_toggle_fps(self):
        self.window.show_fps = not self.window.show_fps

    def on_make_screenshot(self):
        make_screenshot()
        self.state.play_sound('screenshot')

    def draw_build_version(self):
        if not self.build_version:
            self.build_version = _('Unknown build')
            version_file = os.path.join(self.state.root_dir, 'VERSION.txt')

            if os.path.isfile(version_file):
                with open(version_file, 'r') as f:
                    self.build_version = f.read()

        create_text(self.build_version, width=self.window.width - (MARGIN * 2), align='left').draw()

    def draw_debug(self, player_sprite = None):
        draw_debug(player_sprite, self.window)