def get_task(name=None):
    task = _('Keine Aufgabe')

    tasks = {
        "horse": _('Suche Blut für das Pferd')
    }

    if name in tasks:
        task = tasks[name]

    return task
