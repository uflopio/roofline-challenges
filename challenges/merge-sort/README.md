---
slug: merge-sort
title: Merge Sort
difficulty: MEDIUM
ranked: false
tags: [sirt]
supporterOnly: false
spec:
  signature:
  - name: a
    kind: in
    dtype: u64
    shape: [n]
    init: uniform(0, 18446744073709551615)
  - name: b
    kind: out
    dtype: u64
    shape: [n]
  - name: n
    kind: const
    dtype: i32
  inputs:
  - n: 1021
  - n: 2048
  - n: 4096
  - n: 33546240
---

Use [Merge Sort](https://en.wikipedia.org/wiki/Merge_sort) to sort an array $\underline{a}$ of length $n$ in ascending order $\underline{b}_i \leq \underline{b}_{i + 1}$.

## Input

- `a` - input list of `long long`s with $n$ elements.
- `n` - the number of elements in $\underline{a}$. 

## Output

- `b` - the sorted array of inputs from $a$.
