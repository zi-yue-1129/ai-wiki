---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- theory/models/cnn
tags:
- neuroscience
- perception
aliases:
  - Geirhos 2019
  - 形狀偏好
  - Shape Bias
  - Stylized-ImageNet
---

# Shape Bias in CNNs (Geirhos et al. 2019)

Geirhos et al. (2019) asked a simple question with a sharp answer: do convolutional networks trained on ImageNet recognise objects by their shape, as people do, or by their texture? They found that standard networks rely mainly on texture, and that the same architecture trained on a stylised version of ImageNet shifts toward shape. The paper matters for NeuroAI because it gives a concrete behavioural difference between networks and people, and a way to test whether a change in training closes it.

This page is part of [Perception and the Visual System](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Humans identify objects largely by shape, and they do so even when texture is misleading. A network can reach high accuracy on ImageNet without learning the same cue, because texture is often a reliable shortcut in natural photographs. If so, a network may succeed for the wrong reason, which would limit how far it can serve as a model of human vision.

## The approach

The authors created images with a texture–shape cue conflict. Each image keeps the shape of one object category but takes the texture of another category, produced by style transfer, so that shape and texture point to different labels. The classifier's choice then shows which cue it used. The authors call the stylised training set Stylized-ImageNet (SIN).

The steps were:

1. Build cue-conflict images by style transfer between ImageNet images.
2. Test standard ImageNet-trained networks and human observers on the conflict images.
3. Train the same architecture (ResNet-50) on a mixture of standard and stylised images, or on stylised images alone.
4. Measure accuracy on ImageNet, object detection on PASCAL VOC and MS COCO, and robustness to image distortions.

Step 3 is the intervention. Keeping the architecture fixed isolates the effect of the training data.

## Results

The study ran nine psychophysical experiments with 97 observers, totalling 48,560 trials. The main results are these.

- **Humans** chose the shape category on 95.9% of their correct decisions.
- **Standard ImageNet-trained CNNs** chose the texture category most of the time. Shape decisions were 17.2% for VGG-16, 31.2% for GoogLeNet, 42.9% for AlexNet and 22.1% for ResNet-50.
- **Training on SIN shifted the same ResNet-50** toward shape. Its shape bias rose from 22% to 81% of decisions on the cue-conflict images, compared with 95.9% for humans.

The detection and classification results for the same architecture, from Table 2 of the paper, are:

| Training data | ImageNet top-1 (%) | PASCAL VOC mAP50 (%) | MS COCO mAP50 (%) |
|---|---|---|---|
| ImageNet only | 76.13 | 70.7 | 52.3 |
| SIN only | 60.18 | 70.6 | 51.9 |
| SIN + ImageNet | 74.59 | 74.0 | 53.8 |
| SIN + ImageNet, then ImageNet fine-tuning ("Shape-ResNet") | 76.72 | 75.1 | 55.2 |

The shape-biased model matches or exceeds the standard model on classification, and it is better on object detection. The paper also reports greater robustness to image distortions for the shape-biased networks.

## Limitations

- **One intervention.** Stylised training changes one kind of shortcut. It does not give a full account of human vision, and it does not settle how people weigh shape and texture across all tasks.
- **Accuracy cost on SIN alone.** A network trained only on SIN reaches 60.18% top-1 on ImageNet, lower than the standard model, so the shape-biased representation is not automatically better for every purpose.
- **Behaviour, not mechanism.** The evidence is about which cue decides the label. It does not show that the internal computation matches human visual processing.

## Connections

- **Model comparison:** [Yamins et al. (2014)](../yamins-2014/index.md) showed that CNN features predict responses in higher visual cortex. This study asks which cue those networks rely on for classification.
- **CNN architecture:** the architecture family is covered on [CNN](../../../theory/models/cnn/index.md).
- **Perception:** the ventral and dorsal streams that shape human recognition are in [Perception and the Visual System](../index.md).

## Open questions

- **Does a shape bias make networks more brain-like?** It moves them closer to human behaviour on this test, but whether it also matches the internal computation is not shown.
- **Which training signals create shape bias?** The paper changes the data. Whether objectives, architectures or developmental-style training produce the same bias is an open question.

## References

### Seminal papers

- Geirhos, R., Rubisch, P., Michaelis, C., Bethge, M., Wichmann, F. A. & Brendel, W. (2019). ImageNet-trained CNNs are biased towards texture. *ICLR*. https://arxiv.org/abs/1811.12231 — Shows that ImageNet-trained CNNs rely on texture, and that training on Stylized-ImageNet gives a shape bias and better detection and robustness.
- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). ImageNet Classification with Deep Convolutional Neural Networks. *NeurIPS*. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The AlexNet paper that made deep convolutional networks the standard model for image recognition.
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that object-recognition performance predicts how well networks explain IT responses.

### Surveys and reviews

- Lindsay, G. W. (2021). Convolutional Neural Networks as a Model of the Visual System: Past, Present, and Future. *Journal of Cognitive Neuroscience*. https://doi.org/10.1162/jocn_a_01544 — A review of how CNNs have been used as models of the visual system.
- Goodale, M. A. & Milner, A. D. (1992). Separate visual pathways for perception and action. *Trends in Neurosciences*. https://doi.org/10.1016/0166-2236(92)90344-8 — Proposes the ventral (perception) and dorsal (action) streams of human vision.
