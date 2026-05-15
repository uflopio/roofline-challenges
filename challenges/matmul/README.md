---
slug: matmul
title: Matrix Multiply
difficulty: MEDIUM
ranked: false
tags: [matrix, compute-bound]
depends_on: [vector-add]
supporterOnly: false
spec:
  tolerance: 0.01
  signature:
  - name: A
    kind: in
    dtype: f32
    shape: [m, n]
    init: uniform(0, 1)
  - name: B
    kind: in
    dtype: f32
    shape: [k, n]
    init: uniform(0, 1)
  - name: C
    kind: out
    dtype: f32
    shape: [m, n]
  - name: m
    kind: const
    dtype: i32
  - name: n
    kind: const
    dtype: i32
  - name: k
    kind: const
    dtype: i32
  inputs:
  - m: 512
    n: 512
    k: 512
  - m: 1021
    n: 1021
    k: 1021
  - m: 2048
    n: 2048
    k: 2048
  - m: 4093
    n: 4093
    k: 4093
---

Compute the dense matrix multiplication $C = AB$.

Given matrices $A$ of shape $M \times K$ and $B$ of shape $K \times N$, produce matrix $C$ of shape $M \times N$ such that

$$
C_{ij} = \sum_{k}^{K} A_{ik} \cdot B_{kj}
$$

All matrices are stored in row-major order.

## Input

- `A` - input matrix of shape `[m][k]` stored in row-major order.
- `B` - input matrix of shape `[k][n]` stored in row-major order.
- `m` - the number of rows in `A` and `C`.
- `n` - the number of columns in `B` and `C`.
- `k` - the number of columns in `A` and rows in `B`.

## Output
- `C` - output matrix of shape `[m][n]` such that $C = AB$.
