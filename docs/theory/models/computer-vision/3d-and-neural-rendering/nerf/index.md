---
status: draft
last_reviewed: 2026-10-28
tags:
  - computer vision
  - representation learning
aliases:
  - Neural Radiance Field
  - Neural Radiance Fields
  - NeRF
  - 神經輻射場
---

# Neural Radiance Fields (NeRF)

Neural Radiance Fields (NeRF) represent a static scene as a multilayer perceptron that maps a 3D position and a viewing direction to a colour and a volume density, and render pixels by integrating along camera rays. Introduced in 2020, it became the reference method for novel view synthesis from photographs. It is one of the two key methods on the [3D Vision and Neural Rendering](../index.md) page.

## Overview

Before NeRF, learned view synthesis relied on discrete voxel grids, which limit resolution, or on single-depth-per-ray networks, which smooth detail.[^1]

NeRF replaces these with one continuous function, fitted to each scene's posed photographs through differentiable rendering alone.

## Key concepts

- **Input and output**: a point $(x, y, z)$ and a viewing direction go in; a density $\sigma$ and a colour $\mathbf{c}$ come out, so colour can vary with viewing angle.
- **Positional encoding**: the sine-and-cosine mapping of inputs, without which the network struggles with fine detail.
- **Hierarchical sampling**: a coarse network finds where density lies, and a fine network samples there.

## How it works

The paper's continuous rendering integral, with $\mathbf r(t)=\mathbf o+t\mathbf d$ the ray from the camera, is

$$C(\mathbf r)=\int_{t_n}^{t_f} T(t)\,\sigma(\mathbf r(t))\,\mathbf c(\mathbf r(t),\mathbf d)\,dt,\qquad T(t)=\exp\!\Big(-\int_{t_n}^{t}\sigma(\mathbf r(s))\,ds\Big).$$

It is approximated by stratified samples along each ray, giving alpha compositing:

$$\hat C(\mathbf r)=\sum_{i=1}^{N} T_i\,(1-e^{-\sigma_i\delta_i})\,\mathbf c_i,\qquad T_i=\exp\Big(-\sum_{j<i}\sigma_j\delta_j\Big),$$

where $\delta_i$ is the spacing between samples. Each input coordinate is first encoded as sines and cosines at $L$ octave frequencies, with $L=10$ for positions and $L=4$ for directions.

One training step works as follows.

1. Sample a batch of 4096 rays, one through each sampled pixel.
2. Evaluate the coarse network at $N_c=64$ stratified samples and composite the colour $\hat C_c$.
3. Use the coarse weights to place $N_f=128$ further samples, evaluate the fine network, and composite $\hat C_f$.
4. Minimise the squared error of both $\hat C_c$ and $\hat C_f$ against the photographed colour, with Adam.

Training takes 100,000 to 300,000 iterations, about one to two days on one NVIDIA V100 per scene.[^2]

## Results

Among the compared methods, NeRF has the highest PSNR on every benchmark; LLFF has slightly better LPIPS on real forward-facing scenes.[^3]

| Method | Diffuse Synthetic 360° | Realistic Synthetic 360° | Real Forward-Facing |
|---|---|---|---|
| SRN | 33.20 | 22.26 | 22.84 |
| NV | 29.62 | 26.05 | not reported |
| LLFF | 34.38 | 24.88 | 24.13 |
| NeRF | 40.15 | 31.01 | 26.50 |

Baselines needed at least 12 hours of training per scene, while the NeRF weights take about 5 MB.[^4]

## Limitations

- **Per-scene optimisation.** Each scene needs its own network, trained from scratch.
- **Slow rendering.** One rendered image needs 150 to 200 million network queries; the paper reports about 30 seconds per frame on a V100.[^2]
- **Static scenes.** Moving content and changing light are outside the method's scope.
- **Aliasing and unbounded scenes.** One ray per pixel blurs fine detail at different scales,[^5] and scenes with content at any distance remain hard.[^6]

## Open questions

- **Speed.** Hash-grid encodings cut training to seconds and rendering to tens of milliseconds at 1080p.[^7] Explicit primitives later reached real-time rates; see [3D Gaussian Splatting](../gaussian-splatting/index.md).
- **Generalising across scenes.** Whether one network can produce radiance fields for unseen scenes without per-scene optimisation is an active question.
- **Editing and geometry.** Scenes in weights are hard to edit, and surfaces extracted from density are often noisy.

[^1]: Mildenhall et al. (2020), Section 6.3: SRN keeps one depth and colour per ray, and NV's explicit 128³ voxel grid cannot scale to fine detail at high resolution.
[^2]: Mildenhall et al. (2020), Section 5.3 and Appendix A: about 100,000 to 300,000 iterations, and about 30 seconds per frame at the paper's ray counts.
[^3]: Mildenhall et al. (2020), Table 1, PSNR values; SSIM and LPIPS are also reported. NV is not reported on real forward-facing data because it reconstructs only bounded objects.
[^4]: Mildenhall et al. (2020), Section 6.3: LLFF needed over 15 GB for one realistic synthetic scene, against about 5 MB for NeRF.
[^5]: Barron et al. (2021, *Mip-NeRF*), abstract: rendering conical frustums instead of rays reduces aliasing.
[^6]: Barron et al. (2021, *Mip-NeRF 360*), abstract: NeRF-like models struggle with unbounded scenes.
[^7]: Müller et al. (2022), abstract: a multiresolution hash encoding enables training in seconds and rendering in tens of milliseconds at 1920×1080.

## References

### Seminal papers

- Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T., Ramamoorthi, R. & Ng, R. (2020). *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*. ECCV. https://arxiv.org/abs/2003.08934 — The paper itself: a continuous 5D scene function fitted by volume rendering.
- Barron, J. T., Mildenhall, B., Tancik, M., Hedman, P., Martin-Brualla, R. & Srinivasan, P. P. (2021). *Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields*. ICCV. https://arxiv.org/abs/2103.13415 — Conical frustums replace rays, reducing aliasing in NeRF renderings.
- Barron, J. T., Mildenhall, B., Verbin, D., Srinivasan, P. P. & Hedman, P. (2021). *Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields*. arXiv. https://arxiv.org/abs/2111.12077 — Extends NeRF to unbounded 360-degree scenes with a non-linear parameterisation.
- Müller, T., Evans, A., Schied, C. & Keller, A. (2022). *Instant Neural Graphics Primitives with a Multiresolution Hash Encoding*. ACM Transactions on Graphics. https://arxiv.org/abs/2201.05989 — A hash-grid encoding and fused GPU kernels that speed training and rendering.

### Surveys and textbooks

- Tewari, A., Thies, J., Mildenhall, B., Srinivasan, P., Tretschk, E., Wang, Y., et al. (2021). *Advances in Neural Rendering*. arXiv. https://arxiv.org/abs/2111.05849 — A survey of neural rendering and the scene representations it uses.
