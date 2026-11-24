---
status: draft
last_reviewed: 2026-11-19
---

# ACT-R: a modular architecture of mind (Anderson et al., 2004)

ACT-R is a cognitive architecture: a computational theory of the mind, realised as a program, that aims to explain and predict human behaviour across many kinds of cognition.

!!! note "Scope of this page"
    This version is built from three kinds of source: the abstract of the 2004 paper named in the title, the review by Ritter and colleagues, and the standard-model paper by Laird and colleagues. This version reads the 2004 paper from a copy hosted at IIT Delhi, for its equations and the list of its empirical examples. The official ACT-R documentation was not opened, and the equations are not yet checked against the printed journal version. The page stays a draft until that check and the detailed empirical results are added.

## Overview

A **cognitive architecture** is a fixed set of mechanisms that together describe how a mind is structured and how it processes information. The idea is that one architecture, with one set of components, should be able to account for many tasks, not just one. ACT-R is one of the best-known such architectures.

The name stands for *adaptive control of thought-rational*. The 2004 abstract traces the architecture to Anderson and Lebiere (1998), and says it has since "evolved into a theory that consists of multiple modules but also explains how these modules are integrated to produce coherent cognition". Ritter and colleagues describe it as a hybrid cognitive architecture made of programmable information-processing mechanisms, which can be used to predict and explain human behaviour, including cognition and interaction with the environment.

The architecture sits in the wider [Cognitive Architectures](../index.md) section, alongside related systems such as Soar and the agent architectures discussed in [CoALA](../coala/index.md).

## Key concepts

- **Module**: a specialised subsystem. The 2004 paper gives the perceptual-motor modules, the goal module and the declarative memory module as examples. It says these modules are associated with distinct cortical regions.
- **Buffer**: the place where a module holds a chunk so that other parts of the system can detect it. The 2004 paper says modules "place chunks in buffers where they can be detected by a production system".
- **Production rule**: a condition-action rule that responds to the pattern of information across the buffers. At any point in time, a single production rule is selected to respond to the current pattern.
- **Subsymbolic process**: a quantity that guides which rule is selected to fire and that shapes the internal operations of some modules. Much of learning in ACT-R involves tuning these processes.
- **Hybrid architecture**: the term Ritter and colleagues use for ACT-R. Their review traces the history that shaped this form and contrasts it with other architectures.
- **Standard model of the mind**: the community consensus that Laird and colleagues propose, synthesised from ACT-R, Sigma and Soar.

## Problem

Cognitive science and artificial intelligence have long needed a single computational account of the mind that covers perception, memory, learning and motor control together. Separate models of each ability are easier to build, but they do not show how the abilities fit together.

Laird, Lebiere and Rosenbloom describe the effort to reach such an account. Their proposed standard model "spans key aspects of structure and processing, memory and content, learning, and perception and motor", and it is extended from three existing cognitive architectures: ACT-R, Sigma and Soar. Their point is that the architectures agree on many things and disagree on others, and a shared reference makes that agreement and disagreement visible.

ACT-R addresses a narrower version of this problem. It asks how a set of specialised modules can be wired together so that the whole system produces coherent behaviour, and how the parts learn from experience.

## Core idea

The 2004 paper treats ACT-R as one integrated system. Specialised modules hold information in buffers. A production system watches the buffers and picks one rule to respond to the pattern it sees. Subsymbolic quantities control which rule is chosen and how some modules operate, and learning changes those quantities over time.

Ritter, Tehranchi and Oury describe the same architecture as a theory of cognition realised as a computer program. In their review it is a set of programmable information-processing mechanisms, together with tools for building models. The aim is to predict and explain behaviour in concrete tasks. The review states that ACT-R has produced several major accomplishments in both basic and applied science, including insights about human behaviour.

The architecture's credibility therefore rests on how well its mechanisms predict behaviour. Its design is a claim about the structure of the mind, not only a tool for building intelligent systems.

## Equation or algorithm

The 2004 paper states the subsymbolic layer in named equations. The paper does not number them, so they are cited here by name, with the paper's own symbols.

**Base-level learning equation.** The base-level activation of a chunk grows with how often it was practised and falls with how long ago. With \(t_j\) the time since the \(j\)th practice and \(d\) a decay parameter,

\[
B_i = \ln \sum_{j=1}^{n} t_j^{-d}
\]

The paper uses \(d = 0.5\) as its default value.

**Activation equation.** Total activation adds a contextual term to base-level activation, \(A_i = B_i + \sum_j W_j S_{ji}\), where \(W_j\) is the attention weight given to each context element and \(S_{ji}\) is the strength of association from that element to the chunk.

**Retrieval.** A chunk can be retrieved only if its activation exceeds a threshold \(\tau\), and activation carries noise. Retrieval time falls off exponentially with activation, \(T_i = F e^{-A_i}\), where \(F\) is a latency factor.

**Production choice.** Each production has a utility \(U_i\). The probability that production \(i\) is chosen among the applicable productions is

\[
P_i = \frac{e^{U_i/t}}{\sum_j e^{U_j/t}}
\]

where \(t\) controls the noise in the utilities, with a typical value of about 0.5. The paper defines utility from the estimated probability of achieving the goal if the production is chosen, \(P\), the goal value \(G\) and the estimated cost \(C\), as \(U = PG - C\).

**Caveat on these equations.** They were read from a copy of the paper hosted at IIT Delhi, in which text extraction dropped some operators. The reconstructed form of the utility equation (including its minus sign) and the value of the spreading-activation constant are not yet confirmed against the printed page. The paper also reports different values for that constant in different fits, so the constant should be read with its context. Before this page is complete, these equations should be checked against the published journal version.

The processing cycle named in the abstract is as follows. Each module places a chunk in its buffer. The production system reads the pattern across the buffers. A single production is selected, with subsymbolic values helping to decide which one. The selected production responds and changes the buffers or modules, and the cycle repeats. The paper gives a cycle time of about 50 ms.

## Results

The 2004 abstract describes "a number of simple and complex empirical examples" that illustrate how the modules function singly and in concert. These examples are illustrations of the architecture at work. The abstract does not report a single benchmark number, and this page gives none.

The review by Ritter and colleagues describes ACT-R's record in general terms: several major accomplishments in both basic and applied science, including insights about human behaviour. The standard-model paper reports a different kind of result, a synthesis of agreement across ACT-R, Sigma and Soar. It identifies places where the architectures agree and where they disagree, and it notes areas where the consensus remains incomplete.

The paper's body names the empirical examples it uses. These include the fan effect in sentence recognition, a dual-task study pairing a vocal tone task with a manual position task, the Tower of Hanoi and Tower of London, two-button probability learning, paired-associate recall, and a naval air-defence identification task. Each is presented as an illustration of how the modules work together, not as a single benchmark score.

## Limitations

- **Incomplete coverage.** The review by Ritter and colleagues names several areas it expects to add, including emotions and physiology, usability, and the use of nongenerative models. These are gaps in the architecture as presented, not solved problems.
- **Illustrative evidence.** The 2004 abstract presents its empirical examples as illustrations of how the modules work. It does not present them as a systematic test across tasks.
- **Disagreement across architectures.** The standard-model paper stresses that ACT-R, Sigma and Soar differ on some points, so no single architecture is accepted as the whole account.
- **Model-building choices.** A cognitive architecture predicts behaviour only once it is set up for a task. The sources read for this page do not settle how much of a model's fit comes from the architecture and how much from the choices made in setting it up.

## Key methods

- [CoALA](../coala/index.md) (Sumers et al., 2023): applies the vocabulary of cognitive architectures to language agents. It is a conceptual framework, not a model of human behaviour.
- Soar: a production-system architecture. It is one of the three architectures synthesised in the standard model.
- Sigma: a third architecture named in the standard-model synthesis. It shares the goal of a common account of the mind, but its details are not described in the sources read for this page.

## Connections

- Parent topic: [Cognitive Architectures](../index.md)
- Other method on this topic: [CoALA](../coala/index.md)
- [Memory & Learning in the Brain](../../memory-learning/index.md): the brain's memory systems, which architectures such as ACT-R try to model at a functional level. The 2004 abstract ties ACT-R's modules to distinct cortical regions.
- [Building machines that learn and think like people](../../cognitive-science/building-machines-like-people/index.md): Lake and colleagues argue that human-like learning needs causal models, intuitive theories and compositionality, which sets a demanding bar for any architecture.
- [Psychology & AI](../../psychology/index.md): the cognitive-psychology tradition that architectures like ACT-R draw on and test.
- [Global workspace](../../consciousness/global-workspace/index.md): another architectural theory of the mind, with a different focus on how information is shared across the system.
- [AI Agents](../../../theory/models/agents/index.md): systems that take actions in an environment, which CoALA classifies using architecture-style categories.

The brain connection is conceptual at this stage. The 2004 abstract links the modules to cortical regions, and the standard-model paper is written to span cognitive science and neuroscience, so the architectures are meant to be compared with accounts from both fields.

## Applications

- **Modelling human behaviour**: explaining and predicting human performance in basic and applied research, as Ritter and colleagues report for ACT-R.
- **A shared reference for research**: the standard model gives researchers in AI, cognitive science, neuroscience and robotics a common set of components to compare against.
- **Agent design**: CoALA borrows the memory and decision-cycle vocabulary of cognitive architectures to organise modern language agents.

## Open questions

- **Can one architecture serve as a standard model?** Laird and colleagues propose a consensus model but state that it is not itself an architecture, and they identify disagreements to resolve.
- **Emotion and physiology.** How should these be added to a model that currently centres on cognition, as Ritter and colleagues propose?
- **Usability.** How can the architecture be made easier for researchers to build and test models with?
- **Nongenerative models.** How should models that do not generate behaviour be used within the architecture, as the review suggests?
- **Which subsymbolic settings matter most?** The abstract says learning tunes the subsymbolic processes. Which of those settings drive fit to human data across tasks is a question for the full paper, and this page does not answer it.

## References

### Seminal papers

- Anderson, J. R., Bothell, D., Byrne, M. D., Douglass, S., Lebiere, C. & Qin, Y. (2004). An Integrated Theory of the Mind. *Psychological Review*, 111(4), 1036–1060. https://doi.org/10.1037/0033-295X.111.4.1036 — The paper named in the title. It presents ACT-R's modules, buffers and production system, and how subsymbolic learning tunes them. Read from its abstract for this version.
- Laird, J. E., Lebiere, C. & Rosenbloom, P. S. (2017). A Standard Model of the Mind: Toward a Common Computational Framework Across Artificial Intelligence, Cognitive Science, Neuroscience, and Robotics. *AI Magazine*, 38(4), 13–26. https://doi.org/10.1609/aimag.v38i4.2744 — Proposes a community consensus model of the mind synthesised from ACT-R, Sigma and Soar, and highlights where the architectures agree and disagree.
- Lake, B. M., Ullman, T. D., Tenenbaum, J. B. & Gershman, S. J. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*, 40, e253. https://doi.org/10.1017/S0140525X16001837 — Argues that human-like learning needs causal models, intuitive theories of physics and psychology, and compositionality.
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P. & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST '23*, 1–22. ACM. https://doi.org/10.1145/3586183.3606763 — Describes a language-model agent that stores experiences, reflects on them and retrieves them to plan believable behaviour.
- Sumers, T. R., Yao, S., Narasimhan, K. & Griffiths, T. L. (2023). Cognitive Architectures for Language Agents. arXiv. https://arxiv.org/abs/2309.02427 — Organises language agents by their memory, action space and decision procedure, drawing on cognitive architectures.

### Surveys and textbooks

- Ritter, F. E., Tehranchi, F. & Oury, J. D. (2019). ACT-R: A cognitive architecture for modeling cognition. *WIREs Cognitive Science*, 10(3), e1488. https://doi.org/10.1002/wcs.1488 — Reviews ACT-R's history, its theory of cognition as a computer program, its tools and its accomplishments in basic and applied science.
