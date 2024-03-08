import logging
import os

import arcade
import mouse

import constants.controls.keyboard
from constants.controls.controller import AXIS_RIGHT, AXIS_LEFT, AXIS_DOWN, AXIS_UP
from state.settingsstate import SettingsState
from utils.screenshot import make_screenshot
from utils.text import MARGIN, create_text

MOUSE_POINTER_SPEED = 10
PERFORMANCE_GRAPH_WIDTH = 160
PERFORMANCE_GRAPH_HEIGHT = 90

PERFORMANCE_GRAPH_BACKGROUND = (0, 0, 0, 80)


class View(arcade.View):

    def __init__(self, window):
        # Call the parent class and set up the window
        super().__init__(window)

        self.state = None
        self.scene = arcade.Scene()
        self.build_version = ''
        # Initialize the camera for static GUI elements
        self.camera_gui = arcade.Camera()
        self.shadertoy = None
        self.alt_key_pressed = False

        self.view = None
        self.time = 0
        self.move_pointer = None
        self.perf_graph = None

    def on_key_press(self, key, modifiers):

        super().on_key_press(key, modifiers)

        if key == arcade.key.LALT:
            self.alt_key_pressed = True
        if self.alt_key_pressed and key == arcade.key.ENTER or key == arcade.key.F11:
            self.on_toggle_fullscreen()

        if key in constants.controls.keyboard.KEY_TOGGLE_FPS:
            self.on_toggle_fps()
        if key in constants.controls.keyboard.KEY_TOGGLE_DEBUG:
            self.on_toggle_debug()
        if key in constants.controls.keyboard.KEY_SOUND_QUIETER:
            self.state.sound_volume -= 0.1
        if key in constants.controls.keyboard.KEY_SOUND_LOUDER:
            self.state.sound_volume += 0.1
        if key in constants.controls.keyboard.KEY_SCREENSHOT:
            self.on_make_screenshot()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LALT:
            self.alt_key_pressed = False

    def on_show_view(self):
        # Set the background color
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.perf_graph = arcade.PerfGraph(
            PERFORMANCE_GRAPH_WIDTH,
            PERFORMANCE_GRAPH_HEIGHT,
            background_color=PERFORMANCE_GRAPH_BACKGROUND
        )
        self.perf_graph.left = self.window.width - MARGIN - self.perf_graph.width
        self.perf_graph.bottom = MARGIN

    def on_toggle_fullscreen(self):
        self.window.set_fullscreen(not self.window.fullscreen)
        settings = SettingsState().load()
        settings.fullscreen = self.window.fullscreen
        settings.save()

    def on_toggle_fps(self):
        self.state.settings.show_fps = not self.state.settings.show_fps

        self.state.settings.save()

    def on_toggle_debug(self):
        self.window.debug = not self.window.debug

    def on_make_screenshot(self):
        screenshot = make_screenshot()
        self.state.play_sound('screenshot')

        return screenshot

    def draw_build_version(self):
        if not self.build_version:
            self.build_version = _('Unknown build')
            version_file = os.path.join(self.state.root_dir, 'VERSION.txt')

            if os.path.isfile(version_file):
                with open(version_file, 'r') as f:
                    self.build_version = f.read()

        create_text(self.build_version, width=self.window.width - (MARGIN * 2), align='left').draw()

    def on_update(self, delta_time=0):
        if self.state.settings.show_fps:
            self.perf_graph.update_graph(delta_time=delta_time)

    def on_stick_motion(self, controller, stick_name, x_value, y_value):
        logging.info(f"Stick motion {stick_name}, {x_value}, {y_value}")

        x_value = round(x_value)
        y_value = round(y_value)

        x, y = 0, 0

        if x_value == AXIS_RIGHT:
            x += MOUSE_POINTER_SPEED
        elif x_value == AXIS_LEFT:
            x -= MOUSE_POINTER_SPEED

        if y_value == AXIS_DOWN:
            y += MOUSE_POINTER_SPEED
        elif y_value == AXIS_UP:
            y -= MOUSE_POINTER_SPEED

        move_pointer = (x, y)

        if x == 0 and y == 0:
            move_pointer = None

        self.move_pointer = move_pointer

    def on_button_press(self, controller, key):
        logging.info(f"Controller button {key} pressed")
        mouse.click()

    def push_controller_handlers(self):
        for controller in self.window.controllers:
            controller.push_handlers(self)

    def pop_controller_handlers(self):
        for controller in self.window.controllers:
            controller.pop_handlers()

    def update_mouse(self):
        if self.move_pointer:
            x, y = self.move_pointer
            mouse.move(x, y, absolute=False)

    def render_shadertoy(self):
        if self.shadertoy:
            self.shadertoy.render(time=self.time)

    def draw_debug(self, delta_time=0):
        if self.state.settings.show_fps:
            self.perf_graph.draw()
