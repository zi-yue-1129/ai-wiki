---
status: draft
last_reviewed: 2026-10-28
tags:
- motor control
- internal models
- prediction
- neuroscience
aliases:
  - 內部前向模型
  - 前向模型
  - Internal forward model
  - Forward model
  - Efference copy
---

# Internal forward models (Kawato 1987; Wolpert, Ghahramani & Jordan 1995)

An internal forward model is a learned mapping, inside the nervous system, from a motor command and the current state of the body to the predicted next state. The brain can use such a prediction to act before delayed sensory feedback arrives, and to tell its own sensations apart from changes in the world. It is a long-standing idea in motor control, and it is also a basic component of model-based reinforcement learning.

This page is part of [Motor Control and the Cerebellum](../index.md). It covers one method in detail. Its relation to the other two methods is on the chapter overview.

## Overview

Suppose you move your hand and the world bumps it. The sensory signal arrives a fraction of a second after the event, and by then the next command has to be issued. A controller that only reacts to feedback would always be late. The forward-model idea is that the brain keeps a running prediction of what its movement will do, and corrects that prediction when the real feedback arrives.

## Problem

Motor control faces delays, noise and changing dynamics. Feedback from the eyes and skin takes time to reach the brain, so a controller that depends on it alone cannot make fast corrections. The brain must also infer the current state of the arm, such as its position and velocity, when sensors are noisy. The question is how the nervous system can plan and correct movement with these limits, and whether it represents the consequences of its own commands internally.

## Core idea

The central proposal is that the nervous system contains two complementary learned mappings. A forward model predicts the next sensory state from the current state and the outgoing command. An inverse model, which acts as the controller, produces a command that would bring about a desired state. The forward model's prediction is available immediately, so it can be combined with delayed feedback to give a better estimate of the current state.

Kawato, Furukawa and Suzuki (1987) proposed a hierarchical network for the control and learning of voluntary movement, in which dynamics and inverse-dynamics models are learned through practice. They tested it in computer simulations with a robotic manipulator. Wolpert, Ghahramani and Jordan (1995) tested the idea in a sensorimotor task. They asked how errors in people's estimates of hand position spread over time, and used optimal state estimation to interpret the result. Their conclusion was that the pattern supports an internal model of the motor system.

## Equation or algorithm

A forward model predicts the next state from the current state and command:

\(\hat{x}_{t+1} = f(x_t, u_t)\)

The predicted state is then corrected when feedback arrives. In the linear case this is the update used by a Kalman filter:

\(\hat{x}_{t+1} \leftarrow \hat{x}_{t+1} + K\,(y_{t+1} - \hat{y}_{t+1})\)

Here \(y_{t+1}\) is the observed sensory feedback, \(\hat{y}_{t+1}\) is the predicted feedback, and \(K\) is a gain that sets how much the error changes the estimate. The forward model supplies the prediction. The gain sets how much the controller trusts the feedback relative to the prediction.

Learning is often described as error-driven. The mismatch between predicted and actual sensory feedback is used to adjust the forward model.

## Results

The experimental evidence for forward models is indirect. The forward model is not observed directly, so its existence is inferred from behaviour. Wolpert, Ghahramani and Jordan (1995) analyse how errors in estimated hand position propagate over time, within the framework of optimal state estimation, and they take the result as direct support for an internal model. Wolpert, Miall and Kawato (1998) review internal models in the cerebellum.

## Limitations

- **Indirect evidence.** A forward model is inferred from behaviour and from the way errors spread, not read off a neuron. Other explanations of the same data are possible.
- **Form of the model is unclear.** It is not settled whether the brain learns an exact model of the body or an approximate one that works only in the situations it has been trained on.
- **Where the model is stored is uncertain.** The cerebellum is a leading candidate. [Cerebellar Supervised Learning](../marr-albus-ito/index.md) describes Ito's hypothesis (Ito, 2008) that the cerebellum encodes such models. Other regions may share the role.
- **Prediction and adaptation are linked.** Shadmehr, Smith and Krakauer (2010) review evidence that forward models remain calibrated through motor adaptation, which is driven by sensory prediction errors.

## Connections

- **Optimal control.** Optimal feedback control needs an estimate of the body's state, which the forward model supplies. See [Optimal Feedback Control](../optimal-feedback-control/index.md).
- **Cerebellum.** The cerebellum is proposed to learn internal models, which links this page to [Cerebellar Supervised Learning](../marr-albus-ito/index.md).
- **World models and model-based RL.** A learned model of the environment that predicts the outcome of actions is the AI counterpart of a forward model. See [World Models](../../../theory/models/world-models/index.md) and [Model-Based vs Model-Free Control](../../decision-reward/model-based-vs-model-free/index.md).

## Applications

- **Robotics.** State estimation that combines a dynamics prediction with delayed sensors is standard in robot control. See [Robotics](../../../applications/robotics/index.md).
- **Model-based reinforcement learning.** Agents that learn a forward model of the environment and plan with it apply the same idea; see [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).

## Open questions

- **Where are forward models learned and kept?** The cerebellum is a candidate, but the full network is not mapped.
- **Are forward models exact or approximate?** Whether the brain's models are general or tied to particular tasks is debated.
- **Are perception and action served by the same models?** The same prediction may support both, but the evidence for a shared model is still being studied.

## References

### Seminal papers

- Kawato, M., Furukawa, K. & Suzuki, R. (1987). A hierarchical neural-network model for control and learning of voluntary movement. *Biological Cybernetics*. https://doi.org/10.1007/BF00364149 — Proposes a hierarchical network in which dynamics and inverse-dynamics models are learned through practice, tested in simulation.
- Wolpert, D. M., Ghahramani, Z. & Jordan, M. I. (1995). An internal model for sensorimotor integration. *Science*. https://doi.org/10.1126/science.7569931 — Analyses how errors in estimated hand position propagate over time, and takes this as support for an internal model of the motor system.

### Surveys and textbooks

- Wolpert, D. M., Miall, R. C. & Kawato, M. (1998). Internal models in the cerebellum. *Trends in Cognitive Sciences*. https://doi.org/10.1016/S1364-6613(98)01221-2 — Reviews internal models in the cerebellum.
- Kawato, M. (1999). Internal models for motor control and trajectory planning. *Current Opinion in Neurobiology*. https://doi.org/10.1016/S0959-4388(99)00028-8 — Discusses internal models for motor control and trajectory planning.
- Shadmehr, R., Smith, M. A. & Krakauer, J. W. (2010). Error correction, sensory prediction, and adaptation in motor control. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-060909-153135 — Reviews evidence that forward models stay calibrated through motor adaptation driven by sensory prediction errors.
