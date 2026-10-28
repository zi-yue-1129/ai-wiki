---
related:
- theory/paradigms/supervised/generalization-theory/index.md
tags:
  - active learning
  - learning theory
  - sample complexity
---

# Theory and Sample Complexity

Active learning theory asks how many labels are needed to reach a target error, and how much better that is than passive learning from randomly chosen labels. The main result is that for some problems the number of labels needed can drop from what is needed with random sampling to something exponentially smaller, but only under strong assumptions about the data.

## Overview

Theory compares the label complexity of active and passive learners under a fixed hypothesis class and a data distribution. Disagreement-based methods keep the set of hypotheses consistent with the labels so far, and they query only where the consistent hypotheses still disagree. Results show that the gains depend heavily on noise and on the distribution of the data.

## Key ideas

- **Coarse sample complexity**: early bounds show that active learning can reduce the number of labels in favourable cases, which motivated the field.
- **Disagreement-based learning**: query only where consistent hypotheses disagree, which gives label savings in the realisable case.
- **Importance-weighted sampling**: correct for the bias of selective sampling by weighting labelled examples, which allows agnostic active learning under noise.
- **True sample complexity**: bounds that depend on the actual difficulty of the problem, not on worst-case constants, which clarifies when active learning helps in practice.

## Connections

The bounds use the same notions of hypothesis complexity as [generalisation theory](../../supervised/generalization-theory/index.md). The importance-weighting idea also appears in [domain adaptation](../../transfer/domain-adaptation/index.md), where the source and target distributions differ.

## Applications

Deciding whether an active labelling campaign is likely to save money, and designing query rules for settings with noisy labels where the theory is best understood.

## Open questions

Theory often assumes a realisable or simple noise model, while labels in practice are noisy and costly. The gap between theoretical label savings and gains in deep learning remains poorly explained.

## References

### Seminal papers

- Dasgupta (2005), "Coarse sample complexity bounds for active learning", NeurIPS. https://proceedings.neurips.cc/paper/2005/hash/6e82873a32b95af115de1c414a1849cb-Abstract.html — Early bounds showing when active learning can reduce the number of labels needed.
- Balcan, Beygelzimer & Langford (2009), "Importance weighted active learning", ICML, arXiv:0812.4952 — Importance-weighted sampling that gives active learning guarantees under label noise.
- Balcan, Hanneke & Vaughan (2010), "The true sample complexity of active learning", Machine Learning. https://doi.org/10.1007/s10994-010-5174-y — Gives sample-complexity bounds that depend on the true difficulty of the problem.

### Surveys and textbooks

- Hanneke (2014), *Theory of Disagreement-Based Active Learning*, Foundations and Trends in Machine Learning. https://doi.org/10.1561/2200000037 — Monograph on disagreement-based active learning and its label complexity.
- Settles (2009), "Active learning literature survey", Computer Sciences Technical Report 1648, University of Wisconsin-Madison. https://research.cs.wisc.edu/techreports/2009/TR1648.pdf — Survey that summarises the theoretical results alongside practical methods.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Hanneke (2011), "Rates of convergence in active learning", Annals of Statistics. No link checked.
