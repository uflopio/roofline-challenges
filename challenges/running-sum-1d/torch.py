import torch

def solution(input_tensor: torch.Tensor, window_size: int) -> torch.Tensor:
        """
        PyTorch implementation of 1D running sum problem.
        
        Args:
            input_tensor: Input tensor
            window_size: Size of the sliding window
            
        Returns:
            Sums of the input tensor over the sliding window
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=input_tensor.dtype):
            
            # Perform 1D convolution using PyTorch's built-in function
            # using kernel of ones to compute the running sum
            input_reshaped = input_tensor.view(1, 1, -1)
            kernel = torch.ones(window_size, dtype=input_tensor.dtype, device=input_tensor.device)
            kernel_reshaped = kernel.view(1, 1, -1)
            
            # Calculate padding size to maintain the same output size
            padding = window_size // 2
            
            # Perform convolution
            result = torch.nn.functional.conv1d(
                input_reshaped, 
                kernel_reshaped, 
                padding=padding
            )
            
            # Reshape back to original dimensions
            return result.view(-1)
