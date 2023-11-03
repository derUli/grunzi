""" Main character sprite """

import constants.game
from sprites.character import Character

class MainCharacter(Character):
    """ Main character sprite class """

    def __init__(self, sprite_dir, cache, sprite='pig.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.center_camera = True

        self.last_movement = 0
        self.id = constants.game.MAIN_CHARACTER_ID

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        if self.state.show_detailed:
            screen.blit(self.state.show_detailed, (0, 0))
