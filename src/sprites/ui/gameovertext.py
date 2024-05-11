import random

import arcade

from utils.text import create_text


class GameOverText:
    def __init__(self):
        self.random_text = None
        self.texts = []

    def setup(self):
        self.random_text = self.generate_random_text()
        self.texts = []

        window = arcade.get_window()

        gameover_text_rendered = create_text(
            text=self.random_text,
            bold=True
        )

        gameover_text_rendered.x = window.width / 2 - gameover_text_rendered.content_width / 2
        gameover_text_rendered.y = window.height / 2 - gameover_text_rendered.content_height / 2

        self.texts.append(gameover_text_rendered)

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
