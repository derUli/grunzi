#!/usr/bin/env python3

""" Starts the game """

import os
import sys

from views.startup import StartUp


def start() -> None:
    """ Starts the game """

    frozen = getattr(sys, "frozen", False)
    if frozen:
        return start_frozen()

    return start_debug()


def start_frozen() -> None:
    """ Starts the game"""

    try:
        StartUp(os.path.dirname(__file__)).main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        import logging

        logging.critical("Fatal exception", exc_info=e)
        # messagebox.showerror('Error', repr(e))
        sys.exit(1)


def start_debug() -> None:
    """ Start without catching exceptions """

    try:
        StartUp(os.path.dirname(__file__)).main()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    start()
