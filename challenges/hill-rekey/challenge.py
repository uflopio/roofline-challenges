import sympy as sp


def solve(A: list[list[int]], B: list[list[int]], n, l: int, c: list):
    a = sp.Matrix(A)
    b = sp.Matrix(B)
    a_inv = a.inv_mod(l)
    c[:] = (b * a_inv * sp.Matrix(c)) % l


c = [7, 11]
solve([[3, 3], [2, 5]], [[1, 0], [0, 1]], 2, 26, c)
assert c == [6, 5]
