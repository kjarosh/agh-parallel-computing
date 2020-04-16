#include <iostream>
#include <upcxx/upcxx.hpp>

using namespace std;

int square(int a, int b) {
    cout << "Executing on " << upcxx::rank_me() << " process" << endl;
    return a * b;
}

int main(int argc, char *argv[]) {
    upcxx::init();
    int n = 1;
    cout << "Hello from process: " << upcxx::rank_me() << ". RPC on process: " << n << endl;
    upcxx::future<int> fut_result = upcxx::rpc(n, square, 2, 3);
    int result = fut_result.wait();
    cout << "Result: " << result << endl;
    upcxx::finalize();
    return 0;
}
