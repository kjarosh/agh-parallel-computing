from numba import njit
import numpy as np


@njit(parallel=True)
def run(size):
    mx1 = np.random.rand(size, 1)
    mx2 = np.random.rand(1, size)
    return np.dot(mx1, mx2)
