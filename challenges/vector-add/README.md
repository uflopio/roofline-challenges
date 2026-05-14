---
slug: vector-add
title: Vector Addition
difficulty: VERY EASY
ranked: false
tags: [vector, memory-bound, intro]
ranked: false
spec:
  tolerance: 1.0e-5
  signature:
  - name: a
    kind: in
    dtype: f32
    shape: n
    init: uniform(0, 1)
  - name: b
    kind: in
    dtype: f32
    shape: n
    init: uniform(0, 1)
  - name: c
    kind: out
    dtype: f32
    shape: n
    init: uniform(0, 1)
  - name: n
    kind: const
    dtype: i32
    values: ["2**22", "2**23", "2**24", "2**25", "2**26"]
---

Given vectors $\underline{a}$ and $\underline{b}$ of length $n$, produce vector $\underline{c}$ of length $n$ such that $c_i = a_i + b_i$.
