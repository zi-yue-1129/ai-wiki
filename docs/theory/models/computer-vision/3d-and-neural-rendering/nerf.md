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

NeRF represents a scene as a neural network that maps a 3D position and a viewing direction to a colour and a density. New views are rendered by integrating that function along camera rays. It is the landmark method for learned view synthesis, and most later neural rendering work starts from it.

## Overview

[The chapter](index.md) describes the field. This page covers one method in detail: a multilayer perceptron fitted to a set of photographs of a fixed scene, so that it can render views from new camera positions.

## Problem

Given a few dozen images of a scene with known camera poses, produce photorealistic images from viewpoints that are not in the set. Earlier view-synthesis methods used discrete voxel grids or meshes, which were memory-hungry or lost fine detail.

## Core idea

The scene is a continuous function $F_\Theta(\mathbf{x}, \mathbf{d}) = (\mathbf{c}, \sigma)$. It takes a position $\mathbf{x}$ and a viewing direction $\mathbf{d}$, and returns an emitted colour $\mathbf{c}$ and a volume density $\sigma$. The network is trained so that rendered pixels match the photographs. Two details matter. Inputs are passed through a positional encoding, which lets the network represent high-frequency detail. The rendering samples points along each ray more densely where density is high, which the paper calls a hierarchical sampling strategy.

## Equation

The colour of a pixel is an integral along the camera ray $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$:

$$C(\mathbf{r}) = \int_{t_n}^{t_f} T(t)\,\sigma(\mathbf{r}(t))\,\mathbf{c}(\mathbf{r}(t), \mathbf{d})\,dt, \qquad T(t) = \exp\!\left(-\int_{t_n}^{t}\sigma(\mathbf{r}(s))\,ds\right)$$

Here $T(t)$ is the accumulated transmittance. The integral is approximated by sampling points along the ray, and the loss is the squared error between rendered and observed pixel colours.

## Results

The abstract reports state-of-the-art results for synthesising novel views of complex scenes. The comparisons with prior methods are in the paper's results tables, which this page does not restate.

## Limitations

- Training is slow, because each scene needs its own optimisation, and rendering needs many network evaluations per pixel.
- The representation is implicit, so editing, relighting and extracting geometry are harder than with meshes.
- The original method assumes static scenes and known camera poses.

Later work addressed these limits with faster grids and explicit representations, including [3D Gaussian splatting](gaussian-splatting.md).

## Connections

NeRF builds on the volume-rendering ideas that also appear in the [chapter overview](index.md). Its optimisation depends on the gradient machinery in [Automatic differentiation](../../../math/automatic-differentiation/index.md).

## Open questions

- Can radiance fields be trained and rendered at interactive speed without losing quality?
- How should the representation handle moving objects and changing lighting?

## References

### Seminal papers

- Mildenhall, Srinivasan, Tancik, Barron, Ramamoorthi and Ng, *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*, European Conference on Computer Vision (2020). https://doi.org/10.1007/978-3-030-58452-8_24 — The NeRF paper, including the volume rendering formulation and positional encoding.
- Barron et al., *Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields*, IEEE/CVF International Conference on Computer Vision (2021). https://doi.org/10.1109/iccv48922.2021.00580 — Extends NeRF with a multiscale representation that reduces aliasing.
- Kerbl, Kopanas, Leimkuehler and Drettakis, *3D Gaussian Splatting for Real-Time Radiance Field Rendering*, ACM Transactions on Graphics (2023). https://doi.org/10.1145/3592433 — An explicit alternative to the implicit NeRF representation.

### Surveys and textbooks

- Kajiya and Von Herzen, *Ray tracing volume densities*, SIGGRAPH (1984). https://doi.org/10.1145/964965.808594 — The early formulation of rendering through participating media that NeRF's integral builds on.
- Max, *Optical models for direct volume rendering*, IEEE Transactions on Visualization and Computer Graphics (1995). https://doi.org/10.1109/2945.468400 — A survey of the optical models behind volume rendering.
