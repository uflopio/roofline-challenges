---
slug: sum-over-dim
title: Sum Over Dimension
difficulty: EASY
ranked: false
tags: [reduction, matrix, intro]
depends_on: [sum-reduction]
supporterOnly: false
spec:
  tolerance: 0.5
  signature:
  - name: A
    kind: in
    dtype: f32
    shape: ["m", "n"]
    init: uniform(0, 1)
  - name: r
    kind: const
    dtype: f32
    shape: ["m"]
  - name: m
    dtype: i32
    kind: const
  - name: n
    dtype: i32
    kind: const
  inputs:
  - m: 256
    n: 256
  - m: 512
    n: 512
  - m: 1024
    n: 1024
  - m: 2048
    n: 2048
  - m: 4096
    n: 4096
  - m: 8191
    n: 4093
---

Given matrix $A$ of shape $m \times n$, produce vector $\underline{r}$ of length $m$ such that

$$
r_i = \sum_{j}^{n} A_{ij}
$$

## Input

- `A` - input matrix of shape `[m][n]` stored in row-major order.
- `m` - the number of rows in `A`.
- `n` - the number of columns in `A`.

## Output
- `r` - output vector of length `m` containing the row-wise sums of `A`.
