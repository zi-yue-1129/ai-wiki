---
status: draft
last_reviewed: 2026-10-28
tags:
  - language
  - large language models
  - transfer learning
aliases:
  - SimpleTOD
  - 簡單任務導向對話語言模型
  - Hosseini-Asl et al. 2020
---

# SimpleTOD (Hosseini-Asl et al. 2020)

SimpleTOD (Hosseini-Asl et al., 2020) handles a whole task-oriented dialogue turn with one pretrained causal language model. The model writes the dialogue state, the system action and the reply as one text sequence, instead of passing the turn through separate modules. It is a landmark end-to-end method in [customer service and conversational systems](../index.md).

## Overview

A modular task-oriented system has four modules: understanding the user, tracking the dialogue state, choosing an action and generating the reply. Each module has its own model, labels and training data, and an error in one module reaches the next. The authors observed that this decomposition does not require a dedicated model for each part. A single model trained on all the sub-tasks, recast as one sequence prediction problem, can perform better.

The model inherits what a pretrained language model has learned from general text, since it starts from an open-domain causal model.

## Key concepts

- **Belief state**: the slot-value pairs the system believes the user wants, for example a hotel area and a price range.
- **Dialogue action**: the communicative act the system chooses for the turn, such as asking for a missing slot or informing the user of a result.
- **Causal language model**: a model that predicts each token from the tokens before it only.
- **Sequence recasting**: writing structured outputs as text with delimiter tokens, so that one model can generate all of them.
- **Joint goal accuracy**: the share of turns whose predicted belief state matches the annotated one exactly.
- **Combined score**: a MultiWOZ end-to-end measure that averages the inform and success rates and adds the response's BLEU score.

## How it works

Each training turn is serialised into one flat string. It holds the dialogue history, then the belief state, then the result of a database lookup, then the action and the response, separated by special tokens. The model is trained with the usual next-token cross-entropy over the sequence:

$$
\mathcal{L}(\theta) = -\sum_{i} \log p_\theta(x_i \mid x_{<i})
$$

Here $x_i$ is the $i$-th token and $x_{<i}$ the tokens before it. At inference the model reads the history and generates, in order, the belief state, the database query, the action and the response. The lookup uses the generated belief state, and its result is placed in the sequence so that the action and reply can condition on it.

The procedure is:

1. Start from a pretrained open-domain causal language model.
2. Serialise each dialogue turn into a sequence with delimiter tokens.
3. Fine-tune with the next-token loss, so the model learns to generate each part conditioned on the parts before it.
4. At inference, generate the belief state, query the database with it, and generate the action and the response.

## Results

On the MultiWOZ benchmark, the abstract reports that SimpleTOD improves over the prior state of the art in joint goal accuracy for dialogue state tracking. In the end-to-end setting it improves the inform rate by 8.1 points, the success rate by 9.7 points and the combined score by 7.2 points.[^1] The authors also report robustness to noisy annotations.

These are benchmark results, not evidence from live business systems.

## Limitations

- **Benchmark dependence.** The results rely on MultiWOZ, whose annotations contain noise. The authors analyse robustness to that noise, but a score on one corpus still says little about other domains.
- **Fixed database view.** The database is a snapshot passed in as text, and the model itself takes no action that changes it, such as cancelling a booking.
- **Context length.** The sequence grows with every turn, which makes long conversations expensive.
- **Unsupported replies.** Nothing forces the generated reply to agree with the database result it was given. A fluent reply can still contradict the data.

## Open questions

- **Many services.** Whether a single sequence model keeps its advantage as the number of services and schemas grows is open. The Schema-Guided Dialogue dataset was built to test that setting (Rastogi et al., 2019).
- **Live tools.** Benchmarks with live tools and state changes test a different skill. Whether the sequence approach extends to them is not settled (Yao et al., 2024).
- **Evaluation.** Hudeček and Dušek (2023) found instruction-tuned language models weaker than specialised ones at belief tracking, so a benchmark score must be read with the task it measures.

[^1]: Hosseini-Asl et al. (2020), abstract: inform rate up 8.1 points, success rate up 9.7 points and combined score up 7.2 points in the end-to-end setting on MultiWOZ. https://arxiv.org/abs/2005.00796

## References

### Seminal papers

- Hosseini-Asl, E. et al. (2020). A Simple Language Model for Task-Oriented Dialogue. https://arxiv.org/abs/2005.00796 — Recasts understanding, state tracking, action and response as one sequence for a causal language model, with state-of-the-art results on MultiWOZ.
- Budzianowski, P. et al. (2018). MultiWOZ -- A Large-Scale Multi-Domain Wizard-of-Oz Dataset for Task-Oriented Dialogue Modelling. https://arxiv.org/abs/1810.00278 — Crowd-sourced corpus of about 10,000 multi-domain dialogues with belief-state labels, the benchmark on which SimpleTOD is evaluated.
- Rastogi, A. et al. (2019). Towards Scalable Multi-domain Conversational Agents: The Schema-Guided Dialogue Dataset. https://arxiv.org/abs/1909.05855 — Dataset of many services with overlapping functions and little training data, designed to test scalable dialogue systems.

### Surveys and textbooks

- Zhang, Z. et al. (2020). Recent Advances and Challenges in Task-oriented Dialog System. https://arxiv.org/abs/2003.07490 — Survey of task-oriented dialogue research, including dialogue-policy learning, ontology use and evaluation.

### Articles and documentation

- Hudeček, V. & Dušek, O. (2023). Are LLMs All You Need for Task-Oriented Dialogue? https://arxiv.org/abs/2304.06556 — Tests instruction-tuned language models on task-oriented benchmarks, finding weaker belief tracking but good task completion given correct slot values.
- Yao, S. et al. (2024). τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains. https://arxiv.org/abs/2406.12045 — Simulated-customer benchmark in which agents call live domain tools and are graded by database state.
