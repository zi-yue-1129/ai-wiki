---
status: draft
last_reviewed: 2026-10-28
tags:
- agents
- evaluation
- benchmarks
aliases:
- τ-bench
- tau-bench
- 工具代理人與使用者互動
- pass^k
---

# τ-bench: Tool-Agent-User Interaction in Real-World Domains

τ-bench (Yao et al., 2024) evaluates an agent that converses with a simulated user, calls domain tools and must follow written policy. It introduced pass^k, a measure of how consistently an agent succeeds across repeated trials. It is one of three landmark methods on the [Agent Evaluation](../index.md) page.

## Overview

Many agent benchmarks give the agent one instruction and judge the answer it returns. Real service work, such as changing a booking or processing a return, is different. The user reveals needs gradually, and rules limit what the agent may do. The authors argue that existing benchmarks test neither interaction with users nor adherence to domain rules, both of which matter for deployment (Yao et al., 2024).

τ-bench gives the agent API tools for a domain, a policy document and a language model that plays a customer with a goal. It covers two domains, retail and airline.

## Key concepts

- **Simulated user**: a language model prompted with an instruction and a persona. It talks to the agent and reveals information as the conversation proceeds.
- **Domain tools**: APIs that read and write a database, such as looking up an order or cancelling a reservation.
- **Policy**: written rules the agent must follow, such as the conditions under which a refund is allowed.
- **Annotated goal state**: the database state expected when the task has been handled correctly.
- **Pass^k**: the probability that all k independent attempts at a task succeed. Averaged over tasks, it measures reliability, which pass@k does not capture.

## How it works

1. Load a database snapshot and a task that specifies the user's goal.
2. The simulated user opens the conversation. The agent replies, may call tools, and the user answers.
3. The episode ends when either party stops or a turn limit is reached.
4. The grader compares the final database state with the annotated goal state. The paper's evaluation compares state rather than text, so a correct outcome phrased differently still counts.
5. Each task is run several times, and pass^k is computed from the outcomes.

Comparing state avoids the need to match the agent's wording, but it requires that the database and goal state be modelled carefully for every task.

## Results

The paper's abstract reports that state-of-the-art function-calling agents, including gpt-4o, succeed on fewer than half of the tasks. They are also inconsistent: pass^8 is below 25 percent in the retail domain (Yao et al., 2024). The finding is less about one model than about the gap between a single successful run and repeated reliable behaviour, which a single-run score hides.

## Limitations

- **Simulated users.** The customer is a language model, so its behaviour may differ from that of real people, and its difficulty is hard to calibrate.
- **Grader flaws.** Zhu et al. (2025) report that τ-bench counted empty responses as successful, so some reported scores were too high.[^1]
- **Passive user.** In the original design the user only supplies information and never acts on the shared environment, which real support tasks often require. The follow-up benchmark addresses this (Barres et al., 2025).
- **Two domains.** Results in retail and airline say little about other services with different policies.

## Open questions

- **User fidelity.** Whether simulated users can be validated against recorded human conversations is still open.
- **Choice of k.** pass^k is informative but costly, since each extra trial multiplies model calls. How many trials are needed for a deployment decision is unclear.
- **Process versus outcome.** The benchmark grades the final state. Whether a policy was followed on the way, which matters for safety, is not measured directly.

## References

### Seminal papers

- Yao, S. et al. (2024). *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*. arXiv. https://arxiv.org/abs/2406.12045 — Simulated-user benchmark with domain tools and policies, graded by database state, which introduces pass^k.
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces the repeated-sampling measure that pass@k generalises and contrasts with pass^k.
- Barres, V. et al. (2025). *τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment*. arXiv. https://arxiv.org/abs/2506.07982 — Extends τ-bench to a dual-control setting in which the user also acts on a shared environment.

### Surveys and textbooks

- Yehudai, A. et al. (2025). *Survey on Evaluation of LLM-based Agents*. arXiv. https://arxiv.org/abs/2503.16416 — Survey of agent evaluation, including conversational and tool-using benchmarks.

### Articles and documentation

- Zhu, Y. et al. (2025). *Establishing Best Practices for Building Rigorous Agentic Benchmarks*. arXiv. https://arxiv.org/abs/2507.02825 — Identifies grading flaws in several agent benchmarks, including the empty-response issue in τ-bench.
- Kapoor, S. et al. (2024). *AI Agents That Matter*. arXiv. https://arxiv.org/abs/2407.01502 — Critique of agent benchmarking that argues for reporting cost with accuracy and for holdout sets.

[^1]: Zhu et al. (2025), abstract, https://arxiv.org/abs/2507.02825 — States that τ-bench counts empty responses as successful, one of the grading problems the checklist addresses.
