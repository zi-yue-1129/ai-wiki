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

The Marr–Albus–Ito theory proposes that the cerebellar cortex learns motor skills as a supervised learner. Climbing-fibre input acts as a teaching signal, and it changes how Purkinje cells respond to patterns of input from parallel fibres. The theory links a specific circuit to a specific learning rule, and it is one of the clearest examples of a neural circuit explained in terms of a learning algorithm.

This page is part of [Motor Control and the Cerebellum](../index.md). It covers one method in detail. The general paradigm of learning from a teacher is in [Supervised Learning](../../../theory/paradigms/supervised/index.md).

## Overview

The cerebellum holds most of the brain's neurons (see [Neuroscience Basics](../../neuroscience/index.md)), yet damage to it usually impairs coordination and movement adjustment rather than causing paralysis. The Marr–Albus–Ito theory asks what it computes and how its connections support learning.

## Problem

How can a neural circuit learn the right motor output for a context, given only occasional error feedback? The cerebellar circuit is highly structured, with a huge number of granule cells and a single output per Purkinje cell. The question is what that structure computes and how its synapses change.

## Core idea

Marr's 1969 theory proposed that the cerebellar cortex learns motor skills. He described two forms of input-output relation, one for learning movements and one for maintaining posture and balance. In his account, the inferior olive sends a signal that represents an elemental movement, and the climbing fibre carries it to the matched Purkinje cell. The Purkinje cell is also exposed, through the mossy-fibre pathway and the granule cells, to the context in which the movement occurred. Repeated pairing of context and climbing-fibre activity lets the Purkinje cell later initiate the movement from the context alone.

Albus (1971) developed a related model. Its central idea is that the climbing-fibre signal acts as an error signal, so that the cerebellum adjusts its output to reduce the error. In this view the cerebellum is a learning machine that is trained by a teacher, which is what "supervised" means here.

Ito's contribution was experimental. His work on the cerebellar cortex identified a form of synaptic change, long-term depression, at parallel-fibre to Purkinje-cell synapses when those synapses are active together with climbing-fibre input (reviewed in Ito, 2006). This gave a biological mechanism for an error-driven weight change, and it linked the theory to measured synapses. Ito (2008) further argued that the cerebellum learns internal models of the body and the world, which is the connection to [Internal Forward Models](../internal-forward-models/index.md).

## Equation or algorithm

A common simplified form of this family of models treats a Purkinje cell as a weighted sum of parallel-fibre activity:

\(y = \sum_i w_i x_i\)

Here \(x_i\) is the activity of parallel fibre \(i\), \(w_i\) is its synaptic weight, and \(y\) is the Purkinje-cell output. Learning adjusts each weight in proportion to the error signal \(e\) carried by the climbing fibre and the activity of the synapse:

\(\Delta w_i = -\eta \, e \, x_i\)

with learning rate \(\eta\). This is the perceptron-style delta rule from supervised learning. It is a simplified model: the papers do not state it in this form, and the detailed biological rule is still debated.

## Results

Marr's and Albus's papers are theoretical. They argue that a circuit with the assumed connectivity can learn input-output mappings in the stated way, and that the cerebellum fits this theory. Experimental support came later, notably Ito's studies of long-term depression, reviewed in Ito (2006), which provided evidence for the synaptic change the theory needs.

## Limitations

- **The original theories preceded the measurements.** Marr's and Albus's theories were formulated before the synaptic change was measured. Ito's identification of depression at parallel-fibre to Purkinje-cell synapses fixed the direction of that change, which the theories had not pinned down from data.
- **The teaching signal is not fully settled.** Calling the climbing fibre an error signal is a strong interpretation. Its exact content in different tasks is still studied.
- **The model is simplified.** It leaves out the deep cerebellar nuclei, the interneurons and the many connections that shape the output. Later work has added these to the picture.
- **Motor learning is not the whole story.** The cerebellum is also linked to timing and to some cognitive functions, which the motor theory does not explain on its own (Ito, 2008).

## Connections

- **Internal models.** Ito's later view is that the cerebellum learns internal models, which connects this theory to forward prediction. See [Internal Forward Models](../internal-forward-models/index.md).
- **Optimal control.** Whether the cerebellum learns the feedback gains that optimal control predicts is an open hypothesis; see [Optimal Feedback Control](../optimal-feedback-control/index.md).
- **Supervised learning.** The theory is a biological instance of supervised learning, the paradigm in which a teacher supplies the target. See [Supervised Learning](../../../theory/paradigms/supervised/index.md).
- **Division of labour.** Doya (1999) proposed that the cerebellum, basal ganglia and cortex implement supervised, reinforcement and unsupervised learning. The cerebellum's part is the supervised one. Procedural learning more broadly is on [Memory & Learning in the Brain](../../memory-learning/index.md).

## Applications

- **Robot control.** Albus (1975) introduced the cerebellar model articulation controller (CMAC), a table-based function approximator for manipulator control. It applies the cerebellar idea of a sparse, expanded code to engineering control. See [Robotics](../../../applications/robotics/index.md).
- **Neural network design.** The pairing of an expanded input code with an error-driven weight change recurs in AI learning systems, including the perceptron-like models above. See [NeuroAI](../../neuroai/index.md).

## Open questions

- **Does the teaching signal always mean error?** Some studies suggest that climbing-fibre activity carries information beyond a simple error.
- **Where else does learning happen?** The theory places learning in the Purkinje-cell synapses, but plasticity may also occur at other sites in the cerebellum.

## References

### Seminal papers

- Marr, D. (1969). A theory of cerebellar cortex. *Journal of Physiology*. https://doi.org/10.1113/jphysiol.1969.sp008820 — Proposes that the cerebellar cortex learns motor skills, with climbing-fibre input from the inferior olive as the teaching signal.
- Albus, J. S. (1971). A theory of cerebellar function. *Mathematical Biosciences*. https://doi.org/10.1016/0025-5564(71)90051-4 — Develops the cerebellar learning model in which the climbing-fibre signal guides changes in Purkinje-cell output.
- Albus, J. S. (1975). A new approach to manipulator control: the cerebellar model articulation controller (CMAC). *Journal of Dynamic Systems, Measurement, and Control*. https://doi.org/10.1115/1.3426922 — Applies the cerebellar model to robot manipulator control.

### Surveys and reviews

- Ito, M. (2006). Cerebellar circuitry as a neuronal machine. *Progress in Neurobiology*. https://doi.org/10.1016/j.pneurobio.2006.02.006 — Reviews the circuit of the cerebellar cortex and the synaptic plasticity that supports its learning.
- Ito, M. (2008). Control of mental activities by internal models in the cerebellum. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2332 — Argues that the cerebellum learns internal models, including for non-motor functions.
- Doya, K. (1999). What are the computations of the cerebellum, the basal ganglia and the cerebral cortex? *Neural Networks*. https://doi.org/10.1016/S0893-6080(99)00046-5 — Proposes a division of labour among cerebellum, basal ganglia and cortex as supervised, reinforcement and unsupervised learners.
