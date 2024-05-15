import json
import logging
from urllib.error import URLError
from urllib.request import urlopen
class HighscoreStorage:
    def __init__(self):
        self.url = 'https://grunzi.ulidots.de/highscore.php'
        self.highscore = []

    def fetch(self):
        data = '[]'

        try:
            with urlopen(self.url, timeout = 3) as f:
                data = f.read()

        except URLError as e:
            logging.error(e)

        try:
            self.highscore = json.loads(data)
            return True
        except json.decoder.JSONDecodeError as e:
            logging.error(e)
            return False

    def submit(self):
        logging.error('Submit highscore is not implemented')

HighscoreStorage().fetch()