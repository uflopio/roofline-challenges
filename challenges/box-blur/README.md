---
slug: box-blur
title: Box Blur
difficulty: EASY
ranked: true
tags: [graphics, convolution]
supporterOnly: false
spec:
  tolerance: 0.0001
  signature:
  - name: input_image
    kind: in
    dtype: f32
    shape:
    - height
    - width
    init: uniform(0, 255)
  - name: output_image
    kind: out
    dtype: f32
    shape:
    - height
    - width
  - name: height
    kind: const
    dtype: i32
  - name: width
    kind: const
    dtype: i32
  - name: kernel_size
    kind: const
    dtype: i32
  inputs:
  - height: 2560
    width: 1440
    kernel_size: 15
  - height: 2560
    width: 1440
    kernel_size: 21
  - height: 2560
    width: 1440
    kernel_size: 27
  - height: 2048
    width: 2048
    kernel_size: 15
  - height: 2048
    width: 2048
    kernel_size: 21
  - height: 2048
    width: 2048
    kernel_size: 27
  - height: 4096
    width: 4096
    kernel_size: 15
  - height: 4096
    width: 4096
    kernel_size: 21
  - height: 4093
    width: 4093
    kernel_size: 23
---

Apply a box blur filter to a grayscale image by averaging pixels in a square neighborhood:

$$
O_{ij} = \frac{1}{N} \sum_{u=-k}^{k} \sum_{v=-k}^{k} I_{(i + u)\,(j + v)}
$$

where $k = \lfloor \text{kernel\_size}/2 \rfloor$ and $N$ is the number of valid pixels in the kernel.

This creates a blurring effect by smoothing out pixel values. The larger the kernel size, the more blurred the result!

## Input

- `height` - the number of rows in the image.
- `width` - the number of columns in the image.
- `kernel_size` - the side length of the square blur kernel.  
  The kernel is centered on each pixel, and its radius is:
- `input_image` - a 2D grayscale image of shape $\text{width} \times \text{height}$ containing floating-point pixel intensities in the range $[0, 255]$.

## Output

- `output_image` — a blurred grayscale image of shape `[height][width]`.
