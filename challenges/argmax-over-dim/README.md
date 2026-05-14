---
slug: argmax-over-dim
title: Argmax Over Dimension
difficulty: EASY
ranked: true
tags: [reduction, matrix, intro]
depends_on: [sum-reduction]
supporterOnly: false
spec:
  tolerance: 0.0
  signature:
  - name: m
    kind: const
    dtype: i32
  - name: n
    kind: const
    dtype: i32
  - name: A
    kind: in
    dtype: f32
    shape:
    - m
    - n
    init: uniform(0, 1)
  - name: k
    kind: out
    dtype: i32
    shape:
    - m
  inputs:
  - m: 1024
    n: 1024
  - m: 4096
    n: 4096
  - m: 8192
    n: 8192
  - m: 1024
    n: 65536
  - m: 65536
    n: 1024
---

Compute the row-wise argmax of a matrix.

Given matrix $A$ of shape $m \times n$, produce integer vector $\underline{k}$ of length $M$ such that

$$
k_i = \arg\max_j A_{ij}
$$

When two entries tie for the maximum, return the smaller index.
