---
status: draft
last_reviewed: 2026-10-28
---

# ACT-R: a modular architecture of mind (Anderson et al., 2004)

Separate modules communicate through buffers, and production rules choose the next action.

## Problem

How can cognitive processes such as retrieval, decision and motor control emerge from one system that also matches human timing?

## Core idea

Separate modules (visual, motor, declarative memory, goal) exchange information through buffers, and production rules decide which action to take next. Each module's processing time is set to fit human data.

## Equation or algorithm


  1. Each module places its current results in its buffer.
  2. The production rules match the buffers' contents.
  3. The rule that matches fires, changing the buffers and so the next step.

## Results

The paper reports that one architecture accounts for human data from a range of tasks, with the module timings linked to brain regions.

## Limitations

The architecture is a large set of hand-built components, and fitting it to data needs many modelling choices. The memory equation above is one of the parts that is fitted.

## Connections

- Parent topic: [Cognitive Architectures](../index.md)
- Other method on this topic: [CoALA](../coala/index.md)

## References

### Seminal papers

- Anderson, J. R., et al. (2004). An Integrated Theory of the Mind. *Psychological Review*. https://doi.org/10.1037/0033-295X.111.4.1036 — ACT-R, a cognitive architecture that models memory, goals and learning within one system.
- Laird, J. E., Lebiere, C. & Rosenbloom, P. S. (2017). A Standard Model of the Mind: Toward a Common Computational Framework. *AI Magazine*. https://doi.org/10.1609/aimag.v38i4.2744 — Proposes a community consensus on the shared components of Soar, ACT-R and Sigma.
- Lake, B. M., et al. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — Argues that human-like learning needs causal models, intuitive theories and compositionality.

### Surveys and textbooks

- Kotseruba, I. & Tsotsos, J. K. (2020). 40 years of cognitive architectures: core cognitive abilities and practical applications. *Artificial Intelligence Review*. https://doi.org/10.1007/s10462-018-9646-y — A survey of cognitive architectures by the abilities they cover, and their practical uses.
- Sumers, T. R., Yao, S., Narasimhan, K. & Griffiths, T. L. (2023). Cognitive Architectures for Language Agents. arXiv. https://arxiv.org/abs/2309.02427 — Proposes CoALA, a framework that organises language agents by memory, actions and decision-making.
