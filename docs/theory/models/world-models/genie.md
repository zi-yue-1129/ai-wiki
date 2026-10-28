---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/games
tags:
  - world models
  - video generation
  - latent actions
aliases:
  - Genie
  - 生成式互動環境
---

# Genie

Genie is a generative model that turns a single image, sketch or text prompt into an interactive, playable environment. Its distinctive feature is that it learns the controls itself. A latent action model finds a small set of discrete actions from unlabelled internet video, so no action labels are needed to make the generated world respond to input.

## Problem

Video generators produce plausible clips, but the viewer cannot act in them. Training a controllable simulator usually needs logged actions, and most internet video has none. Genie asks whether the actions behind a video can be inferred from the frames alone, and whether the inferred actions give frame-by-frame control of a generated world.

## Overview

The paper calls Genie a foundation world model with 11B parameters, trained on unlabelled internet videos. The abstract states that it can generate varied, action-controllable virtual worlds from text, synthetic images, photographs and sketches. It is the first generative interactive environment trained without labels, in the paper's framing.

## Key concepts

- **Video tokenizer**: a learned spatiotemporal model that turns each frame sequence into discrete tokens and back into pixels.
- **Dynamics model**: an autoregressive model that predicts the tokens of the next frame from past tokens and an action.
- **Latent action model**: a model trained without labels that infers a discrete action between consecutive frames. Its codebook has 8 entries.
- **Frame-by-frame control**: the user's input picks a latent action at each step, and the dynamics model generates the next frame.

## Core idea

Genie has three learned parts: a video tokenizer, a dynamics model that predicts the next frame's tokens, and a latent action model. The latent action model is trained without action labels. It reads frames and produces a latent action, and the dynamics model uses that latent action to predict the next frame. The authors describe the learned latent actions as enabling frame-by-frame controllability of generated environments, without action labels.

## How it works

1. Train the video tokenizer first. The paper uses it to turn video frames into tokens for the dynamics model.
2. Co-train the latent action model and the dynamics model in a second phase. The latent action model works directly on pixels: an encoder sees all previous frames and the next frame, and outputs a continuous latent action that is quantised into one of 8 discrete codes. A decoder takes the previous frames and the latent actions and predicts the next frame. The dynamics model is trained on video tokens.
3. At play time, the latent action model is discarded. The user's input chooses among the learned latent actions, and the dynamics model generates the next frame.

The training data is a curated set of platformer game videos. The paper's final dataset has 6.8M clips of 16 seconds each (about 30k hours). The clips are 160×90 pixels at 10 FPS.

## Key methods

### Genie: Generative Interactive Environments (Bruce et al., 2024)

- **Problem:** Video generators cannot be acted in, and training controllable simulators normally needs action labels that most internet video lacks. Can the controls be learned from unlabelled video, and used to act in generated worlds?
- **Core idea:** Learn a discrete latent action space from unlabelled video with a latent action model, then use those latent actions as the control interface of a generative dynamics model. Because the actions are discrete, the user has only 8 choices at each step.
- **Equation or algorithm:** the latent action model uses a vector quantisation step with 8 codes (\(|A| = 8\) in the paper). Total model size is 11B parameters: about 10.1B for the dynamics model, 200M for the video tokenizer and 300M for the latent action model. The tokenizer is a spatiotemporal transformer VQ-VAE with a codebook of 1024 entries and 32-dimensional latents. The model has a context of 16 frames, and the paper reports inference at around 1 FPS.
- **Results:** The abstract reports frame-by-frame control of generated environments and the use of the learned latent actions to train agents that imitate behaviour from unseen videos. In Table 2, the 2.5B model trained on Platformers with pixel input has an FVD of 40.1 (lower is better). The paper reports no FVD for the 11B model. In the imitation experiment on Procgen CoinRun, a latent-action policy adapted with as few as 200 expert samples matches an oracle behaviour-cloning agent that has ground-truth actions.
- **Limitations:** The latent actions are discrete and are not guaranteed to match the meaning of real controller inputs. The paper states that the model is limited to 16 frames of memory, so consistency beyond that window is not maintained. Inference is slow (around 1 FPS), and the training data comes from platformer games.

## Connections

Genie belongs to the video branch of world models on the [parent overview](index.md), where it appears as "video generation as world simulation". Its latent action model shares the bottleneck idea behind [LAPO](lapo.md), discussed in [action controllability](action-controllability.md). LAPO uses latent actions to train policies and inverse models from video, whereas Genie makes the latent action the control interface of a generated world. [V-JEPA 2](v-jepa-2.md) is covered on its own page and offers a useful contrast between predictive and generative approaches to world models. Games are a natural application area; see [games](../../../applications/games/index.md).

## Applications

Interactive generated environments from prompts, sketches and photographs; training data or demonstrations for embodied agents, shown in the CoinRun imitation experiment; and research on how an agent's actions can be represented from video.

## Open questions

- Whether latent actions learned from game video transfer to robots with different controls.
- How to keep a generated world consistent over long sessions, beyond the 16-frame memory the model has.

## References

### Seminal papers

- Bruce, J., Dennis, M., Edwards, A. et al. (2024). *Genie: Generative Interactive Environments*. ICML 2024. https://proceedings.mlr.press/v235/bruce24a.html — Introduces Genie, a generative model that learns a latent action space from unlabelled video and provides frame-by-frame control of generated environments. The arXiv version is at https://arxiv.org/abs/2402.15391.
- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024 (spotlight). https://arxiv.org/abs/2312.10812 — LAPO, which learns latent actions from action-free video with a vector-quantised bottleneck; a closely related approach.
- Micheli, V., Alonso, E. & Fleuret, F. (2023). *Transformers are Sample-Efficient World Models*. ICLR 2023. https://arxiv.org/abs/2209.00588 — IRIS, a world model built from a discrete autoencoder and an autoregressive Transformer, the same tokenise-then-predict pattern Genie uses.
- Yang, S., Du, Y., Ghasemipour, K., Tompson, J., Kaelbling, L., Schuurmans, D. & Abbeel, P. (2023). *Learning Interactive Real-World Simulators*. arXiv preprint. https://arxiv.org/abs/2310.06114 — A video-based simulator that responds to actions, trained on combined image, robotics and navigation data.
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv preprint. https://arxiv.org/abs/1803.10122 — Early latent world model in which a controller is trained inside the model's own simulated rollouts before transfer to the real environment.

### Surveys and textbooks

- Moerland, T. M., Broekens, J., Plaat, A. & Jonker, C. M. (2020). *Model-based Reinforcement Learning: A Survey*. arXiv preprint. https://arxiv.org/abs/2006.16712 — General survey of learned dynamics models and planning, useful background for the world-model framing.
