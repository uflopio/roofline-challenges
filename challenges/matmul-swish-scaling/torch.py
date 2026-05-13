import torch

def solution(A: torch.Tensor, B: torch.Tensor, scale: float) -> torch.Tensor:
        """
        PyTorch implementation of matrix multiplication followed by Swish followed by scaling.
        
        Args:
            A: First input matrix
            B: Second input matrix
            scale: Scaling factor
            
        Returns:
            Result of scale * swish(A * B)
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=A.dtype):
            matmul_result = torch.matmul(A, B)
            swish_result = matmul_result * torch.sigmoid(matmul_result)
            scaled_result = scale * swish_result
            return scaled_result
