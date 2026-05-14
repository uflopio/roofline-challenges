import torch

def solution(input_image: torch.Tensor, kernel_size: int) -> torch.Tensor:
        """
        PyTorch implementation of box blur.
        
        Args:
            input_image: Input grayscale image of shape (height, width)
            kernel_size: Size of the blur kernel (must be odd, e.g., 3, 5, 7)
            
        Returns:
            Blurred image of shape (height, width)
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=input_image.dtype):
            h, w = input_image.shape
            pad = kernel_size // 2
            
            padded = torch.nn.functional.pad(input_image, (pad, pad, pad, pad), mode='constant', value=0)
            input_reshaped = padded.view(1, 1, h + 2*pad, w + 2*pad)
            
            kernel = torch.ones(1, 1, kernel_size, kernel_size, device=input_image.device)
            
            y = torch.arange(h, device=input_image.device)
            x = torch.arange(w, device=input_image.device)
            yy, xx = torch.meshgrid(y, x, indexing='ij')
            
            i_start = torch.clamp(yy - pad, 0, h)
            i_end = torch.clamp(yy + pad + 1, 0, h) 
            j_start = torch.clamp(xx - pad, 0, w)
            j_end = torch.clamp(xx + pad + 1, 0, w)
            
            valid_elements = (i_end - i_start) * (j_end - j_start)
            
            output = torch.nn.functional.conv2d(input_reshaped, kernel).view(h, w)
            output = output / valid_elements
            
            return output
