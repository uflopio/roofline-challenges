---
slug: gelu
title: GELU Activation
difficulty: VERY EASY
ranked: true 
tags: [vector, memory-bound, intro, activation]
spec:
  tolerance: 0.0001
  signature:
  - name: x
    kind: in
    dtype: f32
    shape: n
    init: uniform(0, 1)
  - name: y
    kind: out
    dtype: f32
    shape: n
  - name: n
    kind: const
    dtype: i32
  inputs:
  - n: 4194301
  - n: 8388608
  - n: 16777216
  - n: 33554432
  - n: 65521
---

Given vector $\underline{x}$ of length $n$, produce vector $\underline{y}$ of length $n$ such that, with $i$ indexing over $n$, 

$$
y_i = \frac{x_i}{2} \left( 1 + \tanh\left( \sqrt{\tfrac{2}{\pi}} \left( x_i + 0.044715 \cdot x_i^3 \right) \right) \right)
$$

Do not use the exact erf-based GELU. Use the approximate form above.

## Input

- `n` - the number of elements in the vectors.
- `x` - input vector of length $n$ containing single-precision floating-point values after applied GELU.

## Output
- `y` - output vector of length n where each element is the approximate GELU activation applied to the corresponding element of x.
