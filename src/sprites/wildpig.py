""" Dog character sprite """
from sprites.character import Character
from sprites.maincharacter import PIG_SOUND_NOTHING


class Wildpig(Character):
    """ Dog sprite class """

    def __init__(self, sprite_dir, cache, sprite='dog.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

    def handle_interact(self, element):
        element.state.say(_('I am very wild.'))
        element.play_sound(PIG_SOUND_NOTHING)
