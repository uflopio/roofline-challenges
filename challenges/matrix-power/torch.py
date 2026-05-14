import torch

def solution(matrix_a: torch.Tensor, n: int) -> torch.Tensor:
        """
        PyTorch implementation of matrix nth power.
        
        Args:
            matrix_a: Input matrix of shape (N, N)
            n: Power to raise the matrix to
            
        Returns:
            Result of matrix^n of shape (N, N)
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False):
            return torch.linalg.matrix_power(matrix_a, n)
