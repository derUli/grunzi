SETTINGS_LOW = 'low'
SETTINGS_MEDIUM = 'medium'
SETTINGS_HIGH = 'high'

SETTINGS_PRESETS = {
    SETTINGS_LOW: {
        'shaders': False,
        'traffic': False,
        'sky': False,
        'videos': False
    },
    SETTINGS_MEDIUM: {
        'shaders': False,
        'traffic': True,
        'sky': True,
        'videos': True
    },
    SETTINGS_HIGH: {
        'shaders': True,
        'traffic': True,
        'sky': True,
        'videos': True,
        'screen_resolution': True
    }
}