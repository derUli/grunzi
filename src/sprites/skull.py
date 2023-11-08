from datetime import datetime

from sprites.wall import Wall

DAY_HALLOWEEN = 31
MONTH_HALLOWEEN = 10


class Skull(Wall):
    def __init__(self, sprite_dir, cache, sprite='skull.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

    def draw(self, screen, x, y):
        """ Draw skull only on Helloween """
        day = datetime.now().day
        month = datetime.now().month

        day = 31
        month = 10

        if month != MONTH_HALLOWEEN and day != DAY_HALLOWEEN:
            self.walkable = True
            return

        self.walkable = False

        super().draw(screen, x, y)
