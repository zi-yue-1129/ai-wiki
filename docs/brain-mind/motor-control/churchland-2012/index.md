---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/rnn
tags:
- neuroscience
- learning
aliases:
  - Churchland et al. 2012
  - 運動皮質的群體動態
  - Neural population dynamics
  - Motor cortex dynamics
---

# Neural Population Dynamics in Motor Cortex (Churchland et al. 2012)

Churchland et al. (2012) analysed the activity of many motor cortex neurons at once during reaching, and argued that the population response is best described as the trajectory of a dynamical system. Structure that is hard to see in single neurons becomes visible in the population state.

This page is part of [Motor Control and the Cerebellum](../index.md). The parent page gives the overview; this page covers the analysis, the dynamical view and the evidence.

## Overview

For decades, motor cortex was studied one neuron at a time. Each neuron was described by its tuning, the direction of movement that made it fire most. This works well for some questions, but single-neuron tuning does not explain how the population produces a movement from start to finish. Two neurons with similar tuning can behave very differently over the course of a reach, and the same neuron can be tuned differently across conditions.

Churchland et al. (2012) changed the unit of analysis. They recorded many neurons at the same time and treated their joint activity as a single state that evolves over time. The question became how that state moves through a space defined by the population, rather than which direction each neuron prefers. This shift is the foundation of the dynamical systems view surveyed by Shenoy, Sahani and Churchland (2013), and it links motor cortex to the wider theory in [Motor Control and the Cerebellum](../index.md).

## Key concepts

- **Population state**: a vector with one entry per neuron, giving the firing of the whole population at one moment.
- **Low-dimensional subspace**: population activity is often well described by a small number of combined patterns, found by a method such as principal component analysis.
- **Dynamical system**: a rule that describes how a state changes over time, with the next state determined by the current state and any inputs.
- **Preparatory state**: activity that appears before a movement begins and that sets the starting point for the movement dynamics.
- **Rotational dynamics**: a pattern in which the population trajectory circles in a low-dimensional plane during the movement, a structure reported for motor cortex.

## How it works

The analysis can be described as a sequence of steps. The paper's own fitting details differ in places, so the steps below are a summary rather than a replication.

1. Record the activity of many neurons in motor cortex at the same time while a monkey performs reaching movements to several targets.
2. Form a population state vector at each time point and each condition, with one entry per neuron.
3. Reduce the dimensionality of the data, for example with principal component analysis, to find the subspace in which most of the activity lies.
4. Plot the trajectories in that subspace, and test whether they follow a consistent rule. A generic linear model of the form $\dot{x} = A x + b$ is one way to express such a rule, where $x$ is the population state in the subspace.
5. Check whether the preparatory state before the movement sets where the trajectory starts.

The central claim is that the trajectories have structure that is shared across reaches and that the rule governing them is the same from one condition to another. This moves the explanation from single-neuron tuning to the properties of the population state and its dynamics.

## Results

The paper's evidence is recordings from motor cortex during reaching, analysed at the population level. The main result, in qualitative terms, is that population activity during the movement follows structured, rotation-like trajectories in a low-dimensional subspace, and that the state reached before the movement shapes what follows. The paper gives its quantitative fits and comparisons, which are not quoted on this page.

The result is important because it shows that a population-level account can make predictions that a single-neuron account does not, such as which dimensions carry the movement and how the preparatory state constrains the movement.

## Limitations

- The data come from monkeys performing reaching movements to a limited set of targets. Extending the result to other movements, species and tasks is a separate question.
- The analysis depends on choices, such as how many dimensions to keep and how trajectories are aligned, which can influence the apparent structure.
- The dynamics are described from correlated activity. The analysis alone does not show that the population dynamics cause the movement.
- Sensory feedback and inputs from other brain areas can also shape the trajectories. Separating these from intrinsic dynamics is difficult.

## Open questions

- **Are the dynamics intrinsic to motor cortex or driven from outside?** Recurrent connections in the circuit could generate rotational dynamics on their own, or the structure could come from inputs. The answer determines how much motor cortex itself computes.
- **How do population dynamics relate to muscle activity?** The population state must eventually drive the muscles, and the mapping between the two is an active area of study.
- **Do the findings generalise?** Results from reaching may not transfer to grasping, speech or whole-body movement. Speech decoding from motor cortex is one case where the population view is being tested; see [Speech neuroprosthesis (Willett et al., 2023)](../../bci/speech-neuroprosthesis/index.md).

## References

### Seminal papers

- Churchland, M. M., Cunningham, J. P., Kaufman, M. T., Foster, J. D., Nuyujukian, P., Ryu, S. I. et al. (2012). Neural population dynamics during reaching. *Nature*. https://doi.org/10.1038/nature11129 — Analyses motor cortex activity during reaching at the population level and describes it as structured dynamics.
- Sussillo, D., Churchland, M. M., Kaufman, M. T. & Shenoy, K. V. (2015). A neural network that finds a naturalistic solution for the production of muscle activity. *Nature Neuroscience*. https://doi.org/10.1038/nn.4042 — Trains recurrent networks to produce muscle activity for reaching, and compares their internal activity with motor cortex recordings.

### Surveys and textbooks

- Shenoy, K. V., Sahani, M. & Churchland, M. M. (2013). Cortical control of arm movements: a dynamical systems perspective. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-062111-150509 — Reviews the case for treating motor cortex as a dynamical system rather than a set of tuned neurons.
- Shadmehr, R., Smith, M. A. & Krakauer, J. W. (2010). Error correction, sensory prediction, and adaptation in motor control. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-060909-153135 — Reviews how the brain uses feedback, forward models and adaptation to control movement, which bears on the inputs to motor cortex.
- Wolpert, D. M. & Ghahramani, Z. (2000). Computational principles of movement neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/81497 — A short review of computational principles for movement, placing population-level accounts among them.
