import re


def atoi(text):
    return int(text) if text.isdigit() else text.lower()


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split('(\\d+)', text)]


def label_value(label, value):
    return ': '.join([label, str(value)])
