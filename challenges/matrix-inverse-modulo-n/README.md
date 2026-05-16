---
slug: matrix-inverse-modulo-n
title: Matrix Inverse Modulo n
difficulty: EASY
ranked: true
supporterOnly: true
tags: [cryptography]
spec:
  signature:
  - name: n
    kind: const
    dtype: i32
  - name: m
    kind: const
    dtype: i32
  - name: A
    kind: in
    dtype: i32
    shape: [n, n]
    init: uniform(0, 25)
  - name: is_invertible
    kind: out
    dtype: i32
    shape: [1]
  inputs:
  - n: 512
    m: 26
  - n: 1024
    m: 26
  - n: 2048
    m: 26
  - n: 4096
    m: 26
  - n: 8192
    m: 26
  - n: 11279
    m: 23
---

Given an **integer** matrix $A$ of shape $n \times n$, determine if it is invertible $\text{mod}\, m$.

For a matrix to be invertible $\text{mod}\, m$ we require that there exists some $A^{-1}$ such that $A^{-1}A = I$ when the multiplication of the elements is performed $\text{mod}\,m$.

## Input

- `n` - dimension of the square matrix `A`.
- `m` - modulus for the arithmetic operations.
- `A` - integer matrix whose invertibility is to be determined.

## Output
- `is_invertible` - a single value indicating whether `A` is invertible modulo `m`.
