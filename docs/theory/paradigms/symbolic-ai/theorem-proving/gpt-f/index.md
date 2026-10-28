---
status: draft
last_reviewed: 2026-10-28
tags:
  - large language models
  - reasoning
  - benchmarks
aliases:
  - GPT-f
  - Tactic prediction
  - 策略預測
  - 語言模型定理證明
  - Generative language modeling for theorem proving
---

# GPT-f (Polu and Sutskever 2020)

GPT-f is a transformer language model that proposes proof steps for an automated prover, first for the Metamath formal language. It is an early landmark of learned tactic prediction: the model writes the next step, and a formal checker accepts or rejects it. It is one of the three landmark methods on the parent page [Automated Theorem Proving and Formal Mathematics](../index.md).

## Overview

Automated provers of the time relied largely on hand-designed search rules. Polu and Sutskever asked whether generation from a language model could address their weakness in producing new mathematical terms. They built GPT-f as a prover and proof assistant for Metamath.[^1] Its proofs entered the main Metamath library, which the authors reported as the first time a deep-learning system contributed proofs adopted by a formal community.

## Key concepts

- **Proof state**: the goal still to be proved, together with the hypotheses available for it.
- **Proof step (tactic)**: the next command that transforms a goal, such as a Metamath step or a Lean or Coq tactic.
- **Tactic prediction**: the learned task of generating a plausible next step from the current state.
- **Best-first search**: a search that expands the partial proof with the highest score first, so promising branches are explored before weak ones.
- **Verifier**: the formal system that accepts or rejects each generated step. The model can propose anything, but only verified steps remain.

## How it works

The model is trained on formal proofs, written as sequences of states and steps, so that it learns to predict the next step. At proof time, the prover runs a best-first search:

1. Place the goal on the frontier with score zero.
2. Remove the node with the highest score.
3. Ask the model for several candidate next steps from that node's proof state.
4. Send each candidate to the verifier, and discard the ones it rejects.
5. Add each accepted step as a child node. Its score is the parent's score plus the log-probability the model gave the step.
6. Stop when every goal is closed, or when the search budget runs out.

For a proof of $k$ steps $a_1, \dots, a_k$ that pass through states $x_0, \dots, x_{k-1}$, the score is

$$
s = \sum_{i=1}^{k} \log p_\theta(a_i \mid x_{i-1}),
$$

where $\theta$ denotes the model parameters. Summing log-probabilities favours proofs that the model finds plausible at every step. The exact search settings vary between experiments and are given in the paper.

## Results

- **Metamath.** GPT-f's accepted proofs are the main result, reported by Polu and Sutskever on the Metamath library.[^1]
- **miniF2F.** Zheng and colleagues introduced the miniF2F benchmark and reported GPT-f as its baseline, with its performance analysed in the paper.[^2] The numbers are in that paper and are not repeated here.
- **Later comparisons.** Lample and colleagues reported that GPT-f solved 56.5% of a held-out set of Metamath theorems, and that their search method reached 65.4% on the same set, rising to 82.6% with online training on unproved theorems.[^3]
- **Lean.** Han and colleagues reported that co-training tactic prediction with proof-artifact data raised the success rate on held-out Lean test theorems from 32% to 48%.[^4]

These figures come from different benchmarks, languages and training setups, so they are not directly comparable.

## Limitations

- **Dependence on data.** The model learns from human-written proofs in one library. Such libraries are small compared with ordinary text, a data-scarce regime that overfits easily.[^4]
- **Failed steps.** Many proposed steps are rejected, and search cost grows with the number of candidates.
- **Narrow guarantee.** A verified proof shows only that the formal statement holds, not that it captures the intended problem.

## Open questions

- **Transfer.** Do models trained on one library carry over to other libraries and to research mathematics?
- **Premise selection.** Tactic prediction and premise selection address different parts of the search.[^5] How best to combine them is open.
- **Human style.** Does a generated proof resemble a human one, or does it exploit library regularities a mathematician would avoid?

## Connections

GPT-f's pattern, in which a model proposes and a checker judges, resembles test-time search in [reasoning models](../../../../models/reasoning/index.md). Its successors add search inspired by AlphaZero.[^3] [AlphaProof](../../../../../applications/mathematics/alphaproof/index.md) applies reinforcement learning at olympiad scale.

## Applications

- **Proof assistance.** A model that proposes tactics can suggest steps to a person writing a proof in Lean or Coq, and the proof assistant checks each one. GPT-f's accepted Metamath proofs show that such results can enter a community library.[^1]
- **Benchmarking.** Formal benchmarks such as miniF2F allow automatic comparison of systems.[^2]

[^1]: Polu and Sutskever (2020), listed above.
[^2]: Zheng et al. (2021), listed above.
[^3]: Lample et al. (2022), listed above. The Metamath figures are as reported in the abstract.
[^4]: Han et al. (2021), listed above. The data-scarcity point is from its abstract.
[^5]: Alemi et al. (2016), cited on the parent page.

## References

### Seminal papers

- Polu, S. & Sutskever, I. (2020). *Generative Language Modeling for Automated Theorem Proving*. arXiv. https://arxiv.org/abs/2009.03393 — Introduces GPT-f, a transformer prover for Metamath whose proofs entered the main library.
- Zheng, K., Han, J. M. & Polu, S. (2021). *MiniF2F: a cross-system benchmark for formal Olympiad-level mathematics*. arXiv. https://arxiv.org/abs/2109.00110 — Presents the miniF2F benchmark and reports GPT-f as its baseline.
- Han, J. M. et al. (2021). *Proof Artifact Co-training for Theorem Proving with Language Models*. arXiv. https://arxiv.org/abs/2102.06203 — Improves Lean tactic prediction with self-supervised data taken from proof terms.
- Lample, G. et al. (2022). *HyperTree Proof Search for Neural Theorem Proving*. arXiv. https://arxiv.org/abs/2205.11491 — Compares a search method with GPT-f on Metamath and adds online training.

### Surveys and textbooks

- Yang, K. et al. (2024). *Formal Mathematical Reasoning: A New Frontier in AI*. arXiv. https://arxiv.org/abs/2412.16075 — A survey of formal theorem proving, covering learned tactic prediction and its open challenges.
