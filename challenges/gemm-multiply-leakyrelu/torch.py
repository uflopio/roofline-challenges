import torch

def solution(A: torch.Tensor, B: torch.Tensor, C: torch.Tensor, alpha: float) -> torch.Tensor:
        """
        PyTorch implementation of GEMM followed by element-wise multiplication followed by LeakyReLU.
                    
        Returns:
            Result of LeakyReLU(GEMM(A, B) * C)
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=A.dtype):
            gemm_result = torch.matmul(A, B)
            multiply_result = gemm_result * C
            leaky_relu_result = torch.nn.functional.leaky_relu(multiply_result, alpha)
            
            return leaky_relu_result
