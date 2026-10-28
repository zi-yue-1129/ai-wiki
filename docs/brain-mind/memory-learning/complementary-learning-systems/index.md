---
status: complete
last_reviewed: 2026-10-28
---

# Complementary learning systems (McClelland, McNaughton & O'Reilly, 1995)

The brain learns with two systems that complement each other: a fast hippocampal store for individual episodes and a slow neocortical learner that builds general knowledge, linked by replay.

## Overview

A learning system faces a dilemma. To remember a new experience, it must change its connections quickly. To learn general knowledge from many experiences, it must change them slowly, so that each new item does not overwrite what is already known. The brain seems to solve this with two structures. The hippocampus learns new episodes quickly. The neocortex learns slowly and gradually absorbs what the hippocampus has stored. McClelland, McNaughton and O'Reilly (1995) argued that this division is not an accident: it is the only arrangement that avoids catastrophic interference while still allowing rapid learning.

The theory has become a standard reference point in memory research, and it is also the source of the idea of replay in machine learning. It is one of the main accounts of how memory is organised over time, and it complements the evidence from patients and from long-term potentiation.

## Key concepts

- **Hippocampus**: a brain region that learns rapidly and stores episodes. In the theory it uses sparse, pattern-separated codes, so that similar experiences are represented by distinct patterns.
- **Neocortex**: the outer layer of the cerebral cortex. In the theory it learns slowly, with distributed, overlapping codes, and extracts shared structure across episodes.
- **Catastrophic interference**: the loss of earlier learning when a network is trained on new items without mixing in the old ones.
- **Interleaved learning**: training on a mixture of old and new items, rather than on new items alone.
- **Replay**: the reactivation of stored activity patterns, which in the hippocampus allows the neocortex to be trained on past experiences.

## Problem

Why does the brain need both a hippocampus and a neocortex? If a single network learned new items quickly, why would it erase what it had learned before? Connectionist models trained with standard learning methods showed this problem clearly: when a network learned new material in sequence, it forgot the old material. The 1995 paper asked what structure a learning system needs to avoid this while still being able to learn new things fast.

## Core idea

The complementary learning systems (CLS) framework proposes two learning systems with opposite properties. The hippocampus stores each new item quickly, with sparse codes that keep items apart so they do not interfere. The neocortex learns slowly. Its codes are distributed and overlapping, which lets it find structure shared across many items, but it changes too much if it learns new items in isolation.

Replay links the two. The hippocampus reactivates recently stored patterns, and these reactivations are used to train the neocortex together with other, older material. Each reactivation changes the cortical connections only a little, so the neocortex can absorb new information without overwriting its structured knowledge. Over time, memories become less dependent on the hippocampus. O'Reilly et al. (2014) summarise the framework as the hippocampus being a sparse, pattern-separated system for rapid learning of episodic memories, and the neocortex being a distributed, overlapping system that gradually integrates across episodes to extract latent semantic structure.

## Equation or algorithm

The 1995 paper uses connectionist simulations rather than a single equation. The procedure can be written as steps:

1. Encode each new episode quickly in the hippocampal store, using sparse codes that keep it separate from other episodes.
2. During rest and sleep, reactivate stored hippocampal patterns, so that they can be replayed to the neocortex.
3. Train the neocortical network on a mixture of replayed old items and new items, rather than on new items alone.
4. Use a slow learning rate in the neocortex, so that each update changes its weights only a little.
5. As consolidation proceeds, rely less on the hippocampus for recall of the items the neocortex has absorbed.

A generic way to write the neocortical update is $w \leftarrow w - \eta_{\text{ctx}} \nabla_w L(\mathcal{B})$, where $\eta_{\text{ctx}}$ is small and the batch $\mathcal{B}$ mixes old and new items. This is a gradient-descent notation used to illustrate the idea, not an equation copied from the paper.

## Results

The 1995 paper reports simulations of sequential and interleaved training. When a network learned new facts in sequence, without mixing in old material, it acquired the new facts quickly, but its performance on existing knowledge deteriorated sharply. This is catastrophic interference. When the new facts were added to the full training set, so that they were mixed with ongoing examples, the network learned them more slowly, caused little interference, and integrated them with its existing structured knowledge. The paper also compares its network with human learners on a paradigm in which two lists are learned in sequence. The network lost the first list almost entirely, while people retained much of it.

Support for the replay part of the account comes from neural recordings. Wilson and McNaughton (1994) recorded large ensembles of hippocampal place cells in three rats during spatial tasks and during subsequent slow-wave sleep. Cells that fired together during behaviour fired together more often in the sleep that followed, and this effect declined gradually over each sleep session. The authors suggest that this reflects synaptic change during waking experience, and that information acquired during behaviour is re-expressed in the hippocampus during sleep.

O'Reilly et al. (2014) review the framework's fate over the following decades and conclude that empirical data over about fifteen years have generally confirmed its key principles.

## Limitations

CLS is a conceptual framework supported mostly by simulations and by a limited set of experimental results. The networks in the simulations are much simpler than the cortex, and the division of labour between the two systems is a hypothesis about how the brain is organised, not a fact that has been measured directly. The framework says little about how replay is chosen, which items should be replayed, and how sleep and waking experience contribute.

The theory has also been revised. O'Reilly et al. (2014) discuss how the hippocampus contributes to both encoding and recall, and how the two systems interact. Kumaran, Hassabis and McClelland (2016) revisit the framework in the light of modern learning systems, and their title asks which learning systems intelligent agents need. Their revision shows that the 1995 account is a starting point rather than a finished theory.

Finally, the framework emphasises retention of learned knowledge, while other work argues that forgetting can help. Richards and Frankland (2017) argue that transience, meaning forgetting, supports flexible decisions and generalisation, so a learning system needs both persistence and forgetting. This does not contradict CLS, but it changes what the neocortical store is for.

## Key methods

Three landmark alternatives explain how memories are organised over time:

- [Medial temporal lobe lesions (Scoville & Milner, 1957)](../medial-temporal-lesions/index.md): patient evidence that the hippocampus is needed to form new memories. CLS is the best-known explanation of that evidence.
- [Long-term potentiation (Bliss & Lømo, 1973)](../long-term-potentiation/index.md): a cellular mechanism for strengthening synapses, which the CLS framework does not specify and can be combined with.
- Standard consolidation: memories depend on the hippocampus at first and become independent of it over time, without the specific division of labour that CLS proposes.

## Connections

- Parent topic: [Memory & Learning in the Brain](../index.md)
- Other method on this topic: [Medial Temporal Lobe Lesions](../medial-temporal-lesions/index.md)
- Other method on this topic: [Long-Term Potentiation](../long-term-potentiation/index.md)
- Machine learning: replay in continual learning is the direct descendant of the interleaving idea. See [Replay and memory in continual learning](../../../theory/paradigms/continual/replay-and-memory/index.md) and the wider [continual learning](../../../theory/paradigms/continual/index.md) paradigm, which deals with catastrophic forgetting.
- Sparse codes: the pattern separation that the theory attributes to the hippocampus is discussed in [Sparse coding](../../computational-neuroscience/sparse-coding/index.md).

## Applications

- **Replay in machine learning.** Replay buffers and rehearsal are standard tools in continual learning, where a network learns new tasks without forgetting old ones. The CLS account is often cited as the origin of this idea, and the continual learning pages describe the methods.
- **Memory design for AI systems.** The split between a fast episodic store and slow, shared weights is a common design pattern in systems that combine retrieval from external memory with a trained model. This is a design analogy rather than evidence about brains.
- **Understanding amnesia.** Patients with hippocampal damage can learn new skills but cannot form new episodic memories, which fits the division of labour the theory proposes. See the [medial temporal lobe lesions](../medial-temporal-lesions/index.md) page.

## Open questions

- How does replay select which memories to reactivate, and does the selection depend on importance, novelty or emotional salience?
- How much of the neocortical transfer happens during sleep and how much during waking rest?
- Does the hippocampus keep a full copy of each episode, or only an index that points to cortical traces? The answer changes how the two systems divide the work.
- How should persistence and forgetting be balanced across systems, as Richards and Frankland (2017) propose, and does the CLS framework need a forgetting mechanism?

## References

### Seminal papers

- McClelland, J. L., McNaughton, B. L. & O'Reilly, R. C. (1995). Why there are complementary learning systems in the hippocampus and neocortex: Insights from the successes and failures of connectionist models of learning and memory. *Psychological Review*. https://doi.org/10.1037/0033-295X.102.3.419 — The original CLS theory, with simulations showing catastrophic interference in sequential learning and its avoidance with interleaved training.
- Wilson, M. A. & McNaughton, B. L. (1994). Reactivation of hippocampal ensemble memories during sleep. *Science*. https://doi.org/10.1126/science.8036517 — Recordings in rats showing that hippocampal cells active during behaviour fire together more often in later sleep, supporting the replay part of the account.

### Surveys and textbooks

- O'Reilly, R. C., Bhattacharyya, R., Howard, M. D. & Ketz, N. (2014). Complementary learning systems. *Cognitive Science*. https://doi.org/10.1111/j.1551-6709.2011.01214.x — Review of the framework's core ideas and their support over fifteen years, covering encoding, recall, consolidation and hippocampus–neocortex interaction.
- Kumaran, D., Hassabis, D. & McClelland, J. L. (2016). What learning systems do intelligent agents need? Complementary learning systems theory updated. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2016.05.004 — A revision of the CLS theory that asks which learning systems intelligent agents need, in the context of replay and deep learning.
- Frankland, P. W. & Bontempi, B. (2005). The organization of recent and remote memories. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn1607 — Review of how recent and remote memories are organised across the hippocampus and the cortex over time.
- Richards, B. A. & Frankland, P. W. (2017). The persistence and transience of memory. *Neuron*. https://doi.org/10.1016/j.neuron.2017.04.037 — Argues that forgetting supports flexible decisions and generalisation, so memory should be seen as a balance of persistence and transience.
