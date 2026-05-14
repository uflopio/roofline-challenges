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
    shape: [B, D]
    init: uniform(-1, 1)
  - name: Y
    kind: out
    dtype: f32
    shape: [B]
  - name: B
    kind: const
    dtype: i32
  - name: D
    kind: const
    dtype: i32
  inputs:
  - B: 16
    D: 1048576
  - B: 32
    D: 524288
  - B: 64
    D: 262144
  - B: 128
    D: 131072
---

Compute the L1 norm of each row of a matrix.

Given matrix $X$ of shape $B \times D$ in row-major order, produce vector $\underline{y}$ of length $B$ such that

$$
y_b = \sum_{d=0}^{D-1} \lvert X_{b,d} \rvert.
$$

## Input

- Matrix $X$ of shape $B \times D$.

## Output

- Vector $\underline{y}$ of length $B$.
