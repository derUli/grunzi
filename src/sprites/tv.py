""" TV character """
import os

import sprites.sprite
from utils.animation import Animation


class TV(sprites.sprite.Sprite):
    """ Fire character class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """

        super().__init__(sprite_dir, cache, 'tv.png')
        sprite_dir = os.path.join(sprite_dir, 'animations', 'dancing_pig')

        self.animation = Animation(
            sprite_dir,
            refresh_interval=0.04,
            size=(56, 31))
        self.walkable = False

    def draw(self, screen, x, y):
        """ Draw current frame of fire animation """
        super().draw(screen, x, y)

        x, y = self.calculate_pos(x, y)
        frame = self.animation.get_frame()

        x += 4
        y += 13
        screen.blit(frame, (x, y))

    def handle_interact(self, element):
        element.state.say(_('My favorite movie.'))