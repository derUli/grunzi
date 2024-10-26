import os

from PIL import Image
from PIL.Image import Resampling


class SpriteSheetReader:
    def __init__(self, filename):
        self.filename = filename
        self.images = []

    def process(self, size, autocrop=False, resize=None):
        self.images = []

        image = Image.open(self.filename).convert('RGBA').crop()

        full_w, full_h = image.size

        w, h = size

        y = 0

        while y < full_h:
            x = 0

            while x < full_w:
                img_area = (x, y, x + w, y + h)
                cropped = image.crop(img_area)

                if autocrop:
                    cropped = cropped.crop()

                print(cropped.size)

                if resize:
                    cropped = cropped.resize(
                        resize,
                        resample=Resampling.BILINEAR
                    )

                self.images.append(cropped)

                x += w

            y += h


# test = SpriteSheetReader(os.path.abspath('../data/images/sprites/char/pig/pig_walk_run.png'))
# test.process(size=(360, 194), resize=(63, 35))
