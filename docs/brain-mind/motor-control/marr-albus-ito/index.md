---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/supervised
tags:
- neuroscience
- supervised learning
aliases:
  - Marr-Albus-Ito
  - 小腦監督學習
  - Cerebellar supervised learning
  - Climbing fibre learning
---

# Cerebellar Supervised Learning (Marr, Albus and Ito)

The Marr–Albus–Ito theory proposes that the cerebellar cortex learns movements in a supervised way. Climbing fibres from the inferior olive carry a teaching signal, and they weaken the synapses that were active just before an error. Ito's later work on long-term depression supplied the synaptic mechanism for this idea.

This page is part of [Motor Control and the Cerebellum](../index.md). The parent page gives the overview; this page covers the theory, its learning rule, and the evidence.

## Overview

The cerebellum sits behind the brainstem and contains a highly regular circuit. Its output cells, the Purkinje cells, receive two kinds of input. Parallel fibres, from a very large population of granule cells, carry a context signal. Climbing fibres, from the inferior olive, each contact a small number of Purkinje cells and fire rarely but strongly. Marr (1969) and Albus (1971) asked what this architecture is for, and both proposed that the climbing-fibre input is a teaching signal.

The theory fits the cerebellum's role in movement. A motor skill is learned by repeating movements and correcting the errors that follow. If the climbing fibres signal those errors, the cerebellum can improve its output without a separate teacher, which is the essence of supervised learning.

## Key concepts

- **Purkinje cell**: the principal output neuron of the cerebellar cortex. Its firing shapes the motor commands that reach the rest of the brain.
- **Parallel fibre**: the axon of a granule cell, carrying a sparse context signal across many Purkinje cells.
- **Climbing fibre**: an input from the inferior olive that contacts a Purkinje cell strongly. In the theory it is the error or teaching signal.
- **Long-term depression (LTD)**: a lasting weakening of a synapse. At parallel-fibre synapses on Purkinje cells it follows the coincident activity of the climbing fibre.[^1]
- **Supervised learning**: learning from input–target pairs, where the target tells the learner what the correct output was. Here the climbing fibre provides the target through its error signal.

## How it works

The theory can be stated as a numbered procedure. The version below is a modern simplification written in our own notation; it is not the notation of the original papers.

1. A context signal arrives through the mossy fibres and is expanded by the granule cells into a pattern of parallel-fibre activity, $x_i$.
2. The Purkinje cell output is a weighted sum of the active parallel fibres, $y = \sum_i w_i x_i$.
3. On each trial, the inferior olive sends a climbing-fibre signal $c$ that is strong when the movement error is large.
4. When $c$ fires together with an active parallel fibre, that synapse is weakened: $\Delta w_i = -\eta\, c\, x_i$, where $\eta$ is a learning rate.
5. Over many trials the output moves towards the correct command, and the pattern of weights stores the learned movement.

Marr's account rests on the one-to-one relation between a climbing fibre and the Purkinje cells it contacts, which he treated as the basis for the teaching signal. His paper proposes two forms of input–output relation, one for learning movements and one for maintaining posture and balance. Albus (1971) reached a companion theory with the same teaching-signal idea.

The rule above is the synaptic form of the idea. Ito's experiments showed that paired activity of climbing and parallel fibres produces the lasting depression that the rule requires.[^1]

## Results

The Marr and Albus papers are theoretical. Their support is the fit between the theory and the known anatomy and physiology of the cerebellar cortex, rather than a benchmark or a measured quantity. The papers do not report numbers that this page needs to quote.

The synaptic side of the theory was tested later. Ito's review of cerebellar long-term depression summarises two decades of data on the induction, signalling and functional roles of LTD at parallel-fibre to Purkinje-cell synapses, and the review supports the idea that paired climbing-fibre and parallel-fibre activity weakens the parallel-fibre input.

## Limitations

- The theories were formulated before the synaptic mechanism was established, so their learning rule was partly a hypothesis about what the physiology would have to do.
- Marr's and Albus's models differ in detail, and both make simplifying assumptions, for example about how the input patterns are formed.
- The rule describes one plasticity mechanism. Other synapses and cell types in the cerebellum also change, and the broader picture is still being built.
- The theory was framed around motor skill. Its extension to other functions is a separate claim, which needs its own evidence.

## Open questions

- **Is the climbing fibre a clean error signal?** Its firing is not a simple measure of error, and the precise mapping from climbing-fibre activity to learning is still under study. Dean et al. (2009) discuss how the microcircuit could act as an adaptive filter in this setting.
- **What is the role of other plasticity sites?** Learning at other synapses in the cerebellum may matter for timing and for generalisation across movements.
- **How does the rule relate to machine supervised learning?** The climbing fibre is a teacher, but it does not supply the full target value; a comparison with supervised learning in [Supervised Learning](../../../theory/paradigms/supervised/index.md) is useful but not exact.

## References

### Seminal papers

- Marr, D. (1969). A theory of cerebellar cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1969.sp008820 — Proposes that climbing-fibre input from the inferior olive teaches Purkinje cells to learn movements, and that a second input form handles posture.
- Albus, J. S. (1971). A theory of cerebellar function. *Mathematical Biosciences*. https://doi.org/10.1016/0025-5564(71)90051-4 — A companion theory of cerebellar learning, in which climbing fibres supply the teaching signal for the cerebellar cortex.
- Kawato, M., Furukawa, K. & Suzuki, R. (1987). A hierarchical neural-network model for control and learning of voluntary movement. *Biological Cybernetics*. https://doi.org/10.1007/BF00364149 — A hierarchical network that learns a feedforward controller from feedback error, an early computational model of cerebellar-style learning.

### Surveys and textbooks

- Ito, M. (2001). Cerebellar long-term depression: characterization, signal transduction, and functional roles. *Physiological Reviews*. https://doi.org/10.1152/physrev.2001.81.3.1143 — Reviews the physiology of long-term depression at cerebellar Purkinje cell synapses and its proposed functions.
- Dean, P., Porrill, J., Ekerot, C.-F. & Jörntell, H. (2009). The cerebellar microcircuit as an adaptive filter: experimental and computational evidence. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2756 — Reviews experimental and computational evidence that the cerebellar microcircuit acts as an adaptive filter.
- Wolpert, D. M., Miall, R. C. & Kawato, M. (1998). Internal models in the cerebellum. *Trends in Cognitive Sciences*. https://doi.org/10.1016/S1364-6613(98)01221-2 — Reviews evidence that the cerebellum learns forward and inverse internal models for movement.

[^1]: Ito's review describes long-term depression induced when climbing-fibre and parallel-fibre inputs to a Purkinje cell are repeatedly associated. The review discusses the signalling mechanism and its functional role, and the wider interpretation remains debated.
