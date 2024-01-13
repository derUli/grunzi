""" Current task """

from typing import Union


class Task:
    def __init__(self, task_id: Union[str, None]):
        """
        @param task_id: Identifier of the task
        """
        self._task_id = task_id

    def get_id(self) -> Union[str, None]:
        """
        @return: task id
        """
        return self._task_id

    def set_id(self, task_id: Union[str, None]) -> None:
        """
        Set task id
        @param task_id: the task id
        """
        self._task_id = task_id

    def get_display_text(self) -> Union[str, None]:
        """
        @return: Display text for the current task
        """
        task = _('Keine Aufgabe')

        tasks = {
            'find_code': _('Find the code to deactivate the laser'),
            'horse': _('Give the horse blood'),
            'blast': _('Blast your way free')
        }

        if self._task_id in tasks:
            task = tasks[self._task_id]

        return task
