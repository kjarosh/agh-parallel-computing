from multiprocessing.pool import Pool
from timeit import timeit

import sys
import pandas
import pyximport
import numba
from matplotlib import pyplot as plt

pyximport.install(language_level=3)

import _numba.pi.seq
import _numba.pi.seq_fastmath
import _numba.pi.parallel
import _numba.pi.parallel_fastmath
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


def test_sizes(sizes, plot):
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

    plot_results(results, sizes, 'Computation time of Pi number depending on points number', 'points', 'time [s]')


def test_sizes_threads(sizes, threads, plot):
    for i in sizes:
        global size
        size = i
        results = []
        for j in threads:
            print("threads: ", j)
            global processes
            processes = j
            numba.set_num_threads(min(j, numba.config.NUMBA_NUM_THREADS))
            file_name = "result-{}-{}.dat".format(i, j)

            if plot:
                r = pandas.read_csv(file_name, sep="\t")
            else:
                r = test()
                r.to_csv(file_name, sep="\t", index_label=False)
            results.append(r)
        plt_title = "Computation time of Pi number depending on threads number for {} points".format(i)
        plot_results(results, threads, plt_title, 'threads', 'time [s]')


def plot_results(results, index, title, xlabel, ylabel):
    columns = ['{} {}'.format(value[0], value[1]) for value in results[0].values]
    data = [[value[2] for value in result.values] for result in results]
    df = pandas.DataFrame(data, index=index, columns=columns)
    df.plot(colormap='jet', marker='.', markersize=10, title=title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.yscale('log')
    plt.show()


def main():
    plot = len(sys.argv) >= 2 and sys.argv[1] == 'plot'
    sizes = [100000, 200000, 300000, 400000, 500000, 600000]
    threads = [1, 2, 4, 8, 16]
    test_sizes(sizes, plot)
    test_sizes_threads(sizes, threads, plot)


if __name__ == '__main__':
    main()
