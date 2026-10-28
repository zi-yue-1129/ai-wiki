---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math/automatic-differentiation
  - theory/models/transformer
  - brain-mind/attention-brain-machine
tags:
  - computer vision
  - transformers
  - neuroscience
aliases:
  - 特徵歸因
  - 顯著性方法
  - 積分梯度
  - 夏普利值
  - Feature attribution
  - Integrated Gradients
  - Shapley value
  - LIME
  - SHAP
  - Grad-CAM
---

# Feature attribution: SHAP, LIME and saliency

Feature attribution methods give each input feature a score for how much it contributed to one prediction. The family includes gradient-based saliency maps, Integrated Gradients, perturbation methods such as LIME, and Shapley-value methods such as SHAP. The outputs are easy to read, but several of these methods have failed basic tests.

## Overview

Take a trained model and one input. An attribution method returns one number per input feature (a pixel, a token or a table column) saying how much that feature pushed the output toward the predicted class, relative to a reference. Attribution is local: it explains one decision, not the whole model. It belongs to [explainable AI](index.md); the circuit-level work in [mechanistic interpretability](mechanistic-interpretability.md) asks which internal units carry out the computation instead.

Two families dominate. Gradient methods ask how the output changes when the input moves slightly. Perturbation and game-theoretic methods ask how the output changes when features are removed or averaged over.

## Key concepts

- **Baseline (reference input)**: what "absent" means for a feature, such as a black image or a zero embedding. Most attribution values are measured against it.
- **Completeness**: the scores add up to the difference between the output for the input and the output for the baseline. Integrated Gradients and Shapley values have this property; a plain gradient map does not.
- **Shapley value**: a feature's average marginal contribution over all subsets of the other features, from cooperative game theory (Shapley, 1953).

## How it works

**Gradients.** Simonyan et al. (2013) used the gradient of the class score with respect to the input, in absolute value, as a saliency map. Grad-CAM averages the gradient at the last convolutional layer over space, channel by channel, and produces a coarse heat map (Selvaraju et al., 2017).

**Integrated Gradients.** Sundararajan et al. (2017) integrate the gradient along a straight path from a baseline $x'$ to the input $x$:

$$\mathrm{IG}_i(x) = (x_i - x'_i)\int_0^1 \frac{\partial F\big(x' + \alpha(x - x')\big)}{\partial x_i}\,d\alpha$$

The attributions add up to $F(x) - F(x')$, so the baseline determines what the result means.

**LIME.** Ribeiro et al. (2016) sample perturbed versions of the input, such as sentences with some words removed, weight each by its similarity to the original, and fit a sparse linear model $g$ to the black box's outputs:

$$\xi(x) = \arg\min_{g \in G}\; \mathcal{L}(f, g, \pi_x) + \Omega(g)$$

Here $\pi_x$ measures proximity and $\Omega$ penalises complexity. The coefficients of $g$ are the explanation.

**Shapley values (SHAP).** The Shapley value of feature $i$ is

$$\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(|N|-|S|-1)!}{|N|!}\,\big[v(S \cup \{i\}) - v(S)\big]$$

Lundberg and Lee (2017) showed that LIME, DeepLIFT and related methods are additive feature attributions, and that Shapley values are the only additive attribution satisfying local accuracy, missingness and consistency. The exact sum has exponentially many terms. TreeSHAP computes it exactly for tree ensembles in polynomial time (Lundberg et al., 2020).

## Key methods

The table compares the main methods. Each has a known weakness.

| Method | Idea | Known weakness |
|---|---|---|
| Gradient saliency (Simonyan et al., 2013) | Gradient of the class score with respect to the input | Noisy and sensitive to small input changes |
| Grad-CAM (Selvaraju et al., 2017) | Class-weighted activation maps at a convolutional layer | Coarse resolution; defined for convolutional networks |
| DeepLIFT (Shrikumar et al., 2017) | Propagates activation differences from a reference backward | Depends on the reference activations |
| Integrated Gradients (Sundararajan et al., 2017) | Averages gradients along a path from a baseline | Depends on the baseline and path |
| LIME (Ribeiro et al., 2016) | Local sparse linear surrogate fitted to perturbed samples | Varies with sampling; can be gamed (Slack et al., 2020) |
| SHAP (Lundberg & Lee, 2017) | Shapley values of a value function | Exponential cost; the value function must be chosen |

**Sanity checks.** Adebayo et al. (2018) asked whether saliency maps depend on what the model has learned. When the trained weights were replaced layer by layer with random ones, several popular methods produced nearly unchanged maps. Hooker et al. (2019) removed the features each method ranked highest, retrained, and found that many methods were no better than a random ranking.

**Transformers.** Attention weights are often read as explanations, but Jain and Wallace (2019) found that they are frequently uncorrelated with gradient-based importance, and that different attention distributions can give the same prediction. Chefer et al. (2021) instead propagate relevance through the attention layers of vision Transformers. For language models, gradient-based attributions over token embeddings are common (Zhao et al., 2023).

## Connections

- **Brain and mind.** The [saliency-based visual attention](../../brain-mind/attention-brain-machine/saliency-map/index.md) model scores image locations by feature contrast, with no gradients or trained network. The shared name hides two separate traditions.
- **Gradients.** Gradient methods rely on [automatic differentiation](../../theory/math/automatic-differentiation/index.md) to compute input gradients.
- **Mechanistic work.** Attribution says which inputs mattered; [mechanistic interpretability](mechanistic-interpretability.md) says which circuits carried that information.

## Applications

- **Debugging.** A map may reveal that a model relies on a watermark rather than the object.
- **Tabular decisions.** TreeSHAP makes exact Shapley attributions practical for tree ensembles, common in credit and clinical risk models (Lundberg et al., 2020).
- **Medical imaging.** Saliency maps shown to clinicians need validation first, since several methods fail basic tests (Adebayo et al., 2018).

## Open questions

- **Ground truth.** No agreed correct attribution exists for a prediction. Sanity checks and removal benchmarks test some properties but do not settle which method is right.
- **Choice of reference.** Janzing et al. (2020) argue that dropped features should be replaced by unconditional expectations, and the choice changes the attribution.
- **Manipulation.** A biased classifier can be wrapped so that LIME and SHAP explanations look unbiased (Slack et al., 2020). Audits must test the model, not only its explanations.
- **Causal meaning.** An attribution shows what the model uses, not what causes an outcome in the world.

## References

### Seminal papers

- Simonyan, K., Vedaldi, A. & Zisserman, A. (2013). *Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps*. arXiv. https://arxiv.org/abs/1312.6034 — Defines gradient-based class saliency maps for image classifiers.
- Sundararajan, M., Taly, A. & Yan, Q. (2017). *Axiomatic Attribution for Deep Networks*. ICML. https://arxiv.org/abs/1703.01365 — Introduces Integrated Gradients, derived from two attribution axioms.
- Ribeiro, M. T., Singh, S. & Guestrin, C. (2016). *"Why Should I Trust You?": Explaining the Predictions of Any Classifier*. KDD. https://arxiv.org/abs/1602.04938 — Introduces LIME, a local sparse linear surrogate fitted to perturbed samples.
- Lundberg, S. M. & Lee, S.-I. (2017). *A Unified Approach to Interpreting Model Predictions*. NeurIPS. https://arxiv.org/abs/1705.07874 — Unifies LIME, DeepLIFT and related methods and introduces SHAP values.
- Selvaraju, R. R., et al. (2017). *Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization*. ICCV. https://arxiv.org/abs/1610.02391 — Produces class-specific localisation maps from gradients at the last convolutional layer.
- Shrikumar, A., Greenside, P. & Kundaje, A. (2017). *Learning Important Features Through Propagating Activation Differences*. ICML. https://arxiv.org/abs/1704.02685 — Presents DeepLIFT, which compares each neuron's activation with a reference activation.
- Shapley, L. S. (1953). *A Value for n-Person Games*. In Kuhn & Tucker (eds.), *Contributions to the Theory of Games II*. Princeton University Press. https://doi.org/10.1515/9781400881970-018 — The original definition of the Shapley value, later applied to models.
- Adebayo, J., et al. (2018). *Sanity Checks for Saliency Maps*. NeurIPS. https://arxiv.org/abs/1810.03292 — Proposes randomisation tests showing that several saliency methods fail them.
- Hooker, S., et al. (2019). *A Benchmark for Interpretability Methods in Deep Neural Networks*. NeurIPS. https://arxiv.org/abs/1806.10758 — Proposes a removal-based benchmark, finding many feature-importance methods no better than random.
- Slack, D., et al. (2020). *Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods*. AIES. https://arxiv.org/abs/1911.02508 — Shows how a biased classifier can be wrapped to pass LIME and SHAP explanations.
- Janzing, D., Minorics, L. & Blöbaum, P. (2020). *Feature relevance quantification in explainable AI: A causal problem*. AISTATS. https://arxiv.org/abs/1910.13413 — Argues that dropped features should be replaced by unconditional expectations, not conditional ones.
- Chefer, H., Gur, S. & Wolf, L. (2021). *Transformer Interpretability Beyond Attention Visualization*. CVPR. https://arxiv.org/abs/2012.09838 — Computes relevance for Transformers through the attention layers instead of visualising attention.
- Jain, S. & Wallace, B. C. (2019). *Attention is not Explanation*. NAACL. https://arxiv.org/abs/1902.10186 — Finds learned attention weights often uncorrelated with gradient-based importance.
- Lundberg, S. M., et al. (2020). *From local explanations to global understanding with explainable AI for trees*. Nature Machine Intelligence. https://doi.org/10.1038/s42256-019-0138-9 — Presents TreeSHAP, an exact polynomial-time method for tree ensembles.

### Surveys and textbooks

- Zhao, H., et al. (2023). *Explainability for Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2309.01029 — Taxonomy of explainability techniques for Transformer-based language models.
