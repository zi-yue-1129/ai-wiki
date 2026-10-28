---
related:
- applications/healthcare
---

# Semi- & Weakly Supervised Learning

Labels are often the bottleneck: a radiologist's hour is expensive, but unlabelled scans are plentiful. These paradigms squeeze more out of limited or imperfect supervision.

## Semi-supervised learning

**Setting:** a small labelled set \(D_L\) and a large unlabelled set \(D_U\) from the same distribution.

**Assumptions that make it work:**

- **Smoothness**: nearby points share labels.
- **Cluster assumption**: decision boundaries pass through low-density regions.
- **Manifold assumption**: data lie on a low-dimensional manifold.

| Method | Idea |
|---|---|
| Self-training / pseudo-labelling | Train on \(D_L\), label confident points in \(D_U\), retrain |
| Co-training | Two models on different feature views label data for each other |
| Consistency regularisation | Predictions should be stable under perturbation (Π-model, Mean Teacher, UDA) |
| FixMatch and successors | Pseudo-label a weakly augmented image, train the strongly augmented version to match |
| Graph-based label propagation | Spread labels over a similarity graph |
| Generative approaches | Semi-supervised VAEs and GANs |
| Pre-train then fine-tune | Self-supervised pre-training on \(D_U\) + supervised fine-tuning on \(D_L\) — today's dominant recipe |

Noisy Student (Xie et al., 2020) showed self-training with a larger, noised student improves ImageNet accuracy and robustness.

## Weakly supervised learning

**Setting:** labels exist but are noisy, coarse, indirect or incomplete.

| Type | Example | Methods |
|---|---|---|
| Inexact (coarse) | Image-level label "contains tumour", need pixel mask | Multiple-instance learning, class activation maps |
| Inaccurate (noisy) | Crowdsourced labels with errors | Noise-robust losses, label-noise modelling, co-teaching |
| Incomplete | Only some positives labelled | PU learning (see [Other Paradigms](../other/index.md)) |
| Programmatic | Heuristic labelling functions | Data programming (Snorkel) combines many noisy rules |
| Distant supervision | Align text with a knowledge base to label relations | Relation extraction |
| Natural-language supervision | Image–caption pairs from the web | CLIP — weakly supervised at internet scale |

Whole-slide pathology images are a canonical case: gigapixel slides with only a slide-level diagnosis are handled by attention-based multiple-instance learning (Ilse et al., 2018; Campanella et al., 2019).

## Practical advice

1. Start with a strong pre-trained model; it often beats elaborate semi-supervised tricks.
2. Check that unlabelled data really come from the same distribution — otherwise pseudo-labels reinforce errors.
3. Calibrate confidence before thresholding pseudo-labels.
4. Keep a clean, expert-labelled test set; never evaluate on pseudo-labels.

## Human learning parallel

Children receive very few explicit labels ("that's a dog") relative to the vast unlabelled experience they absorb. Studies of semi-supervised category learning (e.g. Zhu et al., 2007, "Humans perform semi-supervised classification too") show that unlabelled examples shift human category boundaries in the same direction predicted by the cluster assumption.

## Subtopics

- [Consistency regularisation](consistency-regularisation/index.md): Mean Teacher, MixMatch and FixMatch.
- [Pseudo-labelling and self-training](pseudo-labelling-and-self-training/index.md): confident predictions as training targets.
- [Graph-based methods](graph-based-methods/index.md): label propagation, manifold regularisation and graph networks.
- [Weak and programmatic supervision](weak-and-programmatic-supervision/index.md): labelling functions, data programming and Snorkel.
- [Theory and assumptions](theory-and-assumptions/index.md): smoothness, cluster and manifold assumptions.

## Further reading

- van Engelen & Hoos (2020), "A survey on semi-supervised learning", *Machine Learning*. https://doi.org/10.1007/s10994-019-05855-6
- Zhou (2018), "A brief introduction to weakly supervised learning", *National Science Review*. https://doi.org/10.1093/nsr/nwx106

## References

- Laine & Aila (2017), "Temporal ensembling for semi-supervised learning", ICLR, [arXiv:1610.02242](https://arxiv.org/abs/1610.02242) — Early consistency method that uses averaged predictions as targets.
- Sohn et al. (2020), "FixMatch: simplifying semi-supervised learning with consistency and confidence", NeurIPS, [arXiv:2001.07685](https://arxiv.org/abs/2001.07685) — A simple, strong method combining pseudo-labels and consistency.
- Zhu, Ghahramani & Lafferty (2003), "Semi-supervised learning using Gaussian fields and harmonic functions", ICML. https://www.cs.cmu.edu/~zhuxj/pub/zgl.pdf — Label propagation over graphs, a foundational graph method.
- Ratner et al. (2017), "Snorkel: rapid training data creation with weak supervision", [arXiv:1711.10160](https://arxiv.org/abs/1711.10160) — Turns labelling functions into training data quickly.
- Oliver et al. (2018), "Realistic evaluation of deep semi-supervised learning algorithms", NeurIPS, [arXiv:1804.09170](https://arxiv.org/abs/1804.09170) — Shows that fair evaluation changes many reported conclusions.
