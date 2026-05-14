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
  - shape: [1024, 1024]
    dim: 0
  - shape: [2048, 2048]
    dim: 1
  - shape: [4096, 4096]
    dim: 0
  - shape: [8191, 4093, 7]
    dim: 2
---

Given a tensor $A$ with rank $n$ and shape $\text{shape}$ stored in row-major order, compute the maximum value over a specified axis $\text{dim}$.

## Input

- `input` - a pointer to a contiguous tensor stored in row-major order containing 32-bit floating-point values.
- `shape` - an integer array describing the dimensions of the input tensor. Its length is given by `shape_size`.
- `shape_size` - the number of dimensions (rank) of the tensor.
- `dim` - the axis along which to compute the maximum (0-indexed, valid in `[0, shape_size)`).

## Output

- `output` - a pointer to a tensor containing the maximum values computed by reducing `input` along dimension `dim`.
