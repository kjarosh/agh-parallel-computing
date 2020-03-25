import random

from numba import njit
from numba import prange


@njit(parallel=True)
def run(points):
    circle_points = 0
    for _ in prange(points):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if (x-1)**2 + (y-1)**2 < 1:
            circle_points += 1
    return 4 * circle_points / points
