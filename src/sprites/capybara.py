""" Frog character sprite """

from sprites.character import Character


class Capybara(Character):
    """ Frog sprite class """

    def __init__(self, sprite_dir, cache, sprite='capybara.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.next_quack = None
        self.sound = None
        self.h = None
        self.target_h = None
        self.next_target_h_update = 0
        self.h_min = None
        self.h_max = None
