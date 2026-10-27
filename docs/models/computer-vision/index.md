# Computer Vision

## Task map

| Task | Output | Representative models |
|---|---|---|
| Image classification | Class | ResNet, EfficientNet, ViT, ConvNeXt |
| Object detection | Boxes + classes | Faster R-CNN, YOLO family, DETR, RT-DETR |
| Semantic / instance / panoptic segmentation | Per-pixel labels | U-Net, Mask R-CNN, Mask2Former |
| Promptable segmentation | Masks for any object | SAM, SAM 2 (video) |
| Open-vocabulary detection | Find objects described in text | Grounding DINO, OWL-ViT |
| Pose estimation | Keypoints | OpenPose, ViTPose |
| Depth estimation | Depth map | Depth Anything, MiDaS |
| 3D reconstruction / novel views | 3D scene | NeRF, 3D Gaussian Splatting, DUSt3R |
| Video understanding | Actions, events | SlowFast, VideoMAE, video VLMs |
| Tracking | Trajectories | SORT, ByteTrack |
| OCR and document understanding | Text, layout | PaddleOCR, Donut, VLMs |
| Image generation and editing | Images | See [Generative Models](../generative/index.md) |

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

Yamins et al. (2014) found that CNNs that perform better at object recognition also better predict neural responses in monkey IT cortex, launching the "task-optimised deep networks as brain models" programme — see [NeuroAI](../../brain-mind/neuroai/index.md).

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

Medical imaging ([Healthcare](../../applications/healthcare/index.md)), autonomous driving ([Autonomous Driving](../../applications/autonomous-driving/index.md)), industrial inspection ([Manufacturing](../../applications/manufacturing/index.md)), crop monitoring, remote sensing, retail, security, sports analytics, AR/VR, and animal behaviour tracking in neuroscience (DeepLabCut).

## Resources

- Stanford CS231n
- [d2l: Computer Vision](https://d2l.ai/chapter_computer-vision/index.html)
- Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed. (free PDF)
- [Ultralytics](https://docs.ultralytics.com/), [Detectron2](https://github.com/facebookresearch/detectron2), [timm](https://github.com/huggingface/pytorch-image-models)
