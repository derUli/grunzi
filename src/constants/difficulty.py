""" Difficulty constants """

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3

MAX_SKULLS = {
    DIFFICULTY_EASY: 10,
    DIFFICULTY_MEDIUM: 15,
    DIFFICULTY_HARD: 20
}

SKULL_SPAWN_RANGE = {
    DIFFICULTY_EASY: (0, 100),
    DIFFICULTY_MEDIUM: (0, 80),
    DIFFICULTY_HARD: (0, 60)
}

SKULL_HURT = {
    DIFFICULTY_EASY: 10,
    DIFFICULTY_MEDIUM: 20,
    DIFFICULTY_HARD: 30
}


class Difficulty:
    def __init__(self, difficulty):
        self.max_skulls = MAX_SKULLS[difficulty]
        self.skull_spawn_range = SKULL_SPAWN_RANGE[difficulty]
        self.skull_hurt = SKULL_HURT[difficulty]
