---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/agents
  - theory/paradigms/evolutionary
tags:
  - agents
  - search
aliases:
  - Darwin Gödel Machine
  - DGM
  - 達爾文哥德爾機
  - 自我改進代理人
---

# Darwin Gödel Machine (Zhang et al. 2025)

The Darwin Gödel Machine (DGM) is a coding agent that modifies its own code, tests each change on benchmarks and keeps the changes that work in a growing archive. Jenny Zhang and colleagues reported it in 2025. It is the self-improvement method on the parent page [AI for AI Research](../index.md).

## Overview

The idea of a self-improving AI is old. Schmidhuber (2003) described a Gödel machine that rewrites any part of its own code once it has found a proof that the rewrite is useful. Zhang et al. (2025) point out that proving most changes beneficial is impossible in practice. The DGM replaces the proof with empirical validation: each change is judged by running coding benchmarks.

Its design draws on Darwinian evolution and open-endedness research. Instead of keeping only the best agent, it keeps a diverse archive, so that many different paths through the search space can be explored in parallel. Related work includes ADAS (Hu et al., 2024), which searches over agent designs written in code, and the evolutionary coding agent AlphaEvolve (Novikov et al., 2025). An earlier self-improving system, STOP (Zelikman et al., 2023), improved the code that calls a language model but did not change the model itself. [Evolutionary methods](../../../theory/paradigms/evolutionary/index.md) in general are the background for this search strategy.

## Key concepts

- **Gödel machine**: a theoretical self-improver that changes its code only when it can prove a change is beneficial.
- **Archive**: the stored set of agents produced so far. Each new agent is a child of an earlier one, so the archive grows as a tree.
- **Self-modification**: an agent edits its own code, which can include the tools it uses to make later edits.
- **Empirical validation**: a change is kept on the basis of its results on coding benchmarks, not on a proof.
- **Open-endedness**: the search favours diverse agents, not only the highest-scoring ones, so that dead ends can still lead somewhere.

## How it works

A simplified version of the loop is:

1. Start the archive with the initial coding agent.
2. Sample an agent from the archive. The sample is not restricted to the best agent.
3. Ask a foundation model to create a new version of the sampled agent by modifying its code. The reported changes include better code-editing tools, better management of long context and peer-review mechanisms.
4. Run the new agent on coding benchmarks such as SWE-bench and Polyglot.
5. Add the new agent to the archive if it runs and is scored, then repeat from step 2.

In symbols, with $A$ the archive, $M$ the foundation model and $\mathrm{eval}$ the benchmark score:

$$
p \sim A, \qquad c = M(p), \qquad A \leftarrow A \cup \{c\} \text{ if } c \text{ runs and } \mathrm{eval}(c) \text{ is defined}
$$

The rule for keeping a child is a simplification. The paper's selection of parents is more involved.

## Results

The abstract reports that the DGM raised SWE-bench performance from 20.0% to 50.0%, and Polyglot performance from 14.2% to 30.7%. It states that the DGM significantly outperforms baselines that have no self-improvement or no open-ended exploration. The improvements came from changes to the agent's code, such as better editing tools. All experiments were run with safety precautions, including sandboxing and human oversight.

## Limitations

- **Narrow domain.** The gains are measured on coding benchmarks, which is the task the agent is improving at. They do not show general self-improvement.
- **Benchmark overfitting.** Selecting changes on a benchmark can make the agent fit that benchmark. Results on held-out tasks matter more.
- **Many evaluations.** Each new agent must be run on benchmarks, so the method needs substantial computation.
- **Safety of self-modification.** Code that rewrites itself must run in isolation. The authors used sandboxing and human oversight, and any system of this kind needs comparable precautions. See [sandboxing and computer use](../../../engineering/agents/sandboxing-and-computer-use/index.md).

## Open questions

- Does archive-based search keep improving over long runs, or does it plateau?
- Do improvements to coding agents transfer to other kinds of task?
- As the agent's code grows more complex, can people still audit each self-modification?
- How much do the results depend on the benchmark being a good proxy for real software quality?

## References

### Seminal papers

- Zhang, J. et al. (2025). Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents. arXiv. https://arxiv.org/abs/2505.22954 — Self-modifying coding agents, validated empirically on benchmarks, raising SWE-bench performance from 20.0% to 50.0%.
- Schmidhuber, J. (2003). Goedel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements. arXiv. https://arxiv.org/abs/cs/0309048 — Proposes a self-referential solver that rewrites its own code once it has proof that the rewrite is useful.
- Zelikman, E. et al. (2023). Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation. arXiv. https://arxiv.org/abs/2310.02304 — A language model improves the scaffolding program that calls it, and the authors discuss the limits of that step.
- Hu, S., Lu, C. & Clune, J. (2024). Automated Design of Agentic Systems. arXiv. https://arxiv.org/abs/2408.08435 — Proposes searching automatically over agentic system designs written in code, rather than designing them by hand.

### Articles and documentation

- Novikov, A. et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery. arXiv. https://arxiv.org/abs/2506.13131 — White paper on an evolutionary coding agent that improves algorithms through automatic evaluators.
