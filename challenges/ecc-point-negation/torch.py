import torch

def solution(xs: torch.Tensor, ys: torch.Tensor, p: int) -> torch.Tensor:
        with torch.no_grad():
            assert xs.shape == ys.shape
            assert xs.dtype == torch.int64 and ys.dtype == torch.int64
            device = xs.device
            p64 = torch.tensor(p, dtype=torch.int64, device=device)

            assert xs.dtype == torch.int64 and ys.dtype == torch.int64
            assert xs.device.type == "cuda" and ys.device.type == "cuda"

            neg_y = (p64 - (ys % p64)) % p64
            out = torch.stack((xs, neg_y), dim=1)
            return out
