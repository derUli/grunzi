import random

from arcade import FACE_DOWN, FACE_UP

from sprites.items.item import Item, Tree


class Chainsaw(Item):
    def on_use(self, b, state=None, handlers=None):
        from sprites.characters.skullsprite import SkullSprite
        from sprites.characters.chicken import Chicken


        if isinstance(b, Tree):
            b.fade_destroy()
            self.play_sound(state)
            return

        if isinstance(b, SkullSprite):
            b.hurt(50)
            self.play_sound(state)
            return

        if isinstance(b, Chicken):
            b.hurt(100)
            self.play_sound(state)
            return

        state.beep()

    def play_sound(self, state):
        sound_number = random.randint(1, 4)
        state.play_sound('chainsaw' + str(sound_number))

    def generate_rotated(self, image):
        rotated = super().generate_rotated(image)

        rotated[FACE_UP - 1] = image.copy().rotate(90, expand=True)

        rotated[FACE_DOWN - 1] = image.copy().rotate(270, expand=True)

        return rotated
