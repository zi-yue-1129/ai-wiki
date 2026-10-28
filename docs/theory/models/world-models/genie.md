---
status: draft
last_reviewed: 2026-10-28
tags:
  - world models
  - video generation
  - latent actions
aliases:
  - Genie
  - 生成式互動環境
---

# Genie

Genie is a generative model that turns a single image or prompt into an interactive, playable environment. Its distinctive feature is that it learns the controls itself. A latent action model finds a small set of discrete actions from unlabelled internet video, so no action labels are needed to make the generated world respond to input.

## Problem

Video generators produce plausible clips, but the viewer cannot act in them. Training a controllable simulator usually needs logged actions, and most internet video has none. Genie asks whether the actions behind a video can be inferred from the frames alone, and whether the inferred actions give frame-by-frame control of a generated world.

## Core idea

Genie has three learned parts: a video tokenizer, a dynamics model that predicts the next frame's tokens, and a latent action model. The latent action model is trained without action labels. It reads frames and chooses a latent action at each step, and the dynamics model uses that latent action to predict the next frame. The authors describe the latent actions as enabling frame-by-frame controllability of generated environments, without action labels.

## How it works

1. Tokenise each video frame with a learned video tokenizer.
2. Train a latent action model on unlabelled video, inferring a discrete latent action between consecutive frames.
3. Train a dynamics model that predicts the next frame's tokens from past tokens and the latent action.
4. At play time, the user's input chooses among the learned latent actions, and the dynamics model generates the next frame.

## Key methods

- Versus [LAPO](lapo.md), which learns latent actions in order to train policies and inverse models from video, Genie focuses on generating an interactive world and makes the latent action the control interface.
- Versus [V-JEPA 2](v-jepa-2.md), which predicts in representation space for planning, Genie generates pixels that a user can play with.

## Results

The abstract states that the latent action space learned without labels allows frame-by-frame control of generated environments, and that the learned actions can be used to train agents that imitate behaviours from unseen videos. Quantitative results are in the paper.

## Limitations

- The latent actions are discrete and are not guaranteed to match the meaning of real controller inputs. A latent action may combine several effects.
- Generated worlds are only as consistent as the dynamics model's memory of earlier frames. Long-horizon consistency is a limit the paper treats as open.

## Connections

Genie belongs to the video branch of world models on the [parent overview](index.md), where it appears as "video generation as world simulation". Its latent action model shares the bottleneck idea behind [LAPO](lapo.md), discussed in [action controllability](action-controllability.md). Games are a natural application area; see [games](../../../applications/games/index.md).

## Applications

Interactive generated environments, training data for embodied agents, and research tools for studying how an agent's actions are represented.

## Open questions

- Whether latent actions learned from game video transfer to robots with different controls.
- How to keep a generated world consistent over long sessions.

## References

### Seminal papers

- Bruce, J., Dennis, M., Edwards, A. et al. (2024). *Genie: Generative Interactive Environments*. ICML 2024. https://proceedings.mlr.press/v235/bruce24a.html — Introduces Genie, a generative model that learns a latent action space from unlabelled video and provides frame-by-frame control of generated environments. The arXiv version is at https://arxiv.org/abs/2402.15391.

### Articles and preprints

- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024 (spotlight). https://arxiv.org/abs/2312.10812 — Learns latent actions from action-free video with a quantised bottleneck, a closely related approach.
- Yang, S. et al. (2023). *Learning Interactive Real-World Simulators*. arXiv preprint. https://arxiv.org/abs/2310.06114 — A video-based simulator that responds to actions, trained on combined image, robotics and navigation data.
- Micheli, V., Alonso, E. & Fleuret, F. (2022). *Transformers are Sample-Efficient World Models*. arXiv preprint. https://arxiv.org/abs/2209.00588 — IRIS, a world model built from a discrete autoencoder and an autoregressive Transformer, the same tokenise-then-predict pattern Genie uses.
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv preprint. https://arxiv.org/abs/1803.10122 — Early latent world model: features come from a world model trained without supervision, and a compact policy can be trained inside the model's own simulated environment before transfer.
