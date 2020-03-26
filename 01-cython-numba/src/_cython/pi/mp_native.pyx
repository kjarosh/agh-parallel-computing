cdef extern from *:
    """
    static double _one_process(int points) {
        int circle_points = 0;

        for (int i = 0; i < points; ++i) {
            double x = (double) rand() / RAND_MAX;
            double y = (double) rand() / RAND_MAX;

            if ((x - 1) * (x - 1) + (y - 1) * (y - 1) < 1) {
                ++circle_points;
            }
        }

        return 4.d * circle_points / points;
    }

    static void _srand(void) {
        srand(time(NULL));
    }
    """
    double _one_process(int points)
    void _srand()

_srand()

def one_process(points):
    return _one_process(points)

cdef _run(points, pool):
    processes = pool._processes

    data = [points // processes for _ in range(processes)]
    circle_points = sum(pool.map(one_process, data))
    return 4 * circle_points / points

def run(points, pool):
    return _run(points, pool)
