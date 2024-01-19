""" Dog character sprite """
from sprites.character import Character
from sprites.maincharacter import PIG_SOUND_NOTHING


class Wildpig(Character):
    """ Dog sprite class """

    def __init__(self, sprite_dir, cache, sprite='dog.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.sentence = 0
        self.sentences = [
            _('I am very wild.'),
            _('Can I haz pizza?'),
            _('I have not consumed a pink elephant.'),
            _('I deny the climate.'),
            _('Do you have pizza?')
        ]

    def handle_interact(self, element):
        if element.state.display_text.is_visible():
            return

        element.state.say(self.sentences[self.sentence])
        element.play_sound(PIG_SOUND_NOTHING)

        if self.sentence < len(self.sentences) - 1:
            self.sentence += 1
        else:
            self.sentence = 0


