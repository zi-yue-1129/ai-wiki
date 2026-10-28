---
status: draft
last_reviewed: 2026-10-28
---

# ACT-R: a modular architecture of mind (Anderson et al., 2004)

ACT-R is a cognitive architecture: a computational theory of the mind, realised as a program, that aims to explain and predict human behaviour across many kinds of cognition.

!!! note "Scope of this page"
    This page is built from the sources listed under References, which were read in full or in abstract. The 2004 paper named in the title is not summarised here, so its detailed claims, equations and results are left out. Treat the mechanism sections as a guide to the architecture rather than as a reproduction of that paper.

## Overview

A **cognitive architecture** is a fixed set of mechanisms that together describe how a mind is structured and how it processes information. The idea is that one architecture, with one set of components, should be able to account for many tasks, not just one. ACT-R is one of the best-known such architectures. Ritter and colleagues describe it as a hybrid cognitive architecture made of programmable information-processing mechanisms, which can be used to predict and explain human behaviour, including cognition and interaction with the environment.

The architecture sits in the wider [Cognitive Architectures](../index.md) section, alongside related systems such as Soar and the agent architectures discussed in [CoALA](../coala/index.md).

## Key concepts

- **Cognitive architecture**: a set of mechanisms, intended as a general theory of the mind, that can be run on a computer to produce behaviour.
- **Hybrid architecture**: the term Ritter and colleagues use for ACT-R. Their review traces the history that shaped this form and contrasts it with other architectures.
- **Working memory**: the short-term store that holds the current perceptual input, goals and intermediate results of reasoning. The CoALA paper uses the same term in its description of Soar.
- **Production rule**: a condition-action rule. It fires when its conditions match the contents of working memory, and its action changes what is in working memory or sends a command out. Rules of this kind make up a production system.
- **Standard model of the mind**: the community consensus that Laird and colleagues propose, synthesised from ACT-R, Sigma and Soar.

## Problem

Cognitive science and artificial intelligence have long needed a single computational account of the mind that covers perception, memory, learning and motor control together. Separate models of each ability are easier to build, but they do not show how the abilities fit together.

Laird, Lebiere and Rosenbloom describe the effort to reach such an account. Their proposed standard model "spans key aspects of structure and processing, memory and content, learning, and perception and motor", and it is extended from three existing cognitive architectures: ACT-R, Sigma and Soar. Their point is that the architectures agree on many things and disagree on others, and a shared reference makes that agreement and disagreement visible.

## Core idea

ACT-R is presented as a theory of cognition that is realised as a computer program. In the review by Ritter, Tehranchi and Oury, the architecture is a set of programmable information-processing mechanisms, and the review describes tools for working with it. The aim is to predict and explain behaviour in concrete tasks. The same review states that ACT-R has produced several major accomplishments in both basic and applied science, including insights about human behaviour.

The architecture's credibility therefore rests on how well its mechanisms predict behaviour. Its design is a claim about the structure of the mind, not only a tool for building intelligent systems.

## Equation or algorithm

The original paper specifies ACT-R's own processing cycle and its equations, which this page does not reproduce. What the sources read here do describe is the production-system cycle that CoALA attributes to Soar, a closely related architecture. The steps below show that general pattern, and they should be read as an illustration of how such architectures run, not as ACT-R's exact procedure.

1. Working memory holds the current perceptual input, the goals and the results of intermediate reasoning.
2. Each production rule checks its preconditions against the contents of working memory.
3. The matching rules propose candidate actions, and the candidates are evaluated and ranked.
4. The selected action is applied. It may be an external action, such as a motor command, or an internal one, such as a change to memory.

Soar's decision loop evaluates the productions that match working memory and applies the one that matches best. ACT-R uses a production system of its own, but its precise cycle, timing and memory equations are part of the original paper, outside what this page covers.

## Results

The review by Ritter and colleagues describes ACT-R's record in general terms: several major accomplishments in both basic and applied science, including insights about human behaviour. It does not give a single benchmark number, and this page gives none, because the detailed results of the 2004 paper were not read for this version.

The standard-model paper reports a different kind of result, a synthesis of agreement across ACT-R, Sigma and Soar. It identifies places where the architectures agree and where they disagree, and it notes areas where the consensus remains incomplete.

## Limitations

- **Incomplete coverage.** The review by Ritter and colleagues names several areas it expects to add, including emotions and physiology, usability, and the use of nongenerative models. These are gaps in the architecture as presented, not solved problems.
- **Disagreement across architectures.** The standard-model paper stresses that ACT-R, Sigma and Soar differ on some points, so no single architecture is accepted as the whole account.
- **Model-building choices.** A cognitive architecture predicts behaviour only once it is set up for a task. The sources read for this page do not settle how much of a model's fit comes from the architecture and how much from the choices made in setting it up.

## Key methods

- [CoALA](../coala/index.md) (Sumers et al., 2023): applies the vocabulary of cognitive architectures to language agents. It is a conceptual framework, not a model of human behaviour.
- Soar: a production-system architecture that stores productions in long-term memory and applies them against working memory. It is one of the three architectures synthesised in the standard model.
- Sigma: a third architecture named in the standard-model synthesis. It shares the goal of a common account of the mind but is not described in the sources read for this page.

## Connections

- Parent topic: [Cognitive Architectures](../index.md)
- Other method on this topic: [CoALA](../coala/index.md)
- [Memory & Learning in the Brain](../../memory-learning/index.md): the brain's memory systems, which architectures such as ACT-R try to model at a functional level.
- [Building machines that learn and think like people](../../cognitive-science/building-machines-like-people/index.md): Lake and colleagues argue that human-like learning needs causal models, intuitive theories and compositionality, which sets a demanding bar for any architecture.
- [Psychology & AI](../../psychology/index.md): the cognitive-psychology tradition that architectures like ACT-R draw on and test.
- [Global workspace](../../consciousness/global-workspace/index.md): another architectural theory of the mind, with a different focus on how information is shared across the system.
- [AI Agents](../../../theory/models/agents/index.md): systems that take actions in an environment, which CoALA classifies using architecture-style categories.

The brain connection is conceptual. The standard-model paper is written to span cognitive science and neuroscience, as its title states, so the architectures are meant to be compared with accounts from both fields.

## Applications

- **Modelling human behaviour**: explaining and predicting performance in laboratory tasks and in applied settings, as Ritter and colleagues report for ACT-R.
- **A shared reference for research**: the standard model gives researchers in AI, cognitive science, neuroscience and robotics a common set of components to compare against.
- **Agent design**: CoALA borrows the memory and decision-cycle vocabulary of cognitive architectures to organise modern language agents.

## Open questions

- **Can one architecture serve as a standard model?** Laird and colleagues propose a consensus model but state that it is not itself an architecture, and they identify disagreements to resolve.
- **Emotion and physiology.** How should these be added to a model that currently centres on cognition, as Ritter and colleagues propose?
- **Usability.** How can the architecture be made easier for researchers to build and test models with?
- **Nongenerative models.** How should models that do not generate behaviour be used within the architecture, as the review suggests?

## References

### Seminal papers

- Laird, J. E., Lebiere, C. & Rosenbloom, P. S. (2017). A Standard Model of the Mind: Toward a Common Computational Framework Across Artificial Intelligence, Cognitive Science, Neuroscience, and Robotics. *AI Magazine*. https://doi.org/10.1609/aimag.v38i4.2744 — Proposes a community consensus model of the mind synthesised from ACT-R, Sigma and Soar, and highlights where the architectures agree and disagree.
- Lake, B. M., Ullman, T. D., Tenenbaum, J. B. & Gershman, S. J. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — Argues that human-like learning needs causal models, intuitive theories of physics and psychology, and compositionality.
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P. & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv. https://arxiv.org/abs/2304.03442 — Describes a language-model agent that stores experiences, reflects on them and retrieves them to plan believable behaviour.
- Sumers, T. R., Yao, S., Narasimhan, K. & Griffiths, T. L. (2023). Cognitive Architectures for Language Agents. arXiv. https://arxiv.org/abs/2309.02427 — Organises language agents by their memory, action space and decision procedure, drawing on cognitive architectures.

### Surveys and textbooks

- Ritter, F. E., Tehranchi, F. & Oury, J. D. (2019). ACT-R: A cognitive architecture for modeling cognition. *WIREs Cognitive Science*. https://doi.org/10.1002/wcs.1488 — Reviews ACT-R's history, its theory of cognition as a computer program, its tools and its accomplishments in basic and applied science.
