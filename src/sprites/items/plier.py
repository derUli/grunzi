import PIL
from arcade import FACE_DOWN, FACE_RIGHT, FACE_LEFT

from sprites.items.fence import Fence
from sprites.items.item import Item

SCORE_DESTROY_FENCE = 100


class Plier(Item):
    def on_use_with(self, b, args):
        if isinstance(b, Fence):
            if b.fade_destroy():
                args.state.play_sound('tools', 'plier')
                args.state.score += SCORE_DESTROY_FENCE
            return

        args.state.noaction(args.player)

    def generate_rotated(self, image):
        rotated = super().generate_rotated(image)

        rotated[FACE_DOWN - 1] = PIL.ImageOps.flip(image.copy())
        rotated[FACE_LEFT - 1] = image.copy().rotate(90, expand=False)
        rotated[FACE_RIGHT - 1] = image.copy().rotate(270, expand=False)

        return rotated

    def copy(self):
        """ Copy item """
        return Plier(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
