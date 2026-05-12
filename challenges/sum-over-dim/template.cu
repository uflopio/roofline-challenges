#include <cuda_runtime.h>

// Row-wise sum: r[i] = sum_j A[i*n + j], for i in 0..m-1.
// A is row-major, shape M x N. r has length M.
void solve(const float *A, float *r, int m, int n) {

}
