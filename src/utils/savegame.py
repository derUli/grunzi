import os

DEFAULT_SAVE = 'default'
QUICKSAVE = 'quicksave'

def load_game(data_dir, name, state):
    save_dir = os.path.join(data_dir, 'savegames', name)
    state_file = os.path.join(save_dir, 'state.json')

    if not os.path.exists(state_file):
        return False

    with open(state_file, 'r') as f: 
        state.from_json(f.read())
    
def save_game(data_dir, name, state):
    save_dir = os.path.join(data_dir, 'savegames', name)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    state_file = os.path.join(save_dir, 'state.json')

    with open(state_file, 'w') as f: 
        f.write(state.to_json())