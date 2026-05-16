import numpy as np
import sympy as sp
from math import gcd


def solve(n, A: np.ndarray, m: int):
    det = sp.Matrix(A).det()
    return gcd(int(det), m) == 1
