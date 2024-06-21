""" Other utility functions """

import re


def atoi(text: str) -> int | str:
    """
    If the string is numeric convert it to int
    @param text: Text
    @return: Int or string
    """

    return int(text) if text.isdigit() else text.lower()


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """

    return [atoi(c) for c in re.split(r"(\d+)", text)]
