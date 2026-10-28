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

Geirhos et al. (2019) asked a simple question with a sharp answer: do convolutional networks trained on ImageNet recognise objects by their shape, as people do, or by their texture? They found that standard networks rely mainly on texture, and that training on a shape-emphasising dataset shifts them toward shape. The paper matters for NeuroAI because it gives a concrete behavioural difference between networks and people, and a way to test whether a change in training closes it.

This page is part of [Perception and the Visual System](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Humans identify objects largely by shape, and they do so even when texture is misleading. A network can reach high accuracy on ImageNet without learning the same cue, because texture is often a reliable shortcut in natural photographs. If so, a network may succeed for the wrong reason, and this would limit how far it can serve as a model of human vision.

## The approach

The authors created a conflict dataset, which they called Stylized-ImageNet. Each image keeps the shape of its original object but takes the texture of a different image, produced by style transfer. Shape and texture then point to different categories, and the classifier's choice shows which cue it used.

The steps were:

1. Apply style transfer to ImageNet images, so that object shape and texture conflict.
2. Test standard ImageNet-trained networks and human observers on the conflict images.
3. Train the same architecture (ResNet-50) on a mixture of standard and stylised images.
4. Measure shape-based classification, object detection and robustness to image distortions.

Step 3 is the intervention. Keeping the architecture fixed isolates the effect of the training data.

## Results

The paper reports that:

- Standard networks trained on ImageNet relied mainly on texture, unlike humans.
- Training on the stylised data shifted the same architecture toward shape-based recognition, which matched human behaviour more closely.
- The shape-biased networks improved object detection and robustness to image distortions.

The summary used for this page gives these results qualitatively. Check the full paper before quoting figures.

## Limitations

- The style-transfer data intervenes on one kind of shortcut. It is not a full account of human vision, and it does not settle how people weigh shape and texture across all tasks.
- A shape bias does not remove other failures. Networks can remain vulnerable to small adversarial changes that people ignore.
- The comparison depends on the chosen architecture and dataset, so the size of the effect may vary with other models.

## Connections

- **Model comparison**: this study uses the same convolutional family examined in [Yamins et al. (2014)](../yamins-2014/index.md), but tests what the networks learn rather than how well they predict neurons.
- **CNN architecture**: the architecture family is covered on [CNN](../../../theory/models/cnn/index.md).
- **Perception**: the ventral and dorsal streams that shape human recognition are in [Perception and the Visual System](../index.md).

## Open questions

- **Does a shape bias make networks more brain-like?** It makes them closer to human behaviour on this test, but whether it also matches the internal computation is not shown.
- **Which training signals create shape bias?** The paper changes the data. Whether objectives, architectures or developmental-style training produce the same bias is an open question.

## References

### Seminal papers

- Geirhos, R., Rubisch, P., Michaelis, C., Bethge, M., Wichmann, F. A. & Brendel, W. (2019). ImageNet-trained CNNs are biased towards texture. *ICLR*. https://arxiv.org/abs/1811.12231 — Shows that standard CNNs rely on texture, and that stylised training shifts them toward shape.
- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). ImageNet Classification with Deep Convolutional Neural Networks. *NeurIPS*. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The AlexNet paper that made deep convolutional networks the standard model for image recognition.
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that object-recognition performance predicts how well networks explain IT responses.

### Surveys and reviews

- Lindsay, G. W. (2021). Convolutional Neural Networks as a Model of the Visual System: Past, Present, and Future. *Journal of Cognitive Neuroscience*. https://doi.org/10.1162/jocn_a_01544 — A review of how CNNs have been used as models of the visual system, and what they explain and miss.
- Goodale, M. A. & Milner, A. D. (1992). Separate visual pathways for perception and action. *Trends in Neurosciences*. https://pubmed.ncbi.nlm.nih.gov/1374953/ — The ventral and dorsal streams that set up the human-side contrast in the shape question.
