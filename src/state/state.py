import json

from state.playerstate import PlayerState

class State:
    def __init__(self, data_dir=None):
        """ Constructor """
        self.player_state = PlayerState(data_dir)
        self.level = 1

    def to_dict(self):
        """ To dictionary """
        return {
            "health": self.player_state.health
        }

    def to_json(self):
        """ To json """
        return json.dumps(self.to_dict())

    def from_dict(self, savegame):
        """ From dictionary """
        self.player_state.health = savegame['health']
        self.player_state.update_health()

    def from_json(self, data):
        """ To dictionary """
        savegame = json.loads(data)
        self.from_dict(savegame)
