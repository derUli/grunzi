""" Game over screen """

import random

import arcade

from utils.text import create_text

MARGIN = 10

FONT_SIZE_TITLE = 30
FONT_SIZE_SUBTITLE = 22


class GameOverText:
    """ Game over screen """

    def __init__(self):
        """ Constructor """

        self.random_text = None
        self.texts = []

    def setup(self):
        """ Setup game over text """

        self.random_text = GameOverText.generate_random_text()
        self.texts = []

        window = arcade.get_window()

        gameover_text = create_text(
            text=self.random_text,
            font_size=FONT_SIZE_TITLE
        )

        gameover_text.x = window.width / 2 - gameover_text.content_width / 2
        gameover_text.y = window.height / 2 - gameover_text.content_height / 2

        self.texts.append(gameover_text)

        press_button_text = create_text(
            text=_('Press any key to continue'),
            font_size=FONT_SIZE_SUBTITLE
        )

        press_button_text.x = window.width / 2 - press_button_text.content_width / 2
        press_button_text.y = MARGIN

        self.texts.append(press_button_text)

    @staticmethod
    def generate_random_text() -> str:
        """
        Generate random game over text
        @return: random sentence
        """

        sausages = [
            _('bacon'),
            _('salami'),
            _('schnitzel'),
            _('Cutlet'),
            _('Mett'),
            _('Suckling pig'),
            _('Pulled Pork'),
            _('Spare ribs')
        ]

        return _('You are') + ' ' + random.choice(sausages) + '!'

    def draw(self):
        """ Draw text """

        for text in self.texts:
            text.draw()
