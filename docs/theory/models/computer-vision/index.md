---
related:
- brain-mind/neuroai
- applications/healthcare
- applications/autonomous-driving
- applications/manufacturing
---

# Computer Vision

## Task map

| Task | Output | Representative models |
|---|---|---|
| Image classification | Class | ResNet, EfficientNet, ViT, ConvNeXt |
| [Object detection](object-detection/index.md) | Boxes + classes | Faster R-CNN, YOLO family, DETR, RT-DETR |
| [Semantic / instance / panoptic segmentation](segmentation/index.md) | Per-pixel labels | U-Net, Mask R-CNN, Mask2Former |
| Promptable segmentation | Masks for any object | SAM, SAM 2 (video) |
| Open-vocabulary detection | Find objects described in text | Grounding DINO, OWL-ViT |
| Pose estimation | Keypoints | OpenPose, ViTPose |
| Depth estimation | Depth map | Depth Anything, MiDaS |
| [3D reconstruction / novel views](3d-and-neural-rendering/index.md) | 3D scene | NeRF, 3D Gaussian Splatting, DUSt3R |
| [Video understanding and generation](video/index.md) | Actions, events, generated clips | SlowFast, VideoMAE, video diffusion |
| Tracking | Trajectories | SORT, ByteTrack |
| OCR and document understanding | Text, layout | PaddleOCR, Donut, VLMs |
| Image generation and editing | Images | See [Generative Models](../../paradigms/unsupervised/density-and-generative-models/generative-models/index.md) |

## Evolution of architectures

1. **Hand-crafted features**: SIFT, HOG + SVM
2. **CNN era** (2012–2020): AlexNet → VGG → GoogLeNet → ResNet → EfficientNet
3. **Transformer era** (2020–): ViT treats 16×16 patches as tokens; Swin adds hierarchy and local windows
4. **Self-supervised vision foundation models**: DINO/DINOv2/DINOv3, MAE, CLIP — general visual features without labels
5. **Vision-language integration**: see [Multimodal Models](../multimodal/index.md)

## Convolution intuition

A small kernel slides over the image detecting local patterns. Three key properties:

- **Local receptive fields**
- **Weight sharing** across positions
- **Hierarchy**: stacked layers see larger regions and more abstract features

All three come straight from visual neuroscience:

| Visual cortex | CNN |
|---|---|
| Receptive fields (Hubel & Wiesel) | Local connectivity of kernels |
| V1 simple cells detect oriented edges | First-layer kernels learn Gabor-like filters |
| Complex cells tolerate position shifts | Pooling |
| V1 → V2 → V4 → IT hierarchy | Shallow → deep layers |
| IT neurons are object-selective | Deep-layer features |

Yamins et al. (2014) found that CNNs that perform better at object recognition also better predict neural responses in monkey IT cortex, launching the "task-optimised deep networks as brain models" programme — see [NeuroAI](../../../brain-mind/neuroai/index.md).

## Human vs machine vision

| Aspect | Humans | Deep networks |
|---|---|---|
| Preferred cue | Shape | ImageNet CNNs prefer texture (Geirhos et al., 2019); fixable with training |
| Adversarial examples | Barely affected | Tiny perturbations can flip predictions |
| Out-of-distribution generalisation | Strong | Weaker, though large-scale pre-training has narrowed the gap |
| Few-shot learning | One or two views suffice | Needs pre-training |
| Illusions | Susceptible to many | Some networks show similar illusions |
| Power | Visual cortex: a few watts | GPUs: hundreds of watts |

## Applications

Medical imaging ([Healthcare](../../../applications/healthcare/index.md)), autonomous driving ([Autonomous Driving](../../../applications/autonomous-driving/index.md)), industrial inspection ([Manufacturing](../../../applications/manufacturing/index.md)), crop monitoring, remote sensing, retail, security, sports analytics, AR/VR, and animal behaviour tracking in neuroscience (DeepLabCut).

## Resources

- Stanford CS231n
- [d2l: Computer Vision](https://d2l.ai/chapter_computer-vision/index.html)
- Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed. (free PDF)
- [Ultralytics](https://docs.ultralytics.com/), [Detectron2](https://github.com/facebookresearch/detectron2), [timm](https://github.com/huggingface/pytorch-image-models)

## References

### Seminal papers

- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). *ImageNet Classification with Deep Convolutional Neural Networks*. NeurIPS. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The AlexNet result that started the deep-learning era in vision.
- Redmon, J., et al. (2016). *You Only Look Once: Unified, Real-Time Object Detection*. CVPR. https://arxiv.org/abs/1506.02640 — Frames object detection as a single regression pass, enabling real-time detection.
- Ronneberger, O., et al. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. arXiv. https://arxiv.org/abs/1505.04597 — An encoder–decoder with skip connections, the standard architecture for pixel-level segmentation.
- Dosovitskiy, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR. https://arxiv.org/abs/2010.11929 — The Vision Transformer, which applies a plain Transformer to image patches.

### Surveys and textbooks

- Szeliski, R. *Computer Vision: Algorithms and Applications*, 2nd ed. https://szeliski.org/Book/ — A comprehensive textbook covering classical and learning-based vision; the author offers a free PDF for personal use.

### Lectures and videos

- Li, F.-F., Adeli, E., Johnson, J., et al. *CS231n: Deep Learning for Computer Vision*. Stanford University. https://cs231n.stanford.edu/ — A Stanford course on neural networks for visual recognition, with lecture materials and assignments.
