---
status: draft
last_reviewed: 2026-10-28
tags:
- motor control
- optimal control
- neuroscience
aliases:
  - 最優回饋控制
  - Optimal feedback control
  - OFC
  - Todorov and Jordan 2002
---

# Optimal feedback control (Todorov & Jordan, 2002)

Optimal feedback control proposes that movement is produced by a controller that minimises a cost under noise, and that the controller corrects only the errors that matter for the task. It offers an account of several features of human movement, and it connects motor behaviour to the optimal control methods used in engineering.

This page is part of [Motor Control and the Cerebellum](../index.md). It covers one method in detail. The predictive machinery that such a controller needs is on [Internal Forward Models](../internal-forward-models/index.md).

## Overview

When you reach for a cup, your hand does not follow one fixed path. Trajectories vary from attempt to attempt, and some of that variation lies in directions that do not change where the hand ends up. Optimal feedback control asks why the nervous system would allow such variation, and why it corrects some deviations but not others.

The proposed answer is that the brain aims at a goal, not a trajectory. It tries to reach the goal at the lowest cost, counting both task error and effort, with noise in both motor commands and sensing. Under these conditions, the best strategy is to let movement vary where variation is harmless and to push back only where it threatens the goal.

## Problem

Motor coordination involves more degrees of freedom than a task needs. A human arm has more joints and muscles than are required to place the hand at one point, so many movements achieve the same result. Some accounts assume a single preferred trajectory or a fixed rule for resolving this redundancy. Optimal feedback control asks why movement variation has the structure it does.

## Core idea

Todorov and Jordan (2002) treat motor coordination as stochastic optimal feedback control. The controller chooses commands at each moment to minimise an expected cost, using sensory feedback to choose its next command. It is not required to hold the movement on a predefined path, so it allows deviation in task-irrelevant directions and corrects deviations that would affect the outcome.

The authors argue that the pattern of movement variability follows from this single principle, rather than from a separate mechanism for each feature.

## Equation or algorithm

The general problem is to choose controls \(u_t\) that minimise an expected cost, given a state \(x_t\) that evolves with noise:

\(\min_{u} \ \mathbb{E}\left[\sum_{t=0}^{T} c(x_t, u_t)\right] \quad \text{subject to} \quad x_{t+1} = f(x_t, u_t) + \xi_t\)

Here \(c\) is the cost, combining task error and effort, \(f\) is the body's dynamics, and \(\xi_t\) is noise. The controller can only observe a noisy version of the state, so it must estimate the state from its observations, as a Kalman filter does in the linear case.

In the linear-quadratic-Gaussian case, the optimal control law is a linear feedback rule, \(u_t = -L_t \hat{x}_t\), where \(\hat{x}_t\) is the estimated state and the gain \(L_t\) follows from the cost and the dynamics. The gain is larger in directions where errors affect the cost, and smaller where they do not. That is the mechanism behind the selective correction described above.

## Results

The predicted pattern is that variability is allowed in redundant, task-irrelevant directions, while deviations that affect the task outcome are corrected. This page does not quote numbers from the 2002 paper's experiments. The key evidence for the theory is the match between this predicted pattern and observed movement variability, and such a match does not by itself show that the brain runs this exact algorithm.

## Limitations

- **Cost functions are chosen by the modeller.** The predictions depend on the assumed cost. Different costs can produce different patterns, so a good fit does not by itself identify the brain's objective.
- **Dynamics must be known or learned.** The controller needs a model of the body to predict the effects of its commands and to estimate the state. Where that model is inaccurate, the predicted behaviour may differ from observed behaviour. The predictive machinery is discussed on the [Internal Forward Models](../internal-forward-models/index.md) page.
- **Optimality is a framework.** Optimality accounts describe what a movement system appears to achieve. They do not, on their own, specify the neural circuit that carries out the computation. Todorov (2004) discusses optimality principles in sensorimotor control.
- **Simple forms assume linearity.** The closed-form solution holds for linear dynamics and quadratic costs. Real limbs and muscles are nonlinear, so approximate methods are needed.

## Connections

- **Internal models.** Feedback control at short delays needs a prediction of the body's state, which is the role of the forward model. See [Internal Forward Models](../internal-forward-models/index.md).
- **Cerebellum.** The cerebellum is proposed to adjust movements through learned corrections; the cerebellar view is on [Cerebellar Supervised Learning (Marr, Albus & Ito)](../marr-albus-ito/index.md).
- **Reinforcement learning and model-based control.** An optimal controller that plans with a model of the dynamics is a model-based method. The contrast with value-based learning is on [Model-Based vs Model-Free Control](../../decision-reward/model-based-vs-model-free/index.md), and the framework is on [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).

## Applications

- **Robotics.** Optimal control and state estimation are standard tools in robot control, and the feedback-gain idea carries over. See [Robotics](../../../applications/robotics/index.md).

## Open questions

- **What is the brain's cost?** Effort, accuracy and other terms all plausibly matter, and identifying the real objective is difficult.
- **How is the model learned?** The controller needs an internal model of the body. How this model is acquired and kept accurate over time is an open question, and the cerebellum is a candidate.
- **How far does linear theory reach?** Extending the framework to nonlinear dynamics remains an active area.

## References

### Seminal papers

- Todorov, E. & Jordan, M. I. (2002). Optimal feedback control as a theory of motor coordination. *Nature Neuroscience*, 5(11), 1226–1235. https://doi.org/10.1038/nn963 — Proposes that movement coordination follows from stochastic optimal feedback control, in which only task-relevant errors are corrected.
- Harris, C. M. & Wolpert, D. M. (1998). Signal-dependent noise determines motor planning. *Nature*, 394(6695), 780–784. https://doi.org/10.1038/29528 — Proposes minimum-variance theory: because noise grows with the size of the command, trajectories are chosen to minimise the variance of the final position.

### Surveys and textbooks

- Todorov, E. (2004). Optimality principles in sensorimotor control. *Nature Neuroscience*, 7(9), 907–915. https://doi.org/10.1038/nn1309 — Discusses optimality principles in sensorimotor control, the framework that this method builds on.
- Scott, S. H. (2004). Optimal feedback control and the neural basis of volitional motor control. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn1427 — Discusses optimal feedback control and its neural basis in volitional movement.
- Shadmehr, R., Smith, M. A. & Krakauer, J. W. (2010). Error correction, sensory prediction, and adaptation in motor control. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-060909-153135 — Reviews how sensory prediction errors drive motor adaptation and keep forward models calibrated.
