import random


def run(size):
    mx1 = [random.random() for _ in range(size)]
    mx2 = [random.random() for _ in range(size)]
    result = [0] * size * size

    for col in range(size):
        for row in range(size):
            result[col + size * row] = mx1[col] * mx2[row]

    return result
