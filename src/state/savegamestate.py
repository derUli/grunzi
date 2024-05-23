""" Used to handle save games """

import logging
import os

import jsonpickle

from constants.mapconfig import DIFFICULTY_MEDIUM
from constants.maps import MAPS
from constants.savegames import SAVEGAME_DEFAULT
from utils.path import get_savegame_path
from utils.utils import natural_keys


class SaveGameState:
    def __init__(self):
        # Screen resolution
        self.completed = []
        self.current = None
        self.score = {}
        self.difficulty = DIFFICULTY_MEDIUM
        self.version = 2

    def get_selectable(self) -> list:
        """ Get selectable maps """

        selectable = self.completed
        for map in MAPS:
            if map not in self.completed:
                selectable.append(map)
                break

        return sorted(selectable, key=natural_keys)

    @staticmethod
    def exists() -> bool:
        """
        Check if there is an existing savegame file
        @return: bool
        """
        return os.path.exists(get_savegame_path(SAVEGAME_DEFAULT))

    @staticmethod
    def load():
        """
        Load savegame file
        @return: SavegameState
        """
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

            if SaveGameState().version != state.version:
                return SaveGameState()

        return state

    def save(self) -> None:
        """ Save settings as json file """
        with open(get_savegame_path(SAVEGAME_DEFAULT), 'w') as f:
            f.write(jsonpickle.encode(self, unpicklable=True))


def new_savegame(map, difficulty):
    state = SaveGameState()
    state.current = map
    state.difficulty = difficulty
    state.save()

    return state
