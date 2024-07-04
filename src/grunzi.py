#!/usr/bin/env python3

""" Starts the game """

import logging
import os
import sys
import tkinter.messagebox as messagebox

from views.startup import StartUp


def start() -> None:
    """ Starts the game """

    try:
        StartUp(os.path.dirname(__file__)).main()
    except KeyboardInterrupt as e:
        sys.exit()
    except Exception as e:
        logging.critical("Fatal exception", exc_info=e)
        messagebox.showerror('Error', (str(e)))
        sys.exit()


if __name__ == "__main__":
    start()
