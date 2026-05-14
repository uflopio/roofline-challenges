#include <cuda_runtime.h>

// ECC Point Negation (batched).
// For each (x_i, y_i) on the curve y^2 = x^3 + 7 (mod p), emit
// (x_i, (p - y_i) mod p). Inputs and outputs are 64-bit ints since
// p = 2^61 - 1 exceeds int32.
void solve(const long long *xs, const long long *ys, long long p, long long *out_xy, int n) {

}
