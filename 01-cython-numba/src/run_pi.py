import sys
from multiprocessing.pool import Pool
from timeit import timeit

import numba
import pandas
import pyximport
from matplotlib import pyplot as plt
from pandas import DataFrame

pyximport.install(language_level=3)

import _numba.pi.seq
import _numba.pi.seq_fastmath
import _numba.pi.parallel
import _numba.pi.parallel_fastmath
import _numba.pi.mp
import _numba.pi.mp_fastmath
import _python.pi.seq
import _python.pi.mp
import _cython.pi.seq
import _cython.pi.seq_native
import _cython.pi.mp
import _cython.pi.mp_native

iterations = 100
size = 1000
pool = Pool(processes=8)


def set_processes(pc):
    global pool
    pool = Pool(processes=pc)
    numba.set_num_threads(min(pc, numba.config.NUMBA_NUM_THREADS))


testing_data = [
    {
        'name': 'Python',
        'type': 'Seq',
        'exec': lambda: _python.pi.seq.run(size),
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
        'type': 'MP',
        'exec': lambda: _numba.pi.mp.run(size, pool),
    },
    {
        'name': 'Numba',
        'type': 'MP Fastmath',
        'exec': lambda: _numba.pi.mp_fastmath.run(size, pool),
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
    {
        'name': 'Cython',
        'type': 'MP Native',
        'exec': lambda: _cython.pi.mp_native.run(size, pool),
    },
]

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def test(parallel_only=False):
    print("size:", size)
    results = DataFrame(columns=['type', 'name', 'time'])
    for td in testing_data:
        if parallel_only and 'Seq' in td['type']:
            continue

        if 'filter' in td and not td['filter'](size):
            time = None
        else:
            time = timeit(stmt=td['exec'], number=iterations)

        row = {
            'name': td['name'],
            'type': td['type'],
            'time': time,
        }
        results = results.append(row, ignore_index=True)

    print(results, '\n')
    return results


def test_sizes(sizes, plot):
    file_name = "result-sizes.dat"

    if plot:
        results = pandas.read_csv(file_name, sep="\t")
    else:
        results = DataFrame(columns=['type', 'name', 'time', 'size'])
        for i in sizes:
            global size
            size = i
            r = test()
            r['size'] = i
            results = pandas.concat([results, r], ignore_index=True)

        results['kind'] = results['type'].astype(str) + ' ' + results['name']
        results.to_csv(file_name, sep="\t", index=False)

    plot_results(results, 'size', 'Computation time of Pi number depending on points number', 'size', 'time [s]')


def test_threads(threads, plot):
    global size
    size = 1_000_000
    global iterations
    iterations = 50
    file_name = "result-threads.dat"

    if plot:
        results = pandas.read_csv(file_name, sep="\t")
    else:
        results = DataFrame(columns=['type', 'name', 'time', 'threads'])
        for j in threads:
            print("threads:", j)
            set_processes(j)
            r = test(True)
            r['threads'] = j
            results = pandas.concat([results, r], ignore_index=True)

        results['kind'] = results['type'].astype(str) + ' ' + results['name']

        # speedup
        seq_times = results[results['threads'] == 1]
        seq_times['base_time'] = seq_times['time']
        seq_times = seq_times.filter(['kind', 'base_time'])
        results = results.merge(seq_times, on='kind')
        results['speedup'] = results['base_time'].astype(float) / \
                             results['time'].astype(float)

        results.to_csv(file_name, sep="\t", index=False)

    plt_title = "Computation time of Pi number depending on threads number for {} points".format(size)
    plot_results(results, 'threads', plt_title, 'threads', 'time [s]')


def plot_results(results, index, title, xlabel, ylabel):
    results.set_index(index)
    results.groupby('kind')['time'].plot(legend=True, title=title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def main():
    plot = len(sys.argv) >= 2 and sys.argv[1] == 'plot'
    sizes = [100000, 200000, 300000, 400000, 500000, 600000]
    test_sizes(sizes, plot)
    threads = [1, 2, 3, 4, 5, 6, 7, 8]
    test_threads(threads, plot)


if __name__ == '__main__':
    main()
