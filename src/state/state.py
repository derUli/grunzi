import json
import os

from state.playerstate import PlayerState
from state.task import Task
from utils.image import ImageCache
from utils.reflections import get_class


class State:
    def __init__(self, data_dir=None, gamepad=None):
        """ Constructor """
        self.cache = ImageCache()
        self.sprites_dir = os.path.join(data_dir, 'images', 'sprites')
        """ Constructor """
        self.player_state = PlayerState(data_dir, gamepad)
        self.level = 1
        self.edit_mode = False
        self.show_only_layer = None
        self.atmosphere = None
        self.task = Task(None)

    def to_dict(self):
        """ To dictionary """

        inventory = self.player_state.inventory
        if inventory:
            inventory = inventory.to_dict()

        savdict = {
            'health': self.player_state.health,
            'inventory': inventory,
            'level': self.level,
            'task': self.task.get_id()
        }

        if self.atmosphere:
            savdict = savdict | self.atmosphere.to_dict()

        return savdict

    def to_json(self):
        """ To json """
        return json.dumps(self.to_dict())

    def from_dict(self, savegame):
        """ From dictionary """

        self.player_state.health = savegame['health']
        self.player_state.update_health()
        self.player_state.inventory = None

        self.atmosphere.start(savegame)

        if 'level' in savegame and savegame['level']:
            self.level = savegame['level']

        if 'task' in savegame and savegame['task']:
            self.task.set_id(savegame['task'])

        if 'inventory' in savegame and savegame['inventory']:
            inventory = savegame['inventory']

            if 'sprite_file' in inventory:
                sprite_file = inventory['sprite_file']

            klass = get_class(inventory['sprite_class'])
            self.player_state.inventory = klass(
                self.sprites_dir, self.cache, sprite_file)

            if 'id' in inventory:
                self.player_state.inventory.id = inventory['id']

            if 'attributes' in inventory:
                self.player_state.inventory.attributes = inventory['attributes']

    def from_json(self, data):
        """ To dictionary """
        savegame = json.loads(data)
        self.from_dict(savegame)

    def update_task(self, task):
        self.task = task
