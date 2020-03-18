from timeit import timeit

import pandas
import pyximport

pyximport.install()

import _python.mmul_trivial
import _python.mmul_numpy
import _cython.mmul_trivial
import _cython.mmul_trivial_native
import _cython.mmul_numpy
import _numba.mmul_numpy
import _numba.mmul_numpy_fastmath_parallel
import _numba.mmul_numpy_parallel
import _numba.mmul_trivial

size = 1000
testing_data = [
    {
        'name': 'Python',
        'type': 'Trivial',
        'exec': lambda: _python.mmul_trivial.run(size),
    },
    {
        'name': 'Cython',
        'type': 'Trivial',
        'exec': lambda: _cython.mmul_trivial.run(size),
    },
    {
        'name': 'Cython Native',
        'type': 'Trivial',
        'exec': lambda: _cython.mmul_trivial_native.run(size),
    },
    {
        'name': 'Numba',
        'type': 'Trivial',
        'exec': lambda: _numba.mmul_trivial.run(size),
    },
    {
        'name': 'Python',
        'type': 'Numpy',
        'exec': lambda: _python.mmul_numpy.run(size),
    },
    {
        'name': 'Cython',
        'type': 'Numpy',
        'exec': lambda: _cython.mmul_numpy.run(size),
    },
    {
        'name': 'Numba',
        'type': 'Numpy',
        'exec': lambda: _numba.mmul_numpy.run(size),
    },
    {
        'name': 'Numba Parallel',
        'type': 'Numpy',
        'exec': lambda: _numba.mmul_numpy_parallel.run(size),
    },
    {
        'name': 'Numba Fastmath Parallel',
        'type': 'Numpy',
        'exec': lambda: _numba.mmul_numpy_fastmath_parallel.run(size),
    },
]

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def main():
    results = pandas.DataFrame(columns=['type', 'name', 'time'])
    for td in testing_data:
        time = timeit(stmt=td['exec'], number=1000)
        results = results.append({
            'name': td['name'],
            'type': td['type'],
            'time': time,
        }, ignore_index=True)

    print(results)


if __name__ == '__main__':
    main()
