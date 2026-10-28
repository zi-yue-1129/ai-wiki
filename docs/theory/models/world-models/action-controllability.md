---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/world-models
tags:
  - world models
  - controllability
aliases:
  - 動作可控性
  - action controllability
---

# Action Controllability in World Models

A world model is useful for planning only if its predictions change when the agent's action changes. Many learned models fail this test. They predict plausible next frames while using the action input very little. This page describes that failure, the shortcuts behind it, and the remedies proposed in the recent literature. The family-level picture is on the [World Models & Embodied AI](index.md) page.

## Overview

An action-conditioned world model takes the current state and an action, and predicts the next state. Training on logged data rewards getting the next frame right. In video and robot data the next frame is usually close to the current one, so a model can reach low prediction error by copying the present state and paying little attention to the action. Its predictions then barely respond to what the agent does, and a planner that searches over actions has little signal for telling the options apart.

## Key concepts

- **Action-ignoring model**: a model whose predicted future changes little when the action changes.
- **Inverse dynamics**: predicting the action that caused a transition between two observations. LAPO uses an inverse model to infer latent actions from consecutive observations.
- **Shortcut**: a route to low training loss that bypasses the intended signal, for example copying the answer into the latent code.
- **Controllability**: how much the predicted future depends on the chosen action.

## How it works

The recent literature describes three mechanisms that let a model ignore actions, and one family of remedies that adds training targets.

1. **Copying through an inverse-dynamics head.** If the inverse model sees both the current and the next observation, it can encode the next observation itself into the "latent action". Schmidt and Jiang (2024) warn that without a bottleneck the inverse model "would likely result in the IDM learning to simply copy" the next observation. Their remedy is vector quantisation of the latent action, which limits how much information reaches the forward model. See [LAPO](lapo.md).
2. **Endpoint versus displacement decoding.** Zhang et al. (2026, preprint) argue that an inverse decoder reading concatenated endpoint embeddings is weaker than one that reconstructs the executed action from the latent displacement between consecutive observations. Their ablations state that "displacement-based action decoding is consistently more effective than endpoint concatenation." They also argue that supervising the displacement regularises the transition geometry, so adjacent embeddings cannot collapse without losing action information.
3. **Myopic controllability.** Rudolph et al. (2024) observe that inverse dynamics and mutual-information objectives capture controllability only for a limited number of timesteps. They propose action bisimulation, which extends single-step controllability with a recursive invariance constraint.

A different remedy adds a training target rather than changing the decoder. Shi et al. (2026, preprint) argue that "action control requires more than injecting action features", and that the model must stay consistent under counterfactual changes to actions and observations. Their CoCo framework applies this across multi-step rollouts, which reference, inverse-action and zero-action rollouts constrain, so that the model cannot rely on statistical shortcuts that work without any action effect.

For contrast, [DINO-WM](dino-wm.md) takes the action through a simple path. Its predictor concatenates an embedding of the action to every patch vector of frozen DINOv2 features, and its only training objective is latent prediction. It has no explicit controllability term.

## Key methods

### LAPO (Schmidt & Jiang, 2024)

- **Problem:** learn action-relevant latents from video that has no action labels, without the inverse model simply copying the next observation.
- **Core idea:** a vector-quantised bottleneck on the latent action, between an inverse model and a forward model.
- **Equation or algorithm:** the inverse and forward models are trained jointly to minimise next-state error, with quantisation applied to the latent before the forward model. Details are on the [LAPO](lapo.md) page.
- **Results:** on Procgen, LAPO exceeds the expert in 9 of 16 tasks within 4M frames (Section 6.1 of the paper).
- **Limitations:** the bottleneck trades information against blocking the copying shortcut, and it does not guarantee that the latent matches the real action. The latent still needs a small labelled decoder.

### Action bisimulation (Rudolph et al., 2024)

- **Problem:** single-step inverse dynamics captures only the controllability that shows up within a short horizon.
- **Core idea:** an action-bisimulation encoding inspired by bisimulation metrics. It extends single-step controllability with a recursive invariance constraint.
- **Equation or algorithm:** the constraint is recursive over time. The exact formulation is in the paper.
- **Results:** this page quotes no numerical results for this paper; the abstract makes qualitative claims only.
- **Limitations:** this page has checked only the abstract's qualitative claims, not the paper's experiments. The horizon constraint is the paper's focus, so the longer-horizon benefit should be read from its experiments.

### DINO-WM (Zhou et al., 2025)

- **Problem:** task-agnostic planning with a world model built on pre-trained visual features.
- **Core idea:** an action-conditioned predictor on frozen DINOv2 patch features, with goal features used as prediction targets.
- **Equation or algorithm:** an action encoder maps each action into a vector that is concatenated to every patch vector before prediction. Planning uses model predictive control with the cross-entropy method (CEM). The only training loss described is the latent prediction loss.
- **Results:** the paper reports zero-shot behavioural solutions at test time on six environments.
- **Limitations:** the method adds no controllability objective, so any dependence on the action comes only from the latent prediction loss.

### Delta-JEPA (Zhang et al., 2026, preprint)

- **Problem:** an action decoder that reads endpoint embeddings may not capture the action well, so the question is which signal the decoder should read.
- **Core idea:** decode the executed action from the latent displacement between consecutive observations (the abstract calls the method LDAD).
- **Equation or algorithm:** an inverse decoder over latent displacements, with displacement-level supervision. The exact losses are in the paper.
- **Results:** across four visual continuous-control tasks, the abstract reports that the method improves planning over JEPA-based and representation-learning world-model baselines. The abstract gives no numbers.
- **Limitations:** preprint, not peer reviewed. The evidence in the abstract is limited to four tasks.

### CoCo (Shi et al., 2026, preprint)

- **Problem:** action-conditioned world models can fit the data by exploiting statistical biases without making the visible dynamics depend on the action.
- **Core idea:** a counterfactual consistency framework with multi-step constraints on reference, inverse-action and zero-action rollouts.
- **Equation or algorithm:** consistency constraints on counterfactual rollouts, added to the training objective. The exact formulation is in the paper.
- **Results:** the abstract reports an ARC_inv of 0.412 and an ARC_ref of 0.483 on Mini-SSMB, and a 17.07% reduction in DE relative to the baseline on the same benchmark. On VP2 visual planning, it reports the highest average success rate among the state-of-the-art models compared, at 73.1%. The abstract names four benchmarks: Mini-SSMB, VP2, BAIR and RoboNet.
- **Limitations:** preprint, not peer reviewed. The abstract does not give the training cost of the multi-step consistency terms.

## Connections

Planning with a learned model is covered in [model-based reinforcement learning](../../paradigms/reinforcement-learning/model-based-rl/index.md). A controllability failure there shows up as a planner that cannot tell apart actions with different consequences.

LAPO connects to imitation learning, where latent actions can serve as the output space of a policy; see [behavioural cloning](../../paradigms/imitation/behavioural-cloning/index.md).

## Applications

Controllable world models are needed wherever an agent plans with a learned simulator, for example robot manipulation and navigation from video or logged trajectories.

## Open questions

- Do controllability tests that swap actions measure what planning actually needs?
- Do decoders that read displacements, rather than endpoint embeddings, change the quality of predicted frames?
- How much multi-step consistency training costs compared with its gain in planning success?

## References

### Seminal papers

- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024 (spotlight). https://arxiv.org/abs/2312.10812 — Introduces LAPO, which recovers latent actions from action-free video and uses a vector-quantised bottleneck to stop the inverse model from copying the next observation.
- Rudolph, M., Chuck, C., Black, K., Lvovsky, M., Niekum, S. & Zhang, A. (2024). *Learning Action-based Representations Using Invariance*. Reinforcement Learning Journal, vol. 1 (presented at RLC 2024). https://rlj.cs.umass.edu/2024/papers/Paper39.html — Analyses how single-step inverse dynamics captures controllability and proposes action bisimulation for longer horizons.
- Zhou, G., Pan, H., LeCun, Y. & Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025 (PMLR 267). https://proceedings.mlr.press/v267/zhou25t.html — Action-conditioned predictor on frozen DINOv2 patch features, used for planning.

### Articles and preprints

- Zhang, Z. et al. (2026). *Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding*. arXiv preprint 2606.31232. https://arxiv.org/abs/2606.31232 — Decodes actions from latent displacement rather than endpoint concatenation. Preprint, not peer reviewed.
- Shi, Y. et al. (2026). *Overcoming Statistical Bias in Action-Controllable World Models*. arXiv preprint 2608.04653. https://arxiv.org/abs/2608.04653 — Proposes CoCo, counterfactual consistency regularisation for action-controllable world models. Preprint, not peer reviewed.
