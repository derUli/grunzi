import os
import re
import time
import pygame
import utils.quality

def atoi(text):
    return int(text) if text.isdigit() else text.lower()


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split('(\d+)', text)]


IMAGE_EXTENSIONS = ['.jpg', '.png', '.gif']


class Animation():

    def __init__(self, animation_dir, refresh_interval=0.1,
                 start_frame=0, size=None, async_load=True):
        """ Constructor """

        self.current_frame = start_frame
        self.refresh_interval = refresh_interval
        self.files = []
        self.frames = []
        self.loaded = False
        self.last_refresh = time.time()
        self.size = size
        self.async_load = async_load
        self.load_chunks = 5

        files = sorted(os.listdir(animation_dir), key=natural_keys)

        for file in files:
            extension = os.path.splitext(file)[1]
            if extension.lower() in IMAGE_EXTENSIONS:
                fullpath = os.path.join(animation_dir, file)
                self.files.append(fullpath)

    def load(self):
        for file in self.files:
            frame = pygame.image.load(file).convert_alpha()

            if self.size:
                frame = utils.quality.scale_method()(
                    frame,
                    self.size
                )

            self.frames.append(frame)

            if self.async_load:
                self.files = self.files[1:]
                return

        self.loaded = True

    def get_frame(self):
        if not self.loaded:
            self.load()

        frame = self.frames[self.current_frame]

        if time.time() - self.last_refresh < self.refresh_interval:
            return frame

        next_frame = self.current_frame + 1

        if next_frame >= len(self.frames):
            next_frame = 0

        self.current_frame = next_frame
        self.last_refresh = time.time()

        return frame
