""" String utils """

import re


def atoi(text: str) -> int:
    """
    Parses the string interpreting its content as an integral number,
    which is returned as a value of type int.

    @param text: The string
    @return: The integral value
    """
    return int(text) if text.isdigit() else text.lower()


def natural_keys(text: str) -> list:
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split('(\\d+)', text)]


def label_value(label: str, value: any) -> str:
    """
    @param label: label text
    @param value: value
    @return:
    """
    return ': '.join([label, str(value)])
