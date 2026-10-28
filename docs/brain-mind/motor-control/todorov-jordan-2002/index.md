---
status: draft
last_reviewed: 2026-10-28
related:
- applications/robotics
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- planning
aliases:
  - Todorov and Jordan 2002
  - 最優回饋控制
  - Optimal feedback control
  - Minimal intervention principle
---

# Optimal Feedback Control (Todorov & Jordan 2002)

Todorov and Jordan (2002) proposed that coordinated movement is the output of an optimal feedback controller. The controller chooses commands that minimise a task cost, and because the cost penalises only errors that matter to the task, it allows variability where it does not matter and corrects it where it does.

This page is part of [Motor Control and the Cerebellum](../index.md). The parent page gives the overview; this page covers the method, its equations and the evidence for it.

## Overview

A reaching movement can be completed in many ways. The hand can follow many paths, and the joint angles that place it on a target are not unique, since the arm has more joints than the task strictly needs. Yet the variability in human movements is not spread evenly. Some directions vary a great deal across repetitions, and others are tightly corrected. A simple idea is that the brain treats each movement as a control problem and solves it optimally.

Todorov and Jordan's proposal is that the motor system chooses feedback control laws, rules that map the current state to a command, and that these laws minimise a cost. Because the cost is defined by the task, the same framework explains both the variability that is tolerated and the corrections that are made. It is a major part of the wider theory summarised in [Motor Control and the Cerebellum](../index.md).

## Key concepts

- **State and command**: the state describes the body and task, for example the position and velocity of the hand. The command is the control signal sent to the muscles.
- **Cost function**: a function that scores each movement, penalising deviation from the goal and the effort spent. The optimal controller is the one with the lowest expected cost.
- **Feedback control**: commands that depend on the current state, so that deviations are corrected as they occur, not planned open-loop in advance.
- **Minimal intervention principle**: the idea that the controller only corrects deviations that affect the task outcome. Variability in task-irrelevant dimensions is left alone.
- **Stochastic dynamics**: the body and sensors include noise, so the controller must account for uncertain future states.

## How it works

Consider a linear system with state $x_t$, command $u_t$ and motor noise $\xi_t$. The standard formulation used in much of this literature is

$$x_{t+1} = A x_t + B u_t + \xi_t, \qquad J = \mathbb{E}\Big[\sum_t \big(x_t^\top Q_t x_t + u_t^\top R u_t\big)\Big].$$

Here $J$ is the expected cost, with $Q_t$ penalising state deviations and $R$ penalising effort. For this linear–quadratic case, the optimal controller is a linear feedback law $u_t = -L_t x_t$, and the gain matrices $L_t$ come from a backward recursion over time. The recursion is the Riccati equation, and it is solved once for the whole movement.

The procedure can be written as four steps.

1. Specify the dynamics of the body and the sensory noise.
2. Specify a cost that penalises errors relevant to the task and the effort of the command.
3. Compute the feedback gains $L_t$ by working backwards from the end of the movement.
4. Apply the feedback law. Each deviation is corrected in proportion to its cost, so the controller acts on task-relevant errors and not on the rest.

The key consequence is the minimal intervention principle. If the task only constrains the final position of the hand, then deviations along the path are not corrected, and the variability is allowed to accumulate. Deviations that would change the final position tend to be corrected quickly.

## Results

The paper's evidence is a set of simulations and comparisons with observed human movements. The authors use the framework to account for how variability and correction are distributed across the task, and the claim here is qualitative. The numerical comparisons are in the paper and are not quoted on this page.

The paper's main contribution is conceptual. It shows that one principle, optimal feedback control with a task-specific cost, can account for features of coordination that simpler accounts treat separately.

## Limitations

- The framework depends on the choice of cost function. The cost is a modelling decision, and different costs can fit the same data, so the theory is hard to falsify on behaviour alone.
- The linear–quadratic case is a simplification. Real arms are nonlinear, and real sensors are delayed, which the basic formulation does not include.
- The framework says what the controller should do, not how the nervous system computes the gains. The neural implementation is a separate question.
- Optimality is assumed rather than always tested. Some movements may follow heuristics that only approximate the optimum.

## Open questions

- **What cost does the brain minimise?** Effort, accuracy, time and energy are all candidates, and the weighting among them is an empirical question. Scott (2004) reviews the framework for volitional movement.
- **Does the nervous system compute the feedback gains?** The framework is compatible with several neural mechanisms, and separating them needs recordings or perturbations during movement.
- **How do optimal feedback control and learning fit together?** The controller is assumed to be known. How it is learned, and how it adapts to changes in the body, is addressed in the review by Shadmehr, Smith and Krakauer (2010).
- **Does the framework extend to richer tasks?** Its applications to tasks with complex dynamics or long-horizon planning are less developed, and the link to model-based control is an open area.

## References

### Seminal papers

- Todorov, E. & Jordan, M. I. (2002). Optimal feedback control as a theory of motor coordination. *Nature Neuroscience*. https://doi.org/10.1038/nn963 — Argues that coordinated movement follows from feedback control that minimises a task-specific cost.
- Todorov, E. (2004). Optimality principles in sensorimotor control. *Nature Neuroscience*. https://doi.org/10.1038/nn1309 — A later review of optimality principles in sensorimotor control.
- Wolpert, D. M. & Ghahramani, Z. (2000). Computational principles of movement neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/81497 — A short review of computational principles for movement, including optimal control and internal models.

### Surveys and textbooks

- Scott, S. H. (2004). Optimal feedback control and the neural basis of volitional motor control. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn1427 — Reviews the optimal feedback control framework and its neural interpretation for volitional movement.
- Shadmehr, R., Smith, M. A. & Krakauer, J. W. (2010). Error correction, sensory prediction, and adaptation in motor control. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-060909-153135 — Reviews how the brain uses noisy, delayed feedback, forward models and adaptation to control movement.
- Wolpert, D. M., Miall, R. C. & Kawato, M. (1998). Internal models in the cerebellum. *Trends in Cognitive Sciences*. https://doi.org/10.1016/S1364-6613(98)01221-2 — Reviews evidence that the cerebellum learns forward and inverse internal models, the predictive counterpart to feedback control.
