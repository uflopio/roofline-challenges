---
slug: matrix-logsumexp
title: Matrix LogSumExp
difficulty: MEDIUM
ranked: true
tags: [reduction, matrix, numerical-stability]
depends_on: [sum-over-dim, argmax-over-dim]
supporterOnly: false
spec:
  tolerance: 0.001
  signature:
  - name: A
    kind: in
    dtype: f32
    shape: [m, n]
    init: uniform(0, 1)
  - name: m
    kind: const
    dtype: i32
  - name: n
    kind: const
    dtype: i32
  - name: s
    kind: out
    dtype: f32
  inputs:
  - m: 1021
    n: 1021
  - m: 2048
    n: 2048
  - m: 4096
    n: 4096
  - m: 8192
    n: 8192
---

Given matrix $A$ of shape $m \times n$, produce $s$ such that

$$
\hat{A}_{ij} = \max_{ij} A_{ij} \quad s = \log\left(\sum_{i}^{M} \sum_{j}^{N} \exp\left(A_{ij} - \hat{A}_{ij} \right) \right) + \hat{A}_{ij} 
$$

NB: The shift by $\hat{A}_{ij}$ is required for numerical stability. Without it, $\exp(A_{ij})$ overflows the `f32` range as soon as $A_{ij}$ exceeds $\sim 88$.

## Input

- `A` - input matrix of shape `[m][n]` stored in row-major order.
- `m` - the number of rows in `A`.
- `n` - the number of columns in `A`.

## Output
- `s` - the log-sum-exp value computed from the formula above.
