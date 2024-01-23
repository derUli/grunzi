""" Main character sprite """

import logging
import os

import pygame
from PygameShader.shader import horizontal_glitch

from constants.graphics import SPRITE_SIZE
from constants.headup import NPC_HEALTH_COLOR_FRIENDLY, NPC_HEALTH_HEIGHT
from sprites.blood import Blood
from sprites.character import Character
from sprites.fadeable import Fadeable
from sprites.weapon import Weapon
from utils.atmosphere import ATMOSPHERE_FOG, ATMOSPHERE_SNOW, ATMOSPHERE_RAIN
from utils.audio import play_sound

HORSE_FOG = 255

TASK_ID = 'horse'


class Horse(Character, Fadeable):
    """ Chicken sprite class """

    def __init__(self, sprite_dir, cache, sprite='horse.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.sentence = -1
        self.attributes = {
            'blood': 0,
            'given_blood': 0,
            'full_of_blood': False
        }

        self.task = None
        self.fade_frame = None

        self.sentences = [
            _('Infinity bloodless!'),
            _('I don\'t have a single drop of blood left.'),
            _('Please give me some blood!'),
            _('I am infinitely thirsty for blood.')
        ]

        self.horse_sound = os.path.abspath(
            os.path.join(
                sprite_dir,
                '..',
                '..',
                'sounds',
                'horse',
                'horse.ogg')
        )

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        x, y = self.calculate_pos(x, y)
        if self.fade_frame is not None:
            self.fade_frame += 1

            horizontal_glitch(screen, 0.5, 0.08, self.fade_frame)

            if self.fade_frame > 127:
                self.purge = True

        pos = (x, y)

        self.draw_health(screen, pos)

    def draw_health(self, screen, pos):

        x, y = pos
        w, h = SPRITE_SIZE

        y += h - NPC_HEALTH_HEIGHT

        w = w / 100 * self.attributes['blood']
        h = NPC_HEALTH_HEIGHT

        surface = pygame.surface.Surface((w, h))

        surface.fill(NPC_HEALTH_COLOR_FRIENDLY)

        screen.blit(surface, (x, y))

    def next_sentence(self):
        self.sentence += 1

        if self.sentence >= len(self.sentences):
            self.sentence = 0

        return self.sentences[self.sentence]

    def handle_interact(self, element):
        if element and element.state:
            if element.state.display_text.is_visible():
                return

            play_sound(self.horse_sound)
            element.state.say(self.next_sentence())

            self.task = TASK_ID

    def ai(self, level):
        part = 0.5

        if self.attributes['given_blood'] <= 0:
            self.attributes['given_blood'] = 0
            return

        self.attributes['blood'] += part
        self.attributes['given_blood'] -= part

        if self.attributes['blood'] >= 100:
            self.attributes['blood'] = 100
            self.attributes['given_blood'] = 0

        if self.attributes['blood'] < 0:
            self.attributes['blood'] = 0

    def handle_interact_item(self, element):
        """ Handle interact """
        logging.debug('interact')
        if not element:
            return

        if isinstance(element.state.inventory, Blood):
            amount = element.state.inventory.blood_amount

            element.state.inventory.blood_amount -= amount
            self.attributes['given_blood'] += amount

            element.state.inventory = None
            self.sentences = [
                _('Now I have a bit more blood.'),
                _('I still haven\'t enough blood.'),
                _('Yummy blood!'),
                _('Give me more blood!'),
                _('Tasty blood!'),
                _('I need more blood!')
            ]
            self.sentence = -1

            play_sound(self.horse_sound)

            element.state.say(self.next_sentence())
        elif isinstance(element.state.inventory, Weapon):
            element.state.say(_('Hahaha! It tickles!'))
        else:
            element.state.say(_("I don't need this."))

    def update_atmosphere(self, atmosphere):
        fog = atmosphere.get_layer_by_id(ATMOSPHERE_FOG)

        if not fog:
            return
        if self.attributes['blood'] >= 100:
            fog.update(0)

            snow = atmosphere.get_layer_by_id(ATMOSPHERE_SNOW)
            if snow and snow.is_running():
                snow.stop()

            rain = atmosphere.get_layer_by_id(ATMOSPHERE_RAIN)

            if rain:
                rain.set_value(500)

            return

        fog.update(HORSE_FOG)

    def finish_task(self):
        if self.fade_frame is None:
            self.fade_frame = 0

    def update_state(self, state):
        full_of_blood = 'full_of_blood' in self.attributes and self.attributes['full_of_blood']
        if self.attributes['blood'] >= 100 and not full_of_blood:
            self.attributes['full_of_blood'] = True
            state.task.set_id(None)

            state.player_state.say(_('Now I am full of blood.'), handle_text_shown=self.finish_task)

        if self.task:
            state.task.set_id(self.task)
            self.task = None
