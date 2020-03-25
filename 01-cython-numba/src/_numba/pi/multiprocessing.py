import random

from numba import jit
from numba import prange


@jit
def run(points, pool):
    result =  pool.apply_async(worker, (points,))
    result.wait()
    return result.get()

@jit
def worker(points):
    circle_points = 0
    for _ in prange(points):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if (x-1)**2 + (y-1)**2 < 1:
            circle_points += 1
    return 4 * circle_points / points