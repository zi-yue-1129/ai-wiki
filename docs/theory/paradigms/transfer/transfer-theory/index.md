---
related:
- theory/paradigms/supervised/generalization-theory/index.md
tags:
  - transfer learning
  - learning theory
  - negative transfer
---

# Transfer Theory

Transfer theory asks when learning on a source domain actually helps a target domain, and by how much. The answers are bounds on target error that depend on how different the domains are, and an account of when transfer hurts, which is called negative transfer.

## Overview

The main bound says that target error is at most source error plus a term that measures the discrepancy between the two domains, plus a term for the unavoidable error of the best joint hypothesis. The discrepancy is usually measured with a divergence that depends on the hypothesis class. A small discrepancy means that the source is informative about the target.

## Key ideas

- **Domain divergence**: the H-divergence and related measures quantify how different two distributions look to the classifiers under study, and they give the bound above.
- **Representation learning**: the bound suggests learning representations that keep the source error low while making domains indistinguishable, which is what domain-adversarial methods do.
- **Negative transfer**: when source and target are too dissimilar, using the source can make performance worse than training from scratch.
- **Measuring transfer**: comparing against a from-scratch baseline is the practical test, since theory bounds are often loose.

## Connections

The bounds rely on the same tools as [generalisation theory](../../supervised/generalization-theory/index.md) in supervised learning. The divergence-minimising methods are described in [domain adaptation](../domain-adaptation/index.md), and the question of which tasks should share a model is in [multi-task learning](../multi-task-learning/index.md).

## Applications

Deciding whether to reuse a model from one hospital at another, choosing a source dataset for a new language, and deciding whether a simulator is good enough to train a robot policy.

## Open questions

Bounds are often too loose to guide practice, and divergence measures are hard to estimate from finite unlabelled data. A general theory of when transfer helps, which covers label and concept shift, is still incomplete.

## References

### Seminal papers

- Ben-David, Blitzer, Crammer, Kulesza, Pereira & Vaughan (2010), "A theory of learning from different domains", Machine Learning. https://doi.org/10.1007/s10994-009-5152-4 — Bounds target error by source error plus a divergence between the two domains.
- Ben-David, Blitzer, Crammer & Pereira (2006), "Analysis of representations for domain adaptation", NeurIPS. https://proceedings.neurips.cc/paper_files/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf — Earlier version of the bound, applied to the choice of learned representations.
- Rosenstein, Marx, Kaelbling & Dietterich (2005), "To transfer or not to transfer", NIPS workshop on inductive transfer. https://people.csail.mit.edu/mtr/papers/RosensteinM05c.html — Shows that transfer from an unrelated source can hurt, which is the basic case of negative transfer.

### Surveys and textbooks

- Torrey & Shavlik (2009), "Transfer learning", in *Handbook of Research on Machine Learning Applications*. https://ftp1.cs.wisc.edu/machine-learning/shavlik-group/torrey.handbook09.pdf — Chapter on transfer methods and on how to tell when they help.
- Weiss, Khoshgoftaar & Wang (2016), "A survey of transfer learning", Journal of Big Data. https://link.springer.com/10.1186/s40537-016-0043-6 — Survey with definitions of transfer settings and a discussion of negative transfer.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Redko, Morvant, Habrard, Sebban & Bennani (2019), *Advances in Domain Adaptation Theory*, Elsevier. https://tienda.elsevier.com/books/advances-in-domain-adaptation-theory/redko/978-1-78548-236-6 — Theoretical bounds on how well a model trained in one domain transfers to another.
