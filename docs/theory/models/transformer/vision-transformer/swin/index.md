---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/vision-transformer
  - theory/models/cnn/backbones-and-scaling
  - theory/models/computer-vision
tags:
  - transformers
  - computer vision
  - vision backbones
  - dense prediction
aliases:
  - Swin
  - Swin Transformer
  - Shifted windows
  - 移位視窗 Transformer
---

# Swin Transformer

The Swin Transformer is a hierarchical [Vision Transformer](../index.md) that computes self-attention only inside local windows, and shifts the windows from one layer to the next so information can flow between them. Liu et al. (2021) use this design to build a general-purpose backbone for classification, detection and segmentation, with cost that grows linearly with image size.

## Overview

The [ViT](../index.md) computes global self-attention over every patch. That cost grows with the square of the number of patches, which makes high-resolution images and dense prediction expensive, and it gives a single-scale feature map. Swin keeps the Transformer block but restricts attention to windows, and merges patches between stages to build a feature pyramid like those of CNN backbones. That makes it usable for detection and segmentation, where ViT was harder to adapt.

## Key concepts

- **Window**: a non-overlapping group of \(M \times M\) patches inside which self-attention is computed. The default is \(M = 7\).
- **Shifted window**: the partition is moved by \((\lfloor M/2 \rfloor, \lfloor M/2 \rfloor)\) pixels in alternating layers, so each window overlaps its neighbours in the next layer.
- **Patch merging**: a layer that concatenates each \(2 \times 2\) group of neighbouring patches and projects them to \(2C\) channels, halving the resolution.
- **Relative position bias**: a learned bias added to the attention logits, indexed by the relative offset between two patches.
- **Model variants**: Swin-T, Swin-S, Swin-B and Swin-L, differing in base channel width \(C\) and layer depths.

## How it works

The network has four stages. The first stage splits the image into \(4 \times 4\) patches and projects them to width \(C\). Each later stage starts with a patch merging layer, which halves the resolution and doubles the channels, and then applies blocks in pairs: a regular window block, then a shifted window block. Each pair is:

\[
\hat z^{l} = \mathrm{W\text{-}MSA}\big(\mathrm{LN}(z^{l-1})\big) + z^{l-1}, \qquad
z^{l} = \mathrm{MLP}\big(\mathrm{LN}(\hat z^{l})\big) + \hat z^{l}
\]

followed by the same pattern with the shifted-window attention (SW-MSA). Attention within a window is

\[
\mathrm{Attention}(Q, K, V) = \mathrm{SoftMax}\!\left(\frac{QK^\top}{\sqrt{d}} + B\right)V
\]

where \(B\) is the relative position bias, taken from a smaller learned table of size \((2M-1)\times(2M-1)\). For the shifted windows, the paper uses a cyclic shift of the feature map and an attention mask that limits self-attention to within each sub-window.

The cost comparison in the paper is \(\Omega(\text{MSA}) = 4hwC^2 + 2(hw)^2C\) for global attention and \(\Omega(\text{W-MSA}) = 4hwC^2 + 2M^2hwC\) for windowed attention. The first term grows with the square of the number of patches \(hw\), and the second grows linearly with it when \(M\) is fixed.

## Key methods

### Swin Transformer: Hierarchical Vision Transformer using Shifted Windows (Liu et al., 2021)

- **Problem:** Transformers had become strong vision backbones, but a plain ViT has global attention and one scale of features, which makes it costly for high-resolution inputs and awkward for detection and segmentation.
- **Core idea:** Restrict self-attention to local windows, shift the windows between layers so that windows connect, and merge patches between stages to build a hierarchy.
- **Equation or algorithm:** The window attention with relative position bias, the shifted-window mechanism with masking, and the patch merging layer described above.
- **Results:** The abstract reports 87.3% top-1 accuracy on ImageNet-1K for its largest model after ImageNet-22K pre-training, 58.7 box AP and 51.1 mask AP on COCO test-dev, and 53.5 mIoU on ADE20K validation. The paper says these results surpass the previous state of the art by +2.7 box AP and +2.6 mask AP on COCO, and by +3.2 mIoU on ADE20K. In the paper's Table 1, Swin-T reaches 81.3% top-1 with 29M parameters at \(224^2\), and Swin-S reaches 83.0% with 50M. The paper's Table 1 lists Swin-B at 83.5% with 88M parameters, and another table in the paper gives 83.3% for the same setting.
- **Limitations:** Windowed attention limits the direct interaction between distant patches, so the shifted windows must do the work of mixing information across the image. The window size \(M\) is a fixed hyperparameter, and the paper uses \(M = 7\) by default. The reported top-1 accuracy for Swin-L is given after ImageNet-22K pre-training, not from ImageNet-1K alone.

## Components and variants

- **Model sizes.** Swin-T uses base width \(C = 96\) with depths \(\{2, 2, 6, 2\}\). Swin-S uses \(C = 96\) with depths \(\{2, 2, 18, 2\}\). Swin-B uses \(C = 128\) with the same depths as Swin-S. Swin-L uses \(C = 192\).
- **Window size.** The default \(M = 7\) keeps the windowed cost linear. Larger windows approach global attention at higher cost.
- **Relative position bias.** A learned table indexed by relative offset replaces absolute position embeddings, which lets the model generalise across windows.

## Connections

- [Vision Transformer (ViT)](../index.md) is the global-attention baseline that Swin changes.
- [DeiT](../deit/index.md) is a ViT training recipe with global attention, and it is a useful contrast to Swin's architectural change.
- [ConvNeXt](../../../cnn/backbones-and-scaling/convnext/index.md) is the convnet that the ConvNeXt paper compares directly against Swin on the same detection and segmentation benchmarks.
- [Transformers & Attention](../../index.md) gives the attention block that Swin modifies.
- [Computer vision](../../../computer-vision/index.md) lists Swin among the backbones used for detection and segmentation.

## Open questions

- **Locality versus global context.** Shifted windows connect distant regions only over several layers. Whether this gives the same long-range modelling as global attention, for tasks that need it, is not settled.
- **Hand-designed hierarchy.** The stage layout and window size are chosen by hand. Whether the gains come from the hierarchy or from the window attention itself is hard to separate.
- **Comparison with convnets.** Later convnet work reports results that match Swin on the same benchmarks. Which design choices account for the gap is still discussed.

## References

### Seminal papers

- Liu, Z., et al. (2021). *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*. ICCV 2021. [DOI 10.1109/ICCV48922.2021.00986](https://doi.org/10.1109/ICCV48922.2021.00986). Also [arXiv:2103.14030](https://arxiv.org/abs/2103.14030) — Introduces Swin, with shifted-window attention and a hierarchical design.
- Dosovitskiy, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929) — The global-attention ViT that Swin modifies.
- Liu, Z., et al. (2022). *A ConvNet for the 2020s*. CVPR 2022. [DOI 10.1109/CVPR52688.2022.01167](https://doi.org/10.1109/CVPR52688.2022.01167) — A convnet that compares directly with Swin on ImageNet, COCO and ADE20K.
- Touvron, H., et al. (2021). *Training data-efficient image transformers & distillation through attention*. ICML 2021, PMLR 139. [arXiv:2012.12877](https://arxiv.org/abs/2012.12877) — DeiT, a ViT that keeps global attention and is trained on ImageNet alone, the contrast case for Swin's windowed design.

### Surveys and textbooks

(none checked for this page)

### Lectures

(none checked for this page)

### Articles and documentation

- Microsoft, *Swin-Transformer*, GitHub. [microsoft/Swin-Transformer](https://github.com/microsoft/Swin-Transformer) — The official code and models, linked from the arXiv abstract.

## Further learning

(none added yet)
