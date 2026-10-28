---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai
  - start/history/symbolic-era
tags:
  - history
  - expert systems
  - AI winter
aliases:
  - 專家系統
  - AI 寒冬
  - 專家系統與寒冬
  - Expert systems and AI winters
---

# History: expert systems and the AI winters (1974–2006)

After the first wave of optimism, AI entered a period of expert systems, large public projects and cuts in funding. Two periods of reduced funding, usually called the AI winters, followed. The period ended with a return of neural networks, trained on much larger data and computing budgets. This page covers the decline of general-purpose ambitions, the rise and fall of expert systems, and the gradual change in method that set up the deep-learning revolution in the next chapter.

## Overview

The early symbolic programmes had promised general intelligence, and they struggled when problems grew beyond toy domains. In 1972, Lighthill's survey for the UK Science Research Council argued that AI had failed to deliver on its broad aims, and identified the combinatorial explosion as a central obstacle [(Lighthill, 1972)](https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm). Funding for basic research in the UK was cut sharply after the report, which is usually taken as the start of the first winter.

## Key concepts

- **Expert system**: a program that encodes the knowledge of a domain specialist as rules and uses them to reach conclusions. Expert systems were the dominant commercial form of AI in the 1980s.
- **Knowledge engineering**: the process of extracting and encoding expert knowledge, which proved slow and hard to maintain.
- **AI winter**: a period of reduced funding and interest after an overpromised technology fails to meet expectations.
- **Backpropagation**: a method for computing gradients through multi-layer networks, which made neural networks trainable again in the 1980s.

## Expert systems

Expert systems applied rule-based reasoning to specialised fields, including medical diagnosis and equipment configuration. They were useful within narrow limits, but they had costs. Knowledge had to be elicited from experts and kept up to date, rules interacted in unpredictable ways, and the systems could not learn from data. Commercial interest in them grew strongly in the 1980s and then fell as maintenance costs rose and some of the hardware markets they relied on changed.

## The return of neural networks

In 1986, Rumelhart, Hinton and Williams showed that backpropagation could train multi-layer networks to learn internal representations, which answered part of the critique of single-layer perceptrons [(Rumelhart, Hinton and Williams, 1986)](https://doi.org/10.1038/323533a0). The result revived interest in connectionist models. Funding and enthusiasm for neural networks rose and fell again in the 1990s, and the field moved toward statistical methods such as support vector machines and probabilistic models, which had stronger theory and performed well on the data then available. The turn toward statistical methods was a broad change in machine learning, and it shaped the field's methods well beyond neural networks.

## Data and compute

By the 2000s, the amount of labelled data and computing power had grown enough to change what was practical. A large labelled image database, ImageNet, gave researchers a benchmark large enough to test deep networks at scale [(Deng et al., 2009)](https://doi.org/10.1109/cvpr.2009.5206848). The shift from hand-written rules to learned representations, begun in earnest in the 1980s, now had the data to work with it.

## Connections

This period connects to the [symbolic-era history](../symbolic-era/index.md) that came before it, and to the [Symbolic AI](../../../theory/paradigms/symbolic-ai/index.md) page on rule-based systems. The methods that replaced expert systems are covered in [Machine learning](../../../theory/machine-learning/index.md), and backpropagation itself is in [Automatic differentiation](../../../theory/math/automatic-differentiation/index.md).

## Applications

Expert systems were used in medicine, finance, configuration of computer systems and industrial diagnosis. Their legacy is visible in business rule engines and decision-support software, which still use explicit rules alongside learned models.

## Open questions

- Were the winters caused by overpromising, by the methods themselves, or by the funding structures of the time?
- Why did expert systems fail to scale, and does the same problem return when rules are written by hand alongside learned models?
- How much did the turn to statistical methods delay the return of neural networks?

## References

### Seminal papers

- Rumelhart, Hinton and Williams, *Learning representations by back-propagating errors*, Nature (1986). https://doi.org/10.1038/323533a0 — Shows that backpropagation can train multi-layer networks to learn useful internal representations.
- Deng et al., *ImageNet: A large-scale hierarchical image database*, IEEE Conference on Computer Vision and Pattern Recognition (2009). https://doi.org/10.1109/cvpr.2009.5206848 — Describes the large labelled image database that later became the benchmark for deep networks.

### Surveys and textbooks

- Lighthill, *Artificial Intelligence: A General Survey*, Science Research Council (1972). https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm — A critical survey whose conclusions led to cuts in UK AI research funding.

### Articles and documentation

- Hinton, Osindero and Teh, *A Fast Learning Algorithm for Deep Belief Nets*, Neural Computation (2006). https://doi.org/10.1162/neco.2006.18.7.1527 — The paper that is usually counted as the start of the deep-learning revival, covered in [the next chapter](../deep-learning-revolution/index.md).
- Krizhevsky, Sutskever and Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, NeurIPS (2012). https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The AlexNet paper, which marked the scale-up of deep networks on large data.
