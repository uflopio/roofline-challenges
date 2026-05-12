#include <cuda_runtime.h>

// Compute s = log(sum_{i,j} exp(A[i,j] - max)) + max, max = max over A.
// A is row-major M x N. `s` is a single-element output buffer.
// The max shift is required for numerical stability.
void solve(const float *A, float *s, int m, int n) {

}
