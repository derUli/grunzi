from datetime import date


def is_halloween() -> bool:
    """ Check if today is Halloween """

    today = date.today()
    return today.month == 10 and today.day == 31