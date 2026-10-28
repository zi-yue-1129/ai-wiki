---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
tags:
  - world models
  - self-supervised
  - robotics
aliases:
  - V-JEPA 2
  - V-JEPA 2-AC
---

# V-JEPA 2

V-JEPA 2 is a self-supervised video model that predicts masked content in representation space rather than in pixels. The paper extends it into a world model, V-JEPA 2-AC, by post-training an action-conditioned predictor on a small amount of unlabelled robot video. The authors then use that predictor to plan robot motions toward image goals.

## Overview

Assran et al. (2025) take the video encoder trained on large amounts of internet video and add a predictor that knows what the robot does. The encoder stays frozen during robot training. Only a predictor of about 300M parameters is trained, on roughly 62 hours of robot video from the DROID dataset. The authors then deploy the model zero-shot on Franka arms in two labs, using image goals and no task-specific training or rewards. The same paper also reports video understanding and question-answering results, which are outside the scope of this page.

## Key concepts

- **Joint-embedding predictive architecture (JEPA)**: a model that predicts the representation of hidden parts of its input, not their raw pixels.
- **Mask denoising in representation space**: the encoder sees the visible patches, and the predictor fills in the representations of the masked patches.
- **EMA target encoder**: the prediction target comes from an exponential moving average of the encoder weights, with stop-gradient, which the paper uses to avoid representation collapse.
- **Action-conditioned predictor**: a predictor that takes the robot's end-effector change as input and predicts the next representation.
- **Planning with CEM and MPC**: candidate action sequences are sampled, scored by distance to a goal representation, and the best ones refine the sampling distribution. Only the first action is executed before replanning.

## How it works

1. Pre-train a video encoder on a large mixture of video and images. The paper's data mix, VideoMix22M, has about 22 million samples, and the abstract describes the pretraining as covering over one million hours of video. The encoder is a ViT-g with up to one billion parameters.
2. Freeze the encoder and post-train the action-conditioned predictor on robot clips. Each action is the 7-dimensional change in end-effector state between adjacent frames, and each state is a 7-dimensional vector relative to the robot base.
3. At control time, sample candidate action sequences, predict their outcomes in representation space, and score each predicted end state by its distance to the goal image's representation. Keep the best candidates, update the sampling distribution, and execute only the first action before replanning.

## Key methods

### V-JEPA 2 (Assran et al., 2025)

- **Problem:** Video models learn appearance and motion well, but a model that only predicts video cannot tell a robot what its own actions will do. The paper asks whether a representation learned without labels can be turned into an action-conditioned predictor with little robot data, and whether it can drive planning on a real arm.
- **Core idea:** Pre-train the video encoder with masked prediction in representation space. Then keep the encoder fixed and post-train an action predictor on a small amount of robot video, with the executed motions as inputs. Use that predictor in a model predictive control loop that searches for actions reaching an image goal.
- **Equation or algorithm:** In the pretraining stage, the predictor and encoder are trained to minimise an L1 distance between the predictions for masked patches and the target representations from the EMA encoder. In schematic form:

\[
\min \big\lVert P_\phi\big(\Delta_y, E_\theta(x)\big) - \mathrm{sg}\big(\bar E(y)\big) \big\rVert_1
\]

  For V-JEPA 2-AC the encoder is frozen and the predictor is trained with two losses. A teacher-forcing loss averages the L1 error of one-step predictions over a window of T = 15 steps. A two-step rollout loss compares the predicted representation after two steps of self-generated predictions with the true one. The total is their sum. Planning uses CEM with model predictive control, with the L1 distance between the predicted final representation and the goal representation as the cost. Sampled actions are kept inside an L1 ball of radius 0.075. For pick-and-place, the controller first optimises toward an intermediate sub-goal for 4 steps, then a second sub-goal for 10 steps, then the final goal for 4 steps.

- **Results:** On the robot experiments, the paper reports success out of 10 trials per task, averaged over two labs:

| Method | Reach | Grasp Cup | Grasp Box | Reach w/ Obj Cup | Reach w/ Obj Box | Pick-and-Place Cup | Pick-and-Place Box |
|---|---|---|---|---|---|---|---|
| Octo (average) | 100% | 15% | 0% | 15% | 70% | 15% | 10% |
| V-JEPA 2-AC (average) | 100% | 65% | 25% | 75% | 75% | 80% | 65% |

  V-JEPA 2-AC matches Octo on Reach and is higher on every other task in this table. The Cosmos comparison, run on Lab 2 only, reports 80% on Reach and 0% on Grasp Cup and Pick-and-Place Cup. The paper reports about 16 seconds of planning per action for V-JEPA 2-AC on a single GPU with 800 samples and 10 iterations, and about 4 minutes for Cosmos with 80 samples. The abstract also reports video-understanding results, such as 77.3 top-1 accuracy on Something-Something v2 and 39.7 recall-at-5 on Epic-Kitchens-100 action anticipation. These are not robot results.

- **Limitations:** The model has no explicit camera calibration, and the robot base is often out of view, so action axes must be inferred implicitly. Autoregressive error builds up over long rollouts, and the search space grows quickly with the horizon. Goals must be images, and language goals are left to future work. The paper's predictions reach about 16 seconds ahead. Scaling is studied only up to one billion encoder parameters. Action anticipation does not fully solve the EK100 benchmark, and accuracy drops at longer horizons.

## Connections

[DINO-WM](dino-wm.md) is the closest comparison. It trains its predictor on the target environment's own trajectories with a frozen image encoder, whereas V-JEPA 2 starts from a general video encoder and adds robot video only in post-training. [Genie](genie.md) generates interactive video in pixel space, while V-JEPA 2 predicts in representation space and uses the predictor for planning. V-JEPA 2 also raises the question studied in [action controllability](action-controllability.md): whether the predictor depends on the action it is given. The joint-embedding predictive idea comes from the [self-supervised](../../paradigms/self-supervised/index.md) line of work. The wider family is described on the [parent overview](index.md).

## Open questions

- How much robot data a new embodiment needs, and whether the 62-hour figure is a practical lower bound.
- Whether planning in representation space keeps the fine spatial detail that precise grasping needs. Grasp Box is the weakest task for V-JEPA 2-AC, at 25% on average.
- Whether the results hold for camera positions and tasks outside the two labs in the paper.

## References

### Seminal papers

- Assran, M., Bardes, A., Fan, D. et al. (2025). *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning*. arXiv:2506.09985. https://arxiv.org/abs/2506.09985 — Introduces V-JEPA 2 and its action-conditioned variant V-JEPA 2-AC, post-trained on robot video for zero-shot planning.
- Assran, M. et al. (2023). *Self-Supervised Learning From Images With a Joint-Embedding Predictive Architecture*. CVPR 2023. https://openaccess.thecvf.com/content/CVPR2023/html/Assran_Self-Supervised_Learning_From_Images_With_a_Joint-Embedding_Predictive_Architecture_CVPR_2023_paper.html — The image version of the joint-embedding predictive approach that V-JEPA 2 extends to video.
- Zhou, G., Pan, H., LeCun, Y. & Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025, PMLR 267. https://proceedings.mlr.press/v267/zhou25t.html — A predictor on frozen image features and the main comparison point for planning from pretrained features.
- Bruce, J. et al. (2024). *Genie: Generative Interactive Environments*. ICML 2024, PMLR 235, pp. 4603–4623. https://proceedings.mlr.press/v235/bruce24a.html — The generative counterpart: a latent action model trained on unlabelled video.
- Schmidt, D. & Jiang, M. (2023). *Learning to Act without Actions*. arXiv:2312.10812. https://arxiv.org/abs/2312.10812 — Learns latent actions from action-free video, the action-learning counterpart to predictors trained on robot video. The paper was presented as an ICLR 2024 spotlight.

### Surveys and textbooks

- Moerland, T. M. et al. (2020). *Model-based Reinforcement Learning: A Survey*. arXiv:2006.16712. https://arxiv.org/abs/2006.16712 — Survey of learned dynamics models and their use in planning and control.
