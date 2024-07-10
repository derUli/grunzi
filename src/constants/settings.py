# Graphics
DEFAULT_FULLSCREEN = True
DEFAULT_BORDERLESS = False
DEFAULT_VSYNC = True
DEFAULT_SHOW_FPS = False
DEFAULT_FILMGRAIN = 0.5
DEFAULT_FOG = True
DEFAULT_COLOR_TINT = True
DEFAULT_QUALITY = 4

# Sound
DEFAULT_MUSIC_VOLUME = 1.0
DEFAULT_SOUND_VOLUME = 1.0
DEFAULT_ATMO_VOLUME = 1.0

# Controllers
DEFAULT_VIBRATION = True

# Other
DEFAULT_MUTED = False
DEFAULT_FIRST_START = False
DEFAULT_ANTIALIASING = 4
UNLIMITED_FRAMERATE = 10000


class QualityPreset:
    def __init__(self, val: int):
        self.filmgrain = 0.0
        self.fog = False
        self.color_tint = False
        self.antialiasing = DEFAULT_ANTIALIASING
        self.set(val)

    def set(self, val: int) -> None:
        self.antialiasing = 0

        if val >= 1:
            self.antialiasing = 2

        if val >= 2:
            self.antialiasing = 4
            self.color_tint = True

        if val >= 3:
            self.fog = True

        if val >= 4:
            self.filmgrain = DEFAULT_FILMGRAIN

        if val >= 5:
            self.antialiasing = 8

        if val >= 6:
            self.antialiasing = 16
