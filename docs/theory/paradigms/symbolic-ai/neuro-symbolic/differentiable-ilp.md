---
last_reviewed: 2026-11-04
related:
  - theory/paradigms/symbolic-ai/neuro-symbolic
tags:
  - neuro-symbolic AI
  - inductive logic programming
  - rule learning
aliases:
  - Differentiable inductive logic programming
  - ∂ILP
  - Differentiable ILP
  - 可微分歸納邏輯程式設計
  - 可微分 ILP
---

# Differentiable Inductive Logic Programming

Differentiable inductive logic programming (∂ILP) learns logic rules from examples by replacing the discrete search over rules with a differentiable forward-chaining procedure, so that the rules can be fitted with gradient descent. Part of [Neuro-symbolic AI](index.md).

## Overview

Inductive logic programming (ILP) learns a set of logical rules that explain positive examples and reject negative ones, given background facts. Classical ILP searches over discrete rules. That search is combinatorial, and it is sensitive to noise, because one wrong example can rule out a correct rule. Evans and Grefenstette (2018) relax the search. Each candidate rule is given weights over possible predicates, and the derived consequences are computed in a differentiable way. The learned rules are then read off from the weights.

## Key concepts

- **Inductive logic programming**: learning rules that explain examples from background knowledge.
- **Forward chaining**: deriving new facts by applying rules to known facts, repeatedly.
- **Soft predicate choice**: each slot in a rule body is a weighted choice over candidate predicates, with weights normalised by a softmax.
- **Template**: a fixed rule shape, with a chosen number of rules, whose unknown predicates are selected by learned weights.

## How it works

The procedure can be summarised in five steps. The paper gives the exact formulation.

1. **Templates.** The user specifies rule shapes, for example a rule with two body atoms and one head, and how many rules of each shape to learn.
2. **Soft selection.** Each body atom is a weighted combination of candidate predicates applied to the rule's variables. The weights are softmax-normalised.
3. **Differentiable forward chaining.** Truth values of derived atoms are computed from the rules and the facts with a differentiable approximation of logical OR and AND, applied for a fixed number of steps.
4. **Training.** The derived truth values are compared with labelled examples, and gradient descent adjusts the weights. A temperature parameter is gradually reduced so that the soft choices approach discrete ones.
5. **Extraction.** After training, the highest-weighted predicates in each slot give the learned discrete rules, which can be checked by a person.

## Key methods

- [Markov logic networks](markov-logic-networks.md): attach weights to given formulas and define a probability distribution over worlds. The formulas are supplied, not learned from examples.
- [Logic tensor networks](logic-tensor-networks.md): train groundings to satisfy axioms given in advance. ∂ILP instead learns the rules themselves.

## Connections

- [Knowledge graphs](../knowledge-graphs/index.md): rules learned over relations can be used to complete a graph.
- [Neuro-symbolic AI](index.md) gives the wider context of combining rules with learning.
- Garcez and Lamb (2023) discuss rule extraction from neural models, a related question of making learned behaviour explicit.

## Applications

- **Relational learning**: learning rules over relations from noisy examples, a setting the paper evaluates.
- **Interpretable models**: learned rules that a person can inspect and correct.
- **Neural perception with rules**: combining a learned perception model with explicit rules, as in the neuro-symbolic surveys.

## Open questions

- Templates are chosen by hand. Learning which templates to use is an open problem.
- The number of candidate rules grows quickly with the number of predicates and constants, which limits scale.
- Soft semantics during training can produce rules that do not hold exactly, and the step that makes them discrete can change their behaviour.

## References

### Seminal papers

- Evans, R. & Grefenstette, E. (2018). Learning explanatory rules from noisy data. *Journal of Artificial Intelligence Research* 61, 1–64. https://doi.org/10.1613/jair.5714 — Introduces ∂ILP, a differentiable method for learning rules from noisy examples.
- Manhaeve, R., Dumančić, S., Kimmig, A., Demeester, T. & De Raedt, L. (2018). DeepProbLog: neural probabilistic logic programming. arXiv:1805.10872. https://arxiv.org/abs/1805.10872 — Combines neural predicates with a probabilistic logic programming language, another way to join rules and learning.
- Dong, H., Mao, J., Lin, T., Wang, C., Li, L. & Zhou, D. (2019). Neural logic machines. arXiv:1904.11694. https://arxiv.org/abs/1904.11694 — Learns relational rules with neural modules that apply logical operations.

### Surveys and textbooks

- Garcez, A. d'A. & Lamb, L. C. (2023). Neurosymbolic AI: the 3rd wave. *Artificial Intelligence Review* 56(11), 12387–12406. https://doi.org/10.1007/s10462-023-10448-w — Survey of rule learning and rule extraction in neuro-symbolic systems.
- Besold, T. R., d'Avila Garcez, A. S. & Bader, S. (2017). *Neural-Symbolic Learning and Reasoning: A Survey and Interpretation*. arXiv:1711.03902. https://arxiv.org/abs/1711.03902 — Surveys neural-symbolic learning, including rule induction.
