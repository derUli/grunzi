""" Online Highscore """

import json
import logging
from urllib.error import URLError
from urllib.request import urlopen


class HighscoreStorage:
    def __init__(self):
        """
        Constructor
        """
        self.url = 'https://grunzi.ulidots.de/highscore.php'
        self.highscore = [{
            'name': 'Timo Sofia',
            'score': 0
        }
        ]

    def fetch(self) -> bool:
        """
        Fetch online highscore

        @return: success
        """
        data = '[]'
        try:
            with urlopen(self.url, timeout=3) as f:
                data = f.read()

        except URLError as e:
            logging.error(e)

        try:
            self.highscore = json.loads(data)
            return True
        except json.decoder.JSONDecodeError as e:
            logging.error(e)
            return False

    def submit(self, name: str, score: int):
        """
        Submit highscore

        @param name: The player name
        @param score: The score

        @return: success
        """
        logging.error('Submit highscore is implemented yet')
        return False


HighscoreStorage().fetch()
