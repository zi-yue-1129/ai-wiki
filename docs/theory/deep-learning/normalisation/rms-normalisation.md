---
status: complete
last_reviewed: 2026-11-05
related:
  - theory/deep-learning/normalisation
  - theory/models/transformer
tags:
  - RMSNorm
  - normalisation
  - language models
aliases:
  - 均方根正規化
  - RMSNorm
  - Root mean square layer normalization
---

# RMSNorm

RMSNorm rescales a feature vector using its root mean square without subtracting its mean. It retains a scale-normalisation mechanism while giving up the shift invariance of LayerNorm. Zhang and Sennrich introduced it as a simpler normaliser and evaluated it across several model families.[^rms]

## Problem and scope

The [normalisation chapter](index.md) compares the family. LayerNorm computes a mean and a centred second moment over selected features. RMSNorm asks whether normalising the uncentred second moment alone can provide useful training behaviour with less computation.

This is a choice of normalisation statistic, separate from where the layer sits in a model. RMSNorm can be used in recurrent and feedforward models as well as in Transformer residual blocks.[^rms]

## Equation and axes

For one normalised group $x\in\mathbb{R}^d$, define the mean square $q$ and a stabilised denominator $r_\epsilon$:

$$
q=\frac{1}{d}\sum_{i=1}^{d}x_i^2,\qquad
r_\epsilon=\sqrt{q+\epsilon},\qquad
y_i=g_i\frac{x_i}{r_\epsilon}.
$$

Here $g_i$ is a learned gain and $\epsilon>0$ stabilises division near zero. The mathematical RMS is $\sqrt q$; $r_\epsilon$ includes the implementation's stabiliser. The displayed form has no additive bias.[^implementation]

Removing mean subtraction does not prohibit a later bias. The original paper writes an activation of the form $f(\bar a_i+b_i)$ after its normalised, gain-scaled value. PyTorch's RMSNorm module exposes a gain but no bias argument. Bias handling therefore needs to be checked in the specific model or implementation.[^rms][^implementation]

For activations shaped $[B,T,D]$, a common language-model choice is one group of $D$ features per token. Normalising over $[T,D]$ instead would couple different tokens. In PyTorch 2.15, the module reduces over the trailing dimensions specified by its normalised shape; using shape $D$ and shape $(T,D)$ are different operations. No statistics from other batch elements are needed.[^implementation]

## RMS is not standard deviation

Let $\mu=d^{-1}\sum_i x_i$ and $\sigma^2=d^{-1}\sum_i(x_i-\mu)^2$. Then $q=\sigma^2+\mu^2$: an uncentred second moment includes both spread and mean offset.

For comparison, LayerNorm uses

$$
y_i^{\mathrm{LN}}=g_i\frac{x_i-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta_i.
$$

Its centring step changes the normalised representation even when the two layers use identical gains and epsilon.[^layernorm]

Before applying gain or bias, put $z_i=x_i/r_\epsilon$. Its feature mean and mean square are

$$
\frac{1}{d}\sum_i z_i=\frac{\mu}{\sqrt{q+\epsilon}},\qquad
\frac{1}{d}\sum_i z_i^2=\frac{q}{q+\epsilon}.
$$

Thus RMSNorm does not generally produce zero mean or unit variance. Even its mean square is exactly one only in the idealised case $\epsilon=0$ with $q>0$. Learned per-feature gains can change these statistics further.

### Worked comparison

These are original calculations, not benchmark measurements. Use unit gains, no biases and $\epsilon=0$ for the nonconstant vectors below:

| Input | Mean | RMS | RMS-normalised output | Layer-normalised output |
|---|---|---|---|---|
| $(1,3)$ | 2 | $\sqrt5$ | $(0.4472,1.3416)$ | $(-1,1)$ |
| $(2,6)$ | 4 | $\sqrt{20}$ | $(0.4472,1.3416)$ | $(-1,1)$ |
| $(3,5)$ | 4 | $\sqrt{17}$ | $(0.7276,1.2127)$ | $(-1,1)$ |

Doubling $(1,3)$ leaves its ideal RMS-normalised output unchanged. Adding 2 to each feature changes that output, while the centred LayerNorm output is unchanged. These two transformations test different invariances.

For a constant nonzero vector and positive epsilon, LayerNorm's centred output is zero before affine parameters. RMSNorm instead retains a nonzero signal. At the zero vector, positive epsilon gives a finite denominator and zero output in either case.

## Scale invariance and epsilon

For nonzero $x$ and a positive scalar $c$, the unstabilised RMS satisfies $\mathrm{RMS}(cx)=c\,\mathrm{RMS}(x)$. Consequently, ideal RMS normalisation is invariant to positive rescaling. A negative scalar reverses the normalised vector's sign.

A fixed positive epsilon makes scale invariance approximate:

$$
z_\epsilon(cx)=\frac{cx}{\sqrt{c^2q+\epsilon}}
=\frac{x}{\sqrt{q+\epsilon/c^2}}\qquad(c>0).
$$

The difference becomes small when $q$ dominates both $\epsilon$ and $\epsilon/c^2$. It can matter near zero. This qualifies the paper's ideal rescaling analysis rather than contradicting it.[^rms]

For example, take $x=(0.001,0.001)$, $c=2$ and $\epsilon=10^{-6}$. Each output coordinate changes from approximately 0.7071 to 0.8944. An implementation test that expects exact scale invariance with finite epsilon would therefore be incorrect.

## Implementation checks

- **Axes and parameters.** Record the normalised shape, learned gain, any separate bias and residual placement. Shape agreement alone does not establish equivalence.
- **Epsilon convention.** Adding epsilon inside the square root differs from adding it after the square root. Copying weights between these formulas does not make their outputs identical.
- **Precision and defaults.** Record epsilon explicitly when comparing implementations. PyTorch 2.15 documents its omitted-epsilon default using the computation type: fp16/bf16/fp32 inputs use float32 machine epsilon, while fp64 inputs use float64 machine epsilon.[^implementation]
- **Training and evaluation.** The displayed RMS statistic is computed from the current group, without BatchNorm-style running batch statistics. This describes the normaliser, not the behaviour of dropout or other layers elsewhere in the model.[^batchnorm]

## Results and limitations

The original paper reports comparable task performance to LayerNorm with running-time reductions ranging from 7% to 64% across its tested configurations. These are model- and implementation-dependent results, not a guaranteed reduction in modern language-model decoding time.[^results]

A concrete example is Table 2's TensorFlow/Nematus RNNSearch translation experiment: LayerNorm takes $665\pm32.5$ seconds per 1,000 training steps, versus $501\pm11.8$ seconds for RMSNorm. Using the reported central values gives a time reduction of $(665-501)/665\approx24.7\%$, or about $665/501\approx1.33$ times the step throughput. Time reduction and throughput increase use different denominators.[^results]

The paper also studies **partial RMSNorm**, which estimates the statistic using a subset of features. That changes the estimator and is distinct from ordinary full-feature RMSNorm; fewer arithmetic operations do not by themselves guarantee lower wall-clock time.[^partial]

Performance comparisons should specify hardware, precision, tensor shapes, kernels and workload, then check both task quality and end-to-end time. Dropping centring changes the function: replacing LayerNorm in an already trained checkpoint is not generally an output-preserving rewrite.

## Connections and applications

LLaMA is a concrete language-model example: its architecture section specifies RMSNorm for pre-normalisation of Transformer sublayers.[^llama] The [Transformer page](../../models/transformer/index.md) explains the broader block structure.

Xiong et al. analyse LayerNorm placement in Transformers; that work motivates treating placement and the chosen statistic as separate design decisions. It does not prove that every RMSNorm model can use the same optimiser settings or omit warm-up.[^placement]

[LayerNorm](../../models/mlp/layer-normalisation/index.md) retains centring, while BatchNorm uses statistics across training examples.[^layernorm][^batchnorm] Choosing among them requires considering which feature groups and transformations should be normalised, as well as the measured cost.

## Open questions

When does preserving a feature mean help or hurt a particular task? How do epsilon, precision and fused implementations affect behaviour for small activations? The original efficiency results do not settle these questions for every architecture.

[^rms]: Zhang and Sennrich (2019), sections 3–4 and 4.1: the normalised value, subsequent bias/activation and ideal invariance analysis.
[^layernorm]: Ba, Kiros and Hinton (2016), *Layer Normalization*: per-case mean/variance statistics and learned gain and bias.
[^implementation]: PyTorch 2.15, *RMSNorm* API documentation: trailing normalised axes, gain-only module, epsilon placement and computation-type default.
[^batchnorm]: Ioffe and Szegedy (2015), *Batch Normalization*, contrasted with the per-group RMS formula on this page.
[^results]: Zhang and Sennrich (2019), abstract and section 6, especially Table 2: runtime range, translation setup and time per 1,000 training steps.
[^partial]: Zhang and Sennrich (2019), section 5 and section 6.1: partial RMS estimation and implementation-dependent timing.
[^llama]: Touvron et al. (2023), section 2.2: RMSNorm and pre-normalisation in LLaMA.
[^placement]: Xiong et al. (2020), *On Layer Normalization in the Transformer Architecture*: placement-dependent gradient behaviour in LayerNorm Transformers.

## References

### Seminal papers

- Zhang, B. & Sennrich, R. (2019). *Root Mean Square Layer Normalization*. NeurIPS 2019. https://arxiv.org/abs/1910.07467 — Introduces full and partial RMSNorm, with invariance analysis and task timings.
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). *Layer Normalization*. https://arxiv.org/abs/1607.06450 — Defines per-case feature centring, variance normalisation and learned affine parameters.
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*. https://arxiv.org/abs/1502.03167 — Introduces batch-dependent normalisation for comparison with per-case feature statistics.
- Xiong, R. et al. (2020). *On Layer Normalization in the Transformer Architecture*. https://arxiv.org/abs/2002.04745 — Analyses how LayerNorm placement affects initial gradients and warm-up requirements.
- Touvron, H. et al. (2023). *LLaMA: Open and Efficient Foundation Language Models*. https://arxiv.org/abs/2302.13971 — Documents RMSNorm pre-normalisation as part of the LLaMA architecture.

### Articles and documentation

- PyTorch contributors. *RMSNorm*, PyTorch 2.15 documentation. https://docs.pytorch.org/docs/2.15/generated/torch.nn.RMSNorm.html — Specifies normalised axes, affine gain, epsilon convention and numerical defaults.
