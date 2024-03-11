""" Difficulty constants """

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3

MAX_SKULLS = {
    DIFFICULTY_EASY: 10,
    DIFFICULTY_MEDIUM: 15,
    DIFFICULTY_HARD: 20
}


class Difficulty:
    def __init__(self, difficulty):
        self.max_skulls = MAX_SKULLS[difficulty]
