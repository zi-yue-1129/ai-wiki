---
status: draft
last_reviewed: 2026-10-28
tags:
  - reasoning
  - knowledge representation
aliases:
  - ∂ILP
  - Differentiable ILP
  - Differentiable inductive logic programming
  - 可微分歸納邏輯程式設計
  - 歸納邏輯程式設計
  - Inductive logic programming
  - Learning explanatory rules from noisy data
---

# Differentiable Inductive Logic Programming (∂ILP)

∂ILP learns logic programs from examples by gradient descent, instead of the discrete search of classical inductive logic programming. Evans and Grefenstette introduced it in 2017 as a preprint and published it in 2018. It is the differentiable-logic landmark of the [neuro-symbolic AI overview](../index.md): the rules it learns stay readable, and the learning tolerates noise.

## Overview

Inductive logic programming (ILP) learns logical rules from examples and background knowledge. Given examples of grandparent pairs and facts about parents, an ILP system can recover the rule that a grandparent is a parent of a parent. Its rules are readable and it needs little data. Its weak points are noise, since one mislabelled example can derail a discrete search, and raw input such as pixels, which ILP cannot use directly.

Evans and Grefenstette's framework addresses both weaknesses. It solves the tasks ILP suits and tolerates noise in the training data. Because it is trained by backpropagation against a likelihood objective, it can also be connected to neural networks over ambiguous data.[^1]

## Key concepts

- **Background knowledge**: facts and predicates supplied in advance, such as the relations that describe a domain.
- **Clause**: a rule with a head and a body, such as *grandparent(X, Z) if parent(X, Y) and parent(Y, Z)*.
- **Soft forward chaining**: deriving facts step by step, where each derived atom gets a truth value between 0 and 1 computed from its body.

## How it works

The method keeps the skeleton of ILP and makes each step differentiable. The steps below are a general scheme for this family of systems; the exact operators and training schedule are in the paper.

1. **Enumerate candidate clauses** over the background predicates.
2. **Weight the clauses.** Give each candidate a learnable weight, so the program is a weighted mixture of clauses rather than a single choice.
3. **Chain softly.** Compute each derived atom's truth value with smooth connectives. A generic form is

$$
v(\text{body}_c) = \prod_{i} v(b_i), \qquad v(p) = 1 - \prod_{c:\,\text{head}(c)=p} \bigl(1 - w_c\, v(\text{body}_c)\bigr)
$$

where $w_c$ is the weight of clause $c$. Repeating the step derives deeper consequences.

4. **Score the program** against the observed facts under a likelihood objective. A mislabelled example then shifts the score slightly instead of eliminating a hypothesis.
5. **Sharpen and read off.** Gradient descent pushes most weights toward zero or one, and the highest-weighted clauses are reported as the learned program.

## Results

The abstract reports that the framework solves the tasks traditional ILP systems are suited for, shows robustness to noise and error in the training data that ILP cannot match, and addresses domains such as ambiguous perception where ILP cannot be applied.[^1] The abstract gives no numerical results, so this page quotes none. The paper's experiments should be read before any figure is cited.

## Limitations

- **Designer-chosen templates.** The candidate clauses must be fixed in advance, and their number grows quickly with the number of predicates and body atoms.
- **Local optima.** Gradient descent on a non-convex relaxation can settle on a program that fits the data approximately but is not the intended rule.
- **Dependence on background knowledge.** The learned rules can only use the predicates supplied; the method cannot invent a missing concept.
- **Approximate truth.** The sharpened rules may behave differently from the soft program that produced them.

## Open questions

- Can the candidate clauses themselves be learned, so that the designer does not fix the template?
- How can one confirm that a read-off rule behaves like the soft program it came from?
- Do differentiable logic learners scale to large knowledge bases?

## Connections

∂ILP is the learning counterpart of the rule-based tradition in [knowledge representation](../../knowledge-graphs/index.md), since it learns definite clauses of the kind a knowledge base stores. Other differentiable logics include Logic Tensor Networks,[^2] DeepProbLog,[^3] Logical Neural Networks[^4] and Neural Logic Machines,[^5] which generalise rules learned from small tasks to larger ones. On the proving side, [neural theorem provers](../neural-theorem-prover/index.md) make a similar move. The argument that learning should yield explanatory, causal rules is developed in [Building Machines That Learn and Think Like People](../../../../../brain-mind/cognitive-science/building-machines-like-people/index.md).

[^1]: Evans and Grefenstette (2018), listed above. The summary of findings is taken from the abstract.
[^2]: Serafini and d'Avila Garcez (2016), listed above.
[^3]: Manhaeve et al. (2018), listed above.
[^4]: Riegel et al. (2020), listed above.
[^5]: Dong et al. (2019), listed above. The generalisation example is from the abstract.

## References

### Seminal papers

- Evans, R. & Grefenstette, E. (2018). *Learning Explanatory Rules from Noisy Data*. Journal of Artificial Intelligence Research. https://doi.org/10.1613/jair.5714 — Introduces differentiable inductive logic programming, which learns logic rules by gradient descent and tolerates noisy training data.
- Serafini, L. & d'Avila Garcez, A. (2016). *Logic Tensor Networks: Deep Learning and Logical Reasoning from Data and Knowledge*. arXiv. https://arxiv.org/abs/1606.04422 — Defines Real Logic, with truth values in the unit interval, and implements it in tensor networks.
- Manhaeve, R. et al. (2018). *DeepProbLog: Neural Probabilistic Logic Programming*. arXiv. https://arxiv.org/abs/1805.10872 — Adds neural predicates to a probabilistic logic programming language and trains them from examples.
- Riegel, R. et al. (2020). *Logical Neural Networks*. arXiv. https://arxiv.org/abs/2006.13155 — Proposes neurons that carry the meaning of a weighted real-valued logic formula, trained with a contradiction-penalising loss.
- Dong, H. et al. (2019). *Neural Logic Machines*. arXiv. https://arxiv.org/abs/1904.11694 — Learns lifted logical rules from small tasks and generalises them to larger instances, such as longer arrays.

### Surveys and textbooks

- Besold, T. R. et al. (2017). *Neural-Symbolic Learning and Reasoning: A Survey and Interpretation*. arXiv. https://arxiv.org/abs/1711.03902 — Surveys neural-symbolic learning and reasoning, relating computational-logic and connectionist models of cognition.
