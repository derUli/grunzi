import pygame
import pygame_menu
import utils.savegame

class PausableComponent():

    # Todo refactor to own class
    def pause_menu(self):

        menu = pygame_menu.Menu(height=300,
                                theme=pygame_menu.themes.THEME_BLUE,
                                title='Pause menu',
                                width=400)

        menu.add.button('Continue', self.continue_game)  # Continue game
        menu.add.button('Save Game', self.save_game)  # Continue game
        menu.add.button('Back To Main Menu',
                        self.back_to_main_menu)  # Return to main menu

        self.menu = menu
        menu.mainloop(self.screen)

    def continue_game(self):
        self.menu.disable()

    def save_game(self):
        utils.savegame.save_game(utils.savegame.DEFAULT_SAVE, self.state)
        self.continue_game()

    def back_to_main_menu(self):
        self.continue_game()
        self.handle_change_component(None)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause_menu()
            return

        super().handle_event(event)
