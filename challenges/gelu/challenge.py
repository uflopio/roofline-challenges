import numpy as np


def gelu(x):
    sqrt = np.sqrt(2 / np.pi)
    return sqrt * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))


def solve(x: list, n: int):
    return gelu(np.array(x))
