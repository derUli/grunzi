import json
import os
import time

from utils.path import get_userdata_path

DEFAULT_SAVE = 'default'


def load_game(name, state):
    save_dir = os.path.join(get_userdata_path(), 'savegames', name)
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


def has_savegame(name):
    """ Check if a savegame exists """
    save_dir = os.path.join(get_userdata_path(), 'savegames', name)
    state_file = os.path.join(save_dir, 'state.json')

    return os.path.exists(state_file)


def save_game(name, state, diff_list=None):
    save_dir = os.path.join(get_userdata_path(), 'savegames', name)

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
