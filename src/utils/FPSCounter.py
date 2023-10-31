import time


class FPSCounter:

    def __init__(self):
        self.reset()

    def reset(self):
        self.fps = None
        self.max_fps = None
        self.min_fps = None
        self.fps_avg = []
        self.last_fps_shown = int(time.time())

    def get_fps(self, clock):
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

        return fps

    def get_fps(self, clock):
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

        return fps

    def avg_fps(self):
        return int(sum(self.fps_avg) / len(self.fps_avg))

    def get_fps_text(self):
        return str(self.fps) + ' (AVG: ' + str(self.avg_fps()) + ', MIN: ' + \
            str(self.min_fps) + ', MAX: ' + str(self.max_fps) + ')'
