// Harness for `vector-add`. Generates deterministic input, calls the
// user-provided `solve()`, times it on the GPU side, then validates the
// output against a CPU reference. Emits one RESULT line per run.
//
// Usage: `vector-add [N]`   (default N = 2^20)

#include <cuda_runtime.h>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstdint>

// User-provided host function (compiled together with this harness).
extern void solve(const float *a, const float *b, float *c, int n);

static void cuda_check(cudaError_t e, const char *file, int line) {
  if (e != cudaSuccess) {
    fprintf(stderr, "CUDA %s:%d: %s\n", file, line, cudaGetErrorString(e));
    std::exit(1);
  }
}
#define CK(e) cuda_check((e), __FILE__, __LINE__)

int main(int argc, char **argv) {
  const int N = argc > 1 ? std::atoi(argv[1]) : (1 << 20);

  // Host buffers + deterministic inputs.
  float *h_a = (float *)std::malloc(N * sizeof(float));
  float *h_b = (float *)std::malloc(N * sizeof(float));
  float *h_c = (float *)std::malloc(N * sizeof(float));
  float *h_ref = (float *)std::malloc(N * sizeof(float));

  uint32_t s = 0x9E3779B9u; // splitmix-ish seed
  auto rnd = [&](void) {
    s ^= s << 13;
    s ^= s >> 17;
    s ^= s << 5;
    return (float)((s & 0xFFFFFF) / 16777215.0);
  };
  for (int i = 0; i < N; i++) {
    h_a[i] = rnd();
    h_b[i] = rnd();
    h_ref[i] = h_a[i] + h_b[i];
  }

  // Device buffers + copy inputs over.
  float *d_a, *d_b, *d_c;
  CK(cudaMalloc(&d_a, N * sizeof(float)));
  CK(cudaMalloc(&d_b, N * sizeof(float)));
  CK(cudaMalloc(&d_c, N * sizeof(float)));
  CK(cudaMemcpy(d_a, h_a, N * sizeof(float), cudaMemcpyHostToDevice));
  CK(cudaMemcpy(d_b, h_b, N * sizeof(float), cudaMemcpyHostToDevice));

  // Warm up — pays off the first-launch JIT/cache cost so the timed run
  // measures steady-state performance.
  solve(d_a, d_b, d_c, N);
  CK(cudaDeviceSynchronize());

  // Timed run.
  cudaEvent_t t0, t1;
  CK(cudaEventCreate(&t0));
  CK(cudaEventCreate(&t1));
  CK(cudaEventRecord(t0));
  solve(d_a, d_b, d_c, N);
  CK(cudaEventRecord(t1));
  CK(cudaEventSynchronize(t1));
  float ms = 0;
  CK(cudaEventElapsedTime(&ms, t0, t1));

  CK(cudaMemcpy(h_c, d_c, N * sizeof(float), cudaMemcpyDeviceToHost));

  // Validate.
  int wrong = 0;
  for (int i = 0; i < N; i++) {
    if (std::fabs(h_c[i] - h_ref[i]) > 1e-5f) {
      if (wrong < 5)
        std::fprintf(stderr, "mismatch i=%d got=%f want=%f\n", i, h_c[i],
                     h_ref[i]);
      wrong++;
    }
  }

  if (wrong > 0) {
    std::printf("RESULT:wrong n=%d mismatches=%d\n", N, wrong);
  } else {
    // Microseconds, two decimals, so 0.42ms reads as 420 not 0.
    std::printf("RESULT:accepted n=%d t_us=%.2f\n", N, ms * 1000.0);
  }

  std::free(h_a);
  std::free(h_b);
  std::free(h_c);
  std::free(h_ref);
  cudaFree(d_a);
  cudaFree(d_b);
  cudaFree(d_c);
  return wrong > 0 ? 1 : 0;
}
