import unittest
import gettext
import arcade
import os
from state.viewstate import ViewState
from utils.screenshot import make_screenshot
from views.mainmenu import MainMenu
from window.gamewindow import GameWindow

_ = gettext.gettext

class ScreenshotTest(unittest.TestCase):
    def setUp(self):

        self.window = GameWindow()

        root_dir = os.path.join('..', 'src')
        self.state = ViewState(root_dir=root_dir, map_name='world')

        gettext.install('messages')
    def tearDown(self):
        arcade.close_window()

    def test_screenshot(self):

        self.skipTest('Fix Me')
        view = MainMenu(self.window, self.state)

        view._fade_in = None
        self.window.show_view(view)
        self.window.on_draw()

        # TODO: Fix this
        self.assertTrue(os.path.exists(make_screenshot()))