---
status: draft
last_reviewed: 2026-10-28
---

# CoALA: cognitive architectures for language agents (Sumers et al., 2023)

An agent with modular memory and a set of internal actions, designed for language models.

## Problem

Language agents built on large language models have shown strong results, but there is no systematic framework for organising them.

## Core idea

Describe an agent with modular memory (working, episodic, semantic and procedural), a set of internal actions (retrieval, reasoning, learning) and external actions (grounding in an environment), and a decision cycle that chooses among them.

## Method

A conceptual framework. The paper uses it to categorise existing agents and to suggest directions for building new ones.

## Results

The paper reports no new system or benchmark. Its contribution is the categorisation and the design vocabulary.

## Limitations

A framework is not an evaluated system, and the categories may blur when a real agent does not fit them neatly.

## Connections

- Parent topic: [Cognitive Architectures](../index.md)
- Other method on this topic: [ACT-R](../act-r/index.md)

## References

### Seminal papers

- Anderson, J. R., et al. (2004). An Integrated Theory of the Mind. *Psychological Review*. https://doi.org/10.1037/0033-295X.111.4.1036 — ACT-R, a cognitive architecture that models memory, goals and learning within one system.
- Laird, J. E., Lebiere, C. & Rosenbloom, P. S. (2017). A Standard Model of the Mind: Toward a Common Computational Framework. *AI Magazine*. https://doi.org/10.1609/aimag.v38i4.2744 — Proposes a community consensus on the shared components of Soar, ACT-R and Sigma.
- Lake, B. M., et al. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — Argues that human-like learning needs causal models, intuitive theories and compositionality.

### Surveys and textbooks

- Kotseruba, I. & Tsotsos, J. K. (2020). 40 years of cognitive architectures: core cognitive abilities and practical applications. *Artificial Intelligence Review*. https://doi.org/10.1007/s10462-018-9646-y — A survey of cognitive architectures by the abilities they cover, and their practical uses.
- Sumers, T. R., Yao, S., Narasimhan, K. & Griffiths, T. L. (2023). Cognitive Architectures for Language Agents. arXiv. https://arxiv.org/abs/2309.02427 — Proposes CoALA, a framework that organises language agents by memory, actions and decision-making.
