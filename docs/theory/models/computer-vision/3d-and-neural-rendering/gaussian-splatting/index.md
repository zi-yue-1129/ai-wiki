---
status: draft
last_reviewed: 2026-10-28
tags:
  - computer vision
  - efficient inference
aliases:
  - 3D Gaussian Splatting
  - Gaussian Splatting
  - 3DGS
  - 3D 高斯濺射
---

# 3D Gaussian Splatting

3D Gaussian splatting (3DGS) represents a scene as millions of explicit, anisotropic 3D Gaussians, optimised from photographs and rendered by projecting the Gaussians onto the image and blending them. Introduced in 2023, it reached state-of-the-art visual quality at real-time rendering rates. It is one of the two key methods on the [3D Vision and Neural Rendering](../index.md) page.

## Overview

Neural radiance fields store the scene in a network that must be queried many times for each ray, which makes rendering slow.[^1] 3DGS keeps the volumetric blending of radiance fields but makes the scene a set of explicit primitives. These can be drawn with a rasteriser, sorted and blended, without a network query per sample. Because the primitives can be stretched, a few of them can cover thin and elongated structures.

## Key concepts

- **Gaussian primitive**: a position, a covariance matrix $\Sigma$ that sets its shape and orientation, an opacity $\alpha$, and colour coefficients. Anisotropic means the Gaussian can be stretched along different axes.
- **Spherical harmonics**: a basis on the sphere whose coefficients let each Gaussian's colour vary with viewing direction.
- **Splatting**: projecting a 3D Gaussian onto the image plane as a 2D ellipse.
- **Adaptive density control**: cloning, splitting and pruning Gaussians during optimisation.

## How it works

The method proceeds in the following steps.

1. **Initialise** one Gaussian at each sparse point from camera calibration (structure from motion). Each starts isotropic, with a radius set by the distance to its nearest neighbours.
2. **Parameterise** the covariance as $\Sigma = RSS^{\top}R^{\top}$, from a scale vector and a rotation quaternion. This keeps $\Sigma$ a valid covariance matrix during optimisation.
3. **Render** by sorting the Gaussians that overlap each pixel by depth and blending them front to back:

$$C=\sum_i T_i\,\alpha_i\,\mathbf c_i,\qquad T_i=\prod_{j<i}(1-\alpha_j).$$

4. **Colour** each Gaussian with spherical-harmonic coefficients evaluated at the viewing direction. Higher-order terms are introduced gradually during training.
5. **Optimise** with a loss $\mathcal L=(1-\lambda)\mathcal L_1+\lambda\mathcal L_{\text{D-SSIM}}$, with $\lambda=0.2$.
6. **Control density.** Every 100 iterations, Gaussians whose view-space position gradient exceeds 0.0002 are cloned or split, and near-transparent Gaussians are removed. Opacities are periodically reset to near zero.

Standard training runs for 30,000 iterations.[^2]

## Results

The paper evaluates on the Mip-NeRF 360, Tanks and Temples, and Deep Blending datasets. On the Mip-NeRF 360 scenes, the 30,000-iteration model is compared with the paper's baselines.[^2]

| Method | PSNR | LPIPS | Training | FPS | Memory |
|---|---|---|---|---|---|
| Plenoxels | 23.08 | 0.463 | 25 min 49 s | 6.79 | 2.1 GB |
| Instant-NGP (Big) | 25.59 | 0.331 | 7 min 30 s | 9.43 | 48 MB |
| Mip-NeRF 360 | 27.69 | 0.237 | 48 h | 0.06 | 8.6 MB |
| 3DGS, 7K iterations | 25.60 | 0.279 | 6 min 25 s | 160 | 523 MB |
| 3DGS, 30K iterations | 27.21 | 0.214 | 41 min 33 s | 134 | 734 MB |

Mip-NeRF 360 has the higher PSNR on these scenes, but it needs 48 hours of training and renders at 0.06 frames per second. The 30K model has better SSIM and LPIPS, and renders above real time.

## Limitations

- **Poorly observed regions.** Regions that the input photographs see little of produce elongated or "splotchy" Gaussians.[^3]
- **Popping.** Large Gaussians in regions of view-dependent appearance cause popping, and the simple visibility algorithm can switch blending order abruptly.
- **No regularisation.** The paper applies no regularisation to the optimisation, which would help with unseen regions and popping.
- **Memory.** Peak GPU memory for large scenes can exceed 20 GB in the unoptimised prototype, and the rendered model takes several hundred megabytes.[^4]

## Open questions

- **Anti-aliasing.** Sudden changes in blending order could be addressed by anti-aliasing, which the paper leaves to future work.
- **Compactness.** Millions of Gaussians remain large; the paper suggests point-cloud compression as a route to lower memory.
- **Editing and surfaces.** Explicit primitives are easier to edit than network weights, which the survey by Chen and Wang highlights.[^5] Extracting clean surfaces is not addressed by the original method.

[^1]: Kerbl et al. (2023), abstract: recent faster methods trade speed for quality; the paper reports real-time display at 1080p.
[^2]: Kerbl et al. (2023), Table 1, Mip-NeRF 360 columns. The Mip-NeRF 360 row is copied from its original paper.
[^3]: Kerbl et al. (2023), Section 7.4: limitations on under-observed regions and elongated artifacts.
[^4]: Kerbl et al. (2023), discussion of memory use in the conclusions.
[^5]: Chen and Wang (2024), abstract: 3D Gaussian splatting offers real-time rendering and unprecedented editability.

## References

### Seminal papers

- Kerbl, B., Kopanas, G., Leimkühler, T. & Drettakis, G. (2023). *3D Gaussian Splatting for Real-Time Radiance Field Rendering*. ACM Transactions on Graphics. https://arxiv.org/abs/2308.04079 — The paper itself: explicit Gaussians, optimised from photographs and rendered in real time.
- Zwicker, M., Pfister, H., van Baar, J. & Gross, M. (2001). *EWA volume splatting*. Proceedings Visualization 2001 (VIS '01), IEEE. https://doi.org/10.1109/VISUAL.2001.964490 — Elliptical Gaussian splatting for volume data, an early ancestor of the approach.
- Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T., Ramamoorthi, R. & Ng, R. (2020). *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*. ECCV. https://arxiv.org/abs/2003.08934 — The radiance-field method that 3DGS replaces with explicit primitives.
- Müller, T., Evans, A., Schied, C. & Keller, A. (2022). *Instant Neural Graphics Primitives with a Multiresolution Hash Encoding*. ACM Transactions on Graphics. https://arxiv.org/abs/2201.05989 — The fast radiance-field baseline in the paper's comparisons.
- Barron, J. T., Mildenhall, B., Verbin, D., Srinivasan, P. P. & Hedman, P. (2021). *Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields*. arXiv. https://arxiv.org/abs/2111.12077 — The high-quality but slow baseline on the Mip-NeRF 360 scenes.

### Surveys and textbooks

- Chen, G. & Wang, W. (2024). *A Survey on 3D Gaussian Splatting*. arXiv. https://arxiv.org/abs/2401.03890 — A systematic overview of 3D Gaussian splatting, its principles and applications.
