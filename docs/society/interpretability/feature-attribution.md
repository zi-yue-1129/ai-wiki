---
status: draft
last_reviewed: 2026-10-28
related:
  - society/interpretability
  - theory/models/cnn
  - theory/models/transformer
tags:
  - interpretability
  - explainable AI
  - attribution
aliases:
  - 特徵歸因
  - 可解釋 AI
  - 顯著性圖
  - Feature attribution
  - SHAP
  - LIME
  - Integrated gradients
  - Saliency maps
---

# Feature attribution: SHAP, LIME and saliency

Feature attribution assigns a score to each input feature, such as a pixel, a token or a column in a table, to show how much it contributed to a particular prediction. It is the most common form of explainable AI, and it is used to inspect individual decisions, to find spurious correlations, and to support audits. Attribution methods differ in what they compare against, whether they probe the model from outside or use its gradients, and whether they meet basic consistency requirements. Those differences matter as much as the maps themselves.

## Overview

Given a model \(f\) and an input \(x\), an attribution method returns a vector \(\phi = (\phi_1, \dots, \phi_d)\), where \(\phi_i\) is the credit given to feature \(i\) for the output. The output is usually a score for one class or a predicted value. Large credit means the feature moved the output strongly in the chosen comparison. The meaning of that statement depends on the comparison, which is why the methods disagree.

## Key concepts

- **Attribution**: a per-feature score for one prediction.
- **Baseline** or **reference input**: the comparison point, such as a black image, an average input, or a set of background samples. Most attribution values are differences from it.
- **Local versus global**: local methods explain one prediction; global methods summarise many.
- **Faithfulness**: whether an attribution reflects features the model actually uses.
- **Additivity**: whether the attributions sum to the difference between the prediction and the baseline prediction.

## How it works

Attribution methods fall into two broad families.

**Gradient and propagation methods** use the model's internal structure. Simonyan et al. (2014) take the gradient of the class score with respect to the input pixels as a saliency map. Gradients can be noisy and saturate, so later methods change the propagation rule. Integrated gradients (Sundararajan et al., 2017) average gradients along a straight path from a baseline to the input, which gives an attribution that sums to the output difference. DeepLIFT (Shrikumar et al., 2017) and layer-wise relevance propagation (Bach et al., 2015) redistribute the output score backwards through the layers using rules that depend on reference activations or on the input signal.

**Perturbation and game-theoretic methods** treat the model as a black box. They change the input, observe the output, and fit or average the effects. LIME fits a simple surrogate around one input, and SHAP averages each feature's marginal contribution over coalitions of features.

## Key methods

- **[Saliency maps](saliency-maps.md) (Simonyan et al., 2014).** The gradient of the output with respect to the input. It is fast and needs only backpropagation, but it is sensitive to the gradient's local behaviour and does not satisfy additivity.
- **[Integrated gradients](integrated-gradients.md) (Sundararajan et al., 2017).** The attribution is the input-minus-baseline difference multiplied by the average gradient along the path. It satisfies sensitivity and implementation invariance, and depends on the choice of baseline.
- **[LIME](lime.md) (Ribeiro et al., 2016).** Samples perturbed versions of the input, weights them by proximity, and fits a sparse linear model. The explanation is local and model-agnostic, but its stability depends on sampling and kernel choices.
- **[SHAP](shap.md) (Lundberg & Lee, 2017).** The Shapley value of feature \(i\) is
  \[
  \phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(|N|-|S|-1)!}{|N|!}\,\bigl[v(S \cup \{i\}) - v(S)\bigr],
  \]
  where \(N\) is the set of features and \(v(S)\) is the model's expected output when only the features in \(S\) are known. Lundberg and Lee unify six existing methods under this additive form and propose estimators for it. Shapley-based attribution was used for predictions earlier by Štrumbelj and Kononenko (2014).

## Results

The methods are validated mainly by axioms and sanity checks rather than by one benchmark. Sundararajan et al. (2017) use the axioms of sensitivity and implementation invariance to design integrated gradients, and report that most known attribution methods do not satisfy them. Lundberg and Lee (2017) present a class of additive feature importance measures that unifies six existing methods. Ribeiro et al. (2016) evaluate LIME with simulated and human-subject experiments, including on deciding whether to trust a prediction. Adebayo et al. (2018) propose an actionable methodology for evaluating what a saliency method can explain, and report that some existing saliency methods are independent both of the model and of the data-generating process.

## Limits

- **Sanity.** Some saliency methods are independent of both the model and the data (Adebayo et al., 2018), so their maps can look informative without reflecting what the model learned.
- **Baseline dependence.** Integrated gradients and SHAP depend on the reference input or background distribution, and the explanation changes with that choice.
- **Correlated features.** When features are correlated, Shapley-style values can credit a feature the model does not use, because the method evaluates unlikely input combinations.
- **Causation.** High attribution shows what the model's output depends on under the chosen perturbation, not what causes the real-world outcome.
- **Over-trust.** Explanations can make users trust a model more without making it more accurate. See [Human-AI interaction](../human-ai-interaction/index.md).

## Connections

Attribution is one of the explanation tools in [Interpretability](index.md), next to probing and mechanistic methods. Its fairness uses are discussed in [Fairness definitions](../ethics/fairness-definitions.md), since an attribution can show that a protected attribute or its proxy drives a decision. Saliency maps were developed for convolutional networks, described in [CNN](../../theory/models/cnn/index.md), and they have been extended to Transformers, described in [Transformers](../../theory/models/transformer/index.md). The probing approach in [Probing classifiers](probing.md) answers a different question: what information is present, not which inputs drove a decision.

## Applications

- Debugging image classifiers by checking whether they attend to the object or to background cues.
- Explaining credit, insurance or hiring decisions to affected individuals, where regulations require reasons.
- Finding shortcut features in tabular and clinical models before deployment.
- Checking language models by attributing outputs to input tokens.

## Open questions

- **Faithfulness metrics.** There is no agreed quantitative test that tells a faithful attribution from an unfaithful one for all model classes.
- **Baselines and distributions.** How to choose a reference that is meaningful for the question being asked.
- **Attribution for generative and reasoning models.** Long outputs and multi-step computation make the one-output-one-attribution framing hard to apply.

## References

### Seminal papers

- Simonyan, K., Vedaldi, A. & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. *Proceedings of the ICLR 2014 Workshop*. https://arxiv.org/abs/1312.6034 — Introduces gradient-based saliency maps for image classifiers.
- Bach, S., Binder, A., Montavon, G., Klauschen, F., Müller, K.-R. & Samek, W. (2015). On Pixel-Wise Explanations for Non-Linear Classifier Decisions by Layer-Wise Relevance Propagation. *PLOS ONE*, 10(7), e0130140. https://doi.org/10.1371/journal.pone.0130140 — Propagates a relevance score backwards through a network to attribute a prediction to input pixels.
- Shrikumar, A., Greenside, P. & Kundaje, A. (2017). Learning Important Features Through Propagating Activation Differences. *Proceedings of ICML 2017*. https://arxiv.org/abs/1704.02685 — Introduces DeepLIFT, which attributes outputs relative to reference activations.
- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — Introduces integrated gradients and the sensitivity and implementation-invariance axioms.
- Ribeiro, M. T., Singh, S. & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *Proceedings of KDD 2016*. https://arxiv.org/abs/1602.04938 — Introduces LIME, a local surrogate explanation for any classifier.
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — Introduces SHAP, unifying additive feature attribution methods under Shapley values.
- Štrumbelj, E. & Kononenko, I. (2014). Explaining prediction models and individual predictions with feature contributions. *Knowledge and Information Systems*, 41(3), 647–665. https://doi.org/10.1007/s10115-013-0679-x — Uses Shapley values to explain individual predictions of general models.
- Adebayo, J., Gilmer, J., Muelly, M., Goodfellow, I., Hardt, M. & Kim, B. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — Proposes a methodology for evaluating saliency methods and finds that some are independent of the model and the data.

### Surveys and textbooks

- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. https://christophm.github.io/interpretable-ml-book/ — Free online book covering attribution, Shapley values and surrogate models with worked examples.

## Further learning

- [SHAP documentation](https://shap.readthedocs.io/) — open-source implementations and tutorials for Shapley-based attribution.
- [Captum](https://captum.ai/) — PyTorch library implementing integrated gradients, DeepLIFT and related methods.
