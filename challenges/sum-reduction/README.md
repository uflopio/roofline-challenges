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
    values: ["2**22", "2**23", "2**24", "2**25", "2**26"]
---

Compute the sum $s$ of all elements in the vector $a$ of length $n$.

$$
s = \sum_{i}^{n} a_i
$$
