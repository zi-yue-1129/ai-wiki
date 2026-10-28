---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai
  - theory/paradigms/symbolic-ai/knowledge-graphs
  - theory/paradigms/probabilistic/graphical-models
tags:
  - neuro-symbolic AI
  - logic
  - hybrid AI
aliases:
  - 神經符號 AI
  - 神經符號人工智慧
  - Neuro-symbolic AI
  - Neurosymbolic AI
  - Markov logic networks
---

# Neuro-Symbolic AI

Neuro-symbolic AI combines neural networks, which learn from data, with symbolic components such as logic, rules and knowledge graphs, which represent and reason with structure. The aim is to keep the robustness of learning and the explicitness of reasoning in one system. Part of [Symbolic AI, search and planning](../index.md).

## Overview

Neural networks learn from large data but are hard to inspect, and they often generalise poorly to new combinations of concepts. Symbolic systems reason precisely about structure but need knowledge written by hand. Neuro-symbolic work asks how to get the best of both. Garcez and Lamb (2023) describe the field as a third wave of AI that follows the statistical learning of the second wave.

## Key concepts

- **Logic as constraint**: a logical rule is turned into a training signal, so that the network is penalised when it violates the rule.
- **Logic as representation**: logical formulas are evaluated on continuous, fuzzy truth values, so that they can be differentiated and trained with the network (Serafini & Garcez, 2016).
- **Rule extraction**: a trained network is analysed to produce symbolic rules that describe its behaviour.
- **Probabilistic logic**: weighted logical formulas define a distribution over possible worlds, which is one of the oldest integrations of logic and learning (Richardson & Domingos, 2006).

## How it works

Three broad patterns appear in the literature. In the first, a neural model is trained with a loss that includes logical constraints, which guides learning with prior knowledge. In the second, logical structure is built into the network, so that its inputs and outputs are predicates or relations. In the third, a logical or probabilistic model is learned end to end, with differentiable operations for the rules, as in differentiable inductive logic programming (Evans & Grefenstette, 2018).

## Key methods

- [Markov logic networks](markov-logic-networks.md): weighted first-order formulas that define a log-linear distribution over possible worlds. They combine logic with the probabilistic graphical models described in [graphical models](../../probabilistic/graphical-models/index.md).

Other integrations, including logic tensor networks (Serafini & Garcez, 2016) and differentiable inductive logic (Evans & Grefenstette, 2018), are summarised here and do not have their own pages yet.

## Connections

- [Knowledge graphs and knowledge representation](../knowledge-graphs/index.md) supply the structured facts that neuro-symbolic systems reason about.
- [Probabilistic graphical models](../../probabilistic/graphical-models/index.md) give the probabilistic model that Markov logic networks use.
- [Supervised learning](../../supervised/index.md) covers the neural training methods that are the learning side of most of these systems.

## Applications

- **Reasoning over relational data**: entity resolution and relational classification with logical rules and learned weights (Richardson & Domingos, 2006).
- **Learning with prior knowledge**: training models for tasks where a few rules are known and data are limited.
- **Interpretable learning**: rules induced from data that a person can check (Evans & Grefenstette, 2018).

## Open questions

- Grounding logic in continuous representations is not unique, and different fuzzy semantics can give different results.
- Scaling exact or approximate probabilistic logic to large domains remains costly.
- Whether neuro-symbolic systems generalise better than purely neural ones, and on which tasks, needs systematic evaluation (Garcez & Lamb, 2023).

## References

### Seminal papers

- Richardson, M. & Domingos, P. (2006). Markov logic networks. *Machine Learning* 62(1–2), 107–136. https://doi.org/10.1007/s10994-006-5833-1 — Introduces weighted first-order formulas as a template for a Markov network over possible worlds.
- Serafini, L. & Garcez, A. d'A. (2016). Logic tensor networks: deep learning and logical reasoning from data and knowledge. arXiv:1606.04422. https://arxiv.org/abs/1606.04422 — Proposes real-valued logic that lets first-order formulas be trained together with neural models.
- Evans, R. & Grefenstette, E. (2018). Learning explanatory rules from noisy data. *Journal of Artificial Intelligence Research* 61, 1–64. https://doi.org/10.1613/jair.5714 — Differentiable inductive logic programming that learns rules from noisy data.

### Surveys and textbooks

- Garcez, A. d'A. & Lamb, L. C. (2023). Neurosymbolic AI: the 3rd wave. *Artificial Intelligence Review* 56(11), 12387–12406. https://doi.org/10.1007/s10462-023-10448-w — Survey of the neuro-symbolic field and its main directions.
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook background on logic and probabilistic reasoning that neuro-symbolic work combines with learning.
