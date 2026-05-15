---
slug: l1-norm
title: L1 Norm
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

Compute the L1 norm of each row of a matrix.

Given a matrix $X$ of shape $n \times m$ stored in row-major order, compute a vector $Y$ of length $n$ such that each element is the L1 norm of the corresponding row:

$$
Y_i = \sum_{j=1}^{m} \lvert X_{i,j} \rvert
$$

## Input

- `X` — input matrix of shape $n \times m$ stored in row-major order
- `n` — number of rows in `X`
- `m` — number of columns in `X`

## Output

- `Y` — output vector of length `n`, where each element `Y[i]` is the L1 norm of row `i` of `X`
