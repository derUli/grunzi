""" TV """
import os

import sprites.sprite
from sprites.remote import Remote
from utils.animation import Animation
from utils.audio import play_sound


class TV(sprites.sprite.Sprite):
    """ TV class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """

        super().__init__(sprite_dir, cache, 'tv.png')
        sprite_dir = os.path.join(sprite_dir, 'animations', 'dancing_pig')

        self.animation = Animation(
            sprite_dir,
            refresh_interval=0.04,
            size=(57, 31))
        self.walkable = False
        self.enabled = False

    def draw(self, screen, x, y):
        """ Draw current frame of fire animation """
        super().draw(screen, x, y)
        if not self.enabled:
            return

        x, y = self.calculate_pos(x, y)
        frame = self.animation.get_frame()

        x += 4
        y += 13
        screen.blit(frame, (x, y))

    def handle_interact(self, element):
        if self.enabled:
            element.state.say(_('My favorite movie.'))
        else:
            element.state.say(_('The TV is off.'))
    def handle_interact_item(self, element):
        if isinstance(element.state.inventory, Remote):
            self.enabled = not self.enabled
            element.state.use_item = None
            self.play_sound()
            if self.enabled:
                element.state.say(_('The TV is on.'))
            else:
                element.state.say(_('The TV is off.'))


    def play_sound(self):
        play_sound(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'tv',
                'zap.ogg'
            )
        )