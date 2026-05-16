---
slug: matrix-decrypt-encrypt
title: Matrix Decrypt-Encrypt
difficulty: MEDIUM
ranked: true
tags: [cryptography]
spec:
  signature:
  - name: A
    kind: in
    dtype: i32
    shape: [n, n]
    init: uniform(0, l)
  - name: B
    kind: in
    dtype: i32
    shape: [n, n]
    init: uniform(0, l)
  - name: n
    kind: const
    dtype: i32
  - name: l
    kind: const
    dtype: i32
  - name: c
    kind: inout
    dtype: i32
    shape: [n]
    init: uniform(0, l)
  inputs:
  - n: 4
    l: 10
  - n: 256
    l: 256
  - n: 16
    l: 256
  - n: 12
    l: 48
  - n: 4096
    l: 4096
  - n: 2039
    l: 65521
supporterOnly: false
---

A [Hill cipher](https://en.wikipedia.org/wiki/Hill_cipher) is a cipher based on matrix multiplication. To encrypt a message $\underline{c}$ of length $\leq 1 n \leq 4096$ in an alphabet of size $1 \leq l \leq 65535$, pick some key $A$ of size $n \times n$ and compute $\underline{c}_A = A\underline{c} \mod l$. To decrypt the message, apply $A^{-1}\underline{c}_A = (A^{-1}A)\underline{c} = I\underline{c} = \underline{c}$.

For this problem, given a message $\underline{c}_A$ (encrypted for $A$), the encryption key $A$, and the encryption key $B$, rekey the message $\underline{c}_A$ to become $\underline{c}_B$.

The input $c_A$ will be supplied in `c`. The final output $c_B$ must also be placed in `c`.

## Input

- `A` - original encryption key.
- `B` - target encryption key.
- `n` - size of the Hill cipher key matrices.
- `l` - alphabet modulus.
- `c` - ciphertext encrypted under `A`, provided in place.

## Output
- `c` - the input vector modified in place to become $\underline{c}_B$.
