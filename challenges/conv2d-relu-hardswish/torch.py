import torch

def solution(input_image: torch.Tensor, kernel: torch.Tensor) -> torch.Tensor:
        """
        PyTorch implementation of 2D convolution followed by ReLU followed by HardSwish.
        
        Args:
            input_image: Input image tensor of shape (H, W)
            kernel: Convolution kernel tensor of shape (Kh, Kw)
            
        Returns:
            Result of conv2d -> ReLU -> HardSwish fusion
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=input_image.dtype):
            input_reshaped = input_image.view(1, 1, input_image.size(0), input_image.size(1))
            kernel_reshaped = kernel.view(1, 1, kernel.size(0), kernel.size(1))
            
            padding_h = kernel.size(0) // 2
            padding_w = kernel.size(1) // 2
            
            conv_result = torch.nn.functional.conv2d(
                input_reshaped, 
                kernel_reshaped, 
                padding=(padding_h, padding_w)
            )
            
            conv_result = conv_result.view(input_image.size(0), input_image.size(1))
            relu_result = torch.nn.functional.relu(conv_result)            
            hardswish_result = relu_result * torch.nn.functional.relu6(relu_result + 3) / 6
            
            return hardswish_result
