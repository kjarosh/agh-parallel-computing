#include <iostream>
#include <stdlib.h>
#include <ctime>
#include <upcxx/upcxx.hpp>

using namespace std;


double fRand(double fMin, double fMax)
{
    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}

void fillArray(char *seed, double *a, int size){
	srand(atoi(seed));
	
	for(int i=0; i<size*size; i++){
		a[i] = fRand(0.0, 100000.0);
	}
}


double singleMul(double *a1, double *a2, int x, int y, int size){
	double res = 0.0;

	for(int i=0; i<size; i++){
		res += a2[i*size+y] * a1[x*size+i];
	}

	return res;
}

void matMulRange(double *a1, double *a2, upcxx::global_ptr<double> res, int size, int start, int end){
	for(int i=start; i<=end; i++){
		int x = i%size;
		int y = i/size;

		// res[y*size+x] = singleMul(a1, a2, x, y, size);
		upcxx::rput(singleMul(a1, a2, x, y, size), res + y*size+x);
		// ary[x][y] == ary[x*size+y]
	}
}


void printMatrix(double *a, int size){
	for(int i=0; i<size; i++){
		for(int j=0; j<size; j++){
			cout << a[i*size+j] << " ";
		}
		cout << endl;
	}
}



int main(int argc, char *argv[]){
	char* seed = argv[1];
	int size = atoi(argv[2]);	

	double elapsed_secs = 0;
	

	// start
	clock_t begin = clock();

	// setup UPC++ runtime
	upcxx::init();

	upcxx::dist_object<upcxx::global_ptr<double>> a1(upcxx::new_array<double>(size*size));
	upcxx::dist_object<upcxx::global_ptr<double>> a2(upcxx::new_array<double>(size*size));
	upcxx::dist_object<upcxx::global_ptr<double>> res(upcxx::new_array<double>(size*size));

	double *a1_l = a1->local();
	double *a2_l = a2->local();

	if(upcxx::rank_me() == 0){
		fillArray(seed, a1_l, size);
		fillArray(seed, a2_l, size);

		// printMatrix(a1->local(), size); //dbg
	}
	
	upcxx::barrier();

	upcxx::global_ptr<double> a1_p = a1.fetch(0).wait();
	upcxx::global_ptr<double> a2_p = a2.fetch(0).wait();
	upcxx::global_ptr<double> res_p = res.fetch(0).wait();

	if(upcxx::rank_me() != 0){
		for(int i=0; i<size*size; i++){
			a1_l[i] = upcxx::rget(a1_p + i).wait();
			a2_l[i] = upcxx::rget(a2_p + i).wait();
		}
	}

	upcxx::barrier();


	//split into chunks
	int bsize = (size*size)/upcxx::rank_n();
	int start_id = bsize*upcxx::rank_me();
	int end_id = start_id + bsize - 1;

	// cout << "bsize " << bsize << " start_id " << start_id << " end_id " << end_id << endl; //dbg

	if(upcxx::rank_me() == upcxx::rank_n()){
		end_id = (size*size)-1;
	}

	matMulRange(a1_l, a2_l, res_p, size, start_id, end_id);

	upcxx::barrier();
	//stop
	clock_t end = clock();
	elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;

	if(upcxx::rank_me() == 0){
		cout << elapsed_secs << "s" << endl;

		// double *res_l = res->local();
		// printMatrix(res_l, size); //dbg
	}

	// close down UPC++ runtime
	upcxx::finalize();
	return 0;
}