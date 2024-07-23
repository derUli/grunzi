#!/usr/bin/env python3

""" Starts the game """

import logging
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
        sys.exit()
    except Exception as e:
        logging.critical("Fatal exception", exc_info=e)
        messagebox.showerror('Error', (repr(e)))
        sys.exit()


def start_debug() -> None:
    try:
        StartUp(os.path.dirname(__file__)).main()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    start()
