---
slug: sum-reduction
title: Sum Reduction
difficulty: VERY EASY
ranked: false
tags: [reduction, memory-bound, intro]
spec:
  tolerance: 1.
  signature:
  - name: a
    kind: in
    dtype: f32
    shape: n
    init: uniform(1, 0)
  - name: s
    kind: out
    dtype: f32
  - name: n
    kind: const
    dtype: i32
  inputs:
  - n: 4194304
  - n: 8388608
  - n: 16777216
  - n: 33554432
  - n: 65521
---

Compute the sum $s$ of all elements in the vector $a$ of length $n$.

$$
s = \sum_{i}^{n} \underline{a}_i
$$

## Input

- `a` - input vector of length `n`.
- `n` - the number of elements in `a`.

## Output
- `s` - the sum of all elements of `a`.
