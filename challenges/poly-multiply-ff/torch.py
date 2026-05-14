import torch

def solution(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
        """
        Naive O(n^2) convolution over Z_p. Works on CPU with Python ints, returns CUDA uint32.
        """
        MOD = P
        with torch.no_grad():
            A_cpu = A.detach().to("cpu").contiguous().view(-1).tolist()
            B_cpu = B.detach().to("cpu").contiguous().view(-1).tolist()
            n = len(A_cpu)
            assert n == len(B_cpu)

            # ensure [0, P) and Python-int arithmetic
            a = [int(x) % MOD for x in A_cpu]
            b = [int(x) % MOD for x in B_cpu]

            out_len = 2 * n - 1
            c = [0] * out_len
            for i in range(n):
                ai = a[i]
                for j in range(n):
                    c[i + j] = (c[i + j] + (ai * b[j]) % MOD) % MOD

            # Build on CPU as uint32, then move to CUDA
            c_tensor = torch.tensor(c, dtype=torch.uint32)
            return c_tensor.to("cuda")
