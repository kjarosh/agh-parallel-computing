from timeit import timeit

import pandas
import pyximport

pyximport.install(language_level=3)

import _python.matrix.mmul_trivial
import _python.matrix.mmul_numpy
import _python.matrix.mmul2_numpy
import _cython.matrix.mmul_trivial
import _cython.matrix.mmul_trivial_native
import _cython.matrix.mmul_numpy
import _cython.matrix.mmul2_numpy
import _numba.matrix.mmul_numpy
import _numba.matrix.mmul_numpy_fastmath_parallel
import _numba.matrix.mmul_numpy_parallel
import _numba.matrix.mmul_trivial
import _numba.matrix.mmul_trivial_parallel
import _numba.matrix.mmul_trivial_fastmath_parallel
import _numba.matrix.mmul2_numpy
import _numba.matrix.mmul2_numpy_fastmath_parallel
import _numba.matrix.mmul2_numpy_parallel

size = 1000
testing_data = [
    {
        'name': 'Python',
        'type': 'Numpy vv',
        'exec': lambda: _python.matrix.mmul_numpy.run(size),
    },
    {
        'name': 'Cython',
        'type': 'Numpy vv',
        'exec': lambda: _cython.matrix.mmul_numpy.run(size),
    },
    {
        'name': 'Numba',
        'type': 'Numpy vv',
        'exec': lambda: _numba.matrix.mmul_numpy.run(size),
    },
    {
        'name': 'Numba Parallel',
        'type': 'Numpy vv',
        'exec': lambda: _numba.matrix.mmul_numpy_parallel.run(size),
    },
    {
        'name': 'Numba Fastmath Parallel',
        'type': 'Numpy vv',
        'exec': lambda: _numba.matrix.mmul_numpy_fastmath_parallel.run(size),
    },

    {
        'name': 'Python',
        'type': 'Trivial vv',
        'exec': lambda: _python.matrix.mmul_trivial.run(size),
    },
    {
        'name': 'Cython',
        'type': 'Trivial vv',
        'exec': lambda: _cython.matrix.mmul_trivial.run(size),
    },
    {
        'name': 'Cython Native',
        'type': 'Trivial vv',
        'exec': lambda: _cython.matrix.mmul_trivial_native.run(size),
    },
    {
        'name': 'Numba',
        'type': 'Trivial vv',
        'exec': lambda: _numba.matrix.mmul_trivial.run(size),
    },
    {
        'name': 'Numba Parallel',
        'type': 'Trivial vv',
        'exec': lambda: _numba.matrix.mmul_trivial_parallel.run(size),
    },
    {
        'name': 'Numba Fastmath Parallel',
        'type': 'Trivial vv',
        'exec': lambda: _numba.matrix.mmul_trivial_fastmath_parallel.run(size),
    },

    {
        'name': 'Numba',
        'type': 'Numpy mm',
        'exec': lambda: _numba.matrix.mmul2_numpy.run(size),
    },
    {
        'name': 'Numba Parallel',
        'type': 'Numpy mm',
        'exec': lambda: _numba.matrix.mmul2_numpy_parallel.run(size),
    },
    {
        'name': 'Numba Fastmath Parallel',
        'type': 'Numpy mm',
        'exec': lambda: _numba.matrix.mmul2_numpy_fastmath_parallel.run(size),
    },
    {
        'name': 'Cython',
        'type': 'Numpy mm',
        'exec': lambda: _cython.matrix.mmul2_numpy.run(size),
    },
    {
        'name': 'Python',
        'type': 'Numpy mm',
        'exec': lambda: _python.matrix.mmul2_numpy.run(size),
    },
]

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def main():
    results = pandas.DataFrame(columns=['type', 'name', 'time'])
    for td in testing_data:
        time = timeit(stmt=td['exec'], number=1000)
        row = {
            'name': td['name'],
            'type': td['type'],
            'time': time,
        }
        results = results.append(row, ignore_index=True)
        print(row)

    print(results)


if __name__ == '__main__':
    main()
