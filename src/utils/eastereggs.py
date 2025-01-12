from datetime import date


def is_halloween() -> bool:
    """ Check if today is Halloween """

    today = date.today()
    return today.month == 10 and today.day == 31


def is_christmas() -> bool:
    """ Check if the current day is christmas """

    today = date.today()

    return today.month == 12

def is_new_year() -> bool:
    """ Check if the current day is the first day of the year """

    today = date.today()

    return True

    return today.month == 1 and today.day == 1

def is_first_april() -> bool:
    """ Check if the current day is first april """

    today = date.today()

    return today.month == 4 and today.day == 1

def get_loading_screen_image_file() -> str:
    """ Get loading screen image file """

    if is_new_year():
        return 'new_year.jpg'

    if is_first_april():
        return 'fool.jpg'

    if is_halloween():
        return 'halloween.jpg'

    if is_christmas():
        return 'christmas.jpg'

    return 'default.jpg'
