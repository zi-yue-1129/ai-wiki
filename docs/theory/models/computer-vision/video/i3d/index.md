---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - computer vision
  - architecture
  - benchmarks
aliases:
  - I3D
  - Two-Stream Inflated 3D ConvNet
  - 膨脹三維卷積網路
  - 膨脹3D卷積
  - 雙流膨脹三維卷積網路
---

# Inflated 3D ConvNet (I3D)

I3D is a video classifier made by expanding a deep 2D image network, Inception-v1, into three dimensions. Because the expanded filters can start from ImageNet weights, the network can be pre-trained on a large video dataset. Carreira and Zisserman introduced it in 2017 with the Kinetics dataset. It is one of the methods on the [Video Understanding and Generation](../index.md) page.

## Overview

Before I3D, two designs dominated action recognition. Two-stream networks ran 2D ConvNets on frames and on precomputed optical flow, so motion entered only through the flow input.[^1] Full 3D convolutional networks, such as C3D, learned motion from pixels but had many more parameters than 2D networks and could not reuse image weights.[^2]

I3D keeps the 3D convolutions and inflates a proven image architecture to supply starting weights. The standard benchmarks were too small to separate architectures, which motivated Kinetics: 400 action classes, at least 400 clips each, about 240,000 training clips.[^3]

The two-stream design is loosely related to the two-streams hypothesis in neuroscience, which proposes a ventral pathway for objects and a dorsal pathway for motion.[^4] The resemblance is only one of organisation. See [Perception and the Visual System](../../../../../brain-mind/visual-perception/index.md).

## Key concepts

- **Spatio-temporal convolution.** A kernel spanning space and time, such as $3\times3\times3$, responds to patterns that move across frames.
- **Inflation.** Each $N\times N$ filter becomes $N\times N\times N$, and pooling kernels gain a temporal dimension.
- **Boring video.** A still image repeated over time, on which the network should match its output on the image. This holds when the 2D weights are copied $N$ times and divided by $N$.[^2]
- **Optical flow.** A field of apparent motion between frames, computed offline for the second stream.

## How it works

Each I3D network takes a short clip of frames and outputs class scores. The inflation rule is

$$
W^{\text{3D}}_{t} = \frac{1}{N}\,W, \qquad t = 1,\dots,N,
$$

where $W$ is the 2D weight. On a boring video the sum over $t$ returns $W$, so the response matches the image network.[^2]

The main model runs two I3D networks, one on RGB frames and one on flow, trained separately and averaged. It is a [convolutional network](../../../cnn/index.md) with one extra axis.

## Results

- **Kinetics-400 from scratch.** The two-stream I3D reaches 71.6% top-1 with RGB and flow together. A C3D-like network reaches 56.1%.
- **Kinetics-400 with ImageNet initialisation.** The two-stream I3D reaches 74.2% top-1 and 91.3% top-5. The earlier two-stream baseline reaches 65.6%.
- **UCF-101 and HMDB-51 after Kinetics pre-training.** The paper reports 98.0% and 80.9%.[^2] The strongest earlier entry, a residual two-stream network with hand-crafted trajectory features, reached 94.6% and 70.3%.

## Limitations

- **Heavy reliance on pre-training.** The strongest results need large-scale pre-training, and every architecture compared gains from Kinetics.[^2]
- **Flow is a separate, costly step.** Flow is computed offline. The authors suggest that iterative flow optimisation is why a flow stream still helps a feedforward RGB network.[^2]
- **Short temporal range.** The clips span short periods, so actions that unfold slowly are hard to model.[^5]

## Open questions

- Does inflation work as well for architectures other than Inception-v1?
- Is a separate flow stream still needed once networks are large and trained on enough video? SlowFast and TimeSformer work on RGB frames alone.[^5][^6]

[^1]: Simonyan and Zisserman (2014), abstract.
[^2]: Carreira and Zisserman (2017): Section 2 (inflation), Introduction (parameter count), Tables 3, 4 and 5. Accuracies are top-1 on Kinetics-400 and mean over three splits for UCF-101 and HMDB-51.
[^3]: Kay et al. (2017): 400 classes, at least 400 clips each, about ten seconds long. The 240,000 training clips figure is in Carreira and Zisserman (2017), Section 3.
[^4]: Goodale and Milner (1992). The two-stream paper notes the link without testing it.
[^5]: Feichtenhofer et al. (2018): a slow pathway at a low frame rate and a fast pathway at a high frame rate.
[^6]: Bertasius et al. (2021), abstract.

## References

### Seminal papers

- Szegedy, C., et al. (2014). *Going Deeper with Convolutions*. arXiv. https://arxiv.org/abs/1409.4842 — The Inception architecture, whose Inception-v1 variant I3D inflates.
- Russakovsky, O., et al. (2014). *ImageNet Large Scale Visual Recognition Challenge*. arXiv. https://arxiv.org/abs/1409.0575 — The ImageNet benchmark whose pre-trained weights initialise I3D.
- Soomro, K., Zamir, A. R. & Shah, M. (2012). *UCF101: A Dataset of 101 Human Actions Classes From Videos in The Wild*. arXiv. https://arxiv.org/abs/1212.0402 — The 101-class action dataset used for fine-tuning.
- Kuehne, H., Jhuang, H., Garrote, E., Poggio, T. & Serre, T. (2011). *HMDB: A large video database for human motion recognition*. ICCV. https://doi.org/10.1109/ICCV.2011.6126543 — The 51-class action dataset used for fine-tuning.
- Carreira, J. & Zisserman, A. (2017). *Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset*. arXiv. https://arxiv.org/abs/1705.07750 — Introduces I3D by inflating Inception-v1 and tests it on three datasets.
- Simonyan, K. & Zisserman, A. (2014). *Two-Stream Convolutional Networks for Action Recognition in Videos*. arXiv. https://arxiv.org/abs/1406.2199 — RGB and optical-flow ConvNets whose predictions are fused.
- Tran, D., et al. (2014). *Learning Spatiotemporal Features with 3D Convolutional Networks*. arXiv. https://arxiv.org/abs/1412.0767 — The C3D network, trained from scratch.
- Kay, W., et al. (2017). *The Kinetics Human Action Video Dataset*. arXiv. https://arxiv.org/abs/1705.06950 — The 400-class YouTube dataset used for pre-training.
- Feichtenhofer, C., Fan, H., Malik, J. & He, K. (2018). *SlowFast Networks for Video Recognition*. arXiv. https://arxiv.org/abs/1812.03982 — Slow and fast pathways that model semantics and motion.
- Bertasius, G., Wang, H. & Torresani, L. (2021). *Is Space-Time Attention All You Need for Video Understanding?* arXiv. https://arxiv.org/abs/2102.05095 — Introduces TimeSformer, a convolution-free video Transformer built on divided space-time self-attention.
- Goodale, M. A. & Milner, A. D. (1992). *Separate visual pathways for perception and action*. Trends in Neurosciences. https://doi.org/10.1016/0166-2236%2892%2990344-8 — The ventral and dorsal pathway account.
