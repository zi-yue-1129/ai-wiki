---
status: draft
last_reviewed: 2026-10-28
related:
  - brain-mind/developmental-cognition
  - engineering/evaluation
tags:
  - model scaling
  - large language models
aliases:
  - 縮放定律
  - 神經縮放定律
  - Scaling laws
  - Neural scaling laws
  - 湧現能力
  - Emergent abilities
---

# Scaling laws and emergent abilities

Scaling laws are empirical rules that describe how a language model's loss falls as its parameters, training data and compute grow. Emergent abilities are capabilities that seem absent in small models and then appear abruptly in large ones; whether they reflect a real property of scale or an artefact of measurement is still disputed.

## Overview

Neural networks improve in a regular way when they are made larger or trained on more data. Hestness et al. (2017) measured this across four domains and found that generalisation error falls as a power law in training-set size.[^1] For Transformer language models, Kaplan et al. (2020) showed that held-out cross-entropy loss follows a power law in model size, dataset size and compute, over more than seven orders of magnitude.[^2] A smooth, predictable trend lets a lab fit a curve to small, cheap runs and estimate the loss of a far larger run before committing to it.

Three questions followed. The first is how to split a fixed budget between parameters and training tokens. Kaplan et al. concluded that the best use of extra compute is to train very large models on a relatively modest amount of data and to stop well before convergence. The Chinchilla study later argued that current models were significantly undertrained and that size and data should grow together; that argument is the subject of [Compute-optimal training](../compute-optimal-training/index.md). The second question concerns the gap between loss and capability. A model whose loss falls smoothly can still gain specific abilities in sudden jumps. Wei et al. (2022) called such jumps emergent abilities.[^3] The third question is whether the jumps are real. Schaeffer et al. (2023) argued that much of the apparent sharpness comes from the choice of scoring metric.[^4]

Scaling has also moved to inference, where extra compute can buy better answers without a larger model. See [Test-time compute scaling](../../reasoning/test-time-scaling.md).

## Key concepts

- **Scaling law**: an empirical relation, usually a power law, between a quantity such as loss and a scale variable such as parameters, tokens or compute. It is a fit to measurements and makes no guarantee beyond the range measured. See the glossary entry [Scaling laws](../../../../reference/glossary/index.md).
- **Power law**: a relation of the form $y \propto x^{-\alpha}$. On log-log axes it is a straight line, which is why these fits are usually drawn that way.
- **Compute budget**: the total arithmetic spent on training. For dense Transformers it is commonly approximated as proportional to the parameter count times the number of training tokens.
- **Overfitting regime**: a model that is large relative to its dataset stops improving on held-out text even while its training loss keeps falling. Kaplan et al. gave simple equations for how this depends on model and dataset size.
- **Constant term**: a fixed offset in many fits, giving a floor that the loss approaches as scale grows.
- **Emergent ability**: a capability absent in smaller models and present in larger ones, which cannot be predicted by extrapolating the performance of smaller models (Wei et al., 2022).
- **Metric choice**: the scoring rule used for a task. Discontinuous scores, such as exact-match accuracy, can turn a smooth underlying improvement into an apparent sudden jump.

## How it works

A scaling study follows a common procedure:

```mermaid
flowchart LR
  A[Train many models<br/>vary N, D and C] --> B[Measure held-out loss]
  B --> C[Fit a power law<br/>often with a constant term]
  C --> D[Choose N and D<br/>for a fixed budget]
  D --> E[Extrapolate to a larger run]
  E --> F[Check on downstream tasks]
```

First, a model family is fixed, usually decoder-only Transformers, and models of several sizes are trained on large text corpora. Held-out loss is recorded against the number of parameters $N$, the number of training tokens $D$ and the training compute $C$. The measurements are then fitted with a relation whose shape Hoffmann et al. (2022) used in their parametric fit:

$$L(N, D) \approx E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}$$

The constants $E$, $A$, $B$, $\alpha$ and $\beta$ are estimated from the data. Their values are in the papers and are not repeated here. Kaplan et al. (2020) fitted one-variable power laws for each dependence first, which is the form in which the idea became widely known.

The best split of a fixed budget then follows from minimising the fitted loss. Any extrapolation assumes the same curve continues beyond the measured range.

## Key methods

Each method has its own page. The comparison here is brief.

| Method | Core claim | Page |
|---|---|---|
| Kaplan et al. (2020) | Loss follows power laws in parameters, data and compute; large models are more sample-efficient | [Kaplan scaling laws](kaplan-scaling-laws/index.md) |
| Chinchilla (Hoffmann et al., 2022) | For a fixed budget, model size and training tokens should grow together | [Compute-optimal training](../compute-optimal-training/index.md) |
| Wei et al. (2022) | Some abilities appear abruptly at scale and cannot be extrapolated from smaller models | [Emergent abilities](emergent-abilities/index.md) |
| Schaeffer et al. (2023) | Apparent emergence largely depends on the metric; continuous metrics give smooth curves | [Emergence as a mirage](emergence-mirage/index.md) |

The first two methods answer the allocation question, how to spend compute. The last two answer whether capability can be predicted from scale. The two emergence papers disagree about the evidence, not about whether scale matters.

## Connections

- Parent topic: [Large Language Models](../index.md). Scaling determines the size and data of the pre-training stage described there.
- The unit that $D$ counts is the token, so the tokeniser changes what a token budget means. A tokeniser that needs more tokens for the same text in one language makes that language more expensive to train on. See [Tokenisation](../tokenisation/index.md).
- The architecture side is covered in [Transformers](../../transformer/index.md). Kaplan et al. reported that width and depth had minor effects within the range they tested, which made model size and data the main variables to study.
- Few-shot prompting, the capability that drew much attention to emergence, is described in [GPT-3 Few-Shot Learning](../gpt-3-few-shot/index.md).
- Measurement choices for emergence overlap with the discussion in [Evaluation](../../../../engineering/evaluation/index.md).
- Brain and mind: children hear tens of millions of words by adolescence, against trillions of tokens for LLMs. Whether human learning follows a comparable scaling curve is a separate question, discussed in [Developmental Cognition](../../../../brain-mind/developmental-cognition/index.md).

## Applications

- **Planning training runs.** Labs fit curves to small runs and use them to choose model size and data before the full run. The GPT-4 technical report describes using scaling predictions in this way.[^5]
- **Budgeting for inference.** The Chinchilla analysis ignores the cost of serving a model. Sardana et al. (2023) modify it to count inference cost, which favours smaller models trained on more data.
- **Data supply.** Villalobos et al. (2022) forecast that, if current trends continue, training sets could reach the stock of public human-written text between 2026 and 2032. Muennighoff et al. (2023) study training on repeated data.
- **Inference-time scaling.** Brown et al. (2024) show that the fraction of problems solved by at least one of many sampled answers grows with the number of samples across four orders of magnitude. Snell et al. (2024) argue that using test-time compute well can be more effective than scaling model parameters alone.

## Open questions

- **Is emergence real?** The Wei et al. and Schaeffer et al. papers disagree on whether sharp jumps are a property of the models or of the metrics. Berti et al. (2025) survey the debate. Because the claim depends on which scales were tested, both sides have limited evidence at the largest scales.
- **Does loss predict capability?** Loss scales more smoothly than accuracy on individual tasks. Gadre et al. (2024) study when downstream performance also follows predictable trends, including for models trained past the compute-optimal point.
- **How much data is enough?** Whether repeated data can substitute for new text, and how far quality filtering can stretch a fixed stock, is unresolved.
- **Do the laws transfer?** Henighan et al. (2020) found power-law scaling in image, video, multimodal and mathematical models as well as text, with similar exponents. Whether new architectures, objectives or modalities keep the same shape has to be measured again each time.
- **Training versus inference.** How to weigh serving cost against training cost, and whether test-time compute can replace parameters for a given query, remain open.

[^1]: Hestness et al. (2017) test four domains: machine translation, language modelling, image processing and speech recognition. See References.
[^2]: The loss-versus-scale results and the phrase "over more than seven orders of magnitude" are from the Kaplan et al. (2020) abstract. The fitted constants are in the paper and are not repeated here.
[^3]: Wei et al. (2022) define the term in their introduction. The examples they give are not repeated here because the full text was not checked for this page.
[^4]: The argument is made by changing the metric on fixed model outputs; see Schaeffer et al. (2023) in References.
[^5]: The report is cited for the practice of forecasting from smaller runs. Its specific figures are not repeated here.

## References

### Seminal papers

- Hestness, J., et al. (2017). *Deep Learning Scaling is Predictable, Empirically*. arXiv. https://arxiv.org/abs/1712.00409 — Reports power-law scaling of generalisation error with training-set size in machine translation, language modelling, image processing and speech.
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — Shows that Transformer language-model loss follows power laws in model size, data and compute, and how to allocate a fixed budget.
- Henighan, T., et al. (2020). *Scaling Laws for Autoregressive Generative Modeling*. arXiv. https://arxiv.org/abs/2010.14701 — Finds power-law plus constant scaling in image, video, multimodal and mathematical models.
- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — Trains over 400 models and argues that model size and training tokens should grow together for a fixed budget.
- Wei, J., et al. (2022). *Emergent Abilities of Large Language Models*. arXiv. https://arxiv.org/abs/2206.07682 — Defines emergent abilities as those absent in small models and present in large ones, and not predictable by extrapolation.
- Schaeffer, R., Miranda, B. & Koyejo, S. (2023). *Are Emergent Abilities of Large Language Models a Mirage?* arXiv. https://arxiv.org/abs/2304.15004 — Argues that apparent emergence depends on discontinuous metrics, and shows smooth curves under continuous ones.
- Snell, C., et al. (2024). *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv. https://arxiv.org/abs/2408.03314 — Studies how a fixed amount of inference compute can be allocated, and compares it with training a larger model.

### Surveys and textbooks

- Berti, L., Giorgi, F. & Kasneci, G. (2025). *Emergent Abilities in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2503.05788 — Surveys the emergence literature and the debate over whether the abilities are truly emergent.

### Articles and documentation

- OpenAI et al. (2023). *GPT-4 Technical Report*. arXiv. https://arxiv.org/abs/2303.08774 — Technical report on a large multimodal model; its development section describes predicting training performance from smaller runs.
- Villalobos, P., et al. (2022). *Will we run out of data? Limits of LLM scaling based on human-generated data*. arXiv. https://arxiv.org/abs/2211.04325 — Forecasts training-data demand against an estimate of the stock of public human-written text.
- Muennighoff, N., et al. (2023). *Scaling Data-Constrained Language Models*. arXiv. https://arxiv.org/abs/2305.16264 — Studies scaling when unique text is limited and data must be repeated during training.
- Sardana, N., et al. (2023). *Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws*. arXiv. https://arxiv.org/abs/2401.00448 — Modifies the Chinchilla analysis to include the cost of inference in choosing model size and data.
- Gadre, S. Y., et al. (2024). *Language models scale reliably with over-training and on downstream tasks*. arXiv. https://arxiv.org/abs/2403.08540 — Studies how scaling predictions hold when models are trained past the compute-optimal regime and evaluated on downstream tasks.
- Brown, B., et al. (2024). *Large Language Monkeys: Scaling Inference Compute with Repeated Sampling*. arXiv. https://arxiv.org/abs/2407.21787 — Shows that the fraction of problems solved by at least one sample grows with the number of samples drawn.
