---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/computer-vision
  - brain-mind/neuroai
tags:
  - 3D vision
  - neural rendering
  - view synthesis
aliases:
  - 三維視覺
  - 神經渲染
  - 神經輻射場
  - Neural rendering
---

# 3D vision and neural rendering

3D vision asks machines to recover the geometry of a scene from images, and neural rendering asks them to produce new images of that scene from new viewpoints. The two problems meet in view synthesis, where a model learns a scene from a few photographs and renders it from positions it has never seen.

## Overview

A two-dimensional image records light arriving at one viewpoint. Depth, shape and occlusion are lost in that projection, so recovering them requires either many views or learned priors. Classical methods used multi-view geometry and triangulation. Learned methods instead fit a representation, often a neural network or a set of primitives, that can predict depth or render colour from a new camera.

## Key concepts

- **Depth estimation**: predicting the distance from the camera to each pixel, from one image or from several.
- **Point cloud**: a set of 3D points, usually from a depth sensor, used as a scene representation.
- **Radiance field**: a function that gives colour and density at each 3D position and viewing direction.
- **Volume rendering**: computing a pixel's colour by integrating colour and density along the camera ray.
- **Novel view synthesis**: rendering a scene from a camera position not in the training set.

## How it works

Depth estimation predicts a depth map from an image. Eigen, Puhrsch and Fergus used a multi-scale deep network for this purpose, combining a coarse global view with finer local detail [(Eigen et al., 2014)](https://arxiv.org/abs/1406.2283). Point-cloud networks treat the 3D data directly. PointNet processes an unordered set of points with a shared per-point network and a symmetric pooling step, so the output does not depend on the order of the points [(Charles et al., 2017)](https://doi.org/10.1109/CVPR.2017.16).

Neural rendering methods then use a scene representation to produce images. The two main families are covered on their own pages.

## Key methods

Two landmark methods define the current field.

- [NeRF](nerf.md): a neural radiance field, an MLP that maps a 3D position and viewing direction to colour and density, rendered by volume integration. It gives high-quality view synthesis but needs long per-scene optimisation.
- [3D Gaussian splatting](gaussian-splatting.md): an explicit scene of 3D Gaussians rendered by rasterisation. It was designed for fast rendering and fast training.

## Connections

The geometry used here overlaps with the 3D and perception topics in [Computer vision](../index.md). The rendering and optimisation steps rely on the differentiation covered in [Automatic differentiation](../../../math/automatic-differentiation/index.md). Work on how biological vision builds a 3D percept, through stereo and motion cues, is linked from [Brain and mind](../../../../brain-mind/index.md).

## Applications

Novel view synthesis is used for film and game asset capture, virtual tours, and mapping for robotics. Depth estimation supports autonomous driving, augmented reality and robotic grasping. Generative 3D, which creates scenes rather than reconstructing them, is an active research area that builds on the same representations.

## Open questions

- How can neural scene representations be made fast to train and fast to render at the same time?
- How should generative and reconstructive 3D models be combined when the input views are sparse or ambiguous?
- How well do learned depth and 3D models generalise outside the scenes they were trained on?

## References

### Seminal papers

- Mildenhall, Srinivasan, Tancik, Barron, Ramamoorthi and Ng, *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*, European Conference on Computer Vision (2020). https://doi.org/10.1007/978-3-030-58452-8_24 — Introduces the neural radiance field for view synthesis with volume rendering.
- Kerbl, Kopanas, Leimkuehler and Drettakis, *3D Gaussian Splatting for Real-Time Radiance Field Rendering*, ACM Transactions on Graphics (2023). https://doi.org/10.1145/3592433 — An explicit Gaussian scene representation for fast, high-quality rendering.
- Eigen, Puhrsch and Fergus, *Depth Map Prediction from a Single Image using a Multi-Scale Deep Network* (2014). https://arxiv.org/abs/1406.2283 — An early deep network for monocular depth prediction.
- Charles, Su, Mo and Guibas, *PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation*, IEEE Conference on Computer Vision and Pattern Recognition (2017). https://doi.org/10.1109/CVPR.2017.16 — A network that processes unordered point clouds directly.

### Surveys and textbooks

- Hartley and Zisserman, *Multiple View Geometry in Computer Vision*, Cambridge University Press (2004, second edition). https://doi.org/10.1017/CBO9780511811685 — The standard textbook on the multi-view geometry that learned 3D methods build on.
