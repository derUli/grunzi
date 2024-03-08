""" Used to store save games """
import logging
import os

import jsonpickle

from constants.difficulty import DIFFICULTY_EASY
from constants.savegames import SAVEGAME_DEFAULT
from utils.path import get_savegame_path


class SaveGameState:
    def __init__(self):
        # Screen resolution
        self.completed = []
        self.current = None
        self.score = 0
        self.difficulty = DIFFICULTY_EASY
        self.version = 1

    @staticmethod
    def exists() -> bool:
        """
        Check if there is an existing savegame file
        @return: bool
        """
        return os.path.exists(get_savegame_path(SAVEGAME_DEFAULT))

    @staticmethod
    def load():
        try:
            return SaveGameState._load(SAVEGAME_DEFAULT)
        except ValueError as e:
            logging.error(e)
        except OSError as e:
            logging.error(e)
        except AttributeError as e:
            logging.error(e)

        return SaveGameState()

    @staticmethod
    def _load(name):
        with open(get_savegame_path(SAVEGAME_DEFAULT), 'r') as f:
            state = jsonpickle.decode(f.read())

            # jsonpickle don't calls __init__()
            # So when loading a state attributes added since then are missing
            # I added a version number
            # If the state version from the code is newer than the stored version
            # discard the old settings state and return a new one

            if SaveGameState().version > state.version:
                return SaveGameState()

            return state

    def save(self) -> None:
        """ Save settings as json file """
        with open(get_savegame_path(SAVEGAME_DEFAULT), 'w') as f:
            f.write(jsonpickle.encode(self, unpicklable=True))


def new_savegame(map):
    state = SaveGameState()
    state.current = map
    state.save()

    return state
