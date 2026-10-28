# Theory

The core theory behind every AI technique.

| Page | Core question |
|---|---|
| [Mathematics](math/index.md) | What roles do linear algebra, calculus, probability, information theory and optimisation play? |
| [Machine Learning](machine-learning/index.md) | How do we learn from data, and how do we know it worked? |
| [Deep Learning](deep-learning/index.md) | Why are multi-layer neural networks so effective, and how are they trained? |
| [Learning Paradigms](paradigms/index.md) | Supervised, unsupervised, semi-/weakly supervised, self-supervised, reinforcement, imitation, transfer, meta, continual, active, online, federated learning — what signal, what setting? |
| [Reinforcement Learning](paradigms/reinforcement-learning/index.md) | How do agents learn behaviour from trial, error and reward — and what does dopamine have to do with it? |
| [Probabilistic & Bayesian Methods](probabilistic/index.md) | How do we represent and reason with uncertainty? Is the brain a Bayesian machine? |
| [Symbolic AI, Search & Planning](symbolic-ai/index.md) | How do logic, knowledge representation, search and planning work, and do they still matter in the LLM era? |
| [Evolutionary & Swarm Intelligence](evolutionary/index.md) | How can evolution and collective behaviour be used for optimisation? |

## Theory or models?

Theory explains how learning and reasoning work in general, independent of any particular network. [Models](models/index.md) is a subsection that covers the concrete model families and the systems built from them. If a page would still hold after its network was swapped for another, it belongs in Theory. The [style guide](../reference/style-guide/index.md) has the full rule.

## The three basic learning signals

| Signal | Paradigm | Typical task | Rough brain analogue |
|---|---|---|---|
| Correct answer for each input | Supervised | Classification, regression | Cerebellar error-correction learning |
| Structure of the data itself | Unsupervised / self-supervised | Clustering, representation learning, LLM pre-training | Cortical predictive coding, statistical learning |
| Sparse reward | Reinforcement | Games, control, alignment | Basal ganglia and dopamine |

This "cerebellum–supervised, cortex–unsupervised, basal ganglia–reinforcement" division of labour was proposed by Doya (1999) and remains a classic idea in [NeuroAI](../brain-mind/neuroai/index.md). The full taxonomy, including imitation, transfer, meta-, continual, active, online and federated learning, is in [Learning Paradigms](paradigms/index.md).
