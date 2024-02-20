import logging
import os
from typing import Union

from orjson import orjson

from utils.audio import play_sound
from utils.path import get_userdata_path

ACHIEVEMENT_CODE_CRACKER = 'code_cracker'
ACHIEVEMENT_DEMOLITION_EXPERT = 'demolition_expert'
ACHIEVEMENT_CAT_SAWER = 'cat_sawer'


class Achievement:
    def __init__(self, achievement_id):
        self.achievement_id = achievement_id
        self.completed = False

    def to_dict(self):
        return {
            'id': self.achievement_id,
            'completed': self.completed,
        }

    def from_dict(self, dict):
        if 'id' in dict:
            self.achievement_id = dict['id']

        if 'completed' in dict:
            self.completed = dict['completed']

    def get_display_text(self) -> Union[str, None]:
        text = _('Unknown')
        achievements = {
            ACHIEVEMENT_CODE_CRACKER: _('Code cracker'),
            ACHIEVEMENT_DEMOLITION_EXPERT: _('Demolition Expert'),
            ACHIEVEMENT_CAT_SAWER: _('Cat sawer')
        }

        if self.achievement_id in achievements:
            text = achievements[self.achievement_id]

        return text


class AchievementsState:
    def __init__(self):
        self.achievements = get_achievements()

    def get_achievement_path(self):
        return os.path.join(get_userdata_path(), 'achievements.json')

    def load(self):
        if not os.path.exists(self.get_achievement_path()):
            self.save()
            return False

        with open(self.get_achievement_path(), 'r') as f:
            jsons = f.read()
            self.from_json(jsons)

        return True

    def save(self):
        with open(self.get_achievement_path(), 'w') as f:
            f.write(self.to_json())

    def from_json(self, data):
        """ To dictionary """
        state = orjson.loads(data)
        self.from_dict(state)

    def from_dict(self, dict):
        for key in dict:
            achievement = Achievement(key)
            achievement.from_dict(dict[key])
            self.achievements[key] = achievement

    def to_dict(self):
        dict = {}
        for key in self.achievements:
            dict[key] = self.achievements[key].to_dict()

        return dict

    def to_json(self):
        """ To JSON """
        return orjson.dumps(self.to_dict()).decode('utf-8')


def get_achievements():
    return {
        ACHIEVEMENT_CODE_CRACKER: Achievement(ACHIEVEMENT_CODE_CRACKER),
        ACHIEVEMENT_DEMOLITION_EXPERT: Achievement(ACHIEVEMENT_DEMOLITION_EXPERT),
        ACHIEVEMENT_CAT_SAWER: Achievement(ACHIEVEMENT_CAT_SAWER)
    }


def add_achievement(name, data_dir=None):
    state = AchievementsState()
    state.load()

    if state.achievements[name].completed:
        return False

    state.achievements[name].completed = True
    state.save()

    if data_dir:
        play_sound(os.path.join(data_dir, 'sounds', 'common', 'achievement.ogg'))

    logging.info(f'Added achievement {name}')

    return True
