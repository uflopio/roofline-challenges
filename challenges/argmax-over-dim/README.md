---
slug: argmax-over-dim
title: Argmax Over Dimension
difficulty: EASY
ranked: true
tags: [reduction, matrix, intro]
depends_on: [sum-reduction]
supporterOnly: false
spec:
  signature:
  - name: input
    kind: in
    dtype: f32*
    init: uniform(-0x00800000, 0x00800000)
  - name: output
    kind: out
    dtype: f32*
  - name: shape
    kind: const
    dtype: i32*
  - name: shape_size
    kind: const
    dtype: i32
  - name: dim
    kind: const
    dtype: i32
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

Given a tensor $A$ with rank $n$ and shape $\text{shape}$ stored in row-major order, compute the maximum value over a specified axis $\text{dim}$.
