#include <iostream>
#include <random>
#include <upcxx/upcxx.hpp>

#define N (1024 * 45 * 8)
#define MAX_VAL 100
#define EPS 0.1
#define MAX_ITER ( (long) N * N * 2 )
#define EXPECTED_VAL ( MAX_VAL / 2 )

using namespace std;

bool check_convergence(double *, long, double, double, long);

int main(int argc, char *argv[]) {
    upcxx::init();

    long block = N / upcxx::rank_n();
    assert(block % 2 == 0);
    assert(N == block * upcxx::rank_n());
    long n_local = block + 2;

    upcxx::dist_object<upcxx::global_ptr<double>> u_g(upcxx::new_array<double>(n_local));
    double *u = u_g->local();

    mt19937_64 rgen(1);
    rgen.discard(upcxx::rank_me() * block);
    for (long i = 1; i < n_local - 1; i++)
        u[i] = 0.5 + rgen() % MAX_VAL;

    // fetch the left and right pointers for the ghost cells
    int l_nbr = (upcxx::rank_me() + upcxx::rank_n() - 1) % upcxx::rank_n();
    int r_nbr = (upcxx::rank_me() + 1) % upcxx::rank_n();
    upcxx::global_ptr<double> uL = u_g.fetch(l_nbr).wait();
    upcxx::global_ptr<double> uR = u_g.fetch(r_nbr).wait();
    upcxx::barrier();

    for (long stepi = 0; stepi < MAX_ITER; stepi++) {
        if (stepi % 1000 == 0 && upcxx::rank_me() == 0) {
            cout << "iteration " << stepi << endl;
        }
        // alternate between red and black
        int phase = stepi % 2;
        // get the values for the ghost cells
        if (!phase) u[0] = upcxx::rget(uL + block).wait();
        else u[n_local - 1] = upcxx::rget(uR + 1).wait();
        // compute updates and error
        for (long i = phase + 1; i < n_local - 1; i += 2)
            u[i] = (u[i - 1] + u[i + 1]) / 2.0;
        // wait until all processes have finished calculations
        upcxx::barrier();
        // periodically check convergence
        if (stepi % 200 == 0) {
            if (check_convergence(u, n_local, EXPECTED_VAL, EPS, stepi))
                break;
        }
    }

    upcxx::finalize();
    return 0;
}

bool check_convergence(
        double *u,
        long n_local,
        const double expected_val,
        const double eps,
        long stepi) {
    double err = 0;
    for (long i = 1; i < n_local - 1; i++)
        err = max(err, fabs(EXPECTED_VAL - u[i]));
    double max_err = upcxx::reduce_all(err, upcxx::op_fast_max).wait();
    if (max_err / EXPECTED_VAL <= EPS) {
        if (!upcxx::rank_me())
            cout << "Converged at " << stepi << ", err " << max_err << ", eps " << max_err / EXPECTED_VAL << endl;
        return true;
    }
    return false;
}
