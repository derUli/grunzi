from state.playerstate import PlayerState
import json


class State:

    def __init__(self, data_dir=None):
        self.player_state = PlayerState(data_dir)
        self.level = 1

    def to_json(self):
        data = {
            "health": self.player_state.health
        }

        return json.dumps(data)

    def from_dict(self, savegame):
        self.player_state.health = savegame['health']
        self.player_state.update_health()

    def from_json(self, data):
        savegame = json.loads(data)
        print(savegame)
        self.from_dict(savegame)
