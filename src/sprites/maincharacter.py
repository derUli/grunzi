""" Main character sprite """
import os

import constants.game
from sprites.character import Character
from utils.audio import play_sound

PIG_SOUND_NOTHING = 'nothing.ogg'


class MainCharacter(Character):
    """ Main character sprite class """

    def __init__(self, sprite_dir, cache, sprite='pig.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.center_camera = True
        self.sound = None

        self.last_movement = 0
        self.id = constants.game.MAIN_CHARACTER_ID
        self.sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'pig')
        )

    def draw(self, screen, x, y):
        """ Draw main character """
        super().draw(screen, x, y)

        # Detailed object view
        if self.state.show_detailed:
            screen.blit(self.state.show_detailed, (0, 0))

    def play_sound(self, sound):
        if self.sound and self.sound.get_busy():
            return

        sound_dir = os.path.join(self.sound_dir, sound)
        self.sound = play_sound(sound_dir)
