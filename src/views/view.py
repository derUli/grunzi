""" View base class """

import os

import arcade
import mouse

import constants.controls.keyboard
from constants.controls.controller import AXIS_RIGHT, AXIS_LEFT, AXIS_DOWN, AXIS_UP
from state.settingsstate import SettingsState
from utils.fpscounter import FPSCounter
from utils.gui import center_cursor
from utils.screenshot import make_screenshot
from utils.text import MARGIN, create_text

MOUSE_POINTER_SPEED = 10
MOUSE_POINTER_MODIFIER_DEFAULT = 1.0
MOUSE_POINTER_MODIFIER_FAST = 2.0
PERFORMANCE_GRAPH_WIDTH = 160
PERFORMANCE_GRAPH_HEIGHT = 90

DEFAULT_BACKGROUND = arcade.csscolor.BLACK


class View(arcade.View):
    """ View base class """

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
        self.build_number_text = None

        self.fps_counter = FPSCounter()
        self.background = DEFAULT_BACKGROUND

        self.mouse_modifier = MOUSE_POINTER_MODIFIER_DEFAULT

    def on_show_view(self) -> None:
        """ On show view """
        self.fps_counter = FPSCounter()
        arcade.set_background_color(self.background)

    def on_update(self, delta_time: float):
        self.time += delta_time

        fps = arcade.get_fps()

        if self.window.vsync and fps > self.window.monitor_refresh_rate:
            fps = self.window.monitor_refresh_rate

        self.fps_counter.update(fps)

    def on_draw(self) -> None:
        arcade.set_background_color(DEFAULT_BACKGROUND)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        On key press
        @param key: Key
        @param modifiers: Modifiers
        """
        super().on_key_press(key, modifiers)

        if key == arcade.key.LALT:
            self.alt_key_pressed = True
        if self.alt_key_pressed and key == arcade.key.ENTER or key == arcade.key.F11:
            self.on_toggle_fullscreen()

        if key in constants.controls.keyboard.KEY_TOGGLE_FPS:
            self.on_toggle_fps()
        if key in constants.controls.keyboard.KEY_SCREENSHOT:
            self.on_make_screenshot()

    def on_key_release(self, key: int, modifiers: int) -> None:
        """
        On key release
        @param key: Key
        @param modifiers: Modifier
        """
        if key == arcade.key.LALT:
            self.alt_key_pressed = False

    def on_toggle_fullscreen(self) -> None:
        """ On toggle fullscreen """
        self.window.change_screen_mode(not self.window.fullscreen)
        settings = SettingsState().load()
        settings.fullscreen = self.window.fullscreen
        settings.save()

    def on_toggle_vsync(self) -> None:
        """ On toggle vsync """
        self.window.set_vsync(not self.window.vsync)
        settings = SettingsState().load()
        settings.vsync = self.window.vsync
        settings.save()

    def on_toggle_fps(self) -> None:
        """ On toggle fps """
        self.state.settings.show_fps = not self.state.settings.show_fps
        self.state.settings.save()

    def on_make_screenshot(self) -> str:
        """
        On make screenshot
        @return: path
        """
        screenshot = make_screenshot()
        self.state.play_sound('screenshot')

        return screenshot

    def draw_build_version(self) -> None:
        """ Draw build version """

        # Read version number from version file
        if not self.build_version:
            self.build_version = _('Unknown build')
            version_file = os.path.join(self.state.root_dir, 'VERSION.txt')

            if os.path.isfile(version_file):
                with open(version_file, 'r', encoding='utf-8') as f:
                    self.build_version = f.read()

        # Render the build number text
        if not self.build_number_text:
            self.build_number_text = create_text(
                self.build_version,
                width=self.window.width - (MARGIN * 2),
                align='left'
            )
        self.build_number_text.draw()

    def on_stick_motion(self, controller, stick_name, x_value, y_value):

        x_value = round(x_value)
        y_value = round(y_value)

        x, y = 0, 0

        speed = MOUSE_POINTER_SPEED * self.mouse_modifier

        if x_value == AXIS_RIGHT:
            x += speed
        elif x_value == AXIS_LEFT:
            x -= speed

        if y_value == AXIS_DOWN:
            y += speed
        elif y_value == AXIS_UP:
            y -= speed

        move_pointer = (x, y)

        if x == 0 and y == 0:
            move_pointer = None

        self.move_pointer = move_pointer

    def on_button_press(self, joystick, key):

        if key in constants.controls.controller.KEY_MENU_ITEM:
            mouse.click()

        if key in constants.controls.controller.KEY_SPRINT:
            self.mouse_modifier = MOUSE_POINTER_MODIFIER_FAST

    def on_button_release(self, joystick, key):
        if key in constants.controls.controller.KEY_SPRINT:
            self.mouse_modifier = MOUSE_POINTER_MODIFIER_DEFAULT

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

    def render_shadertoy(self) -> None:
        """ Render Shadertoy shader """

        if self.shadertoy:
            self.shadertoy.render(time=self.time)

    def draw_fps(self):

        if self.state.settings.show_fps:
            self.fps_counter.draw(size=self.window.size)

    def draw_after(self, draw_version_number=False):
        if draw_version_number:
            self.draw_build_version()

        self.draw_fps()
