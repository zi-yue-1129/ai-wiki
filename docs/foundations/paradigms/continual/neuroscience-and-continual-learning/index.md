---
related:
- brain-mind/psychology/index.md
- brain-mind/neuroai/index.md
tags:
  - continual learning
  - neuroscience
  - complementary learning systems
---

# Neuroscience and Continual Learning

Brains learn continually without catastrophically forgetting old skills, and this is one of the main reasons continual learning is studied as a problem. Neuroscience offers ideas such as complementary learning systems and synaptic consolidation, and artificial methods often borrow these ideas, even when the mechanisms differ.

## Overview

Catastrophic forgetting was identified in connectionist models long before deep learning. Brains appear to avoid it through several mechanisms: a fast system that stores episodes and a slow system that extracts structure, sleep-related replay of past experience, and synapses that become more stable as they are used. Each of these has a machine learning counterpart.

## Biological ideas and their analogues

- **Complementary learning systems**: a hippocampal system stores specific episodes quickly, and a neocortical system learns slowly and generalises. This maps onto replay buffers combined with slow parameter updates.
- **Synaptic consolidation**: important synapses are protected from change. This inspired the parameter-importance penalties in [regularisation-based methods](../regularisation-based/index.md).
- **Replay during sleep and rest**: offline reactivation of past experience, which motivates replay in [replay-based methods](../replay-and-memory/index.md).
- **Structural plasticity**: the brain grows and prunes connections, which relates to [architecture-based methods](../architecture-based/index.md).

## Limits of the analogy

Biological memory is far more heterogeneous than any single artificial method. The analogies are inspirational rather than precise, and claims that a method reproduces a biological mechanism need direct evidence.

## Connections

The psychology of memory is covered in [psychology and AI](../../../../brain-mind/psychology/index.md) and [neuro-AI](../../../../brain-mind/neuroai/index.md). The architecture and replay ideas also appear in [meta-learning](../../meta-learning/index.md), where the goal is fast adaptation rather than retention.

## Applications

Designing continual learners for robots and assistants that must keep old skills, and testing theories of memory consolidation through computational models.

## Open questions

It is unclear which biological mechanisms are essential for continual learning and which are incidental. Whether artificial systems can match the lifelong stability of brains at comparable scale is also unresolved.

## References

### Seminal papers

- Kumaran, Hassabis & McClelland (2016), "What learning systems do intelligent agents need? Complementary learning systems theory updated", Trends in Cognitive Sciences. https://web.stanford.edu/~jlmcc/papers/KumaranHassabisMcClelland16FinalMS.pdf — Updates the complementary learning systems theory with a fast episodic system and a slow semantic system.
- Kirkpatrick et al. (2017), "Overcoming catastrophic forgetting in neural networks", PNAS, arXiv:1612.00796 — Applies the idea of synaptic consolidation to protect important parameters.
- Zenke, Poole & Ganguli (2017), "Continual learning through synaptic intelligence", ICML, arXiv:1703.04200 — Models synapses that accumulate importance over time, in the spirit of biological consolidation.

### Surveys and textbooks

- Parisi, Kemker, Part, Kanan & Wermter (2019), "Continual lifelong learning with neural networks: a review", Neural Networks, arXiv:1802.07569 — Review that discusses the biological inspiration for continual learning methods.
- De Lange et al. (2021), "A continual learning survey: defying forgetting in classification tasks", IEEE TPAMI, arXiv:1909.08383 — Survey that connects the artificial methods to the biological ideas they draw on.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- McCloskey & Cohen (1989), "Catastrophic interference in connectionist networks: the sequential learning problem", *Psychology of Learning and Motivation*. No link checked.
