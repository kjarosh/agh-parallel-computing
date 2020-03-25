from timeit import timeit
from matplotlib import pyplot as plt

import pandas
import pyximport

pyximport.install(language_level=3)

import _numba.pi.seq
import _numba.pi.seq_fastmath
import _numba.pi.parallel
import _numba.pi.parallel_fastmath

size = 1000
testing_data = [
    {
        'name': 'Numba',
        'type': 'Seq',
        'exec': lambda: _numba.pi.seq.run(size),
    },
    {
        'name': 'Numba',
        'type': 'Seq Fastmath',
        'exec': lambda: _numba.pi.seq_fastmath.run(size),
    },
    {
        'name': 'Numba',
        'type': 'Parallel',
        'exec': lambda: _numba.pi.parallel.run(size),
    },
    {
        'name': 'Numba',
        'type': 'Parallel Fastmath',
        'exec': lambda: _numba.pi.parallel_fastmath.run(size),
    },
]

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def test():
    print("size: ", size)
    results = pandas.DataFrame(columns=['type', 'name', 'time'])
    for td in testing_data:
        time = timeit(stmt=td['exec'], number=1000)
        row = {
            'name': td['name'],
            'type': td['type'],
            'time': time,
        }
        results = results.append(row, ignore_index=True)

    print(results, '\n')
    return results


def plot_results(results, sizes):
    columns = [value[0] + ' ' + value[1] for value in results[0].values]
    data = [[value[2] for value in result.values] for result in results]
    df = pandas.DataFrame(data, index=sizes, columns=columns)
    df.plot(colormap='jet', marker='.', markersize=10,
            title='Computation time of Pi number depending on points number')
    plt.xlabel("points number")
    plt.ylabel("time [s]")
    plt.show()


def main():
    sizes = [1_000, 10_000, 100_000, 1_000_000]
    results = []
    for i in sizes:
        global size
        size = i
        results.append(test())
    plot_results(results, sizes)


if __name__ == '__main__':
    main()
