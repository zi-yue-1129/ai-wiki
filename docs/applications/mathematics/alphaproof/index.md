---
status: draft
last_reviewed: 2026-10-28
tags:
  - reasoning
  - reinforcement learning
aliases:
  - AlphaProof
  - 形式證明強化學習
  - Lean 證明代理人
---

# AlphaProof (Hubert et al. 2025)

AlphaProof is an agent that learns to write formal proofs in the Lean proof assistant, using reinforcement learning in the style of AlphaZero. It trains on many problems translated automatically into formal statements, and adapts during inference on the hardest ones. Hubert et al. reported the system in Nature in 2025. It is one of the three landmark methods described on the parent page [Mathematics and Formal Proof](../index.md).

## Overview

A proof checker accepts or rejects each step, which turns proof writing into a reinforcement-learning environment: an action is a proof step, and reward comes when the checker accepts the whole proof. Hubert et al. describe the formal language as an environment that grounds reasoning, so learning can come from experience rather than only human-written proofs.

The obstacle is data. Formal proofs are scarce compared with informal mathematics, and writing them by hand is slow. AlphaProof works around this by translating a large collection of natural-language problems into Lean statements with a language model, then keeping the translations it can use for training. The idea of learning from self-play with search comes from AlphaZero (Silver et al., 2018), which learned games without human examples.

## Key concepts

- **Proof states and tactics.** A Lean proof moves through states, each a goal with its hypotheses. A tactic transforms one state into another, and the checker confirms each transformation.
- **Auto-formalisation.** Translating a natural-language problem into a formal statement, which Wu et al. (2022) showed language models can partly do.
- **Tree search with learned guidance.** The agent explores possible tactics as a search tree, guided by learned estimates of which steps are promising, in the spirit of AlphaZero.
- **Test-time reinforcement learning.** For a hard problem, the agent generates many related variants of the problem and learns from them during inference, adapting to that problem before attempting it.

## How it works

The training and solving process has four stages:

1. **Build a problem set.** Translate natural-language problems into Lean statements with a language model, and keep the usable ones.
2. **Search for proofs.** For each statement, a tree search proposes tactics. The Lean checker accepts or rejects each one, and accepted states are expanded.
3. **Learn from outcomes.** Successful and failed attempts update the networks that guide the search.
4. **Adapt on hard problems.** For the most difficult problems, generate and learn from many variants of the problem at inference time (test-time reinforcement learning), then attempt the original again.

The output is a proof Lean has accepted; its correctness depends on the checker and the statement, not on the learned components.

## Results

At the 2024 International Mathematical Olympiad, AlphaProof solved three of the five non-geometry problems, including the hardest problem of the competition. Combined with AlphaGeometry 2 for the geometry problems, the system reached a score equivalent to a silver medallist. The authors report this as the first time an AI system achieved any medal-level performance at the IMO, to their knowledge.

## Limitations

- **Compute.** The IMO result used multi-day computation.
- **Translation risk.** A checked proof proves the formal statement. If the translation from the natural-language problem changed the meaning, the checker still accepts a proof of the wrong result.
- **Partial coverage.** Three of five non-geometry problems were solved, and geometry went to a separate system.
- **Readability.** Formal proofs are precise but long and hard for a human to read.

## Open questions

- Can test-time reinforcement learning work on research problems, where no informal solution is known and variants must be invented? Checking that formal statements match the intended problem is a further open issue.
- Which ingredients matter most? Ren et al. (2025) reach strong results with a different recipe that decomposes problems into subgoals and trains on the resulting cold-start data.

## Connections

- AlphaProof belongs to the formal strand of [Mathematics and Formal Proof](../index.md) and to the theory of [automated reasoning and theorem proving](../../../theory/symbolic-ai/index.md) in symbolic AI.
- Its training method belongs to the self-play family described on the [AlphaZero](../../../theory/paradigms/reinforcement-learning/mcts-and-self-play/alphazero/index.md) page, and its test-time adaptation links to [reasoning models](../../../theory/models/reasoning/index.md).

## Applications

AlphaProof is a research system described in the paper. Its ideas reach wider pipelines: Georgiev et al. (2025) combined an evolutionary coding agent with AlphaProof and other reasoning systems for automated proof generation.

## References

### Seminal papers

- Hubert, T. et al. (2025). *Olympiad-level formal mathematical reasoning with reinforcement learning*. Nature. https://doi.org/10.1038/s41586-025-09833-y — Introduces AlphaProof and reports its IMO 2024 result.
- Silver, D. et al. (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science. https://doi.org/10.1126/science.aar6404 — Introduces AlphaZero, learning games from self-play with tree search.
- de Moura, L. & Ullrich, S. (2021). *The Lean 4 Theorem Prover and Programming Language*. CADE-28, Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-030-79876-5_37 — Describes Lean 4, the proof assistant in which AlphaProof writes proofs.
- Wu, Y. et al. (2022). *Autoformalization with Large Language Models*. arXiv. https://arxiv.org/abs/2205.12615 — Shows language models translating competition problems into formal statements.

### Surveys and textbooks

- Yang, K. et al. (2024). *Formal Mathematical Reasoning: A New Frontier in AI*. arXiv. https://arxiv.org/abs/2412.16075 — Surveys formal theorem proving and the value of automatic checking.

### Articles and documentation

- Mathlib Community (2020). *The Lean Mathematical Library*. CPP 2020, ACM SIGPLAN. https://doi.org/10.1145/3372885.3373824 — Describes Mathlib, the library of formalised mathematics.
- Ren, Z. Z. et al. (2025). *DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition*. arXiv. https://arxiv.org/abs/2504.21801 — Open-weight Lean prover using subgoal decomposition, a different recipe.
- Georgiev, B. et al. (2025). *Mathematical exploration and discovery at scale*. arXiv. https://arxiv.org/abs/2511.02864 — Combines an evolutionary coding agent with AlphaProof for proof generation.
- Chervonyi, Y. et al. (2025). *Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2*. arXiv. https://arxiv.org/abs/2502.03544 — Describes AlphaGeometry 2, combined with AlphaProof at IMO 2024.
