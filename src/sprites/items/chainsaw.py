import random

from arcade import FACE_DOWN, FACE_UP

from sprites.items.item import Item
from sprites.items.tree import Tree

SCORE_DESTROY_TREE = 200
SCORE_KILL_SKULL = 100
SCORE_KILL_CHICKEN = 50


class Chainsaw(Item):
    def on_use_with(self, b, args):
        from sprites.characters.skull import Skull
        from sprites.characters.chicken import Chicken

        if isinstance(b, Tree):
            if b.fade_destroy():
                self.play_sound(args.state)
                self.vibrate(args)
                args.state.score += SCORE_DESTROY_TREE
            return

        if isinstance(b, Skull):
            b.hurt(50)
            self.play_sound(args.state)
            self.vibrate(args)
            args.state.score += SCORE_KILL_SKULL
            return

        if isinstance(b, Chicken):
            b.hurt(100)
            self.play_sound(args.state)
            self.vibrate(args)
            args.state.score += SCORE_KILL_CHICKEN
            return

        args.state.noaction()

    def vibrate(self, args):
        if not args.state.settings.vibration:
            return

        for controller in args.controllers:
            controller.rumble_play_strong()

    def play_sound(self, state):
        sound_number = random.randint(1, 4)
        state.play_sound('chainsaw' + str(sound_number))

    def generate_rotated(self, image):
        rotated = super().generate_rotated(image)

        rotated[FACE_UP - 1] = image.copy().rotate(90, expand=True)
        rotated[FACE_DOWN - 1] = image.copy().rotate(270, expand=True)

        return rotated

    def copy(self):
        """ Copy item """
        return Chainsaw(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
