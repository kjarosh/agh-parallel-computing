import numpy as np


cdef _run(size):
    mx1 = np.random.rand(size, 1)
    mx2 = np.random.rand(1, size)
    return np.dot(mx1, mx2)


def run(size):
    _run(size)
