---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 湧現能力
  - Emergent abilities
  - Emergent Abilities of Large Language Models
---

# Emergent abilities of large language models (Wei et al., 2022)

Wei et al. defined an emergent ability as one that is absent in smaller language models and present in larger ones, and argued that such abilities cannot be predicted by extrapolating the performance of smaller models. The general topic is covered in the parent page, [Scaling laws and emergent abilities](../index.md).

## Overview

Scaling up language models had already been shown to improve performance and sample efficiency predictably on many tasks. Wei et al. (2022) described a different pattern. For some tasks, a family of models performs near chance across the smaller sizes and then rises clearly above chance at a larger size. They called this phenomenon emergence, and they drew the consequence that further scaling might expand a model's abilities in ways that smooth extrapolation would not reveal.


## Key concepts

- **Emergent ability**: in the paper's definition, an ability that is not present in smaller models but is present in larger ones, and so cannot be predicted by extrapolating from small models.
- **Few-shot prompting**: a task is specified by a few worked examples in the prompt, with no weight update. The method that made this practical is described in [GPT-3 Few-Shot Learning](../../gpt-3-few-shot/index.md).
- **Chance level**: the score a model would get by guessing. For multiple-choice tasks it is set by the number of options. A task that stays at chance across sizes shows no ability yet.
- **Threshold scale**: the model size or compute at which performance begins to rise. The value depends on the sizes that were tested.

## How it works

The paper's analysis follows a simple procedure, with no single governing equation:

1. Choose a task and a set of model families, each available at several sizes.
2. Evaluate every model with the same few-shot prompt format, so that only the model changes.
3. Plot performance against scale, using parameters or training compute as the horizontal axis.
4. Identify tasks where performance stays flat near the baseline for smaller models and then rises above it at a threshold.
5. Classify such a task as emergent. The argument is that the flat region alone gives no hint of the later rise, so extrapolation from smaller models would have missed it.

A related idea appears in Ganguli et al. (2022), who describe predictable loss alongside unpredictable specific capabilities.

## Results

The paper reports that, across several model families, a number of few-shot tasks show the flat-then-rising pattern, and that the rise appears only above a certain scale. The authors draw from this the expectation that further scaling could unlock capabilities not yet seen. The paper's abstract states the claim and the definition; the specific benchmarks and the scale thresholds for individual tasks are in the full text. That text was not checked for this page, so its examples are not repeated here.

Srivastava et al. (2022), who introduced the BIG-bench collection, describe the same pattern as quantitative improvement together with new qualitative capabilities.

## Limitations

- **Dependence on sampled scales.** A threshold can only be seen between the sizes that were tested. With few sizes, a gradual rise may look like a jump.
- **Dependence on metric.** Exact-match or other discontinuous scores can make a gradual change look sudden. The later critique by Schaeffer et al. (2023) is built on this point.
- **Description, not mechanism.** The paper documents where emergence appears. It does not explain why a capability switches on at a particular scale.

## Open questions

- Are emergent abilities a property of the models, or of the way they are measured? The critique by Schaeffer et al. (2023) argues the latter for many cases, and the survey by Berti et al. (2025) reviews the disagreement.
- Can the scale at which a given ability appears be predicted before training? The definition in this paper rules out simple extrapolation, so a different kind of predictor would be needed.

## Connections

- Parent topic: [Scaling laws and emergent abilities](../index.md). The critique is on [Emergence as a mirage](../emergence-mirage/index.md).
- Prompting-based reasoning is one of the abilities that the emergence debate is most often applied to. See [Chain-of-thought](../../../reasoning/chain-of-thought.md) and [Reasoning models](../../../reasoning/index.md).
- The smooth-loss laws that this paper contrasts with are in [Kaplan scaling laws](../kaplan-scaling-laws/index.md).
- Human development also shows abilities appearing in stages. See [Developmental Cognition](../../../../../brain-mind/developmental-cognition/index.md).

## References

### Seminal papers

- Wei, J., et al. (2022). *Emergent Abilities of Large Language Models*. arXiv. https://arxiv.org/abs/2206.07682 — The paper itself: defines emergent abilities and argues that they cannot be extrapolated from smaller models.
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that reasoning from intermediate steps appears in sufficiently large models prompted with a few examples.
- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The GPT-3 paper, which made few-shot prompting the setting in which emergence is usually measured.
- Schaeffer, R., Miranda, B. & Koyejo, S. (2023). *Are Emergent Abilities of Large Language Models a Mirage?* arXiv. https://arxiv.org/abs/2304.15004 — The main critique of the emergence claim, arguing that discontinuous metrics produce the apparent jumps.

### Surveys and textbooks

- Berti, L., Giorgi, F. & Kasneci, G. (2025). *Emergent Abilities in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2503.05788 — Reviews the emergence literature and the debate over whether the abilities are truly emergent.

### Articles and documentation

- Srivastava, A., et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — The BIG-bench benchmark, a source of many tasks used to study scaling and emergence.
- Ganguli, D., et al. (2022). *Predictability and Surprise in Large Generative Models*. arXiv. https://arxiv.org/abs/2202.07785 — Argues that generative models combine predictable loss with unpredictable specific capabilities, and discusses the policy implications.
