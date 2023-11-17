import os


def get_version(file):
    text = 'Unknown Build'

    if not os.path.isfile(file):
        return text

    with open(file, 'r') as f:
        text = f.read()

    return text.strip()
