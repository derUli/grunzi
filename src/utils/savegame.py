import os
from utils.path import get_userdata_path

DEFAULT_SAVE = 'default'
QUICKSAVE = 'quicksave'


def load_game(name, state):
    save_dir = os.path.join(get_userdata_path(), 'savegames', name)
    state_file = os.path.join(save_dir, 'state.json')

    if not os.path.exists(state_file):
        return False

    with open(state_file, 'r') as f:
        state.from_json(f.read())
        return True


def has_savegame(name):
    save_dir = os.path.join(get_userdata_path(), 'savegames', name)
    state_file = os.path.join(save_dir, 'state.json')

    return os.path.exists(state_file)


def save_game(name, state):
    save_dir = os.path.join(get_userdata_path(), 'savegames', name)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    state_file = os.path.join(save_dir, 'state.json')

    with open(state_file, 'w') as f:
        f.write(state.to_json())
