---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/computer-vision/3d-and-neural-rendering
tags:
  - Gaussian splatting
  - neural rendering
  - real-time rendering
aliases:
  - 3D 高斯潑濺
  - 高斯潑濺
  - 3D Gaussian splatting
---

# 3D Gaussian splatting

3D Gaussian splatting represents a scene as a set of explicit 3D Gaussians, each with a position, a covariance, an opacity and a view-dependent colour. The Gaussians are projected onto the image plane and blended, which allows real-time rendering. It is an explicit alternative to the implicit [NeRF](nerf.md) representation.

## Overview

The [chapter](index.md) covers the field. This page covers the method. The scene is optimised from input photographs, starting from a sparse point cloud.

## Problem

Radiance fields such as NeRF produce high-quality renderings, but evaluating a network many times per pixel is slow. The paper aims to keep the quality of volumetric rendering while reaching real-time rates, using a rasteriser instead.

## Core idea

Each Gaussian has a mean, a covariance, an opacity, and a colour represented by spherical harmonics of degree up to 3, which makes the colour depend on viewing direction. The covariance is built from a rotation and a scale. During optimisation, the method adds Gaussians by densification every 100 iterations where the positional gradient exceeds 0.0002, splitting large Gaussians by dividing their scale by 1.6. It also prunes Gaussians that are nearly transparent, and it resets opacity every 3000 iterations. The paper calls this density control.

## Equation

The covariance of each Gaussian is

$$\Sigma = R S S^\top R^\top$$

where $R$ is a rotation and $S$ is a diagonal scale. For a pixel, the colour is alpha-blended over the depth-sorted Gaussians $i$ that cover it:

$$C = \sum_{i \in N} c_i \,\alpha_i \prod_{j=1}^{i-1}(1 - \alpha_j)$$

Here $c_i$ is the view-dependent colour of Gaussian $i$, and $\alpha_i$ is its opacity after the two-dimensional projection has been evaluated at the pixel.

## Results

The abstract reports real-time rendering at 1080p, at least 30 frames per second, with competitive training times and quality. The paper's tables give the comparisons.

## Limitations

The paper's limitations section (Sec. 7.4) reports the following:

- The prototype needs more memory than NeRF, with a peak above 20 GB.
- Artefacts can appear in regions the input views observe poorly.
- Large Gaussians can cause popping in view-dependent regions.

The paper also reports floaters near the input cameras (Sec. 5.2), and it assumes static input scenes (Sec. 3).

## Connections

The method is trained by gradient descent on the image loss, using the gradient machinery in [Automatic differentiation](../../../math/automatic-differentiation/index.md).

## Applications

Real-time rendering of captured real-world scenes, which is the setting the paper evaluates.

## Open questions

- How can the number of Gaussians be controlled without losing detail?
- How should Gaussian representations handle dynamic scenes and lighting changes?

## References

### Seminal papers

- Kerbl, Kopanas, Leimkuehler and Drettakis, *3D Gaussian Splatting for Real-Time Radiance Field Rendering*, ACM Transactions on Graphics (2023). https://doi.org/10.1145/3592433 — Introduces the method, its optimisation and its rasterisation renderer.
- Mildenhall, Srinivasan, Tancik, Barron, Ramamoorthi and Ng, *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*, European Conference on Computer Vision (2020). https://doi.org/10.1007/978-3-030-58452-8_24 — The implicit radiance-field representation that this method is an explicit alternative to.
- Barron et al., *Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields*, IEEE/CVF International Conference on Computer Vision (2021). https://doi.org/10.1109/iccv48922.2021.00580 — Extends NeRF with a multiscale representation for anti-aliasing.

### Surveys and textbooks

- Zwicker, Pfister, van Baar and Gross, *EWA Splatting*, IEEE Transactions on Visualization and Computer Graphics (2002). https://doi.org/10.1109/tvcg.2002.1021576 — Elliptical weighted average splatting, a classical splatting method.
- Kajiya and Von Herzen, *Ray tracing volume densities*, SIGGRAPH (1984). https://doi.org/10.1145/964965.808594 — An early formulation of ray tracing through volume densities.
