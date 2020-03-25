from multiprocessing.pool import Pool
from timeit import timeit

import sys
import pandas
import pyximport
from matplotlib import pyplot as plt

pyximport.install(language_level=3)

import _numba.pi.seq
import _numba.pi.seq_fastmath
import _numba.pi.parallel
import _numba.pi.parallel_fastmath
import _numba.pi.multiprocessing
import _python.pi.seq
import _python.pi.mp
import _cython.pi.seq
import _cython.pi.seq_native
import _cython.pi.mp

size = 1000
processes = 8
pool = Pool(processes=processes)
testing_data = [
    {
        'name': 'Python',
        'type': 'Seq',
        'exec': lambda: _python.pi.seq.run(size),
        'filter': lambda s: s <= 100000,
    },
    {
        'name': 'Python',
        'type': 'MP',
        'exec': lambda: _python.pi.mp.run(size, pool),
    },

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
        'type': 'Multiprocessing',
        'exec': lambda: _numba.pi.multiprocessing.run(size, pool),
    },
    {
        'name': 'Numba',
        'type': 'Parallel Fastmath',
        'exec': lambda: _numba.pi.parallel_fastmath.run(size),
    },

    {
        'name': 'Cython',
        'type': 'Seq',
        'exec': lambda: _cython.pi.seq.run(size),
        'filter': lambda s: s <= 100000,
    },
    {
        'name': 'Cython',
        'type': 'Seq Native',
        'exec': lambda: _cython.pi.seq_native.run(size),
    },
    {
        'name': 'Cython',
        'type': 'MP',
        'exec': lambda: _cython.pi.mp.run(size, pool),
    },
]

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def test():
    print("size:", size)
    results = pandas.DataFrame(columns=['type', 'name', 'time'])
    for td in testing_data:
        if 'filter' in td and not td['filter'](size):
            time = None
        else:
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
    columns = ['{} {}'.format(value[0], value[1]) for value in results[0].values]
    data = [[value[2] for value in result.values] for result in results]
    df = pandas.DataFrame(data, index=sizes, columns=columns)
    df.plot(colormap='jet', marker='.', markersize=10,
            title='Computation time of Pi number depending on points number')
    plt.xlabel("points number")
    plt.ylabel("time [s]")
    plt.yscale('log')
    plt.show()


def main():
    plot = len(sys.argv) >= 2 and sys.argv[1] == 'plot'
    sizes = [10000, 20000, 30000, 40000, 50000, 60000]
    results = []
    for i in sizes:
        global size
        size = i
        file_name = "result-{}.dat".format(i)

        if plot:
            r = pandas.read_csv(file_name, sep="\t")
        else:
            r = test()
            r.to_csv(file_name, sep="\t", index_label=False)

        results.append(r)

    plot_results(results, sizes)


if __name__ == '__main__':
    main()
