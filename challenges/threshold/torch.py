import torch

def solution(input_image: torch.Tensor, threshold_value: float) -> torch.Tensor:
        """
        PyTorch implementation of binary thresholding.
        
        Args:
            input_image: Input grayscale image of shape (height, width)
            threshold_value: Threshold value for binarization
            
        Returns:
            Binary image of shape (height, width) with values 0 or 255
        """
        with torch.no_grad():
            # Apply binary thresholding
            return torch.where(input_image > threshold_value, 
                              torch.tensor(255.0, device=input_image.device, dtype=input_image.dtype),
                              torch.tensor(0.0, device=input_image.device, dtype=input_image.dtype))
