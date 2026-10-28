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

3D Gaussian splatting represents a scene as a large set of explicit 3D Gaussians, each with a position, shape, opacity and colour. The Gaussians are projected onto the image plane and blended, which makes rendering fast. It appeared as an alternative to [NeRF](nerf.md) for view synthesis, trading the implicit network for an explicit set of primitives.

## Overview

The [chapter](index.md) covers the field. This page covers the method. Each scene is optimised from photographs and a sparse point cloud. The result can be rendered by rasterisation, a standard operation in graphics hardware, rather than by evaluating a network many times per pixel.

## Problem

Radiance-field methods such as NeRF produce high quality but are slow to render and slow to train. The problem is to keep the quality of volumetric rendering while making both fast enough for interactive use.

## Core idea

The scene is a collection of anisotropic 3D Gaussians. Each Gaussian has a mean, a covariance that sets its shape and orientation, an opacity, and view-dependent colour represented by spherical harmonics. The Gaussians are projected onto the camera as two-dimensional ellipses and composited in depth order. The parameters are optimised by gradient descent against the input images. During training the method adds Gaussians where the reconstruction is poor and removes ones that are nearly transparent, which the authors call adaptive density control.

## Equation

For a pixel, the colour is alpha-blended over the depth-sorted Gaussians $i$ that cover it:

$$C = \sum_{i \in N} c_i \,\alpha_i \prod_{j=1}^{i-1}(1 - \alpha_j)$$

Here $c_i$ is the view-dependent colour of Gaussian $i$, and $\alpha_i$ is its opacity after its 2D projection has been evaluated at the pixel. A Gaussian's 3D covariance is factored into a rotation and a scale, which keeps it positive semidefinite during optimisation.

## Results

The abstract reports real-time rendering at 1080p, at least 30 frames per second, with competitive training times. The paper's tables give the comparisons, which are not restated here.

## Limitations

- The number of Gaussians can grow large, which costs memory.
- Quality can drop in regions that the input views do not observe well.
- The representation is explicit, so it needs care when a method must reason about surfaces or topology.

## Connections

The projection step is an instance of the splatting approach studied in computer graphics, in which Zwicker and colleagues analysed elliptical weighted splatting for rendering [(Zwicker et al., 2002)](https://doi.org/10.1109/tvcg.2002.1021576). The gradients for the optimisation are computed as described in [Automatic differentiation](../../../math/automatic-differentiation/index.md).

## Applications

Real-time capture and display of real-world scenes for film, games and virtual reality. Its explicit form also makes it easier to edit and to combine with mesh-based pipelines than NeRF.

## Open questions

- How can the number of primitives be controlled without losing detail?
- How should Gaussian representations handle dynamic scenes and lighting changes?

## References

### Seminal papers

- Kerbl, Kopanas, Leimkuehler and Drettakis, *3D Gaussian Splatting for Real-Time Radiance Field Rendering*, ACM Transactions on Graphics (2023). https://doi.org/10.1145/3592433 — The paper that introduces the method, its optimisation and its rasterisation renderer.
- Mildenhall, Srinivasan, Tancik, Barron, Ramamoorthi and Ng, *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*, European Conference on Computer Vision (2020). https://doi.org/10.1007/978-3-030-58452-8_24 — The implicit radiance-field method that this approach is compared with.
- Barron et al., *Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields*, IEEE/CVF International Conference on Computer Vision (2021). https://doi.org/10.1109/iccv48922.2021.00580 — An anti-aliased radiance-field variant, cited as a point of comparison for quality.

### Surveys and textbooks

- Zwicker, Pfister, van Baar and Gross, *EWA Splatting*, IEEE Transactions on Visualization and Computer Graphics (2002). https://doi.org/10.1109/tvcg.2002.1021576 — Elliptical weighted average splatting, the classical method behind projecting Gaussians onto the image.
- Kajiya and Von Herzen, *Ray tracing volume densities*, SIGGRAPH (1984). https://doi.org/10.1145/964965.808594 — The early formulation of volume rendering in computer graphics.
