---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai
  - start/history
tags:
  - history
  - symbolic AI
  - perceptron
aliases:
  - 符號時代
  - 達特茅斯會議
  - 符號 AI 時期
  - Symbolic era
---

# History: Dartmouth and the symbolic era (1956–1974)

The field of artificial intelligence took shape in the mid-1950s, when researchers proposed that reasoning could be written as manipulation of symbols and that machines could be made to learn. The first two decades produced striking programs and a wave of optimism, alongside an early debate about what simple learning machines could and could not compute. This page covers that period, which ended with the funding cuts discussed in [the next chapter](../expert-systems-and-winters/index.md).

## Overview

The name "artificial intelligence" appears in the 1955 proposal for a summer research project at Dartmouth College. The proposal states that the study is based on the conjecture that "every aspect of learning or any other feature of intelligence can in principle be so precisely described" that a machine could be built to simulate it [(McCarthy et al., 1955)](http://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html). The workshop took place in 1956 and brought together researchers who would shape the next two decades of the field.

## Key concepts

- **Symbolic AI**: the view that intelligence can be built from symbols, rules and search over a space of states. See [Symbolic AI](../../../theory/paradigms/symbolic-ai/index.md).
- **Physical symbol system**: Newell and Simon's term for a system that manipulates symbols to produce intelligent behaviour.
- **Heuristic search**: the use of rules of thumb to direct search through a large space of possibilities.
- **Perceptron**: a single-layer learning machine that adjusts weights from labelled examples.

## Early programs and the symbolic hypothesis

Newell and Simon's programs, including the Logic Theorist and the General Problem Solver, were among the first to show machines carrying out tasks that humans called reasoning. Newell and Simon later set out their approach as an empirical science of computing, arguing that symbol systems and heuristic search are the basis of intelligence [(Newell and Simon, 1976)](https://doi.org/10.1145/360018.360022). This view shaped research for two decades, and it is the source of the term "symbolic" used in later classifications.

## The perceptron

Rosenblatt introduced the perceptron as a probabilistic model of information storage in the brain. Its learning rule adjusted connection weights from examples, and it gave early evidence that a machine could learn a classification from data rather than from hand-written rules [(Rosenblatt, 1958)](https://doi.org/10.1037/h0042519). The perceptron is one of the earliest meeting points between the statistical learning in [Machine learning](../../../theory/machine-learning/index.md) and the neural models that returned in the 1980s.

## The critique

In 1969, Minsky and Papert analysed the limits of single-layer perceptrons, showing that they cannot compute certain functions such as the exclusive-or. The book is often read as having cooled interest in neural networks, though its analysis applied to single layers and not to multi-layer networks, which later work showed could be trained [(Minsky and Papert, 1969)](https://doi.org/10.7551/mitpress/4943.003.0015). The critique is a good example of how a limitation can be correctly stated and still be misread as a verdict on a whole family of models.

## The first optimism

Early programs produced an atmosphere of confidence. Researchers expected general machine intelligence within a generation. That expectation was tested as programs struggled outside narrow domains. The gap between a demonstration in a toy world and a system that works in the real one is a theme that recurs throughout AI's history.

## Connections

The symbolic programme set many of the questions that the [Symbolic AI](../../../theory/paradigms/symbolic-ai/index.md) pages still answer. The perceptron links to the [Deep learning](../../../theory/deep-learning/index.md) history in the next chapters. For the broader timeline, see the [History of AI](../index.md) overview.

## Applications

The methods of the period were applied to theorem proving, game playing, puzzle solving and early language tasks. Those applications laid the ground for later expert systems and planning software.

## Open questions

- Why did early optimism about symbolic reasoning outrun what the methods could deliver?
- How much of the perceptron critique was about the model, and how much about the way it was presented?
- Which early ideas are being revisited in current work on reasoning systems?

## References

### Seminal papers

- McCarthy, Minsky, Rochester and Shannon, *A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence* (1955). http://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html — The proposal that introduced the name "artificial intelligence" and set out its conjecture.
- Rosenblatt, *The perceptron: A probabilistic model for information storage and organization in the brain*, Psychological Review (1958). https://doi.org/10.1037/h0042519 — The founding paper on the perceptron learning machine.
- Newell and Simon, *Computer science as empirical inquiry: symbols and search*, Communications of the ACM (1976). https://doi.org/10.1145/360018.360022 — Sets out the physical symbol system hypothesis and the role of heuristic search.
- Minsky and Papert, *Perceptrons: An Introduction to Computational Geometry* (1969; expanded edition 1988), MIT Press. https://doi.org/10.7551/mitpress/4943.003.0015 — Analyses the limits of single-layer perceptrons. The link is to the 1988 edition's introductory chapter.

### Surveys and textbooks

- Lighthill, *Artificial Intelligence: A General Survey*, Science Research Council (1972). https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm — A critical survey of AI's progress, which dates the report to 1972 and was published in 1973. It frames the combinatorial explosion as a central obstacle. Covered in more detail in [the next chapter](../expert-systems-and-winters/index.md).
