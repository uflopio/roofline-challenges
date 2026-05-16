import sympy as sp
import numpy as np
from math import gcd


def generate(n: int, l: int) -> dict:
    c = np.random.randint(0, l, size=n)
    B = np.random.randint(0, l, size=(n, n))

    while True:
        A_np = np.random.randint(0, l, size=(n, n))
        A = sp.Matrix(A_np)

        det_A = int(A.det())

        if gcd(det_A, l) == 1:
            return {'A': A_np, 'B': B, 'c': c, 'l': l, 'n': n}


def solve(A: np.ndarray, B: np.ndarray, n, l: int, c: np.ndarray):
    a = sp.Matrix(A)
    b = sp.Matrix(B)
    a_inv = a.inv_mod(l)
    c[:] = np.array((b * a_inv * sp.Matrix(c)) % l).reshape(-1)


c = [7, 11]
solve([[3, 3], [2, 5]], [[1, 0], [0, 1]], 2, 26, c)
assert c == [6, 5]
