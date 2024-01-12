""" Task display for pause menu """
from typing import Union


def get_task(name: Union[str, None] = None) -> Union[str, None]:
    """ Get the current task title """
    task = _('Keine Aufgabe')

    tasks = {
        "horse": _('Suche Blut für das Pferd')
    }

    if name in tasks:
        task = tasks[name]

    return task
