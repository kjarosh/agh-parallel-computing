
cdef extern from *:
    """
    static double _run(int points) {
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
    double _run(int points)
    void _srand()

def run(points):
    return _run(points)

_srand()
