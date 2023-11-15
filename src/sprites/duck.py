""" Duck character sprite """
import time
import os
import logging
import random
from sprites.character import Character
from utils.audio import play_sound

class Duck(Character):
    """ Duck sprite class """

    def __init__(self, sprite_dir, cache, sprite='duck.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.next_quack = None
        self.sound = None

    def play_sound(self):
        if self.sound and self.sound.get_busy():
            logging.debug('busy')
            return

        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'duck')
        )

        files = [
            'duck1.ogg',
            'duck2.ogg',
            'duck3.ogg'

        ]
        file = os.path.join(sound_dir, random.choice(files))

        self.sound = play_sound(file)

    def ai(self, level):
        next_quack = time.time() + random.randint(3, 10)
        if not self.next_quack:
            self.next_quack = next_quack
            return

        if time.time() > self.next_quack:
            self.next_quack = next_quack
            self.play_sound()