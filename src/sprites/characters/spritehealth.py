import logging

import arcade

HEALTH_FULL = 100.0
HEALTH_EMPTY = 0.0
HEALTHBAR_ENEMY_COLOR = arcade.csscolor.RED
HEALTHBAR_FREN_COLOR = arcade.csscolor.GREEN


class SpriteHealth:

    def __init__(self):
        self._health = HEALTH_FULL
        self._died = False

    def _dead(self):
        if self.health < HEALTH_EMPTY:
            self.health = HEALTH_EMPTY

        return self.health <= HEALTH_EMPTY

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value = value

    def hurt(self, damage):
        self.health -= damage

        return self.dead

    def on_die(self):
        logging.info(f"{self.__class__} is dead")

    @property
    def dead(self):
        if self._died:
            return True

        self._died = self._dead()

        if self._died:
            self.on_die()

        return self._died

    def draw_healthbar(self, color_health=HEALTHBAR_ENEMY_COLOR):
        one_percent = self.width / 100
        width = round(one_percent * self.health)
        height = 4

        left = self.left
        top = self.top + height * 2
        right = self.left + width

        alpha = self.alpha

        if alpha > 50:
            alpha = 50

        r, g, b, a = arcade.color.BLACK
        a = alpha

        arcade.draw_line(left, top, right, top, line_width=height, color=(r, g, b, a))

        if self.health < 1:
            return

        r, g, b, a = color_health
        arcade.draw_line(left, top, right, top, line_width=height, color=(r, g, b, a))
