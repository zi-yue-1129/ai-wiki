---
tags:
  - semi-supervised learning
  - weak supervision
  - data programming
---

# Weak and Programmatic Supervision

Weak supervision produces training labels cheaply, from heuristics, rules, existing databases or crowd workers, instead of careful manual annotation. The labels are noisy and sometimes incomplete, and the main task is to combine them into a usable training set.

## Overview

Instead of one expert label per example, several labelling functions each vote on each example, abstaining when they have no opinion. The votes disagree and overlap, so a model must estimate how accurate each source is and how the sources are correlated. The result is a probabilistic label for each example that can train any downstream model.

## Sources of weak labels

- **Labelling functions** are small programs or rules written by domain experts, such as keyword matches or pattern checks.
- **Distant supervision** labels text using an existing knowledge base, such as aligning sentences with known facts.
- **Crowdsourcing** collects several noisy annotations per example, and aggregates them by estimating annotator reliability.
- **Model-generated labels** from pre-trained models, which must be checked for bias and errors.

## Combining the labels

Data programming (Ratner et al., 2016) models the labelling functions as a generative process, learns their accuracies and correlations without ground truth, and outputs a probability for each example. Snorkel packages this approach as a system for rapid dataset creation, and later work extends it to multiple tasks.

## Connections

Weak supervision is a form of [semi-supervised learning](../index.md), using a little expert input and a lot of cheap signal. It relates to [active learning](../../active/index.md), which chooses which labels to request, and to [consistency regularisation](../consistency-regularisation/index.md), which uses unlabelled data. Crowd labels are discussed in the [supervised learning](../../supervised/index.md) section as "where labels come from".

## Applications

Clinical text classification from rules and ontologies, document and entity tagging in enterprise data, medical image labelling from radiology reports, and creating training sets for new products quickly.

## Open questions

Estimating the accuracy of labelling functions without any gold labels is not always identifiable. Bias in heuristic labels can be amplified silently, and it is hard to tell when a weak dataset is good enough for a high-stakes task.

## References

### Seminal papers

- Ratner, De Sa, Wu, Selsam & Ré (2016), "Data programming: creating large training sets, quickly", NIPS, [arXiv:1605.07723](https://arxiv.org/abs/1605.07723) — Models noisy labelling functions as a generative process to produce training labels.
- Ratner, Bach, Ehrenberg, Fries, Wu & Ré (2017), "Snorkel: rapid training data creation with weak supervision", [arXiv:1711.10160](https://arxiv.org/abs/1711.10160) — The Snorkel system, which turns labelling functions into training sets quickly.
- Ratner, Hancock, Dunnmon, Sala, Pandey & Ré (2019), "Training complex models with multi-task weak supervision", AAAI, [arXiv:1810.02840](https://arxiv.org/abs/1810.02840) — Extends weak supervision to several tasks sharing the same labelling functions.
- Mintz, Bills, Snow & Jurafsky (2009), "Distant supervision for relation extraction without labeled data", ACL. https://aclanthology.org/P09-1113/ — Labels text by aligning it with a knowledge base, an early form of weak supervision.
- Dehghani, Mehrjou, Gouws, Kamps & Schölkopf (2018), "Fidelity-weighted learning", ICLR, [arXiv:1711.02799](https://arxiv.org/abs/1711.02799) — Weights noisy labels by an estimate of how reliable they are.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none beyond the entries above)

## Further reading

