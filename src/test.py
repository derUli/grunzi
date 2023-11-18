import time
import timeit


def join1():
    return "foo " + str(time.time()) + " bar"


def join2():
    " ".join(['foo', str(time.time()), 'bar'])


print(timeit.timeit('join1()', setup='from __main__ import join1'))
print(timeit.timeit('join2()', setup='from __main__ import join2'))
