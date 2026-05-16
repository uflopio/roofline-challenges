---
slug: l2-norm
title: L2 Norm
difficulty: EASY
ranked: false
tags: [reduction, vector, memory-bound]
supporterOnly: false
spec:
  tolerance: 0.001
  signature:
  - name: X
    kind: in
    dtype: f32
    shape: [n, m]
    init: uniform(-1, 1)
  - name: Y
    kind: out
    dtype: f32
    shape: [n]
  - name: n
    kind: const
    dtype: i32
  - name: m
    kind: const
    dtype: i32
  inputs:
  - n: 16
    m: 1048576
  - n: 32
    m: 524288
  - n: 64
    m: 262144
  - n: 127
    m: 131071
---

Compute the L2 norm of each row of a matrix.

Given matrix $X$ of shape $n \times m$ in row-major order, produce vector $\underline{y}$ of length $n$ such that

$$
y_i = \sqrt{\sum_{j}^{m} X_{i\,j}^2}
$$

## Input

- `X` - input matrix of shape $n \times m$ stored in row-major order.
- `n` - the number of rows in `X`.
- `m` - the number of columns in `X`.

## Output
- `Y` - output vector of length `n` where each element is the L2 norm of the corresponding row of `X`.
