import random

import arcade

from utils.text import create_text, LARGE_FONT_SIZE, EXTRA_LARGE_FONT_SIZE

MARGIN = 10


class GameOverText:
    def __init__(self):
        self.random_text = None
        self.texts = []

    def setup(self):
        self.random_text = self.generate_random_text()
        self.texts = []

        window = arcade.get_window()

        gameover_text = create_text(
            text=self.random_text,
            font_size=EXTRA_LARGE_FONT_SIZE
        )

        gameover_text.x = window.width / 2 - gameover_text.content_width / 2
        gameover_text.y = window.height / 2 - gameover_text.content_height / 2

        self.texts.append(gameover_text)

        press_button_text = create_text(
            text=_('Press any key to continue'),
            font_size=LARGE_FONT_SIZE
        )

        press_button_text.x = window.width / 2 - press_button_text.content_width / 2
        press_button_text.y = MARGIN

        self.texts.append(press_button_text)

    def generate_random_text(self) -> str:
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
        for text in self.texts:
            text.draw()
