---
slug: matrix-inverse-modulo-n
title: Matrix Inverse Modulo n
difficulty: EASY
ranked: true
tags: [cryptograph]
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
    init: uniform(0, 100)
  - name: is_invertible
    kind: out
    dtype: bool*
  inputs:
  - n: 4194304
  - n: 8388608
  - n: 16777216
  - n: 33554432
  - n: 67108864
---

Given an **integer** matrix $A$ of shape $n \times n$, determine if it is invertible $\text{mod}\, m$.

For a matrix to be invertible $\text{mod}\, m$ we require that there exists some $A^{-1}$ such that $A^{-1}A = I$ when the multiplication of the elements is performed $\text{mod}\,m$.
