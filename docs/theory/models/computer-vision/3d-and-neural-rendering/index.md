---
status: draft
last_reviewed: 2026-10-28
related:
  - brain-mind/visual-perception
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
  - applications/creative
  - applications/autonomous-driving
tags:
  - computer vision
  - generative models
  - representation learning
aliases:
  - 3D vision
  - Neural rendering
  - 三維視覺
  - 神經渲染
  - 新視角合成
  - 三維重建
---

# 3D Vision and Neural Rendering

3D vision recovers the depth, shape and camera position behind a set of images, and neural rendering produces new images of a scene from a learned model of it. Modern systems combine the two, with networks estimating geometry and learned representations such as [NeRF](nerf/index.md) and [3D Gaussian splatting](gaussian-splatting/index.md) render photorealistic views from camera positions that were never photographed.

## Overview

A photograph discards depth. Points at different distances can produce the same colour, so one picture is consistent with many three-dimensional scenes. People resolve this with stereo disparity, motion parallax, shading and perspective, usually without noticing. Computer vision tries to recover the same information from pixels: how far each point is, what the surfaces are, and where the camera was. Neural rendering runs the process the other way. Given a model of a scene, it predicts the picture taken from a new viewpoint, a task called *novel view synthesis*.

Classical systems used explicit geometry such as meshes and voxel grids. From about 2020 the scene was stored in the weights of a neural network fitted to photographs. In 2023 explicit Gaussian primitives restored real-time display rates.[^1]

This page covers depth estimation, point clouds, radiance fields and generative 3D. Two-dimensional image generation is covered in [Generative Models](../../../paradigms/unsupervised/density-and-generative-models/generative-models/index.md).

## Key concepts

- **Depth map**: an image whose value at each pixel is the distance to the surface seen there. Estimating it from one image is ill-posed, and the overall scale is the largest uncertainty.[^2]
- **Point cloud**: an unordered set of 3D points, from a depth sensor such as LiDAR or from reconstruction. Since point order carries no meaning, networks for point clouds must be permutation-invariant.[^3]
- **Radiance field**: a function giving the colour and density at each 3D point for each viewing direction. Density describes how strongly a point absorbs or emits light.
- **Volume rendering**: forming a pixel by summing colours along its camera ray, weighted by density and transmittance.
- **Differentiable rendering**: a renderer whose output changes smoothly with the scene parameters, so pixels can be matched by gradient descent.
- **Score distillation**: using a pretrained 2D diffusion model as a critic of a 3D model's renderings.[^4]

## How it works

Most modern 3D systems share one loop. A scene representation with learnable parameters is rendered from known or estimated camera poses, the rendered pixels are compared with photographs, and the error is propagated back into the parameters. When the loss is small, the parameters are the 3D model.

```mermaid
flowchart LR
  P[Photographs and camera poses] --> R[Scene representation: network, grid or Gaussians]
  R --> D[Differentiable renderer]
  D --> C[Rendered pixels]
  C -- loss against photographs --> U[Gradient update]
  U -. updates parameters .-> R
```

The strands differ in what they predict and optimise.

**Depth from images.** Eigen et al. (2014) predicted depth from one photograph with two stacked networks, a coarse global one and a local refinement, trained with a scale-invariant error.[^5] MiDaS mixed datasets with incompatible depth annotations, using a loss invariant to changes in depth range and scale.[^6] Depth Anything scaled training to tens of millions of unlabelled images, annotated automatically, and reported strong zero-shot results.[^7] DUSt3R regresses a *pointmap*, a 3D position for every pixel in a shared frame, from two or more images without known calibration, using Transformer encoders and decoders.[^8]

**Point clouds.** PointNet consumes raw point sets. A shared multilayer perceptron processes each point and a symmetric pooling operation combines the results, so the output does not depend on point order. It serves classification, part segmentation and scene parsing.[^9] PointNet++ applies the idea hierarchically over nested neighbourhoods, capturing local structure as well as global shape.[^10]

**Radiance fields.** NeRF maps a 3D position and viewing direction to colour and density with a multilayer perceptron, and renders a pixel by integrating along its ray. 3D Gaussian splatting keeps the differentiable-rendering loop but uses explicit anisotropic Gaussians, projected and blended on the GPU. See [NeRF](nerf/index.md) and [3D Gaussian Splatting](gaussian-splatting/index.md).

**Generative 3D.** Generative 3D borrows priors from 2D diffusion models, because 3D training data is scarce. DreamFusion optimises a NeRF so that its renderings from random viewpoints look plausible to a frozen text-to-image diffusion model, with no 3D training data.[^11] Zero-1-to-3 fine-tunes a diffusion model to change the viewpoint of a single object, learning the camera controls from synthetic data.[^12]

## Key methods

Two landmark methods are compared below. Each links to its own page, which gives the equations, results and limitations.

| Method | Year | Representation | What separates it | Page |
|---|---|---|---|---|
| NeRF | 2020 | Implicit: an MLP queried along camera rays | A continuous scene function rendered by volume integration; slow per scene | [NeRF](nerf/index.md) |
| 3D Gaussian splatting | 2023 | Explicit: millions of anisotropic 3D Gaussians | Rasterised rather than ray-marched; real-time rendering with fast optimisation | [3D Gaussian Splatting](gaussian-splatting/index.md) |

## Connections

- **Brain and mind.** Binocular disparity, the small difference between the two eyes' images, is a strong cue to depth. Marr and Poggio (1979) proposed how the visual system matches the two images to recover depth.[^13] Hubel and Wiesel (1962) described neurons in cat visual cortex that respond to input from both eyes.[^14] See [Perception and the Visual System](../../../../brain-mind/visual-perception/index.md) and [Receptive Fields in Visual Cortex](../../../../brain-mind/neuroscience/receptive-fields-hubel-wiesel/index.md). Whether the brain stores scenes in a form comparable to a radiance field is not known.
- **Transformers.** DUSt3R uses Transformer encoders and decoders. See [Vision Transformer](../../transformer/vision-transformer/index.md).
- **Diffusion.** Score distillation and viewpoint-conditioned generation depend on [Diffusion Models](../../../paradigms/unsupervised/density-and-generative-models/diffusion/index.md).
- **Self-supervision.** Depth Anything learns from large pools of unlabelled images, as in [Self-Supervised Learning](../../../paradigms/self-supervised/index.md).

## Applications

- **Autonomous driving.** Depth and LiDAR point clouds locate vehicles, pedestrians and lanes in three dimensions. See [Autonomous Driving](../../../../applications/autonomous-driving/index.md).
- **Film, games and virtual production.** Captured scenes can be rendered from new camera paths, and generated assets can be placed into scenes. Tewari et al. (2021) survey neural rendering for photorealistic synthesis.[^1] See [Creative Applications](../../../../applications/creative/index.md).

## Open questions

- **Scale and metric depth.** Relative depth is easier to learn than depth in metres. Depth Anything reports strong results after fine-tuning on metric labels.[^7]
- **Sparse and unbounded scenes.** Radiance fields produce blur or artifacts where photographs are sparse or the scene is unbounded. Mip-NeRF 360 addresses this partly.[^15]
- **Geometry or appearance.** Radiance methods are judged by rendered images, yet many uses need accurate surfaces, which are often less accurate than the images.
- **Feed-forward or per-scene.** DUSt3R predicts geometry in one pass, whereas NeRF and Gaussian splatting optimise each scene. Whether feed-forward models can match optimisation quality is open.
- **Consistency.** A 2D prior judges each view separately, so generated objects can be inconsistent across viewpoints.

[^1]: Tewari et al. (2021) and Xie et al. (2021) review the field. Kerbl et al. (2023) report real-time rendering at 1080p.
[^2]: Eigen et al. (2014), abstract: a large source of uncertainty comes from the overall scale.
[^3]: Qi et al. (2016), abstract: point clouds are irregular, so the network must respect permutation invariance.
[^4]: Poole et al. (2022), abstract: a 2D diffusion model serves as a prior for optimising a parametric image generator.
[^5]: Eigen et al. (2014), abstract: a coarse global prediction is refined locally, with a scale-invariant error.
[^6]: Ranftl et al. (2019), abstract: the objective is invariant to changes in depth range and scale, and several datasets can be mixed.
[^7]: Yang et al. (2024), abstract: about 62 million unlabelled images are annotated automatically; fine-tuning with metric labels sets new state-of-the-art results.
[^8]: Wang et al. (2023), abstract: no prior calibration or pose information is needed.
[^9]: Qi et al. (2016), abstract: the architecture covers classification, part segmentation and scene parsing.
[^10]: Qi et al. (2017), title: hierarchical feature learning on point sets in a metric space.
[^11]: Poole et al. (2022), abstract: a randomly initialised NeRF is optimised so that its renderings achieve a low loss under the diffusion prior.
[^12]: Liu et al. (2023), abstract: the model is trained on synthetic data and generalises zero-shot to in-the-wild images.
[^13]: Marr and Poggio (1979), title: a computational theory of how human stereo vision recovers depth.
[^14]: Hubel and Wiesel (1962), title: binocular interaction in cat visual cortex.
[^15]: Barron et al. (2021, *Mip-NeRF 360*), abstract: NeRF-like models produce blurry renderings on unbounded scenes.

## References

### Seminal papers

- Marr, D. & Poggio, T. (1979). *A computational theory of human stereo vision*. Proceedings of the Royal Society of London, Series B. https://doi.org/10.1098/rspb.1979.0029 — A theory of how the visual system matches the two eyes' images.
- Hubel, D. H. & Wiesel, T. N. (1962). *Receptive fields, binocular interaction and functional architecture in the cat's visual cortex*. The Journal of Physiology. https://doi.org/10.1113/jphysiol.1962.sp006837 — Early recordings of binocular neurons in cat visual cortex.
- Eigen, D., Puhrsch, C. & Fergus, R. (2014). *Depth Map Prediction from a Single Image using a Multi-Scale Deep Network*. NeurIPS. https://arxiv.org/abs/1406.2283 — Coarse-to-fine networks for single-image depth, trained with a scale-invariant error.
- Ranftl, R., Lasinger, K., Hafner, D., Schindler, K. & Koltun, V. (2019). *Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-shot Cross-dataset Transfer*. arXiv. https://arxiv.org/abs/1907.01341 — One depth model trained on mixed datasets, with a loss invariant to depth range and scale.
- Yang, L., Kang, B., Huang, Z., Xu, X., Feng, J. & Zhao, H. (2024). *Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data*. CVPR. https://arxiv.org/abs/2401.10891 — A monocular depth foundation model trained on about 62 million unlabelled images.
- Wang, S., Leroy, V., Cabon, Y., Chidlovskii, B. & Revaud, J. (2023). *DUSt3R: Geometric 3D Vision Made Easy*. arXiv. https://arxiv.org/abs/2312.14132 — Regresses pointmaps from unposed images with a single model.
- Qi, C. R., Su, H., Mo, K. & Guibas, L. J. (2016). *PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation*. arXiv. https://arxiv.org/abs/1612.00593 — A network that consumes raw point clouds with permutation-invariant pooling.
- Qi, C. R., Yi, L., Su, H. & Guibas, L. J. (2017). *PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space*. NeurIPS. https://arxiv.org/abs/1706.02413 — A hierarchical extension of PointNet over nested neighbourhoods of points.
- Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T., Ramamoorthi, R. & Ng, R. (2020). *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*. ECCV. https://arxiv.org/abs/2003.08934 — Represents a static scene as a neural radiance field, optimised from posed photographs.
- Kerbl, B., Kopanas, G., Leimkühler, T. & Drettakis, G. (2023). *3D Gaussian Splatting for Real-Time Radiance Field Rendering*. ACM Transactions on Graphics. https://arxiv.org/abs/2308.04079 — Explicit anisotropic Gaussians, optimised from photographs and rendered in real time.
- Poole, B., Jain, A., Barron, J. T. & Mildenhall, B. (2022). *DreamFusion: Text-to-3D using 2D Diffusion*. arXiv. https://arxiv.org/abs/2209.14988 — Text-to-3D generation by distilling a frozen 2D diffusion model into a NeRF.
- Liu, R., Wu, R., Van Hoorick, B., Tokmakov, P., Zakharov, S. & Vondrick, C. (2023). *Zero-1-to-3: Zero-shot One Image to 3D Object*. ICCV. https://arxiv.org/abs/2303.11328 — A viewpoint-conditioned diffusion model that generates novel views of a single object.

- Barron, J. T., Mildenhall, B., Verbin, D., Srinivasan, P. P. & Hedman, P. (2021). *Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields*. arXiv. https://arxiv.org/abs/2111.12077 — Extends NeRF to unbounded 360-degree scenes.

### Surveys and textbooks

- Tewari, A., Thies, J., Mildenhall, B., Srinivasan, P., Tretschk, E., Wang, Y., et al. (2021). *Advances in Neural Rendering*. arXiv. https://arxiv.org/abs/2111.05849 — A survey of neural rendering and its scene representations.
- Xie, Y., Takikawa, T., Saito, S., Litany, O., Yan, S., Khan, N., et al. (2021). *Neural Fields in Visual Computing and Beyond*. arXiv. https://arxiv.org/abs/2111.11426 — A review of coordinate-based neural fields in visual computing.
- Chen, G. & Wang, W. (2024). *A Survey on 3D Gaussian Splatting*. arXiv. https://arxiv.org/abs/2401.03890 — A systematic overview of 3D Gaussian splatting, its principles and applications.
