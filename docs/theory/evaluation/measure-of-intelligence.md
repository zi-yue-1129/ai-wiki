---
related:
  - theory/evaluation
  - theory/evaluation/benchmarks
  - theory/paradigms/supervised/generalization-theory
tags:
  - evaluation
  - intelligence
  - generalisation
  - benchmarks
aliases:
  - On the Measure of Intelligence
  - Chollet 2019
  - ARC
  - 智能的度量
last_reviewed: 2026-11-01
---

# On the Measure of Intelligence

Chollet (2019) argues that skill on a fixed set of tasks is the wrong thing to measure if the aim is intelligence. He proposes that intelligence is the efficiency with which a system acquires new skills, and he gives a framework for measuring it that controls for the priors and the experience the system was given. The paper also introduces the Abstraction and Reasoning Corpus (ARC), a benchmark built to test that framework. The place of benchmarks in the wider evaluation chapter is on the [Evaluation](index.md) page.

## Overview

Most benchmarks report how well a system does on a set of tasks. A system that has seen many examples of those tasks can score well without being able to handle new ones. Chollet's point is that the score alone does not separate a system that generalises from one that has been given enough data or built-in knowledge to memorise the answers.

## Central claim

The paper defines intelligence as skill-acquisition efficiency over a scope of tasks. The definition is stated with respect to priors, experience and generalisation difficulty. Under this view, two systems that reach the same skill can differ in intelligence, depending on how much data and how many built-in priors each needed to get there.

## Evaluation framework

The framework names several quantities.

- **Priors:** innate or built-in knowledge given to the system by its developers. A fair test controls for them, and a system with extensive priors should not be benchmarked with a test that those priors already solve.
- **Experience:** training data. Unlimited data can buy skill on a task without giving the system the ability to generalise.
- **Scope:** the range of tasks over which the measure is taken. The paper proposes human-relevant tasks.
- **Generalisation difficulty:** a property that weights tasks in the value function.
- **Developer-aware generalisation:** the ability to handle situations that neither the system nor its developer has seen, as distinct from generalisation that ignores what the developer built in.

A comparison is made between two systems that start from similar priors and experience. The one that reaches greater skill on unknown tasks is the more intelligent.

## The ARC benchmark

ARC is built on an explicit set of priors that the author designs to be close to innate human priors. These follow core-knowledge theory: objects and elementary physics, agents and goals, elementary numbers and arithmetic, and elementary geometry and topology. The tasks are presented as input grids. The paper uses ARC to argue for fair comparisons between AI systems and humans. The number of tasks and the full task format are in parts of the paper that this summary did not read.

## Criticisms

The paper criticises several existing approaches.

- **Skill-based game benchmarks** are described as measuring skill without a measure of generalisation power.
- **Multi-task benchmarks** are described as still highly gameable.
- **Human psychometric tests** can be gamed, because developers know the kinds of tasks they contain.

The author also acknowledges that the definition is not the one true definition. It is meant to be useful for measuring progress rather than to win consensus, and its anthropocentric frame is a deliberate choice.

## Connections

- The problem of building priors into a model is the same one studied in [generalisation theory](../paradigms/supervised/generalization-theory/index.md), where the usual explanations of generalisation are contested.
- The benchmark-validity question, whether a benchmark measures the construct it names, is covered in [benchmark validity](benchmarks/index.md).
- The paper's focus on the efficiency of skill acquisition connects to work on [few-shot learning](../paradigms/meta-learning/index.md), which measures learning from few examples.

## Open questions

- Can a measure of skill-acquisition efficiency be computed for systems whose priors are not known?
- How should the scope of tasks be chosen so that it is neither too narrow nor defined only by human ability?
- Do benchmarks such as ARC keep their value once systems are trained on data that resembles them?

## References

### Seminal papers

- Chollet, F. (2019). On the Measure of Intelligence. [arXiv:1911.01547](https://arxiv.org/abs/1911.01547) — Defines intelligence as skill-acquisition efficiency and introduces the ARC benchmark.
- Legg, S. & Hutter, M. (2007). Universal Intelligence: A Definition of Machine Intelligence. [arXiv:0712.3329](https://arxiv.org/abs/0712.3329) — An earlier formal definition of machine intelligence, which Chollet's framework responds to.
- Lake, B. M. et al. (2016). Building Machines That Learn and Think Like People. [arXiv:1604.00289](https://arxiv.org/abs/1604.00289) — Argues that human-like core knowledge should be built into learning systems, the basis of the priors in ARC.
- Legg, S. & Hutter, M. (2007). A Collection of Definitions of Intelligence. [arXiv:0706.3639](https://arxiv.org/abs/0706.3639) — Surveys the informal and formal definitions of intelligence that the formal measure builds on.
- Spelke, E. S. & Kinzler, K. D. (2007). Core knowledge. Developmental Science, 10, 89–96. [DOI 10.1111/j.1467-7687.2007.00569.x](https://doi.org/10.1111/j.1467-7687.2007.00569.x) — Describes the core knowledge systems for objects, agents and numbers that the ARC priors follow.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
