---
last_reviewed: 2026-11-04
related:
  - theory/paradigms/symbolic-ai/neuro-symbolic
tags:
  - neuro-symbolic AI
  - real-valued logic
  - fuzzy logic
aliases:
  - Logic tensor networks
  - LTN
  - 邏輯張量網路
---

# Logic Tensor Networks

Logic tensor networks (LTNs) are a neuro-symbolic framework in which first-order formulas receive real truth degrees in [0, 1], so that a knowledge base can be trained together with neural networks. Part of [Neuro-symbolic AI](index.md).

## Overview

Logic states rules precisely, and neural networks learn patterns from data. LTN asks whether a learner can be trained to satisfy logical axioms as well as to fit labelled examples. Serafini and d'Avila Garcez (2016) introduced the approach, with a first-order language whose symbols are grounded in vectors and neural networks. Badreddine et al. (2022) give the full framework and its semantics.

## Key concepts

- **Grounding**: each constant is mapped to a vector, and each predicate to a neural network that returns a truth degree in [0, 1] for its arguments.
- **Fuzzy connectives**: conjunction, disjunction, negation and implication are computed with fuzzy operators. The choice of operators shapes what the model learns.
- **Quantifiers**: universal and existential quantifiers are approximated by aggregating truth degrees over a finite set of groundings, for example with a generalised mean.
- **Satisfaction**: the degree to which a formula holds under the current groundings. Training tries to maximise the satisfaction of the knowledge base.

## How it works

Training combines two terms. A data loss is the usual supervised loss on labelled groundings. A satisfaction loss penalises axioms that hold to a low degree. Minimising the sum adjusts both the predicate networks and the vector groundings.

Suppose the knowledge base contains two predicates, Smokes(x) and Friends(x, y), and the axiom "for all x and y, if x and y are friends and x smokes, then y smokes". Each object is a vector, the axiom is evaluated on every pair of objects, and the truth degrees are aggregated over all pairs. Gradients flow back into the predicate networks, so the model is pushed toward values that respect the axiom. This example is schematic; the exact operators and aggregation used are described in the papers.

## Key methods

- [Markov logic networks](markov-logic-networks.md): weighted formulas that define a probability distribution over possible worlds. MLNs keep a probabilistic semantics, while LTNs use real truth degrees.
- [Differentiable inductive logic programming](differentiable-ilp.md): learns rules from examples, rather than satisfying axioms given in advance.

## Connections

- [Knowledge graphs](../knowledge-graphs/index.md) supply the relations and axioms that LTNs can be trained on.
- [Neuro-symbolic AI](index.md) places LTNs among the approaches that use logic as a training constraint.
- Lake et al. (2017) argue that learning systems need structured knowledge of this kind, which motivates the axiom-based approach.

## Applications

- **Learning with background knowledge**: training classifiers when labels are scarce but axioms about the classes are known.
- **Relational data**: combining learned predicates with axioms about relations, as in knowledge completion.
- **Checking models**: finding which axioms a trained model violates, which gives an interpretable test of its behaviour.

## Open questions

- The choice of fuzzy semantics and quantifier aggregation changes the results, and the theory of which choices are sound is incomplete.
- Grounding all pairs of objects grows quadratically with the number of objects, so scaling to large domains is hard.
- Whether satisfaction degrees faithfully reflect logical entailment, rather than being a useful approximation, is still debated.

## References

### Seminal papers

- Serafini, L. & d'Avila Garcez, A. (2016). Logic tensor networks: deep learning and logical reasoning from data and knowledge. arXiv:1606.04422. https://arxiv.org/abs/1606.04422 — Introduces Real Logic and trains neural groundings to satisfy first-order axioms together with data.
- Badreddine, S., d'Avila Garcez, A., Serafini, L. & Spranger, M. (2022). Logic tensor networks. *Artificial Intelligence* 303, 103649. https://doi.org/10.1016/j.artint.2021.103649 — The full framework, its semantics and its training method.
- Lake, B. M., Ullman, T. D., Tenenbaum, J. B. & Gershman, S. J. (2017). *Building machines that learn and think like people*. *Behavioral and Brain Sciences* 40, e253. https://doi.org/10.1017/S0140525X16001837 — Argues that human-like learning needs structured knowledge such as causal and compositional models.

### Surveys and textbooks

- Garcez, A. d'A. & Lamb, L. C. (2023). Neurosymbolic AI: the 3rd wave. *Artificial Intelligence Review* 56(11), 12387–12406. https://doi.org/10.1007/s10462-023-10448-w — Survey of the neuro-symbolic field, including real-valued logics.
- Besold, T. R., d'Avila Garcez, A. S. & Bader, S. (2017). *Neural-Symbolic Learning and Reasoning: A Survey and Interpretation*. arXiv:1711.03902. https://arxiv.org/abs/1711.03902 — Surveys how neural and symbolic methods are combined for learning and reasoning.
