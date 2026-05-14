import torch

def solution(adj_matrix: torch.Tensor) -> torch.Tensor:
        """
        PyTorch implementation of all-pairs shortest path using Floyd-Warshall.
        
        Args:
            adj_matrix: Weighted adjacency matrix (N x N) with positive weights
            
        Returns:
            Distance matrix with shortest paths between all pairs of nodes
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=adj_matrix.dtype):
            N = adj_matrix.size(0)
            device = adj_matrix.device

            dist = adj_matrix.clone().float()
            mask = (adj_matrix == 0) & (torch.eye(N, device=device, dtype=torch.bool) == False)
            dist[mask] = float('inf')
            
            torch.diagonal(dist).fill_(0.0)
            
            for k in range(N):
                dist_through_k = dist[:, k:k+1] + dist[k:k+1, :]
                dist = torch.minimum(dist, dist_through_k)
            
            dist = torch.where(torch.isinf(dist), -1.0, dist)
            
            return dist
