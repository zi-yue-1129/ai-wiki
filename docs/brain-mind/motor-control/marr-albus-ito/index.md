---
status: draft
last_reviewed: 2026-10-28
tags:
- motor control
- cerebellum
- supervised learning
- neuroscience
aliases:
  - 馬爾—阿爾布斯—伊藤小腦學習理論
  - 小腦監督式學習
  - Marr–Albus–Ito theory
  - Cerebellar supervised learning
  - Marr-Albus-Ito
---

# Cerebellar supervised learning (Marr, Albus & Ito)

The Marr–Albus–Ito theory proposes that the cerebellar cortex learns motor skills as a supervised learner. Climbing-fibre input acts as a teaching signal, and it changes how Purkinje cells respond to patterns of input from parallel fibres. The theory links a specific circuit to a specific learning rule, which is why it is often cited as an example of a neural circuit explained in terms of a learning algorithm.

This page is part of [Motor Control and the Cerebellum](../index.md). It covers one method in detail. The general paradigm of learning from a teacher is in [Supervised Learning](../../../theory/paradigms/supervised/index.md).

## Overview

The cerebellum is central to learning motor skills, as Marr's 1969 theory proposed (see [Neuroscience Basics](../../neuroscience/index.md) for its basic structure). The Marr–Albus–Ito theory asks what it computes and how its connections support learning.

## Problem

How can a neural circuit learn the right motor output for a context, given only occasional error feedback? The cerebellar circuit is highly structured. The question is what that structure computes and how its synapses change.

## Core idea

Marr's 1969 theory proposed that the cerebellar cortex learns motor skills. He described two forms of input-output relation, one for learning movements and one for maintaining posture and balance. In his account, the inferior olive sends a signal that represents an elemental movement, and the climbing fibre carries it to the matched Purkinje cell. The Purkinje cell is also exposed, through the mossy-fibre pathway, to the context in which the movement occurred. Repeated pairing of context and climbing-fibre activity lets the Purkinje cell later initiate the movement from the context alone.

Albus (1971) presented another theory of cerebellar function. The "supervised" in this page's title refers to the climbing-fibre input, which is read as a teaching signal.

Ito (2008) proposes, as a hypothesis, that the cerebellum encodes internal models, and that these may extend to mental representations in the cerebral cortex. This is the link to [Internal Forward Models](../internal-forward-models/index.md).

## Equation or algorithm

A common simplified form of this family of models treats a Purkinje cell as a weighted sum of parallel-fibre activity:

\(y = \sum_i w_i x_i\)

Here \(x_i\) is the activity of parallel fibre \(i\), \(w_i\) is its synaptic weight, and \(y\) is the Purkinje-cell output. Learning adjusts each weight in proportion to the error signal \(e\) carried by the climbing fibre and the activity of the synapse:

\(\Delta w_i = -\eta \, e \, x_i\)

with learning rate \(\eta\). This is the perceptron-style delta rule from supervised learning. It is a simplified form written for this page, not a formula quoted from the papers, and the detailed biological rule is still debated.

## Results

Marr's 1969 paper and Albus's 1971 paper are theoretical proposals about cerebellar function. Whether the synaptic changes they require are found in the cerebellum is a question for experiments, which this page does not review in detail.

## Limitations

- **These theories are proposals.** Marr's and Albus's accounts must be checked against measurements of the cerebellar circuit before they can be taken as established.
- **The teaching signal is not fully settled.** Calling the climbing fibre an error signal is a strong interpretation. Its exact content in different tasks is still studied.
- **The model is simplified.** It leaves out the deep cerebellar nuclei, the interneurons and many connections that shape the output.
- **Motor learning is not the whole story.** Ito (2008) proposes that the cerebellum may also contribute to non-motor functions, which the motor theory does not cover.

## Connections

- **Internal models.** Ito (2008) proposes that the cerebellum encodes internal models, which connects this theory to forward prediction. See [Internal Forward Models](../internal-forward-models/index.md).
- **Optimal control.** Whether the cerebellum learns the feedback gains that optimal control predicts is an open hypothesis; see [Optimal Feedback Control](../optimal-feedback-control/index.md).
- **Supervised learning.** The theory is a biological instance of supervised learning, the paradigm in which a teacher supplies the target. See [Supervised Learning](../../../theory/paradigms/supervised/index.md).
- **Division of labour.** Doya (1999) asks what computations the cerebellum, basal ganglia and cerebral cortex perform. Procedural learning more broadly is on [Memory & Learning in the Brain](../../memory-learning/index.md).

## Applications

- **Robot control.** Albus (1975) introduced the cerebellar model articulation controller (CMAC), a table-based function approximator for manipulator control. It applies the cerebellar model to engineering control. See [Robotics](../../../applications/robotics/index.md).
- **Neural network design.** The pairing of an expanded input code with an error-driven weight change recurs in AI learning systems, including the perceptron-like models above. See [NeuroAI](../../neuroai/index.md).

## Open questions

- **Does the teaching signal always mean error?** How well the climbing-fibre signal matches a simple error is an open question.
- **Where else does learning happen?** The theory places learning in the Purkinje-cell synapses, but plasticity may also occur at other sites in the cerebellum.

## References

### Seminal papers

- Marr, D. (1969). A theory of cerebellar cortex. *Journal of Physiology*, 202(2), 437–470. https://doi.org/10.1113/jphysiol.1969.sp008820 — Proposes that the cerebellar cortex learns motor skills, with climbing-fibre input from the inferior olive as the teaching signal.
- Albus, J. S. (1971). A theory of cerebellar function. *Mathematical Biosciences*. https://doi.org/10.1016/0025-5564(71)90051-4 — Presents a theory of cerebellar function, published two years after Marr's account.
- Albus, J. S. (1975). A new approach to manipulator control: the cerebellar model articulation controller (CMAC). *Journal of Dynamic Systems, Measurement, and Control*, 97(3), 220–227. https://doi.org/10.1115/1.3426922 — Applies the cerebellar model to robot manipulator control.

### Surveys and textbooks

- Ito, M. (2006). Cerebellar circuitry as a neuronal machine. *Progress in Neurobiology*, 78(3–5), 272–303. https://doi.org/10.1016/j.pneurobio.2006.02.006 — Reviews the circuitry of the cerebellar cortex.
- Ito, M. (2008). Control of mental activities by internal models in the cerebellum. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2332 — Proposes, as a hypothesis, that the cerebellum encodes internal models, including for mental representations.
- Doya, K. (1999). What are the computations of the cerebellum, the basal ganglia and the cerebral cortex? *Neural Networks*, 12(7–8), 961–974. https://doi.org/10.1016/S0893-6080(99)00046-5 — Asks what computations the cerebellum, basal ganglia and cerebral cortex perform.
