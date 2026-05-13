import torch

def solution(input_array: torch.Tensor) -> torch.Tensor:
        """PyTorch implementation of array sorting on integers."""
        with torch.no_grad():
            sorted_array, _ = torch.sort(input_array)
            return sorted_array
