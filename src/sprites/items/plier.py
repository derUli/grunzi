import PIL
from arcade import FACE_DOWN

from sprites.items.item import Item, Fence


class Plier(Item):
    def on_use(self, b, state=None, handlers=None):
        if isinstance(b, Fence):
            if b.fade_destroy():
                state.play_sound('tools', 'plier')
            return

        state.beep()


    def generate_rotated(self, image):
        rotated = super().generate_rotated(image)

        rotated[FACE_DOWN - 1] = PIL.ImageOps.flip(image.copy())

        return rotated
