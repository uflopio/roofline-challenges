import numpy as np


def solve(n, A: np.ndarray, m: int):
    return np.gcd(np.linalg.det(A), m) == 1
