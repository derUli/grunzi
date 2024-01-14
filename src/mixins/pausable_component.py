import logging
import time

import pygame
from PygameShader.shader import blur

import utils.savegame
from components.component import Component
from components.mixins.loadingindicator import LoadingIndicator
from constants import gamepad
from constants import keyboard
from constants.headup import UI_MARGIN
from utils.audio import pause_sounds, unpause_sounds, stop_sounds
from utils.menu import make_menu
from utils.string import label_value

MAX_BLUR_ITERATIONS = 20
TEXT_COLOR = (255, 255, 255)

AUTOSAVE_INTERVAL = 5 * 60


class PausableComponent(LoadingIndicator):
    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad
        )

        self.next_autosave = 0
        self.update_next_autosave()

    def pause_menu(self):
        self.pressed_keys = []
        pause_sounds()
        self.last_screen = self.screen.copy().convert()
        self.blur_iteration = 0

        menu = make_menu(_('Pause'), self.settings_state.limit_fps)

        menu.add.button(
            _('Continue'),
            self.handle_continue_game)  # Continue game
        menu.add.button(_('Save Game'), self.handle_save_game)  # Continue game
        menu.add.button(_('Back To Main Menu'),
                        self.back_to_main_menu)  # Return to main menu

        self.menu = menu
        self.music_queue.pause()
        menu.mainloop(self.screen, self.draw_background)

    def handle_continue_game(self):
        self.menu.disable()
        unpause_sounds()
        self.music_queue.unpause()
        pygame.mouse.set_visible(0)

    def draw_background(self):
        self.screen.blit(self.last_screen, (0, 0))

        if self.blur_iteration < MAX_BLUR_ITERATIONS:
            blur(self.last_screen, 1)
            self.blur_iteration += 1

        task_text = self.state.task.get_display_text()
        text = label_value(_('Aufgabe'), task_text)
        """ Render a text """
        rendered_text = self.monotype_font.render(
            text,
            utils.quality.font_antialiasing_enabled(),
            TEXT_COLOR
        )

        y = self.screen.get_height() - UI_MARGIN - rendered_text.get_height()

        x = UI_MARGIN

        self.screen.blit(rendered_text, (x, y))

    def handle_save_game(self, savegame_name: str = utils.savegame.SAVEGAME_DEFAULT):

        self.state.atmosphere = self.atmosphere
        utils.savegame.save_game(
            savegame_name,
            self.state,
            self.level.to_diff_list())

        if savegame_name == utils.savegame.SAVEGAME_AUTOSAVE:
            self.update_next_autosave()
            return

        self.state.player_state.say(_('Game saved.'))
        self.handle_continue_game()

    def update_next_autosave(self):
        self.next_autosave = time.time() + AUTOSAVE_INTERVAL

    def should_autosave(self):
        return time.time() > self.next_autosave

    def autosave(self):
        self.change_progress_indicator(True)
        self.handle_save_game(utils.savegame.SAVEGAME_AUTOSAVE)
        self.update_next_autosave()
        logging.debug('Autosave')
        self.change_progress_indicator(False)

    def back_to_main_menu(self):
        self.menu.disable()
        pygame.mouse.set_visible(True)
        stop_sounds()
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
