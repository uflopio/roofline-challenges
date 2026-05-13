import torch

def solution(input_image: torch.Tensor) -> torch.Tensor:
        """
        PyTorch implementation of simple edge detection using gradients.
        
        Args:
            input_image: Input grayscale image of shape (height, width)
            
        Returns:
            Edge detected image of shape (height, width)
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=input_image.dtype):
            h, w = input_image.shape
            
            gx_kernel = torch.tensor([[-1, 0, 1]], device=input_image.device) / 2.0
            gy_kernel = torch.tensor([[-1], [0], [1]], device=input_image.device) / 2.0
            
            input_reshaped = input_image.view(1, 1, h, w)
            gx_kernel = gx_kernel.view(1, 1, 1, 3)
            gy_kernel = gy_kernel.view(1, 1, 3, 1)
            
            gx = torch.nn.functional.conv2d(input_reshaped, gx_kernel, padding=(0, 1))
            gy = torch.nn.functional.conv2d(input_reshaped, gy_kernel, padding=(1, 0))
            
            magnitude = torch.sqrt(gx**2 + gy**2).squeeze()
            
            magnitude[0, :] = 0
            magnitude[-1, :] = 0
            magnitude[:, 0] = 0
            magnitude[:, -1] = 0
            
            if magnitude.max() > 0:
                magnitude = (magnitude / magnitude.max()) * 255.0
            
            return magnitude
