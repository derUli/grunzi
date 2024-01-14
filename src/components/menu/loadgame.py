import utils.savegame
from components.game.maingame import MainGame
from components.menu.menucomponent import MenuComponent
from utils.menu import make_menu

MIN_SCREEN_RESOLUTION = (800, 600)


class LoadGameComponent(MenuComponent):

    def draw_menu(self, screen):
        menu = make_menu(_('Load Game'), self.settings_state.limit_fps)

        if utils.savegame.has_savegame(utils.savegame.SAVEGAME_DEFAULT):
            menu.add.button(_('Manual save'), self.handle_load_manual_save)

        if utils.savegame.has_savegame(utils.savegame.SAVEGAME_AUTOSAVE):
            menu.add.button(_('Autosave'), self.handle_load_autosave)

        menu.add.button(_('Back'), self.handle_back_to_main_menu)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)

    def load(self, name):
        component = self.handle_change_component(MainGame)
        if self.menu:
            self.menu.disable()
        component.load_savegame(name)

    def handle_load_manual_save(self):
        self.load(utils.savegame.SAVEGAME_DEFAULT)

    def handle_load_autosave(self):
        self.load(utils.savegame.SAVEGAME_AUTOSAVE)

    def handle_back_to_main_menu(self):
        """ On click 'Back To Main Menu' """
        component = self.handle_change_component(None)
        component.video = self.video

        if self.menu:
            self.menu.disable()
