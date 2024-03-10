#!/usr/bin/env python3

import logging
import os
import sys

from views.startup import StartUp

ROOT_DIR = os.path.dirname(__file__)

if __name__ == "__main__":
    try:
        StartUp(ROOT_DIR).main()
    except KeyboardInterrupt as e:
        sys.exit()
    except Exception as e:
        logging.fatal("Fatal exception", exc_info=e)
        sys.exit()
