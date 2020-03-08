from libc.stdlib cimport malloc, free

cdef extern from *:
    """
    #pragma GCC push_options
    #pragma GCC optimize ("O0")
    static void _run(int size, float *result) {
        srand(time(NULL));
        float *mx1, *mx2;
        mx1 = malloc(sizeof(float) * size);
        mx2 = malloc(sizeof(float) * size);

        for (int i = 0; i < size; ++i) {
            mx1[i] = rand();
            mx2[i] = rand();
        }

        for (int row = 0; row < size; ++row) {
            for (int col = 0; col < size; ++col) {
                result[row + size * col] = mx1[row] * mx2[col];
            }
        }

        free(mx1);
        free(mx2);
    }
    #pragma GCC pop_options
    """
    void _run(int size, float *result)

def run(size):
    cdef float *result = <float *> malloc(sizeof(float) * size * size)
    try:
        _run(size, result)
    finally:
        free(result)
