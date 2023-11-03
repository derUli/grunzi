import os
import json
from utils.path import get_userdata_path

DEFAULT_SAVE = 'default'

def load_game(name, state):
    save_dir = os.path.join(get_userdata_path(), 'savegames', name)
    state_file = os.path.join(save_dir, 'state.json')

    if not os.path.exists(state_file):
        return None

    with open(state_file, 'r') as f:
        state.from_json(f.read())

    level_file = os.path.join(save_dir, 'level.json')

    if not os.path.exists(level_file):
        return None

    return level_file


def has_savegame(name):
    save_dir = os.path.join(get_userdata_path(), 'savegames', name)
    state_file = os.path.join(save_dir, 'state.json')

    return os.path.exists(state_file)


def save_game(name, state, level=None):
    save_dir = os.path.join(get_userdata_path(), 'savegames', name)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    state_file = os.path.join(save_dir, 'state.json')

    with open(state_file, 'w') as f:
        f.write(state.to_json())

    if not level:
        return

    level_file = os.path.join(save_dir, 'level.json')

    with open(level_file, 'w') as f:
        f.write(json.dumps(level.to_saveable_list()))
