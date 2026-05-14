import numpy as np


def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))


def solve(x: np.ndarray, n: int) -> np.ndarray:

    return gelu(x)
