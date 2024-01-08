""" Main character sprite """

import logging
import os
import random
import time

import pygame

from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_DOWN
from sprites.chainsaw import Chainsaw
from sprites.character import Character
from sprites.feather import Feather
from sprites.killable import Killable
from sprites.maincharacter import PIG_SOUND_NOTHING
from utils.audio import play_sound
from utils.quality import pixel_fades_enabled

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0

BLOOD_COLOR = (163, 8, 8)
CHICKEN_SOUND_FADEOUT = 100


class Horse(Killable, Character):
    """ Chicken sprite class """

    def __init__(self, sprite_dir, cache, sprite='horse.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.sentence = -1
        
        self.sentences = [
            _('Infinity bloodless!'),
            _('I don\'t have a single drop of blood left.'),
            _('Please give me some blood!'),
            _('I am infinitely thirsty for blood.')
        ]

    def next_sentence(self):
        self.sentence += 1
        
        if self.sentence >= len(self.sentences):
            self.sentence = 0

        
        return self.sentences[self.sentence]


    def handle_interact(self, element):
        if element and element.state:
            element.state.say(self.next_sentence())
