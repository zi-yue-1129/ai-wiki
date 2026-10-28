---
related:
- theory/paradigms/semi-supervised/index.md
- theory/paradigms/active/index.md
tags:
  - transfer learning
  - domain adaptation
  - distribution shift
---

# Domain Adaptation

Domain adaptation transfers a model from a labelled source domain to a target domain whose input distribution differs, usually with few or no target labels. A model that scores well on the source can fail on the target because clinic scanners, camera settings or languages differ. Domain adaptation tries to reduce that gap without collecting a full new labelled dataset.

## Overview

The shift is described by how the joint distribution of inputs and labels changes. Under covariate shift the input distribution changes while the label rule stays the same. Label shift changes the class frequencies, and concept shift changes the labelling rule itself. Most domain adaptation methods assume covariate shift, because it is the setting in which a common representation can be learned.

## Methods

- **Discrepancy minimisation**: add a loss that pulls source and target feature distributions together, for example with maximum mean discrepancy (MMD) or matching second-order statistics (CORAL).
- **Domain-adversarial training**: train a domain classifier and make the features it sees uninformative about the domain, so that the label classifier transfers.
- **Test-time adaptation**: update a model on unlabelled target inputs at inference, for example by minimising prediction entropy.
- **Importance re-weighting**: weight source examples by how likely they are under the target distribution.

## Benchmarks

Real-world shifts are hard to simulate. Benchmarks such as WILDS collect shifts that occur in medicine, satellite imagery and web data, and they show that methods which work on synthetic shifts often fail on natural ones.

## Connections

Domain adaptation shares the self-training idea of [semi-supervised learning](../../semi-supervised/index.md), where unlabelled target data is used directly. Choosing which target examples to label is the problem studied in [active learning](../../active/index.md). The theory of when adaptation is possible is in [transfer theory](../transfer-theory/index.md).

## Applications

Medical imaging across hospitals, speech recognition for new accents, self-driving perception under new weather, and sentiment analysis across product domains.

## Open questions

Most methods assume covariate shift, and their guarantees break under label or concept shift. It is hard to validate a domain-adapted model without target labels, and feature alignment can destroy information needed for the task.

## References

### Seminal papers

- Ganin et al. (2016), "Domain-adversarial training of neural networks", JMLR, arXiv:1505.07818 — DANN, which learns features that a domain classifier cannot use to tell source from target.
- Long, Cao, Wang & Jordan (2015), "Learning transferable features with deep adaptation networks", ICML. https://people.eecs.berkeley.edu/~jordan/papers/long-etal-icml2015.pdf — Aligns source and target features across several layers with multi-kernel maximum mean discrepancy.
- Sun & Saenko (2016), "Deep CORAL: correlation alignment for deep domain adaptation", ECCV workshops, arXiv:1607.01719 — Matches the covariance of source and target features with a simple differentiable loss.
- Wang, Shelhamer, Liu, Olshausen & Darrell (2021), "Tent: fully test-time adaptation by entropy minimization", ICLR, arXiv:2006.10726 — Adapts a model at test time using only unlabelled target inputs.
- Koh et al. (2021), "WILDS: a benchmark of in-the-wild distribution shifts", ICML, arXiv:2012.07421 — Benchmark of natural distribution shifts across medicine, satellite imagery and web data.

### Surveys and textbooks

- Weiss, Khoshgoftaar & Wang (2016), "A survey of transfer learning", Journal of Big Data. https://link.springer.com/10.1186/s40537-016-0043-6 — Survey of transfer and adaptation methods, with a section on settings where transfer fails.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Quiñonero-Candela, Sugiyama, Schwaighofer & Lawrence (2009), *Dataset Shift in Machine Learning*, MIT Press. No link checked.
