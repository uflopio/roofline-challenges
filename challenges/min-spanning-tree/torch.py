import torch

def solution(adj_matrix: torch.Tensor) -> torch.Tensor:
        """
        PyTorch implementation of minimum spanning tree using parallel Prim's algorithm.
        
        Args:
            adj_matrix: Weighted adjacency matrix (N x N) with positive integer weights
            
        Returns:
            Total weight of minimum spanning tree as a scalar tensor
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=adj_matrix.dtype):
            N = adj_matrix.size(0)
            device = adj_matrix.device
            
            if N <= 1:
                return torch.tensor(0.0, device=device)
            
            adj_float = adj_matrix.float()
            adj_float = torch.where(adj_float == 0, float('inf'), adj_float)
            
            in_mst = torch.zeros(N, device=device, dtype=torch.bool)
            min_edge_weight = torch.full((N,), float('inf'), device=device)
            
            in_mst[0] = True
            min_edge_weight = adj_float[0].clone() 
            min_edge_weight[0] = 0.0
            
            mst_weight = 0.0
            
            for _ in range(N - 1):
                masked_weights = torch.where(in_mst, float('inf'), min_edge_weight)
                
                min_idx = torch.argmin(masked_weights)
                min_weight = masked_weights[min_idx]
                
                if min_weight == float('inf'):
                    return torch.tensor(float('inf'), device=device)
                
                in_mst[min_idx] = True
                mst_weight += min_weight.item()
                
                new_distances = adj_float[min_idx]
                min_edge_weight = torch.minimum(min_edge_weight, new_distances)
            
            return torch.tensor(mst_weight, device=device)
