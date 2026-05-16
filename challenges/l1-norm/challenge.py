import numpy as np


def solve(X: np.ndarray, n: int, m: int):
    return np.sum(np.abs(X), axis=1)
