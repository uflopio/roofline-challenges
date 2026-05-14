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
      init: uniform(0, 25)
    - name: B
      kind: in
      dtype: i32
      shape: [n, n]
      init: uniform(0, 25)
    - name: c
      kind: inout
      dtype: i32
      shape: [n]
      init: uniform(0, 25)
supporterOnly: true
---

Given two [Hill-cypher](https://en.wikipedia.org/wiki/Hill_cipher) key matrices $A, B \in \mathbb{Z}^{n \times n}_l$ for an alphabet of size $1 < l \leq 2^{16}$ and a ciphertext $\underline{c}_A \in \mathbb{Z}^{n}_l$ encrypted under key $A$, rekey the ciphertext to $\underline{c}_B$ so that $c_B$ decrypted with $B$ yields the same plaintext as $\underline{c}_A$ decrypted with $A$. 

You get the value for $\underline{c}_A$ in the input `c`. When you're done `c` should contain the value for $\underline{c}_B$.
