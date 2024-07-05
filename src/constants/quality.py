class Quality:
    def __init__(self, val):
        self.filmgrain = 0.0
        self.fog = False
        self.color_tint = False
        self.antialiasing = 0

        self.set(val)

    def set(self, val):
        if val >= 1:
            self.antialiasing = 2

        if val >= 2:
            self.antialiasing = 4
            self.color_tint = True

        if val >= 3:
            self.fog = True

        if val >= 4:
            self.filmgrain = 0.7

        if val >= 5:
            self.antialiasing = 8

        if val >= 6:
            self.antialiasing = 16


QUALITY_PRESETS = []

for i in range(0, 7):
    QUALITY_PRESETS.append(Quality(i))
