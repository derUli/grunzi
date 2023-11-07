import gettext

import pygame

import utils.savegame
from constants import gamepad
from constants import keyboard
from utils.menu import make_menu

_ = gettext.gettext


class PausableComponent:
    def pause_menu(self):
        self.last_screen = self.screen.copy().convert_alpha()
        self.last_screen.set_alpha(100)

        menu = make_menu(_('Pause'), self.settings_state.limit_fps)

        menu.add.button(
            _('Continue'),
            self.handle_continue_game)  # Continue game
        menu.add.button(_('Save Game'), self.handle_save_game)  # Continue game
        menu.add.button(_('Back To Main Menu'),
                        self.back_to_main_menu)  # Return to main menu

        self.menu = menu
        menu.mainloop(self.screen, self.draw_background)

    def handle_continue_game(self):
        self.menu.disable()
        pygame.mouse.set_visible(0)

    def draw_background(self, background):
        self.screen.blit(self.last_screen, (0, 0))

        self.show_fps()

    def handle_save_game(self):
        utils.savegame.save_game(utils.savegame.DEFAULT_SAVE, self.state, self.level)
        self.handle_continue_game()

    def back_to_main_menu(self):
        self.handle_continue_game()
        pygame.mouse.set_visible(1)
        self.handle_change_component(None)

    def handle_event(self, event):
        # Pause on PC
        if event.type == pygame.KEYDOWN and event.key in keyboard.ABORT_KEYS:
            self.pause_menu()
            return True
        elif event.type == pygame.JOYBUTTONDOWN and event.button in gamepad.ABORT_KEYS:
            self.pause_menu()
            return True

        return super().handle_event(event)
