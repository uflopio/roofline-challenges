import torch

def solution(input_image: torch.Tensor, num_bins: int) -> torch.Tensor:
        """
        PyTorch implementation of histogram computation.
        
        Args:
            input_image: Input grayscale image of shape (height, width)
            num_bins: Number of histogram bins (typically 256 for 8-bit images)
            
        Returns:
            Histogram array of shape (num_bins,) containing pixel counts
        """
        with torch.no_grad():
            clamped_input = torch.clamp(input_image, 0, num_bins - 1)
            indices = clamped_input.long().flatten()
            histogram = torch.bincount(indices, minlength=num_bins).float()
            return histogram
