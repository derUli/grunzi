from datetime import date


def is_halloween() -> bool:
    """ Check if today is Halloween """

    today = date.today()
    return today.month == 10 and today.day == 31

def is_christmas() -> bool:
    today = date.today()

    return today.month == 12


def get_loading_screen_image_file() -> str:

    if is_halloween():
        return 'halloween.jpg'

    if is_christmas():
        return 'christmas.jpg'

    return 'default.jpg'