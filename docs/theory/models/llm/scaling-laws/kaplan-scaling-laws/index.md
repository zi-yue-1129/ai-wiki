---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Kaplan 縮放定律
  - Kaplan scaling laws
  - 神經語言模型的縮放定律
---

# Scaling laws for neural language models (Kaplan et al., 2020)

Kaplan et al. measured how the cross-entropy loss of Transformer language models falls as the number of parameters, the amount of data and the training compute increase. They used these power laws to decide how a fixed compute budget should be spent. The general topic is covered in the parent page, [Scaling laws and emergent abilities](../index.md).

## Overview

Kaplan and colleagues trained a family of Transformer language models over a wide range of sizes, dataset sizes and compute budgets, recording held-out loss. The aim was a rule that predicts how much each resource is worth.

## Key concepts

- **Cross-entropy loss**: the average negative log-probability the model assigns to the true next token. Lower is better, and the loss is the quantity the scaling laws describe.
- **Model size**: the number of trainable parameters, varied by changing width and depth.
- **Dataset size**: the number of tokens in the training corpus. A model trained on more text than it has capacity to fit can overfit, and the paper gives simple equations for this.
- **Sample efficiency**: how much loss a model reaches per token of training data. Larger models were found to be more sample-efficient.

## How it works

The procedure has five steps:

1. Fix a decoder-only Transformer family and vary its width, depth and parameter count.
2. Train each model on a large text corpus, recording held-out loss at intervals during training.
3. Fit a power law in each variable on its own: loss against parameters with data effectively unlimited, loss against data with model size large, and loss against compute.
4. Fit the overfitting relation, which describes how the gap between training and held-out loss depends on model and dataset size.
5. For a fixed compute budget, use the fitted laws to choose the model size and the amount of training that minimise the predicted loss.

The single-variable form is $L(N) \propto N^{-\alpha_N}$, with the analogous forms for data and compute. The exponents and constants are estimated in the paper and are not repeated here.

## Results

The main result is that loss follows smooth power laws in the three resources across more than seven orders of magnitude, while architectural details such as the width or depth of the network have minor effects within a wide range. The authors concluded that, for a fixed budget, the best training run is a very large model on a relatively modest amount of data, stopped well before convergence. This was a strong statement about allocation: more of the extra compute should go to parameters than to data.

The Chinchilla study later tested the same question with a different design. Hoffmann et al. (2022) reported that the models of their time were significantly undertrained for their size, and that model size and training tokens should grow together. The comparison is discussed on the [compute-optimal training](../../compute-optimal-training/index.md) page.

## Limitations

- **Fitted range.** The laws were fitted on the range tested, with one data distribution and a fixed family of architectures. Extrapolation beyond that range is an assumption.
- **Loss, not capability.** The laws describe next-token loss. They do not directly state how any particular downstream task will change, which is one reason later work studied downstream prediction separately (Gadre et al., 2024).
- **Allocation revised.** The Chinchilla analysis revised the split between model size and data, and later work that accounts for inference cost gives different optima again (Sardana et al., 2023).

## Open questions

- Do the same power-law forms hold for new data mixtures, longer contexts and different objectives? Later studies in other domains found similar shapes with different constants (Henighan et al., 2020).
- How closely does held-out loss track the abilities people care about, such as reasoning or following instructions?
- Why do the exponents take the values they do? The paper describes them empirically, and the question has no accepted theoretical account.

## Connections

- Parent topic: [Scaling laws and emergent abilities](../index.md).
- Other method on the same topic: [Compute-optimal training](../../compute-optimal-training/index.md), which revised the allocation, and [Emergent abilities](../emergent-abilities/index.md), which asks what the smooth losses mean for capabilities.
- The model being scaled is the one described in [Transformers](../../../transformer/index.md). The few-shot behaviour of a much larger model in the same family is described in [GPT-3 Few-Shot Learning](../../gpt-3-few-shot/index.md).

## References

### Seminal papers

- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — The paper itself: power-law loss in parameters, data and compute, and the allocation rule derived from it.
- Hestness, J., et al. (2017). *Deep Learning Scaling is Predictable, Empirically*. arXiv. https://arxiv.org/abs/1712.00409 — Earlier evidence that generalisation error falls as a power law in training-set size across four domains.
- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — Re-examines the allocation question with over 400 training runs and finds that data should grow with model size.
- Henighan, T., et al. (2020). *Scaling Laws for Autoregressive Generative Modeling*. arXiv. https://arxiv.org/abs/2010.14701 — Extends power-law scaling to image, video, multimodal and mathematical models.

### Surveys and textbooks

- Zhao, W. X., et al. (2023). *A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — Broad survey of language-model pre-training and adaptation, placing scale-driven progress in context.

### Articles and documentation

- Sardana, N., et al. (2023). *Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws*. arXiv. https://arxiv.org/abs/2401.00448 — Adds the cost of inference to the scaling analysis, changing the optimal model size.
- Gadre, S. Y., et al. (2024). *Language models scale reliably with over-training and on downstream tasks*. arXiv. https://arxiv.org/abs/2403.08540 — Tests whether scaling predictions hold for over-trained models and for downstream task performance.
