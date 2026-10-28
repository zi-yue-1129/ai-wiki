---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- memory
- sleep
- reinforcement learning
aliases:
  - 睡眠、重播與記憶鞏固
  - Sleep and Memory
  - Memory Consolidation
  - Hippocampal Replay
  - 記憶鞏固
  - 海馬迴重播
  - SWR
---

# Sleep, Replay and Memory Consolidation

New memories are not fixed the moment an experience ends. During rest and sleep the brain replays recent activity, and this replay is thought to help turn fragile memories into stable ones. The same principle, learning from replayed experience, is a standard tool in artificial intelligence, which makes this topic one of the clearest bridges between neuroscience and deep reinforcement learning.

## Overview

Learning a route, a task or a list of items changes the brain within minutes, but the change is not finished at that point. Recordings in rodents show that the neurons active during an experience fire again later, in a compressed form, while the animal rests or sleeps. These reactivations are brief, they are locked to particular network rhythms, and they can run forwards or backwards in time. Together they suggest that the hippocampus replays recent experience, and that replay supports the gradual transfer of memories to the neocortex.
## Core ideas

**Hippocampal replay.** Place cells, hippocampal neurons that fire at particular locations, in the rat hippocampus fire in a sequence that traces the animal's path through a space. When the animal rests after running, the same sequence returns, sometimes in reverse order. Replay during sleep was reported first, and awake replay followed. The [method page](hippocampal-replay/index.md) covers the evidence.

**Sharp-wave ripples.** Replay is carried by a specific network event. In the CA1 region, a large, slow deflection of the local field potential, the sharp wave, is accompanied by a fast oscillation near 200 Hz, the ripple. These events occur during immobility, eating and drinking, and slow-wave sleep. Suppressing them impairs spatial memory in rodents, which ties the event to memory function rather than only to its timing. The [method page](sharp-wave-ripples/index.md) gives the details.

**Systems consolidation.** Early in learning, many memories depend on the hippocampus. With time, the neocortex becomes able to support recall without it. Repeated reactivation is one proposed route for this shift. Frankland and Bontempi (2005) review how recent and remote memories are organised across these structures. The reasons this arrangement is useful are set out on [Complementary Learning Systems](../memory-learning/complementary-learning-systems/index.md), which is not repeated here.

**Sleep stages and learning.** Sleep is not one state. Slow-wave sleep, the deepest non-REM stage, is the stage most consistently linked to the consolidation of declarative memories, such as facts and events, in reviews by Diekelmann and Born (2010) and Rasch and Born (2013). The role of REM sleep is less settled. Slow oscillations, sleep spindles and ripples are thought to coordinate the dialogue between hippocampus and cortex during sleep.

**Experience replay as the AI analogue.** Deep reinforcement learning adopted replay directly. Lin (1992) reused stored experiences to speed up learning, and Mnih et al. (2015) kept a memory of recent frames in the deep Q-network and sampled it at random for updates. Replay breaks the correlation between consecutive steps and lets the learner reuse rare experience. The brain and the algorithm share a principle, but the match is suggestive rather than proven. Mattar and Daw (2018) offer a normative account in which replay is ranked by how much it would change future choices, which gives a testable link between the two. The [method page](experience-replay/index.md) explains the algorithm, and the [theory page on experience replay](../../theory/paradigms/reinforcement-learning/experience-replay/index.md) covers its variants.

## Key methods

Two method pages describe the biology, and one describes the algorithm. Each is compared briefly here.

- [Hippocampal replay (Foster & Wilson, 2006)](hippocampal-replay/index.md): it recovers the replayed sequences themselves, in awake and sleeping animals, and shows that they can run in reverse.
- [Sharp-wave ripples (Buzsáki et al., 1992)](sharp-wave-ripples/index.md): it covers the network event that carries replay, and the experiments that switch it off to test whether it matters for memory.
- [Experience replay (Lin, 1992; Mnih et al., 2015)](experience-replay/index.md): it is an engineering method, a buffer of stored transitions reused for learning, and the place where the brain analogy is tested with code.

## Connections

The consolidation account depends on the fast and slow learning systems described in [Complementary Learning Systems](../memory-learning/complementary-learning-systems/index.md), and the wider picture of memory systems is on [Memory & Learning in the Brain](../memory-learning/index.md).

Replay is also linked to planning. Mattar and Daw's model proposes that replay helps choose actions by updating values before they are needed, which relates to the model-based control discussed on [Model-Based vs Model-Free Control](../decision-reward/model-based-vs-model-free/index.md). Reverse replay, which links an outcome back to the states that led to it, resembles the value propagation of temporal-difference learning, the signal described on [Dopamine Reward Prediction Error](../neuroscience/dopamine-reward-prediction-error/index.md).

On the AI side, replay is part of the standard toolkit of [reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md), and rehearsal of old data is a standard defence against forgetting in [continual learning](../../theory/paradigms/continual/replay-and-memory/index.md).

## Applications

- **Reinforcement learning.** Replay buffers are used by value-based agents such as the deep Q-network and by many off-policy methods, where they improve data efficiency.
- **Continual learning.** Interleaving old and new data during training, inspired by the complementary learning systems account, is a common baseline against catastrophic forgetting.
- **Neuroscience methods.** Closed-loop systems that detect ripples and switch them off in real time are used to test whether replay is causal. These are research tools. They are not established treatments for any condition.

## Open questions

- **Is replay causal or only a readout?** Disrupting ripples impairs memory, but it is still unclear which content and timing are needed for consolidation.
- **Which memories are replayed?** Mattar and Daw's utility account predicts a selection rule. Whether brains follow it across many situations is open.
- **Does sleep replay serve the same purpose as waking replay?** The two may support different functions, such as consolidation and planning.
- **Which memories benefit from sleep?** Evidence for declarative memory is stronger than for other memory types, and the boundaries are still debated.
- **What transfers to machines?** Which replay rules improve large learning systems, and which are only analogies, is an open question.

## References

### Seminal papers

- Wilson, M. A. & McNaughton, B. L. (1994). Reactivation of hippocampal ensemble memories during sleep. *Science* 265, 676–679. https://doi.org/10.1126/science.8036517 — Reports that patterns of hippocampal place-cell activity from waking experience reactivate during sleep.
- Skaggs, W. E. & McNaughton, B. L. (1996). Replay of neuronal firing sequences in rat hippocampus during sleep following spatial experience. *Science* 271, 1870–1873. https://doi.org/10.1126/science.271.5257.1870 — Reports replay of place-cell firing sequences during sleep after spatial experience.
- Foster, D. J. & Wilson, M. A. (2006). Reverse replay of behavioural sequences in hippocampal place cells during the awake state. *Nature* 440, 680–683. https://doi.org/10.1038/nature04587 — Shows that place-cell sequences replay in reverse order during waking rest after running, and suggests a link to reinforcement-learning evaluation.
- Buzsáki, G. et al. (1992). High-frequency network oscillation in the hippocampus. *Science* 256, 1025–1027. https://doi.org/10.1126/science.1589772 — Describes the roughly 200 Hz CA1 oscillations during immobility, consummatory behaviour and slow-wave sleep, the ripple events that carry replay.
- Mattar, M. G. & Daw, N. D. (2018). Prioritized memory access explains planning and hippocampal replay. *Nature Neuroscience* 21, 1609–1617. https://doi.org/10.1038/s41593-018-0232-z — Proposes that memories are replayed in order of utility, which explains both forward planning and reverse replay.
- Lin, L.-J. (1992). Self-improving reactive agents based on reinforcement learning, planning and teaching. *Machine Learning* 8, 293–321. https://doi.org/10.1007/BF00992699 — Introduces experience replay for reinforcement learning agents, which reuse stored experience to speed up learning.
- Mnih, V. et al. (2015). Human-level control through deep reinforcement learning. *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The deep Q-network, which samples uniformly from a replay memory of recent experience.

### Surveys and textbooks

- Buzsáki, G. (2015). Hippocampal sharp wave-ripple: A cognitive biomarker for episodic memory and planning. *Hippocampus* 25, 1073–1188. https://doi.org/10.1002/hipo.22488 — Long review of sharp-wave ripples, their circuit origin, and their role in replay, memory consolidation and planning.
- Wittkuhn, L. et al. (2021). Replay in minds and machines. *Neuroscience & Biobehavioral Reviews* 129, 367–388. https://doi.org/10.1016/j.neubiorev.2021.08.002 — Reviews the computational functions of replay in neuroscience and machine learning, and how the two fields relate.
- Frankland, P. W. & Bontempi, B. (2005). The organization of recent and remote memories. *Nature Reviews Neuroscience* 6, 119–130. https://doi.org/10.1038/nrn1607 — Review of how recent and remote memories are organised across hippocampus and cortex over time.
- Diekelmann, S. & Born, J. (2010). The memory function of sleep. *Nature Reviews Neuroscience* 11, 114–126. https://doi.org/10.1038/nrn2762 — Review of how sleep, especially slow-wave sleep, supports memory consolidation.
- Rasch, B. & Born, J. (2013). About sleep's role in memory. *Physiological Reviews* 93, 681–766. https://doi.org/10.1152/physrev.00032.2012 — Long review of sleep's role in memory, covering sleep stages and mechanisms.
