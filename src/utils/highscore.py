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
        self.url = 'https://grunzi.ulidots.de/'
        self.highscore = []

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

        url = f"{self.url}?name={name}&score={score}"

        try:
            with urlopen(url, timeout=3) as f:
                f.read()
                return True

        except URLError as e:
            logging.error(e)
            return False


HighscoreStorage().fetch()
