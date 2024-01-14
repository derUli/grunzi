import json
import os
import time
from typing import Union

from utils.path import get_userdata_path

SAVEGAME_DEFAULT = 'default'
SAVEGAME_AUTOSAVE = 'autosave'

SAVEGAMES = [
    SAVEGAME_DEFAULT,
    SAVEGAME_AUTOSAVE
]


def build_savegame_directory_path(name: str) -> str:
    return os.path.join(get_userdata_path(), 'savegames', name)


def build_savegame_state_path(name: str) -> str:
    return os.path.join(build_savegame_directory_path(name), 'state.json')


def build_savegame_level_path(name: str) -> str:
    return os.path.join(build_savegame_directory_path(name), 'level.json')


def get_savegames() -> list:
    savegames = []
    for name in SAVEGAMES:
        if has_savegame(name):
            savegames.append(build_savegame_state_path(name))

    savegames.sort(key=lambda f: os.path.getmtime(f), reverse=True)

    return savegames


def get_latest_savegame() -> Union[str, None]:
    savegames = get_savegames()
    if len(savegames) == 0:
        return None

    return os.path.basename(os.path.dirname(savegames[0]))


def load_game(name, state):
    print(get_savegames())
    state_file = build_savegame_state_path(name)
    savegame_file = build_savegame_level_path(name)

    if not os.path.exists(state_file):
        return None

    with open(state_file, 'r') as f:
        state.from_json(f.read())

    if not os.path.exists(savegame_file):
        return None

    with open(savegame_file, 'r') as f:
        return json.loads(f.read())

    return None


def has_savegame(name: str) -> bool:
    """ Check if a savegame exists """
    return os.path.exists(build_savegame_state_path(name))


def has_savegames() -> bool:
    for sav in SAVEGAMES:
        if has_savegame(sav):
            return True

    return False


def save_game(name: str, state, diff_list=None) -> None:
    save_dir = build_savegame_directory_path(name)

    if not diff_list:
        return

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    time_str = time.strftime("%Y-%m-%d-%H-%M-%S")

    state_files = [
        os.path.join(save_dir, 'state-' + time_str + '.json'),
        os.path.join(save_dir, 'state.json'),
    ]
    for state_file in state_files:
        with open(state_file, 'w') as f:
            f.write(state.to_json())

    level_files = [
        os.path.join(save_dir, 'level-' + time_str + '.json'),
        os.path.join(save_dir, 'level.json')
    ]
    for level_file in level_files:
        with open(level_file, 'w') as f:
            f.write(json.dumps(diff_list))
