from components.state.playerstate import PlayerState


class State:

    def __init__(self, data_dir=None):
        self.player_state = PlayerState(data_dir)
        self.level = 1
