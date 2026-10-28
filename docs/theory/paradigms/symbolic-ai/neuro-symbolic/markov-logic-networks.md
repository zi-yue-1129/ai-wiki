---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai/neuro-symbolic
  - theory/paradigms/probabilistic/graphical-models
tags:
  - neuro-symbolic AI
  - probabilistic logic
  - graphical models
aliases:
  - 馬可夫邏輯網路
  - MLN
  - Markov logic
---

# Markov Logic Networks

A Markov logic network (MLN) is a set of first-order logical formulas, each with a real-valued weight. Together with a finite set of objects, it defines a Markov network over all possible worlds. A world is more probable the more satisfied formulas it has, weighted by their weights. Part of [Neuro-symbolic AI](index.md).

## Overview

Classical logic treats a formula as true or false, so one counter-example makes a rule false. Real data contain exceptions and uncertainty. An MLN keeps logical rules but allows them to be violated with a cost that depends on the weight. A rule with a large weight behaves almost like a hard constraint, and a rule with a small weight is a soft preference. Richardson and Domingos (2006) introduced this combination of first-order logic and Markov networks.

## Key concepts

- **Formula and weight**: a first-order formula \(F_i\) with weight \(w_i\). A positive weight favours worlds in which the formula holds.
- **Grounding**: substituting every combination of objects into a formula to get a propositional formula. The MLN defines a Markov network over the grounded atoms.
- **Possible world**: an assignment of truth values to all grounded atoms.
- **Hard and soft constraints**: a formula with infinite weight must hold in every world with non-zero probability. Finite weights make it a soft constraint.

## How it works

For a world \(x\), let \(n_i(x)\) be the number of true groundings of formula \(i\). The MLN defines

\[
P(X=x)=\frac{1}{Z}\exp\!\Big(\sum_i w_i\, n_i(x)\Big),
\]

where \(Z\) is the normalising partition function. Learning the weights from data maximises the likelihood, and the gradient for \(w_i\) is the difference between the observed count \(n_i\) and its expectation under the model. Inference, such as computing the probability of a query atom, requires approximate methods, typically Markov chain Monte Carlo or belief propagation on the grounded network. The grounded network can be very large, which is a central practical issue.

## Variants

- **Discriminative and generative weight learning** fit the weights to predict some atoms given others, or to model the full joint distribution.
- **Symmetry-exploiting inference** works on groups of objects that behave alike, which avoids grounding every formula and reduces the cost for large domains.
- **Learning the formulas themselves** searches over rules as well as weights, and it is much more expensive than weight learning alone.

## Results and limits

- MLNs combine logical knowledge with uncertainty in one model, so an expert's rules can be kept and tuned from data.
- The grounded network grows with the number of objects and the arity of formulas, so inference and learning become expensive for large domains.
- Approximate inference can be inaccurate, and the probability values depend on the chosen weights in ways that are not always easy to interpret.
- Learning formulas from data, rather than writing them by hand, is hard, and it is the bottleneck in many applications.

## Applications

- **Entity resolution**: deciding whether records refer to the same entity, using rules about attributes and relations (Richardson & Domingos, 2006).
- **Relational classification**: predicting labels of objects that depend on the labels of related objects.
- **Information extraction**: combining rules about text with learned weights for noisy signals.

## Open questions

- Scaling inference to very large domains is the main research question, and lifted methods help only when the model has symmetry.
- Combining MLNs with deep neural features, so that the weights come from a network, links them to the neuro-symbolic programme described in Garcez and Lamb (2023).
- Learning structure and weights from noisy data, with guarantees on the quality of the learned rules, is still an open problem.

## References

### Seminal papers

- Richardson, M. & Domingos, P. (2006). Markov logic networks. *Machine Learning* 62(1–2), 107–136. https://doi.org/10.1007/s10994-006-5833-1 — Defines MLNs, their semantics as Markov networks and their use in relational learning.
- Evans, R. & Grefenstette, E. (2018). Learning explanatory rules from noisy data. *Journal of Artificial Intelligence Research* 61, 1–64. https://doi.org/10.1613/jair.5714 — Learns logical rules from noisy data, a related approach to weighted formulas.
- Serafini, L. & Garcez, A. d'A. (2016). Logic tensor networks: deep learning and logical reasoning from data and knowledge. arXiv:1606.04422. https://arxiv.org/abs/1606.04422 — Shows how a real-valued logic can be combined with neural networks, a related way of mixing formulas and learning.

### Surveys and textbooks

- Garcez, A. d'A. & Lamb, L. C. (2023). Neurosymbolic AI: the 3rd wave. *Artificial Intelligence Review* 56(11), 12387–12406. https://doi.org/10.1007/s10462-023-10448-w — Places Markov logic networks within neuro-symbolic research.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; background on Markov networks and approximate inference used by MLNs.
