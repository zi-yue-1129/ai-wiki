---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/computer-vision/3d-and-neural-rendering
tags:
  - NeRF
  - neural rendering
  - view synthesis
aliases:
  - 神經輻射場
  - NeRF
  - Neural radiance field
---

# NeRF: neural radiance fields

NeRF represents a static scene as a multilayer perceptron that maps a 3D position and a viewing direction to a colour and a volume density. New views are rendered by integrating this function along camera rays. The network is fitted to photographs of the scene whose camera poses are known.

## Overview

The [chapter](index.md) describes the field. This page covers the method.

## Problem

Given photographs of a scene with known camera poses, render views from camera positions that are not in the input set. The abstract frames this as novel-view synthesis of complex scenes.

## Core idea

The scene is a function $F_\Theta$ that takes a position $\mathbf{x}$ and a viewing direction $\mathbf{d}$ and returns a colour $\mathbf{c}$ and a density $\sigma$. The density depends on position only, $\sigma = \sigma(\mathbf{x})$, while the colour depends on both, $\mathbf{c} = \mathbf{c}(\mathbf{x}, \mathbf{d})$. Two details matter for quality. Inputs pass through a positional encoding with $L = 10$ frequencies for position and $L = 4$ for direction, which lets the network represent high-frequency detail. Sampling is hierarchical: a coarse network is evaluated at $N_c = 64$ points along each ray, and a fine network at $N_f = 128$ points placed where the coarse density is high.

## Equation

The colour of a pixel is the volume rendering integral along the camera ray $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$:

$$C(\mathbf{r}) = \int_{t_n}^{t_f} T(t)\,\sigma(\mathbf{r}(t))\,\mathbf{c}(\mathbf{r}(t), \mathbf{d})\,dt, \qquad T(t) = \exp\!\left(-\int_{t_n}^{t}\sigma(\mathbf{r}(s))\,ds\right)$$

Here $T(t)$ is the accumulated transmittance. The training loss sums the squared error between rendered and observed pixel colours for the coarse and fine renderings (Eq. 6 of the paper).

## Results

The abstract reports state-of-the-art novel-view synthesis for complex scenes. The paper reports 100,000 to 300,000 training iterations on a single V100 GPU, about one to two days per scene, and about 30 seconds to render a frame. Comparisons with prior methods are in the paper's results tables.

## Limitations

- Each scene needs its own optimisation, which takes about one to two days on the paper's hardware.
- Rendering one frame takes about 30 seconds.
- The method assumes a static scene and known camera poses. For real data, the paper estimates the poses with COLMAP.

## Connections

The explicit alternative to this implicit representation is [3D Gaussian splatting](gaussian-splatting.md). Training uses gradients through the rendering integral, which are computed as described in [Automatic differentiation](../../../math/automatic-differentiation/index.md).

## Open questions

- Can radiance fields be trained and rendered at interactive speed without losing quality?
- How should the representation handle moving objects and changing lighting?

## References

### Seminal papers

- Mildenhall, Srinivasan, Tancik, Barron, Ramamoorthi and Ng, *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*, European Conference on Computer Vision (2020). https://doi.org/10.1007/978-3-030-58452-8_24 — The NeRF paper, with the volume rendering formulation and positional encoding.
- Barron et al., *Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields*, IEEE/CVF International Conference on Computer Vision (2021). https://doi.org/10.1109/iccv48922.2021.00580 — Extends NeRF with a multiscale representation for anti-aliasing.
- Kerbl, Kopanas, Leimkuehler and Drettakis, *3D Gaussian Splatting for Real-Time Radiance Field Rendering*, ACM Transactions on Graphics (2023). https://doi.org/10.1145/3592433 — Introduces 3D Gaussian splatting, an explicit alternative to the NeRF representation.

### Surveys and textbooks

- Kajiya and Von Herzen, *Ray tracing volume densities*, SIGGRAPH (1984). https://doi.org/10.1145/964965.808594 — An early formulation of ray tracing through volume densities.
- Max, *Optical models for direct volume rendering*, IEEE Transactions on Visualization and Computer Graphics (1995). https://doi.org/10.1109/2945.468400 — A survey of the optical models behind volume rendering.
