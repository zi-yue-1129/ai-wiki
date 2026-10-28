---
status: draft
last_reviewed: 2026-10-28
tags:
  - architecture
  - reinforcement learning
aliases:
  - NAS with Reinforcement Learning
  - Zoph and Le
  - 以強化學習進行神經架構搜尋
---

# NAS with Reinforcement Learning (Zoph and Le, 2016)

Zoph and Le (2016) used a recurrent network to write down a neural architecture one decision at a time, and trained that network with reinforcement learning. The reward was the validation accuracy of each generated network. This is the method that started the modern wave of work on [neural architecture search](../index.md).

## Overview

Designing a convolutional network involves many decisions about filters, strides, pooling and connections. Zoph and Le asked whether a program could make those decisions and learn from the results. A controller proposes an architecture, a training run scores it, and a learning rule makes high-scoring proposals more likely. The paper covers CIFAR-10 and a recurrent cell for the Penn Treebank.

## Key concepts

- **Controller.** A two-layer LSTM with 35 hidden units per layer. It outputs a sequence of tokens, and each token names one design choice, such as a filter size, a stride or a connection.
- **Child network.** The network built from the token sequence. It is trained, and its accuracy is the signal the controller learns from.
- **Reward.** In the paper, the maximum validation accuracy over the last five training epochs, raised to the third power. The cube is a sharpening transform that the authors chose, so that differences between good and very good candidates count for more.
- **REINFORCE.** The policy-gradient rule used to update the controller. It is needed because the reward comes from training a network, so it cannot be differentiated with respect to the controller's parameters.
- **Skip connections.** An extension in which the controller also chooses earlier layers to connect to, using set-selection attention.

## How it works

Each search step follows four stages.

1. **Sample.** The controller emits decisions \(a_1, \dots, a_T\). Each decision is drawn from a softmax over its options and conditioned on the decisions before it.
2. **Train the child.** The decoded network is trained for 50 epochs on 45,000 CIFAR-10 training images. The other 5,000 images are held out for validation.
3. **Reward.** The child's reward \(R\) is computed from its validation accuracy, as described above.
4. **Update.** The controller parameters \(\theta_c\) are adjusted to increase the expected reward. The paper uses the REINFORCE estimate

\[
\nabla_{\theta_c} J(\theta_c) \approx \frac{1}{m} \sum_{k=1}^{m} \sum_{t=1}^{T} \nabla_{\theta_c} \log P\big(a_t \mid a_{(t-1):1}; \theta_c\big)\, R_k,
\]

where \(m\) is the number of architectures sampled in one batch.

Each update requires trained networks, so the procedure is distributed. The paper uses 100 controller replicas, each sampling 8 child networks, so 800 networks train at once on 800 GPUs. The search evaluated 12,800 architectures before the best one was selected for a small grid search over training settings.

## Results

On CIFAR-10, the selected network reached a 3.65% test error with 37.4M parameters (Table 1 of the paper). The table places this just behind the best hand-designed models, such as DenseNet-BC (L = 100, k = 40) at 3.46% with 25.6M parameters.

On the Penn Treebank, the searched recurrent cell reached a test perplexity of 62.4. The abstract reports that this is 3.6 perplexity points better than the previous state-of-the-art model on that benchmark.

## Limitations

- **Compute.** The search needed hundreds of GPUs running in parallel. This placed the method out of reach for most research groups, and it is the cost that later methods set out to reduce.
- **Fixed search space.** The controller chooses within a design written by the authors: a set of layer types, filter sizes and connection rules. It cannot invent operations outside that set.
- **Noisy reward.** Each reward is a noisy estimate of final accuracy, because it comes from a short training run.
- **Narrow evidence.** The main results cover CIFAR-10 and the Penn Treebank. Transfer to other tasks is not settled by the paper.

## Open questions

- **Cheaper search.** Can the same results be reached with far less compute? ENAS shares weights between candidate networks and reports a search about 1000 times cheaper (Pham et al., 2018).
- **Choice of optimiser.** Is reinforcement learning the best way to search a discrete space? In a controlled comparison, [regularized evolution](../regularized-evolution/index.md) produced more accurate models early in the search, with the same code and budget (Real et al., 2018).
- **Role of the search space.** How much of the result comes from the controller and how much from the space it searches? Li and Talwalkar (2019) show that random search is a competitive baseline on the same benchmarks.

## References

### Seminal papers

- Zoph, B. & Le, Q. V. (2016). *Neural Architecture Search with Reinforcement Learning*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — The paper itself: an RNN controller trained with reinforcement learning to generate CNN and recurrent cells.
- Real, E., et al. (2018). *Regularized Evolution for Image Classifier Architecture Search*. arXiv:1802.01548. https://arxiv.org/abs/1802.01548 — Compares evolution, RL and random search under matched compute on CIFAR-10.
- Pham, H., et al. (2018). *Efficient Neural Architecture Search via Parameter Sharing*. arXiv:1802.03268. https://arxiv.org/abs/1802.03268 — Shares weights between child networks in an RL controller, reducing search cost by about three orders of magnitude.

### Surveys and textbooks

- Elsken, T., Metzen, J. H. & Hutter, F. (2018). *Neural Architecture Search: A Survey*. arXiv:1808.05377. https://arxiv.org/abs/1808.05377 — Organises NAS methods by search space, search strategy and performance estimation.

### Articles and documentation

- Li, L. & Talwalkar, A. (2019). *Random Search and Reproducibility for Neural Architecture Search*. arXiv:1902.07638. https://arxiv.org/abs/1902.07638 — Shows that random search with early stopping is a competitive baseline on the PTB and CIFAR-10 NAS benchmarks.
- Yang, A., Esperança, P. M. & Carlucci, F. M. (2019). *NAS evaluation is frustratingly hard*. arXiv:1912.12522. https://arxiv.org/abs/1912.12522 — Benchmarks eight NAS methods on five datasets and argues for comparing against random architectures.
