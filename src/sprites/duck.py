""" Duck character sprite """

from sprites.character import Character


class Duck(Character):
    """ Duck sprite class """

    def __init__(self, sprite_dir, cache, sprite='duck.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
