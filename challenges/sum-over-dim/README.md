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
  - m: 1024
    n: 1024
  - m: 4096
    n: 4096
  - m: 8192
    n: 8192
  - m: 1024
    n: 65535
  - m: 65536
    n: 1024
---

Given matrix $A$ of shape $m \times n$, produce vector $\underline{r}$ of length $m$ such that

$$
r_i = \sum_{j}^{n} A_{ij}
$$
