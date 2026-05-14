---
slug: matrix-decrypt-encrypt
title: Matrix Decrypt-Encrypt
difficulty: EASY
ranked: true
tags: [cryptography]
spec:
  signature:
  - name: n
    kind: const
    dtype: i32
  - name: l
    kind: const
    dtype: i32
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
  - n: 2048
    l: 65535
supporterOnly: true
---

Given two [Hill-cypher](https://en.wikipedia.org/wiki/Hill_cipher) key matrices $A, B \in \mathbb{Z}^{n \times n}_l$ for an alphabet of size $1 < l < 2^{16}$ and a ciphertext $\underline{c}_A \in \mathbb{Z}^{n}_l$ encrypted under key $A$, rekey the ciphertext to $\underline{c}_B$ so that $c_B$ decrypted with $B$ yields the same plaintext as $\underline{c}_A$ decrypted with $A$. 

You get the value for $\underline{c}_A$ in the input `c`. When you're done `c` should contain the value for $\underline{c}_B$.

## Input

- `n` - size of the Hill-cipher key matrices and block length.
- `l` - alphabet modulus.
- `A` - original encryption key.
- `B` - target encryption key.
- `c` - ciphertext encrypted under $A$, given in-place.

## Output

- The input vector `c` modified in-place to become $\underline{c}_B$.
