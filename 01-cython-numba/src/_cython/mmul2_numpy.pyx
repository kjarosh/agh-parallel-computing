import numpy as np


cdef _run(size):
    mx1 = np.random.rand(size, size)
    mx2 = np.random.rand(size, size)
    return np.dot(mx1, mx2)


def run(size):
    _run(size)
