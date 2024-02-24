import arcade

from utils.screenshots import make_screenshot


class View(arcade.View):

    def __init__(self, window):
        self.state = None

        # Call the parent class and set up the window
        super().__init__(window)

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        if key == arcade.key.F12:
            make_screenshot()
            self.state.play_sound('screenshot')