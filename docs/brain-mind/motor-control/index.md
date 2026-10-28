---
status: draft
last_reviewed: 2026-10-28
related:
- applications/robotics
- theory/paradigms/reinforcement-learning
- theory/models/world-models
tags:
- neuroscience
- motor control
- cerebellum
- control theory
aliases:
  - 運動控制與小腦
  - Motor Control and the Cerebellum
  - Motor control
  - Cerebellum
  - 小腦
  - 運動控制
---

# Motor Control and the Cerebellum

Moving the body means turning intentions into muscle commands, while the body is slow, noisy and changing. Nervous systems cope with these problems by predicting the consequences of their own commands, correcting errors with feedback, and learning from mistakes. The cerebellum and the motor cortex are the central structures in this work. For AI, motor control is a source of concrete problems: acting under uncertainty, learning from error, and building models of a system's dynamics from data.

This chapter gives an overview of how motor control is understood. Each method is on its own page, linked below.

## Overview

Reaching for a cup looks simple, but the brain faces a sequence of hard problems. Sensory signals arrive with a delay, so the brain cannot rely on feedback alone to guide a fast movement. Muscles change their behaviour with fatigue and load, and the arm's mechanics depend on its posture. Motor control theory asks how a controller can cope with all of this and still produce accurate movement, and which parts of the brain do which job.

The answers developed over several decades. Engineers and physiologists have converged on a few shared ideas: the brain keeps an internal model of the body, it uses feedback in a task-dependent way, and it learns from errors. These ideas bear on the cerebellum's role in adapting movement, and they connect to the population-level dynamics seen in motor cortex.

## Key concepts

- **Internal model**: a learned mapping inside the brain that represents how the body and the world respond to commands. A forward model predicts the outcome of a command; an inverse model proposes a command for a desired outcome.
- **Efference copy**: a copy of a motor command sent to the sensory areas, so that the expected sensory result of one's own movement can be compared with the real one.
- **Climbing fibre and parallel fibre**: the two inputs to a cerebellar Purkinje cell. The climbing fibre carries an error-like teaching signal.
- **Feedback control**: correcting a movement while it happens, using sensed errors.
- **Optimal control**: choosing the commands that best meet a goal, given costs for error and effort and given the noise in the system.
- **Neural population dynamics**: the view that the joint activity of many neurons evolves over time according to rules, rather than each neuron encoding a fixed quantity.

## Key methods

- [Optimal feedback control (Todorov & Jordan 2002)](optimal-feedback-control/index.md): treats movement as optimal control under noise, where feedback corrects only the deviations that matter for the task and other variation is left alone.
- [Cerebellar supervised learning (Marr, Albus & Ito)](marr-albus-ito/index.md): a theory of how the cerebellum learns motor skills, with climbing fibres acting as a teaching signal that changes the strength of synapses on Purkinje cells.
- [Internal forward models (Kawato 1987; Wolpert, Ghahramani & Jordan 1995)](internal-forward-models/index.md): the claim that the brain predicts the sensory outcome of its own commands, which lets it correct movement before delayed feedback arrives.

The first two methods are about how the brain decides and corrects movements. The third is about the predictive machinery those decisions depend on. In practice the three overlap: the cerebellum is thought to learn forward models, and optimal feedback control needs an estimate of the body's state, which a forward model supplies.

## Connections

- **Brain and mind.** The cerebellum is also involved in procedural learning and conditioning; see [Memory & Learning in the Brain](../memory-learning/index.md). The predictive-processing view of the brain, which treats perception and action as the reduction of prediction error, is on [Predictive Coding & Free Energy](../predictive-coding/index.md). Basic structure of the nervous system is covered in [Neuroscience Basics](../neuroscience/index.md), and the modelling tools in [Computational Neuroscience](../computational-neuroscience/index.md).
- **Motor cortex and the brain-computer interface.** Population analyses of motor cortex relate to the decoders used in [Brain-Computer Interfaces](../bci/index.md), including the reach-and-grasp work on [Neural Reach and Grasp](../bci/neural-reach-and-grasp/index.md).
- **Reinforcement learning and model-based control.** A forward model is what a model-based controller uses to plan. The contrast between planning with a learned model and learning values directly is on [Model-Based vs Model-Free Control](../decision-reward/model-based-vs-model-free/index.md), and the reward-based side of learning is on [Decision Making, Dopamine & Reward](../decision-reward/index.md). The general framework is on [Reinforcement Learning](../../theory/paradigms/reinforcement-learning/index.md).
- **NeuroAI.** Motor control has been a testing ground for learning models and world models, covered in [NeuroAI](../neuroai/index.md) and [World Models](../../theory/models/world-models/index.md).

## Applications

- **Robotics.** Albus's later cerebellar model articulation controller (CMAC) is a table-based controller proposed for robot manipulators, which carries the cerebellar idea into engineering. See [Robotics](../../applications/robotics/index.md).
- **Brain-computer interfaces.** Some decoders that read intended movement from motor cortex are built on population-level analyses of that cortex. See the [BCI overview](../bci/index.md).
- **Model-based reinforcement learning.** Agents that learn a model of the environment and plan with it borrow the forward-model idea from motor control. See [Reinforcement Learning](../../theory/paradigms/reinforcement-learning/index.md).

## Open questions

- **Does the cerebellum learn only movement?** Cerebellar circuits are also linked to cognition and timing, and it is debated how far the motor theory extends.
- **Where do motor-cortex dynamics come from?** It is unclear how much of the observed dynamics reflects intrinsic circuit properties, feedback from the body, or learned internal models.
- **Can optimal control scale to learned models?** Optimal feedback control works well when the body's dynamics are known. Learning these dynamics from noisy data, and planning with them, remains hard.
- **How do the methods fit together?** Optimal feedback control, cerebellar learning and forward models are often treated as separate theories. Whether one framework covers all three is an active question.

## References

### Seminal papers

- Marr, D. (1969). A theory of cerebellar cortex. *Journal of Physiology*. https://doi.org/10.1113/jphysiol.1969.sp008820 — Proposes that the cerebellar cortex learns motor skills, with climbing-fibre input from the inferior olive as the teaching signal.
- Albus, J. S. (1971). A theory of cerebellar function. *Mathematical Biosciences*. https://doi.org/10.1016/0025-5564(71)90051-4 — Presents a theory of cerebellar function, published two years after Marr's account.
- Albus, J. S. (1975). A new approach to manipulator control: the cerebellar model articulation controller (CMAC). *Journal of Dynamic Systems, Measurement, and Control*. https://doi.org/10.1115/1.3426922 — Describes a table-based, cerebellum-inspired controller for robot manipulators.
- Todorov, E. & Jordan, M. I. (2002). Optimal feedback control as a theory of motor coordination. *Nature Neuroscience*. https://doi.org/10.1038/nn963 — Proposes that movement coordination follows from stochastic optimal feedback control, in which only task-relevant errors are corrected.
- Wolpert, D. M., Ghahramani, Z. & Jordan, M. I. (1995). An internal model for sensorimotor integration. *Science*. https://doi.org/10.1126/science.7569931 — Analyses how errors in people's estimates of hand position propagate over time, and argues that this supports an internal model of the motor system.
- Churchland, M. M., Cunningham, J. P., Kaufman, M. T., Foster, J. D., Nuyujukian, P., Ryu, S. I. & Shenoy, K. V. (2012). Neural population dynamics during reaching. *Nature*. https://doi.org/10.1038/nature11129 — Reports a brief, strong oscillatory component in the population response of motor cortex during reaching.

### Surveys and textbooks

- Wolpert, D. M., Miall, R. C. & Kawato, M. (1998). Internal models in the cerebellum. *Trends in Cognitive Sciences*. https://doi.org/10.1016/S1364-6613(98)01221-2 — Reviews internal models in the cerebellum.
- Ito, M. (2008). Control of mental activities by internal models in the cerebellum. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2332 — Proposes, as a hypothesis, that the cerebellum encodes internal models, including for mental representations.
- Shadmehr, R., Smith, M. A. & Krakauer, J. W. (2010). Error correction, sensory prediction, and adaptation in motor control. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-060909-153135 — Reviews how errors drive adaptation and how sensory prediction supports it.
- Shenoy, K. V., Sahani, M. & Churchland, M. M. (2013). Cortical control of arm movements: a dynamical systems perspective. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-062111-150509 — Reviews the dynamical systems view of motor cortex and its link to movement.
- Doya, K. (1999). What are the computations of the cerebellum, the basal ganglia and the cerebral cortex? *Neural Networks*. https://doi.org/10.1016/S0893-6080(99)00046-5 — Asks what computations the cerebellum, basal ganglia and cerebral cortex perform.
