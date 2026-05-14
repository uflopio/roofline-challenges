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
    shape: ["m", "n"]
    init: uniform(0, 1)
  - name: B
    kind: in
    dtype: f32
    shape: ["k", "n"]
    init: uniform(0, 1)
  - name: C
    kind: out
    dtype: f32
    shape: ["m", "n"]
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
  - m: 1024
    n: 1024
    k: 1024
  - m: 2048
    n: 2048
    k: 2048
  - m: 4096
    n: 4096
    k: 4096
---

Compute the dense matrix multiplication $C = AB$.

Given matrices $A$ of shape $M \times K$ and $B$ of shape $K \times N$, produce matrix $C$ of shape $M \times N$ such that

$$
C_{i,j} = \sum_{k=0}^{K-1} A_{i,k} \cdot B_{k,j}.
$$

All matrices are stored in row-major order.

## Input

- Matrix $A$ of shape $M \times K$.
- Matrix $B$ of shape $K \times N$.

## Output

- Matrix $C$ of shape $M \times N$ such that $C = A \cdot B$.

## Sizes

- $M = N = K = 2^9$
- $M = N = K = 2^{10}$
- $M = N = K = 2^{11}$
- $M = N = K = 2^{12}$
