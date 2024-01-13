""" Guitar sprite """
import logging
import os

import utils.audio
from sprites.sprite import Sprite


class Guitar(Sprite):
    """ Guitar sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'guitar.png')
        self.sound = None

    def handle_interact(self, element):
        """ Play sound on interaction """
        sound_file = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'guitar', 'guitar.ogg')
        )

        if self.sound and self.sound.get_busy():
            return

        logging.debug('Playing the guitar')

        self.sound = utils.audio.play_sound(sound_file)
