---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/llm/scaling-laws
  - theory/deep-learning/initialisation/mup/index.md
  - theory/paradigms/online/stochastic-bandits
  - theory/evolutionary
tags:
  - optimization
  - hyperparameters
  - model scaling
aliases:
  - Hyperparameter optimization
  - Hyperparameter tuning
  - HPO
  - 超參數最佳化
  - 超參數調整
  - 網格搜尋
  - 隨機搜尋
  - 貝氏最佳化
  - 連續減半
  - 基於族群的訓練
---

# Hyperparameter Optimisation

Hyperparameter optimisation is the search for the settings that are fixed before training starts, such as the learning rate, batch size, weight decay and network width, and that give the best result. The methods differ in how they choose the next setting to try and in how much compute they give each trial.

## Overview

Training fits the parameters \(\theta\) of a model, but many other choices are made beforehand. These are the hyperparameters \(\lambda\). Examples include the learning rate and its [schedule](learning-rate-schedules.md), the Adam coefficients, the strength of weight decay, the batch size, and the depth and width of the network.

Each choice of \(\lambda\) defines a different training run, scored on held-out data. The outer problem is \(\lambda^\* = \arg\max_\lambda S(\lambda)\), where \(S(\lambda)\) is the validation score after training with \(\lambda\). One evaluation can cost hours or days of computation, so only a few trials are affordable compared with the size of the space. Hyperparameter optimisation (HPO) is the set of strategies for searching that space within a fixed budget.

Snoek et al. (2012) describe tuning as often a "black art" that needs expert judgement or brute-force search. The problem is hard for three reasons: the space mixes continuous, discrete and categorical settings; the score is noisy, because different random seeds give slightly different results; and each evaluation is expensive.

## Key concepts

- **Hyperparameter**: a setting chosen before training, in contrast to a parameter, which training learns. See the [glossary](../../reference/glossary/index.md).
- **Search space**: the range and scale of each hyperparameter, for example a learning rate sampled on a log scale between \(10^{-5}\) and \(10^{-1}\).
- **Trial**: one setting evaluated by a training run.
- **Budget (fidelity)**: a cheaper version of a full run, such as fewer epochs, a data subset or a smaller model.
- **Surrogate model and acquisition function**: in Bayesian optimisation, a statistical model of the score as a function of \(\lambda\), and a rule for picking the next point to evaluate.
- **Transfer**: reusing settings found on a small or cheap model for a large one. This is justified only if the best settings are stable across scale.

## How it works

Every method follows the same loop: propose a configuration, train it to some budget, record the validation score, and use the record to propose the next. The methods differ in the proposal rule and in how they divide the budget.

Successive halving is the central budget-allocation algorithm. Given \(n\) configurations, a minimum budget \(r\) and a reduction factor \(\eta > 1\), typically 3 or 4:

1. Train all \(n\) configurations with budget \(r\).
2. Keep the best \(\lfloor n/\eta \rfloor\) of them and multiply the budget by \(\eta\).
3. Repeat until one configuration is left, and train it fully.

Each round keeps about a fraction \(1/\eta\) of the configurations and gives the survivors more budget, so most of the compute goes to the promising trials. Hyperband runs this procedure several times, each with a different trade-off between the number of configurations and the starting budget. It therefore does not need to know in advance how aggressively to stop weak trials.[^1]

## Key methods

Five families cover most practice. The table compares them, and the paragraphs below give the evidence for each.

| Method | How it proposes trials | Budget per trial | Typical use |
|---|---|---|---|
| Grid search | Fixed lattice over the search space | Full | Few hyperparameters, cheap runs |
| Random search | Independent random draws | Full | Simple baseline, many hyperparameters |
| Bayesian optimisation | Surrogate model with an acquisition function | Full | Few continuous hyperparameters, expensive runs |
| Successive halving and Hyperband | Random draws, with early stopping of weak trials | Adaptive | Many configurations, reliable learning curves |
| Population-based training | Copying and perturbing a running population | Full, shared over time | Schedules, reinforcement learning, parallel clusters |
| muTransfer (muP) | Tune a small model, reuse the settings on a large one | Small models only | Pretraining very large networks |

**Grid and random search.** Grid search evaluates every point of a lattice, and its cost grows exponentially with the number of hyperparameters. Random search draws each configuration independently, so every trial explores a new value of every hyperparameter. Bergstra et al. (2011) report that random search works well for several neural-network tasks but is unreliable for deep belief networks.

**Bayesian optimisation.** The method fits a surrogate, usually a Gaussian process, to the settings and scores seen so far. An acquisition function such as expected improvement balances trying settings that look good against trying settings where the model is uncertain (Frazier, 2018; Shahriari et al., 2016). Snoek et al. (2012) applied this to convolutional networks and other learning algorithms, and reported results that reached or exceeded expert tuning. Each step normally waits for the previous result, so parallel versions need extra design, and the method is best suited to fewer than about twenty continuous dimensions. The tree-structured Parzen estimator, one of the sequential methods in Bergstra et al. (2011), models the densities of good and poor settings rather than the score itself.

**Successive halving and Hyperband.** Jamieson and Talwalkar (2015) cast hyperparameter search as non-stochastic best-arm identification and analysed successive halving for it. Li et al. (2016) introduced Hyperband, which runs successive halving in several brackets, and reported a speedup of more than an order of magnitude over Bayesian competitors on deep-learning and kernel problems.[^2] BOHB (Falkner et al., 2018) keeps Hyperband's budget allocation but proposes settings with a model, and its authors report that it outperforms both parent methods. ASHA (Li et al., 2018) makes successive halving asynchronous, promoting a trial as soon as it ranks in the top fraction. This suits large clusters, and the paper reports near-linear scaling with the number of workers.[^3]

**Population-based training.** Population-based training (PBT) trains a population of models in parallel. At intervals, weaker members copy the weights and hyperparameters of stronger ones, then perturb the copied hyperparameters. Because the settings change during training, PBT finds a schedule rather than one fixed value (Jaderberg et al., 2017). The paper reports faster convergence and higher final performance in deep reinforcement learning, and applies the method to machine translation, maximising BLEU directly, and to generative adversarial networks, maximising the Inception score. The whole population must be trained at once, which needs a parallel cluster, and the schedule it finds belongs to the run that produced it.

**muTransfer.** Under the maximal update parametrisation, many optimal hyperparameters stay stable as the model grows. Yang et al. (2022) therefore tune on small models and reuse the best settings for a large one without tuning the large one. The results and their limits are on the [muP page](../deep-learning/initialisation/mup/index.md), which also explains the parametrisation (Yang & Hu, 2020). The method is tied to width, so it does not by itself settle how to transfer settings across depth or dataset size.

## Connections

- **Scaling and planning.** Large runs are too expensive to tune directly, so teams fit trends on small runs and extrapolate, as in [scaling laws](../models/llm/scaling-laws/index.md). [Compute-optimal training](../models/llm/compute-optimal-training/index.md) applies similar reasoning to choose model size and data for a fixed budget.
- **Bandits.** Successive halving is a bandit method, in which exploring new options must be balanced against exploiting known good ones. The [stochastic bandits](../paradigms/online/stochastic-bandits/index.md) page covers the stochastic setting, which differs from the non-stochastic one in the Hyperband analysis.
- **Evolution.** PBT resembles evolutionary search, with its population and selection. See [Evolutionary computation and swarm intelligence](../../evolutionary/index.md).
- **Brain and mind.** The explore-exploit trade-off that bandit-based HPO formalises is also central to [decision and reward](../../brain-mind/decision-reward/index.md) research on people and animals. The parallel is one of structure. Nothing shows that the brain runs a Gaussian process over its own settings, so it is an analogy, not a mechanism.

## Applications

- **Tuning deep networks.** Snoek et al. (2012) show Bayesian optimisation tuning convolutional networks, and Hyperband was evaluated on deep-learning problems (Li et al., 2016).
- **Reinforcement learning.** PBT was developed for deep reinforcement learning, where runs are long and noisy (Jaderberg et al., 2017).
- **Software.** Optuna (Akiba et al., 2019) lets the search space depend on earlier choices and prunes weak trials during training.
- **Pretraining large models.** Yang et al. (2022) report that settings transferred from a 13-million-parameter model beat published BERT-large results, and that settings from a 40-million-parameter model beat published results for the 6.7-billion-parameter GPT-3.

## Open questions

- Early stopping assumes that a trial's ranking at a small budget predicts its ranking at full budget. When and how often does that fail?
- muTransfer covers width. Is there an equally reliable way to transfer hyperparameters across depth, data size and batch size?
- Repeated tuning on a shared validation set can overfit that set. How should tuning cost and selection effects be reported fairly?
- Which methods remain practical when a single trial costs as much as a full training run?

[^1]: Li et al. (2016) describe Hyperband as a bandit-based method that allocates a predefined resource, such as iterations, data samples or features, to randomly sampled configurations. The bracket structure is in the paper and is not repeated here.
[^2]: The abstract of Li et al. (2016) reports a speedup of "over an order-of-magnitude" relative to the competitor set on a variety of deep-learning and kernel-based problems.
[^3]: The abstract of Li et al. (2018) reports that ASHA scales linearly with the number of workers and was demonstrated on a task with 500 workers.

## References

### Seminal papers

- Bergstra, J., Bardenet, R., Bengio, Y. & Kégl, B. (2011). *Algorithms for Hyper-Parameter Optimization*. NIPS 24. https://proceedings.neurips.cc/paper/2011/hash/86e8f7ab32cfd12577bc2619bc635690-Abstract.html — Compares random search with two sequential expected-improvement methods, including the tree-structured Parzen estimator, on neural networks and deep belief networks.
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). *Practical Bayesian Optimization of Machine Learning Algorithms*. arXiv. https://arxiv.org/abs/1206.2944 — Applies Gaussian-process Bayesian optimisation to tune learning algorithms, including convolutional networks, and reports results that match or exceed expert tuning.
- Jamieson, K. & Talwalkar, A. (2015). *Non-stochastic Best Arm Identification and Hyperparameter Optimization*. arXiv. https://arxiv.org/abs/1502.07943 — Casts hyperparameter search as best-arm identification and analyses successive halving for it.
- Li, L., Jamieson, K., DeSalvo, G., Rostamizadeh, A. & Talwalkar, A. (2016). *Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization*. arXiv. https://arxiv.org/abs/1603.06560 — Introduces Hyperband, which speeds up random search through adaptive resource allocation and early stopping.
- Falkner, S., Klein, A. & Hutter, F. (2018). *BOHB: Robust and Efficient Hyperparameter Optimization at Scale*. arXiv. https://arxiv.org/abs/1807.01774 — Combines model-based proposals with Hyperband's budget allocation, and compares the result with both parent methods.
- Li, L., Jamieson, K., Rostamizadeh, A., Gonina, E., Hardt, M., Recht, B. et al. (2018). *A System for Massively Parallel Hyperparameter Tuning*. arXiv. https://arxiv.org/abs/1810.05934 — Introduces ASHA, an asynchronous version of successive halving, and describes its use in a production tuning service.
- Jaderberg, M., Dalibard, V., Osindero, S., Czarnecki, W. M., Donahue, J., Razavi, A. et al. (2017). *Population Based Training of Neural Networks*. arXiv. https://arxiv.org/abs/1711.09846 — Jointly optimises a population of models and their hyperparameters, producing hyperparameter schedules rather than fixed values.
- Yang, G. & Hu, E. J. (2020). *Feature Learning in Infinite-Width Neural Networks*. arXiv. https://arxiv.org/abs/2011.14522 — Proposes the maximal update parametrisation, which allows feature learning as width grows.
- Yang, G., Hu, E. J., Babuschkin, I., Sidor, S., Liu, X., Farhi, D. et al. (2022). *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*. arXiv. https://arxiv.org/abs/2203.03466 — Introduces muTransfer, which tunes on small models and transfers the settings to larger Transformers and ResNets.

### Surveys and textbooks

- Bischl, B., Binder, M., Lang, M., Pielok, T., Richter, J., Coors, S. et al. (2021). *Hyperparameter Optimization: Foundations, Algorithms, Best Practices and Open Challenges*. arXiv. https://arxiv.org/abs/2107.05847 — Reviews grid and random search, evolutionary methods, Bayesian optimisation, Hyperband and racing, with practical recommendations.
- Frazier, P. I. (2018). *A Tutorial on Bayesian Optimization*. arXiv. https://arxiv.org/abs/1807.02811 — Tutorial on Gaussian-process surrogates and acquisition functions, including expected improvement and parallel and multi-fidelity extensions.
- Shahriari, B., Swersky, K., Wang, Z., Adams, R. P. & de Freitas, N. (2016). *Taking the Human Out of the Loop: A Review of Bayesian Optimization*. Proceedings of the IEEE. https://doi.org/10.1109/JPROC.2015.2494218 — Review of Bayesian optimisation as a way to optimise expensive black-box functions, of which hyperparameter tuning is one case.

### Articles and documentation

- Akiba, T., Sano, S., Yanase, T., Ohta, T. & Koyama, M. (2019). *Optuna: A Next-generation Hyperparameter Optimization Framework*. arXiv. https://arxiv.org/abs/1907.10902 — Describes the Optuna software design, with its define-by-run search spaces and pruning of unpromising trials.
