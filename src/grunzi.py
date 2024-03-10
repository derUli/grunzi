#!/usr/bin/env python3

""" Starts the game """

import logging
import os
import sys

from views.startup import StartUp

def start() -> None:
    """ Starts the game """
    try:
        StartUp(os.path.dirname(__file__)).main()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        logging.fatal("Fatal exception", exc_info=e)
        sys.exit()


if __name__ == "__main__":
    start()
