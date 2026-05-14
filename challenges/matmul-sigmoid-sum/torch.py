import torch

def solution(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
        """
        PyTorch implementation of matrix multiplication followed by sigmoid followed by sum.
        
        Args:
            A: First input matrix
            B: Second input matrix
            
        Returns:
            Sum of sigmoid(A * B)
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=A.dtype):
            matmul_result = torch.matmul(A, B)
            sigmoid_result = torch.sigmoid(matmul_result)
            return torch.sum(sigmoid_result)
