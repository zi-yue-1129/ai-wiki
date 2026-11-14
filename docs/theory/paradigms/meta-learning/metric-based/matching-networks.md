---
related:
  - theory/paradigms/meta-learning
  - theory/paradigms/supervised/instance-based-and-probabilistic
  - theory/evaluation/benchmarks/few-shot
tags:
  - meta-learning
  - few-shot learning
  - metric learning
  - attention
aliases:
  - Matching networks
  - 匹配網路
  - One-shot matching
last_reviewed: 2026-11-01
---

# Matching Networks

Matching networks (Vinyals et al., 2016) classify a new example by attention over a small labelled support set. The model is trained on episodes that imitate the test situation, so it learns to match a new example to labelled ones without fine-tuning on the new classes. The family of similar methods is on the [Metric-based Few-shot Learning](index.md) page.

## Problem

One-shot learning means learning a new class from a single labelled example. Deep networks trained by gradient descent usually need far more labels per class, and they cannot absorb a new class quickly without retraining. Non-parametric methods such as nearest neighbours can add examples at once, but they depend on a fixed distance, which is weak on raw images. The paper asks how to combine the two: a learned embedding with a rule that can use new labelled examples at test time.

## Core idea

The model predicts a label as a weighted vote over the labels of the support set \(S = \{(x_i, y_i)\}_{i=1}^{k}\). The weight of each support example is a softmax over its similarity to the query, so the prediction is an attention-weighted average of one-hot labels. This is why the paper relates the rule to kernel density estimation and to nearest neighbours.

The training procedure is episodic. Each episode samples a label set \(L\) from a task distribution, then draws a support set \(S\) and a batch \(B\) from the classes in \(L\). The network is trained to predict the labels in \(B\) given \(S\). The paper's stated principle is that "test and train conditions must match": a model trained on episodes with few examples per class is evaluated on episodes of the same form.

## Algorithm

With cosine similarity \(c\), embeddings \(f\) for the query and \(g\) for the support examples (possibly \(f = g\)), the prediction is

\[
\hat y = \sum_{i=1}^{k} a(\hat x, x_i)\, y_i, \qquad a(\hat x, x_i) = \frac{\exp\big(c(f(\hat x), g(x_i))\big)}{\sum_{j=1}^{k} \exp\big(c(f(\hat x), g(x_j))\big)}
\]

The paper also introduces **full-context embeddings**. In the basic model each support example is embedded alone. The full-context version makes the embeddings depend on the whole support set. A bidirectional LSTM computes \(g(x_i, S)\) over the support set, and an LSTM with read-attention over \(g(S)\) computes \(f(\hat x, S)\) for a fixed number of processing steps.

## Results

The paper evaluates on Omniglot and mini-ImageNet. The tables below use the paper's cosine-matching rows. The full-context variant adds 3.0 points on 1-shot mini-ImageNet and 0.8 points on 5-shot, and the paper reports no difference on Omniglot.

**Omniglot** (Table 1, accuracy, no fine-tuning):

| Setting | 5-way 1-shot | 5-way 5-shot | 20-way 1-shot | 20-way 5-shot |
|---|---|---|---|---|
| Cosine matching | 98.1% | 98.9% | 93.8% | 98.5% |

**mini-ImageNet, 5-way** (Table 2, accuracy):

| Setting | 1-shot | 5-shot |
|---|---|---|
| Cosine matching, no fine-tuning | 41.2% | 56.2% |
| Cosine matching, with full-context embeddings | 44.2% | 57.0% |
| Cosine matching, full-context, with fine-tuning | 46.6% | 60.0% |

These results are on the benchmarks described in [Omniglot](../../../evaluation/benchmarks/few-shot/omniglot.md) and [mini-ImageNet](../../../evaluation/benchmarks/few-shot/mini-imagenet.md).

## Limitations

- **Cost grows with the support set.** The paper calls this "an obvious drawback" of the model, since the computation grows with the size of the support set. The authors mention sparse and sampling-based variants as possible remedies.
- **Label-distribution bias.** On a fine-grained subtask of ImageNet dog classes, performance fell by about 1%. The authors attribute this to training on randomly sampled label sets rather than fine-grained ones, and say the model "suffers" when the label distribution has obvious biases.
- **Distribution shift.** Performance is expected to drop when the test tasks differ far from the training task distribution, which the paper notes in Section 2.2.
- **Fine-tuning overfits.** Fine-tuning on the support set leads to "massive overfitting," although the authors observe gains because the models are highly regularised.

## Connections

- The method is the attention form of the metric-based family, alongside [prototypical networks](https://arxiv.org/abs/1703.05175), which replace attention with a class mean.
- The episodic training it introduced is widely used by other [meta-learning](../index.md) methods for few-shot tasks.
- The nearest-neighbour rule it generalises is covered under [instance-based methods](../../supervised/instance-based-and-probabilistic/index.md) of supervised learning.

## Open issues

- Can the cost of the full support-set computation be reduced without losing accuracy?
- How should episodes be sampled so that the model does not depend on the label distribution of the training tasks?
- Does full-context embedding help more on harder data, as the paper's results suggest, and why?

## References

### Seminal papers

- Vinyals, O., Blundell, C., Lillicrap, T., Kavukcuoglu, K. & Wierstra, D. (2016). Matching Networks for One Shot Learning. NeurIPS. [arXiv:1606.04080](https://arxiv.org/abs/1606.04080) — Introduces attention over a labelled support set, trained on episodes that mimic test conditions.
- Lake, B. M., Salakhutdinov, R. & Tenenbaum, J. B. (2015). Human-level concept learning through probabilistic program induction. Science, 350, 1332–1338. [DOI 10.1126/science.aab3050](https://doi.org/10.1126/science.aab3050) — Cited for the Omniglot benchmark that the matching networks paper uses.
- Snell, J., Swersky, K. & Zemel, R. (2017). Prototypical Networks for Few-shot Learning. [arXiv:1703.05175](https://arxiv.org/abs/1703.05175) — Replaces the attention rule with a distance to class prototypes, a closely related metric-based method.
- Santoro, A. et al. (2016). One-shot Learning with Memory-Augmented Neural Networks. [arXiv:1605.06065](https://arxiv.org/abs/1605.06065) — Uses an external memory for one-shot prediction, a contemporary approach to the same problem.
- Hochreiter, S. & Schmidhuber, J. (1997). Long Short-Term Memory. Neural Computation, 9, 1735–1780. [DOI 10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735) — The LSTM architecture used for the full-context embeddings.

### Surveys and textbooks

- Hospedales, T., Antoniou, A., Micaelli, P. & Storkey, A. (2021). Meta-learning in Neural Networks: A Survey. IEEE TPAMI. [arXiv:2004.05439](https://arxiv.org/abs/2004.05439) — Places matching networks among the other meta-learning families.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
