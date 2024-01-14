import json
import os
import time

from utils.path import get_userdata_path

SAVEGAME_DEFAULT = 'default'
SAVEGAME_AUTOSAVE = 'autosave'


def build_savegame_directory_path(name: str) -> str:
    return os.path.join(get_userdata_path(), 'savegames', name)

def build_savegame_state_path(name: str) -> str:
    return os.path.join(build_savegame_directory_path(name), 'state.json')

def load_game(name, state):
    save_dir = build_savegame_directory_path(name)
    state_file = os.path.join(save_dir, 'state.json')

    if not os.path.exists(state_file):
        return None

    with open(state_file, 'r') as f:
        state.from_json(f.read())

    savegame = os.path.join(save_dir, 'level.json')

    if not os.path.exists(savegame):
        return None

    with open(savegame, 'r') as f:
        return json.loads(f.read())

    return None


def has_savegame(name: str) -> bool:
    """ Check if a savegame exists """
    return os.path.exists(build_savegame_state_path(name))


def has_savegames() -> bool:
    savegames = [
        SAVEGAME_DEFAULT,
        SAVEGAME_AUTOSAVE
    ]

    for sav in savegames:
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
