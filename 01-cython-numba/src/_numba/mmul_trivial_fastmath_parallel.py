import random

from numba import njit, prange


@njit(parallel=True, fastmath=True)
def run(size):
    mx1 = [random.random() for _ in range(size)]
    mx2 = [random.random() for _ in range(size)]
    result = [[0] * size for _ in range(size)]

    for row in prange(size):
        result_row = result[row]
        for col in prange(size):
            result_row[col] = mx1[col] * mx2[row]

    return result
