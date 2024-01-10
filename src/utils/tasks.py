def get_task(name = None):
    if name is None:
        return _('Keine Aufgabe')
        
    tasks = {
        "horse": _('Suche Blut für das Pferd')
    }