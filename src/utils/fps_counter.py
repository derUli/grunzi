""" FPS Counter """

import time

class FPSCounter:
    """ Stores the FPS values to diplay the current framerate """

    def __init__(self):
        self.fps = None
        self.max_fps = None
        self.min_fps = None
        self.fps_avg = []
        self.last_fps_shown = int(time.time())

    def reset(self):
        """ Reset the fps counter """
        self.fps = None
        self.max_fps = None
        self.min_fps = None
        self.fps_avg = []
        self.last_fps_shown = int(time.time())

    def get_fps(self, clock):
        """ Get the current FPS """
        fps = int(clock.get_fps())

        if not self.fps:
            self.fps = fps
            self.fps_avg.append(self.fps)

        if not self.max_fps:
            self.max_fps = fps

        if not self.min_fps and fps > 0:
            self.min_fps = fps

        if fps > self.max_fps:
            self.max_fps = fps

        if self.min_fps is not None and fps < self.min_fps:
            self.min_fps = fps

        if int(time.time()) > self.last_fps_shown:
            self.last_fps_shown = int(time.time())
            self.fps = fps
            self.fps_avg.append(fps)
            print(len(self.fps_avg))

        return fps

    def avg_fps(self):
        """ Calculate the current FPS """
        return int(sum(self.fps_avg) / len(self.fps_avg))

    def get_fps_text(self):
        """ Get fps text for display """
        return str(self.fps) + ' (AVG: ' + str(self.avg_fps()) + ', MIN: ' + \
            str(self.min_fps) + ', MAX: ' + str(self.max_fps) + ')'
