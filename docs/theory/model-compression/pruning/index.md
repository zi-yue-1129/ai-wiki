---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
- brain-mind/neuroscience
tags:
- model compression
- sparsity
- pruning
aliases:
  - Pruning
  - Network Pruning
  - Sparsity
  - 剪枝
  - 網路剪枝
---

# Pruning

Pruning removes parts of a trained network, such as individual weights, neurons, channels or attention heads, that contribute little to its outputs. The remaining network is smaller, and if the removal is structured, it can also be faster. Pruning is one of the three main families of [model compression](../index.md), alongside [quantisation](../quantisation/index.md) and [knowledge distillation](../knowledge-distillation/index.md).

## Overview

A pruned model is described by a **mask**: a binary value for every weight that says whether the weight is kept. Three choices define a pruning method:

- **Granularity.** Unstructured pruning removes single weights, which gives the most freedom but leaves irregular sparsity. Structured pruning removes whole rows, channels, heads or blocks, which leaves a smaller dense matrix that ordinary hardware runs faster.
- **Scoring.** A rule decides which parts are least important. Magnitude is the simplest; others use gradients, Hessian approximations or the activations that a weight multiplies.
- **Schedule.** One-shot pruning removes a fraction in a single step. Iterative pruning alternates removal with retraining, which usually reaches higher sparsity at the same accuracy but costs more compute.

## Key concepts

- **Sparsity**: the fraction of weights removed. A model with 50% sparsity keeps half its weights.
- **Magnitude pruning**: remove the weights with the smallest absolute value. It is cheap and often a strong baseline, as Gale et al. (2019) showed at large scale.
- **N:M sparsity**: a structured pattern that keeps N values in every block of M, such as 2 in every 4. NVIDIA's sparse tensor cores, introduced with the Ampere generation of GPUs, run this pattern at higher speed.
- **Lottery ticket**: Frankle and Carbin (2018) found that a dense network contains sparse subnetworks which, reset to their original initial weights, train to comparable accuracy in isolation.
- **Global versus layer-wise**: a global threshold lets some layers be pruned more than others, which often gives better accuracy for the same total sparsity.

## How it works

The classic pipeline, from Han et al. (2015), has three steps: train a dense network normally, remove weights whose magnitude is below a threshold, then retrain the remaining weights to recover accuracy. Repeating the prune-and-retrain loop raises sparsity gradually. This pipeline needs a full training run per iteration, so it is expensive for models with billions of parameters.

Large language models changed the problem. Retraining them is costly, so recent methods prune in one shot, using only a small calibration set and a closed-form or local correction for each layer.

## Key methods

### Learning both weights and connections (Han, Pool, Tran and Dally, 2015)

- **Problem:** Large networks, such as AlexNet for image classification, contain far more parameters than they need, and storing them is expensive on mobile systems.
- **Core idea:** Train the network to learn which connections matter, prune the weak ones, and retrain. The paper shows that the pruned network keeps accuracy while having far fewer connections.
- **Equation or algorithm:** Weights below a threshold are set to zero and held there with a mask. The network is then retrained on the remaining weights, and the threshold is raised over several rounds.
- **Results:** The abstract reports that the method reduced the number of parameters of AlexNet by a factor of 9, from 61 million to 6.7 million.
- **Limitations:** Retraining costs as much as training, and the unstructured result needs sparse software to run faster. It was developed for convolutional networks before large transformers.

### SparseGPT (Frantar and Alistarh, 2023)

- **Problem:** Iterative pruning and retraining are too expensive for models with billions of parameters, and simple magnitude pruning fails at high sparsity.
- **Core idea:** Prune each layer in one shot, choosing which weights to remove and updating the remaining weights to compensate. The compensation uses an approximate inverse Hessian of the layer's reconstruction error, the same framework used by GPTQ for quantisation.
- **Equation or algorithm:** For a layer with inputs \(X\), the method minimises \(\lVert WX - \hat{W}X \rVert^2\) over masks and updated weights \(\hat{W}\), column by column, with a blockwise update. The solver runs on a small calibration set.
- **Results:** The abstract reports that the method can reach 60% unstructured sparsity with negligible increase in perplexity for large GPT-family models.
- **Limitations:** Unstructured sparsity needs sparse kernels to give speed-ups. The method needs calibration data and an approximate second-order solver, which adds engineering complexity.

### Wanda (Sun et al., 2023)

- **Problem:** SparseGPT is accurate but requires a second-order calculation for each layer. A simpler method that scales to large models would be easier to adopt.
- **Core idea:** Score each weight by its magnitude multiplied by the norm of the corresponding input activation, and prune the lowest-scoring weights within each output, without any weight update or retraining.
- **Equation or algorithm:** The score of weight \(W_{ij}\) is \(|W_{ij}| \cdot \lVert X_j \rVert_2\), computed on calibration inputs. The lowest-scoring weights are removed per output row.
- **Results:** The authors report that Wanda significantly outperforms the established baseline of magnitude pruning on large language models.
- **Limitations:** The method removes weights without correcting the remaining ones, so the accuracy loss at very high sparsity is larger than with methods that update weights.

## Connections

Pruning and sparse computation depend on what chips can skip. The support for N:M patterns and sparse matrix kernels is part of the story in [AI hardware](../../../engineering/hardware/index.md).

Biology has a parallel. During development, the brain forms more synapses than it keeps, and many are eliminated as circuits are refined. Whether this process is a useful model for artificial pruning is debated, but it is a common starting point in discussions of sparse coding and efficient representation; see [neuroscience](../../../brain-mind/neuroscience/index.md).

## Applications

- **Mobile vision models** are pruned to structured sparsity so that they run on small processors.
- **Large language models** are pruned in one shot before quantisation to reduce serving cost.
- **Robotics and embedded control** use pruned networks to fit real-time budgets.

## Open questions

- **Why magnitude works.** Pruning rules are chosen empirically. A theory that predicts which weights can be removed without harm is missing.
- **Hardware for unstructured sparsity.** High unstructured sparsity saves parameters but speeds up little on current accelerators, so structured patterns are often preferred in practice.
- **Pruning during training.** Sparse training could save compute throughout the run, but stability and quality at high sparsity are not fully understood.
- **Reasoning and long context.** The effect of pruning on multi-step reasoning and retrieval is less studied than perplexity.

## References

### Seminal papers

- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — Shows that pruning and retraining cut AlexNet's parameters by a factor of 9.
- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — Identifies sparse subnetworks that train well from their initial weights.
- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — One-shot pruning of large language models with weight reconstruction.
- Sun, M., et al. (2023). *A Simple and Effective Pruning Approach for Large Language Models*. arXiv:2306.11695. https://arxiv.org/abs/2306.11695 — Wanda, a magnitude-times-activation score that needs no retraining.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — A broad survey of sparsity methods across training and inference.
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks sparsity methods and finds magnitude pruning a strong baseline.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
