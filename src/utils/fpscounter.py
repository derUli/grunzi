import time

import arcade
import numpy

FPS_UPDATE_INTERVAL = 1

class FPSCounter:
    def __init__(self):
        self.fps = []
        self.current_fps = -1
        self.last_fps_update = 0

    def reset(self):
        self.fps = []
        self.current_fps = None
        self.last_fps_update = 0
        self.current_fps = -1

    def update(self):
        fps = arcade.get_fps()

        self.fps.append(fps)

        if time.time() > self.last_fps_update + FPS_UPDATE_INTERVAL:
            self.last_fps_update = time.time()
            self.current_fps = int(fps)

    def avg(self, count: int | None = None):

        if count is None:
            return numpy.average(self.fps)

        return numpy.average(self.fps[-count:])
