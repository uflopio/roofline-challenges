#include <cuda_runtime.h>

// Row-wise argmax: k[i] = argmax_j A[i*n + j], for i in 0..m-1.
// Tiebreak by smaller index. A is row-major M x N, k has length M.
void solve(const float *A, int *k, int m, int n) {

}
