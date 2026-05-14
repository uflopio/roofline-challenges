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

Compute the argmax of a tensor over dim.

Find the indices of maximum values along a specified dimension of an input tensor:
\text{output}[i_1, \dots, i_{d-1}, i_{d+1}, \dots, i_n] = \underset{i_d}{\arg\max} \; \text{input}[i_1, \dots, i_d, \dots, i_n]

where dd is the dimension to perform argmax over, nn is the number of dimensions.

$$
k_i = \arg\max_j A_{ij}
$$

When two entries tie for the maximum, return the smaller index.
