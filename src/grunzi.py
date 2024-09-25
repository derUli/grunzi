#!/usr/bin/env python3

""" Starts the game """

import os
import sys
import tkinter.messagebox as messagebox

from views.startup import StartUp


def start() -> None:
    """ Starts the game """

    frozen = getattr(sys, "frozen", False)
    if frozen:
        return start_frozen()

    return start_debug()


def start_frozen() -> None:
    try:
        StartUp(os.path.dirname(__file__)).main()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        import logging

        logging.critical("Fatal exception", exc_info=e)
        messagebox.showerror('Error', repr(e))
        sys.exit(1)


def start_debug() -> None:
    try:
        StartUp(os.path.dirname(__file__)).main()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    start()
