from timeit import timeit

import pandas
import pyximport

pyximport.install()

import _python.mmul_trivial
import _python.mmul_numpy
import _cython.mmul_trivial
import _cython.mmul_trivial_native
import _cython.mmul_numpy

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
        'name': 'Python',
        'type': 'Numpy',
        'exec': lambda: _python.mmul_numpy.run(size),
    },
    {
        'name': 'Cython',
        'type': 'Numpy',
        'exec': lambda: _cython.mmul_numpy.run(size),
    },
]

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def main():
    results = pandas.DataFrame(columns=['type', 'name', 'time'])
    for td in testing_data:
        time = timeit(stmt=td['exec'], number=10)
        results = results.append({
            'name': td['name'],
            'type': td['type'],
            'time': time,
        }, ignore_index=True)

    print(results)


if __name__ == '__main__':
    main()
