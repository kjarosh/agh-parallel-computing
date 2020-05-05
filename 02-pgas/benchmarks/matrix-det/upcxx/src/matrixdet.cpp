#include <iostream>
#include <upcxx/upcxx.hpp>
#include <cstdlib>
#include <ctime>
#include <math.h>
#include <chrono>

#define N 12

using namespace std;
using namespace std::chrono;

void print_matrix(double **matrix, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }
}

double **get_minor(double **a, int column, int size) {
    int n = size - 1;
    double **minor = new double*[n];
    for (int i = 0; i < n; i ++) {
        minor[i] = new double[n];
    }

    // copy array deleting selected column
    int k = 0;
    int l = 0;
    for (int i = 1; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (j != column) {
                minor[k][l] = a[i][j];
                l++;
            }
        }
        l = 0;
        k++;
    }

    return minor;
}

double calculate_det(double **matrix, int size) {
    if (size == 1) {
        return matrix[0][0];
    }
    double det = 0.0;
    for (int j = 0; j < size; j++) {
        double **minor = get_minor(matrix, j, size);
        det += matrix[0][j] * pow(-1, 1+j) * calculate_det(minor, size - 1);
        for(int i = 0; i < size - 1; ++i) {
            delete [] minor[i];
        }
        delete [] minor;
    }
    return det;
}

double run(double **matrix, int size) {
    int id = upcxx::rank_me();
    int proc_n = upcxx::rank_n();
    double sum = 0.0;
    for (int j = id; j < size; j += proc_n) {
        double **minor = get_minor(matrix, j, size);
        sum += matrix[0][j] * pow(-1, 1+j) * calculate_det(minor, size - 1);
    }
    return sum;
}

int main(int argc, char *argv[]) {
    auto start = high_resolution_clock::now();
    upcxx::init();
    srand(time(0));
    upcxx::dist_object<upcxx::global_ptr<double>> u_g(upcxx::new_array<double>(N*N));
    upcxx::dist_object<upcxx::global_ptr<double>> sum(upcxx::new_<double>(0));

    if (upcxx::rank_me() == 0) {
        double *u = u_g->local();
        for (int i = 0; i < N * N; i++) {
            u[i] = rand() / static_cast<double> (RAND_MAX);
            cout << u[i] << " ";
        }
    }
    upcxx::barrier();

    upcxx::global_ptr<double> u = u_g.fetch(0).wait();
    double **matrix = new double*[N];
    for (int i = 0; i < N; i ++) {
        matrix[i] = new double[N];
    }
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            matrix[i][j] = upcxx::rget(u + (i*N + j)).wait();
        }
    }
    double *local_sum = sum->local();
    *local_sum = run(matrix, N);
    upcxx::barrier();

    if (upcxx::rank_me() == 0) {
        int proc_n = upcxx::rank_n();
        for (int i = 1; i < proc_n; i++) {
            *local_sum += upcxx::rget(sum.fetch(i).wait()).wait();
        }
        cout << "\ndet: " << *local_sum << endl;
    }
    auto stop = high_resolution_clock::now();
    if (upcxx::rank_me() ==0 ){
        cout << "Time: " << duration_cast<seconds>(stop - start).count() << "s" << endl;
    }
    upcxx::finalize();
    return 0;
}
