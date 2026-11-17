---
status: complete
last_reviewed: 2026-11-06
related:
  - theory/deep-learning/normalisation
tags:
  - group normalisation
  - normalisation
  - small batches
aliases:
  - 群組正規化
  - 分組歸一化
  - Group normalization
---

# Group normalisation

Group normalisation (GN) divides a sample's channels into groups. Each group shares a mean and variance computed over its channels and spatial positions. This makes a sample's normalised activations independent of its batch neighbours at fixed parameters.[^gn]

## Motivation

During training, [batch normalisation](batch-normalisation.md) pools statistics across samples, typically also across spatial positions for each channel. A detector trained with high-resolution images may fit only a few images per device. With local batch statistics, changing the images on that device changes the estimate used for every image. Group normalisation computes statistics separately for each image, so the same operation can be used with different numbers of images per device.[^bn][^gn]

## Computation and axes

For an activation tensor $x$ with shape $[N,C,H,W]$, choose a positive integer number of groups $G$ that divides $C$. Each group contains $C/G$ channels. With zero-based indices, channel $c$ belongs to group $g(c)=\lfloor c/(C/G)\rfloor$. Let $\mathcal{S}_g$ contain the channel and spatial indices of group $g$, with $M=(C/G)HW$ entries. For sample $n$,

$$
\mu_{n,g}=\frac{1}{M}\sum_{(c,h,w)\in\mathcal{S}_g} x_{n,c,h,w},
\qquad
v_{n,g}=\frac{1}{M}\sum_{(c,h,w)\in\mathcal{S}_g}(x_{n,c,h,w}-\mu_{n,g})^2.
$$

The layer uses these statistics to centre and rescale each activation, then applies a per-channel affine transform.[^gn]

$$
y_{n,c,h,w}=\gamma_c
\frac{x_{n,c,h,w}-\mu_{n,g(c)}}{\sqrt{v_{n,g(c)}+\epsilon}}
+\beta_c.
$$

Here $\epsilon>0$ stabilises division for groups with small or zero variance. The variance uses the divisor $M$, corresponding to correction zero. The learned scale $\gamma_c$ and offset $\beta_c$ are shared across the spatial positions of a channel. PyTorch allows the affine transform to be disabled and uses current input statistics in both training and evaluation.[^torch-gn]

The reshape $[N,C,H,W]\to[N,G,C/G,H,W]$ exposes the reduction axes. Reduce over the final three dimensions and retain one mean and variance for each pair $(n,g)$. Restore the original shape before applying channel gains and offsets.[^gn]

### Worked example

Take one sample with four channels, one row and two spatial positions. Set $G=2$, use unit gains and zero offsets, and use the limit $\epsilon\to0^+$ since both variances are positive.

| Group | Values by channel | Mean | Variance | Normalised values by channel |
|---|---|---|---|---|
| 0 | $(1,3)$ and $(5,7)$ | 4 | 5 | $(-3,-1)/\sqrt{5}$ and $(1,3)/\sqrt{5}$ |
| 1 | $(10,14)$ and $(18,22)$ | 16 | 20 | $(-3,-1)/\sqrt{5}$ and $(1,3)/\sqrt{5}$ |

The first activation becomes $(1-4)/\sqrt{5}\approx-1.3416$. Both positions of each channel use the same group statistics. The second group is a positive rescaling and shift of the first, so their normalised values coincide in this limit. Positive epsilon changes the rescaling slightly.

## Relationship to other normalisers

| Setting | Reduction for each sample | Condition for matching another normaliser |
|---|---|---|
| $G=1$ | All channels and spatial positions | LayerNorm over $(C,H,W)$ gives the same standardised values with the same epsilon and variance convention. |
| $1<G<C$ | Each group of channels and its spatial positions | Each group has its own statistics. |
| $G=C$ | Spatial positions of each channel | InstanceNorm gives the same standardised values when it uses current sample statistics and the same epsilon and variance convention. |

Matching the standardised values is only one part of matching a layer. With affine parameters enabled, PyTorch's LayerNorm over $(C,H,W)$ assigns a scale and bias to each element. GroupNorm assigns one pair per channel and shares it across spatial positions. Full output equivalence requires matching those affine transforms as well.[^gn][^ln][^in][^torch-ln]

## Reported results

Wu and He's ImageNet study trained ResNet-50 on eight GPUs. BatchNorm computed statistics locally on each GPU. Table 2 reports the following validation errors at two per-device training batch sizes.[^results]

| Training images per GPU | BatchNorm error | GroupNorm error |
|---|---|---|
| 2 | 34.7% | 24.1% |
| 32 | 23.6% | 24.1% |

At two images per GPU, the difference is **10.6 percentage points**, equivalent to about a 30.5% relative reduction from the 34.7% baseline. At 32 images per GPU, BatchNorm leads by 0.5 percentage points. The result applies to the paper's training setup and its local BatchNorm baseline. The paper also evaluates detection and instance segmentation on COCO and video classification on Kinetics.[^results]

## Practical considerations

- **Group size.** A fixed number of groups yields different numbers of channels per group as layer width changes. The paper explores both choices. Check divisibility in each layer and compare valid settings on the target task.[^results][^torch-gn]
- **Spatial extent.** The number of values contributing to a group statistic is $(C/G)HW$. If this equals one, centring makes the standardised value zero and the output is the channel offset when affine parameters are enabled.
- **Training behaviour.** The independence of each sample's forward computation concerns the normaliser. Changing the training batch size can still change the gradients aggregated in each optimiser step.
- **Checkpoint compatibility.** A trained BatchNorm layer can use stored statistics at evaluation, whereas GroupNorm computes new statistics from each sample. A model swap therefore changes the function and requires evaluation.[^bn][^torch-gn]

## Connections

The [normalisation overview](index.md) compares the axes used by the main methods. [Layer normalisation](../../models/mlp/layer-normalisation/index.md) also computes statistics within each sample. [RMSNorm](rms-normalisation.md) uses an uncentred second moment, so it provides a separate choice of statistic.

[^gn]: Wu and He (2018), sections 3.1–3.2, equations 1–7 and Figure 3, define the group axes, affine transform and relationship to LayerNorm and InstanceNorm.
[^bn]: Ioffe and Szegedy (2015), section 3, describe minibatch statistics and the inference procedure.
[^ln]: Ba, Kiros and Hinton (2016), *Layer Normalization*, define sample-level statistics and learned affine parameters.
[^in]: Ulyanov, Vedaldi and Lempitsky (2016), *Instance Normalization*, describe spatial statistics per sample and channel, used in training and testing.
[^torch-gn]: PyTorch 2.15, *GroupNorm*, documents channel divisibility, variance convention, optional per-channel affine parameters and statistics in both modes.
[^torch-ln]: PyTorch 2.15, *LayerNorm*, documents trailing reduction axes and per-element affine parameters.
[^results]: Wu and He (2018), section 4.1 and Tables 2–3, specify the ImageNet batch and group comparisons. Sections 4.2–4.3 cover COCO and Kinetics.

## References

### Seminal papers

- Wu, Y. & He, K. (2018). *Group Normalization*. ECCV 2018. https://arxiv.org/abs/1803.08494 — Defines the group statistics and evaluates batch size and group division.
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*. https://arxiv.org/abs/1502.03167 — Describes minibatch statistics during training and fixed statistics for inference.
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). *Layer Normalization*. https://arxiv.org/abs/1607.06450 — Introduces per-sample feature statistics and learned scale and bias.
- Ulyanov, D., Vedaldi, A. & Lempitsky, V. (2016). *Instance Normalization: The Missing Ingredient for Fast Stylization*. https://arxiv.org/abs/1607.08022 — Introduces per-sample channel normalisation over spatial dimensions for style transfer.

### Articles and documentation

- PyTorch contributors. *GroupNorm*, PyTorch 2.15 documentation. https://docs.pytorch.org/docs/2.15/generated/torch.nn.GroupNorm.html — Specifies valid group counts, input statistics and channel affine parameters.
- PyTorch contributors. *LayerNorm*, PyTorch 2.15 documentation. https://docs.pytorch.org/docs/2.15/generated/torch.nn.LayerNorm.html — Specifies trailing normalisation axes and the affine parameter shapes.
