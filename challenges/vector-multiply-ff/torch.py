import torch

def solution(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
        """
        Element-wise multiplication modulo p for uint32 inputs.
        Returns uint32 on CUDA.
        """
        with torch.no_grad():
            # Promote to 64-bit to avoid overflow on the product, then reduce mod P.
            prod = (A.to(torch.int64) * B.to(torch.int64)) % P
            return prod.to(torch.uint32).to("cuda")
