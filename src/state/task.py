""" Task display for pause menu """
from typing import Union


class Task:
    def __init__(self, task_id: Union[str, None]):
        self._task_id = task_id

    def get_task_id(self):
        return self._task_id

    def set_task_id(self, task_id: Union[str, None]):
        self._task_id = task_id

    def get_display_text(self):
        """ Get the current task title """
        task = _('Keine Aufgabe')

        tasks = {
            'find_code': _('Find the code to deactivate the laser'),
            'horse': _('Give the horse blood'),
            'blast': _('Blast your way free')
        }

        if self._task_id in tasks:
            task = tasks[self._task_id]

        return task

