from sprites.wall import Wall
from datetime import datetime

MONTH_CHRISTMAS = 12
class Snowman(Wall):
    def draw(self, screen, x, y):
        """ Draw snowman only in december """
        month = datetime.now().month

        if month != MONTH_CHRISTMAS:
            self.walkable = True
            return

        self.walkable = False


        super().draw(screen, x, y)