import os

import pandas

result_dir = '../report/results'


def prepare_sizes():
    sizes = pandas.read_csv('result-sizes.dat', sep="\t")

    for kind in set(sizes['kind']):
        sizes_kind = sizes[sizes['kind'] == kind]
        sizes_kind = sizes_kind.filter(['time', 'size'])

        file = result_dir + '/sizes-{}.dat'.format(kind.replace(' ', '_').lower())
        sizes_kind.to_csv(file, sep="\t", index=False)


def prepare_threads():
    threads = pandas.read_csv('result-threads.dat', sep="\t")

    for kind in set(threads['kind']):
        threads_kind = threads[threads['kind'] == kind]
        threads_kind = threads_kind.filter(['time', 'threads', 'speedup'])

        file = result_dir + '/threads-{}.dat'.format(kind.replace(' ', '_').lower())
        threads_kind.to_csv(file, sep="\t", index=False)


def main():
    os.makedirs(result_dir, exist_ok=True)
    prepare_sizes()
    prepare_threads()


if __name__ == '__main__':
    main()
