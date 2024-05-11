""" Controller stuff """

# Joystick mappings

AXIS_X = 'x'
AXIS_Y = 'y'

# Mapping button codes of old Joystick API to controller API
JOYSTICK_BUTTON_MAPPING = {
    '9': 'start',
    '1': 'a',
    '2': 'b',
    '0': 'x',
    '3': 'y',
    '8': 'rightshoulder',  # "Select" to select next inventory item
    '4': 'leftstick'  # Left trigger to sprint
}


def joystick_button_to_controller(key) -> str | None:
    """ Map joystick button to controller"""
    button = str(key)
    if button in JOYSTICK_BUTTON_MAPPING:
        return JOYSTICK_BUTTON_MAPPING[button]

    return None
