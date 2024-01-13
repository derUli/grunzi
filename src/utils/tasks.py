""" Task display for pause menu """
from typing import Union


def get_task(name: Union[str, None] = None) -> Union[str, None]:
    """ Get the current task title """
    task = _('Keine Aufgabe')

    tasks = {
        'find_code': _('Find the code to deactivate the laser'),
        'horse': _('Give the horse blood'),
        'blast': _('Blast your way free')
    }

    if name in tasks:
        task = tasks[name]

    return task
