import os

from PIL import Image

class SpriteSheetAnimation:
    def __init__(self, filename):
        self.filename = filename


    def process(self, size):
        image = Image.open(self.filename).convert('RGBA').crop()

        full_w, full_h = image.size

        w, h = size

        x = 0
        y = 0

        while x < full_w:

            img_area = (x, y, x + w, y + h )
            cropped = image.crop(img_area)

            cropped.save('test_' + str(x) +'.png')

            x += w



test = SpriteSheetAnimation(os.path.abspath('../data/images/sprites/char/pig/pig_walk_run.png'))
test.process((360, 194))