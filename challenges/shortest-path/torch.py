import torch

def solution(adj_matrix: torch.Tensor, source: int) -> torch.Tensor:
        """
        PyTorch implementation of single source shortest path.
        
        Args:
            adj_matrix: Weighted adjacency matrix (N x N) with integer weights
            source: Source node index
            
        Returns:
            Shortest distances from source to all nodes
        """
        with torch.no_grad(), torch.autocast("cuda", enabled=False, dtype=adj_matrix.dtype):
            N = adj_matrix.size(0)
            device = adj_matrix.device

            dist = torch.full((N,), float('inf'), device=device)
            dist[source] = 0.0

            u, v = torch.where(adj_matrix > 0)
            weights = adj_matrix[u, v]

            for i in range(N - 1):
                new_dist = dist[u] + weights
                dist.scatter_reduce_(0, v, new_dist, reduce='amin')

            dist = torch.where(torch.isinf(dist), -1.0, dist)
            return dist
