import numpy as np


def solve(X: np.ndarray, n: int, m: int):
    return np.linalg.norm(X, ord=2, axis=1)
