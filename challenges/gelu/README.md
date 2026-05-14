---
slug: gelu
title: GELU Activation
difficulty: VERY EASY
ranked: true 
tags: [vector, memory-bound, intro, activation]
spec:
  tolerance: 0.0001
  signature:
  - name: n
    kind: const
    dtype: i32
    values: ["2**22", "2**23", "2**24", "2**25", "2**26"]
  - name: x
    kind: in
    dtype: f32
    shape: n
    init: uniform(0, 1)
  - name: y
    kind: out
    dtype: f32
    shape: n
---

Given vector $\underline{x}$ of length $n$, produce vector $\underline{y}$ of length $n$ such that, with $i$ indexing over $n$, 

$$
y_i = \frac{x_i}{2} \left( 1 + \tanh\left( \sqrt{\tfrac{2}{\pi}} \left( x_i + 0.044715 \cdot x_i^3 \right) \right) \right)
$$

Do not use the exact erf-based GELU. Use the approximate form above.
