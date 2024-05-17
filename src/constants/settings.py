SETTINGS_LOW = 'low'
SETTINGS_MEDIUM = 'medium'
SETTINGS_HIGH = 'high'

SETTINGS_ALL = {
    SETTINGS_LOW,
    SETTINGS_MEDIUM,
    SETTINGS_HIGH
}

SETTINGS_PRESETS = {
    SETTINGS_LOW: {
        'shaders': False,
        'traffic': False,
        'sky': False,
        'videos': False,
        'antialiasing': 0
    },
    SETTINGS_MEDIUM: {
        'shaders': False,
        'traffic': True,
        'sky': True,
        'videos': True,
        'antialiasing': 4
    },
    SETTINGS_HIGH: {
        'shaders': True,
        'traffic': True,
        'sky': True,
        'videos': True,
        'screen_resolution': True,
        'antialiasing': 16
    }
}
