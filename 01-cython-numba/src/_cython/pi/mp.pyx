import random


cdef _one_process(points):
    c_points = 0
    for p in range(points):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if (x - 1) ** 2 + (y - 1) ** 2 < 1:
            c_points += 1
    return c_points

def one_process(points):
    return _one_process(points)


cdef _run(points, pool):
    processes = pool._processes

    data = [points // processes for _ in range(processes)]
    circle_points = sum(pool.map(one_process, data))
    return 4 * circle_points / points

def run(points, pool):
    return _run(points, pool)
