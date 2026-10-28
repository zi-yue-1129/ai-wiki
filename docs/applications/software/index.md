---
related:
- theory/models/agents
- theory/models/llm
- applications/cybersecurity
- engineering/evaluation
aliases:
  - 軟體開發
  - 程式設計
---

# Software Development

Software engineering is one of the domains most transformed by LLMs, because code is abundant training data and outputs can be automatically tested.

## Evolution of tools

| Generation | Example | Capability |
|---|---|---|
| Autocomplete | IntelliSense, early ML completion | Next token or identifier |
| Inline code generation | GitHub Copilot (2021) | Lines and functions from context |
| Chat assistants | ChatGPT, Claude, Gemini in the IDE | Explain, refactor, debug on request |
| AI-native editors | Cursor, Windsurf and others | Multi-file edits with codebase context |
| Coding agents | Claude Code, OpenAI Codex, GitHub Copilot coding agent, Devin, Jules | Autonomous multi-step tasks: read the repo, edit, run tests, open pull requests |

## Benchmarks

| Benchmark | Measures |
|---|---|
| HumanEval / MBPP | Writing short functions from docstrings (Chen et al., 2021); now saturated
| SWE-bench / SWE-bench Verified | Resolving real GitHub issues in Python repositories (Jimenez et al., 2023)
| LiveCodeBench, Codeforces ratings | Competitive programming, contamination-resistant |
| Terminal-Bench, other agentic suites | Working in real environments |


## Productivity evidence

- Controlled task studies found speedups on well-defined tasks with Copilot (Peng et al., 2023)
- Field experiments at large companies found meaningful increases in completed tasks, larger for less experienced developers (Cui et al., 2024)
- A randomised trial with experienced open-source developers on their own mature repositories found they were ~19% *slower* with early-2025 AI tools despite believing they were faster (Becker et al., 2025). Effects depend heavily on task, codebase and experience

## Practices that work

- Give agents clear specifications, tests and repository context (e.g. a CLAUDE.md / AGENTS.md describing conventions)
- Keep humans reviewing diffs; require tests to pass
- Break work into small, verifiable steps
- Use sandboxes and least-privilege credentials for agents
- Track defect and security rates, not only velocity

## Risks

- Subtle bugs and insecure code; hallucinated package names that attackers can register
- Licence and provenance concerns for generated code
- Skill atrophy, especially for learners
- Maintainability debt from large volumes of generated code
- Agent security: prompt injection via issues, comments or dependencies (see [Cybersecurity](../cybersecurity/index.md))

## Beyond coding

Requirements analysis, test generation, code review, migration of legacy code (e.g. COBOL to Java), documentation, incident response, formal verification assistance.

## Key methods

Three methods are most relevant here. Each links to the page that explains it.

- [Agents](../../theory/models/agents/index.md): coding agents that read a repository, edit files and run tests, as in SWE-bench (Jimenez et al., 2023).
- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md): the architecture behind code models such as Codex (Chen et al., 2021).
- [InstructGPT and RLHF](../../theory/models/llm/instructgpt-rlhf/index.md): instruction tuning behind the chat assistants in the IDE (Ouyang et al., 2022).

## References

### Seminal papers

- Chen et al. (2021). Evaluating Large Language Models Trained on Code. arXiv. https://arxiv.org/abs/2107.03374 — Introduces the Codex model and the HumanEval benchmark of functions written from docstrings.
- Peng et al. (2023). The Impact of AI on Developer Productivity: Evidence from GitHub Copilot. arXiv. https://arxiv.org/abs/2302.06590 — Controlled experiment finding faster task completion with Copilot.
- Cui et al. (2024). The Effects of Generative AI on High Skilled Work: Evidence from Three Field Experiments with Software Developers. *SSRN*. https://doi.org/10.2139/ssrn.4945566 — Field experiments at large firms measuring the effects of AI assistance on developers.
- Becker et al. (2025). Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity. arXiv. https://arxiv.org/abs/2507.09089 — Randomised trial finding experienced developers slower with AI tools, though they expected to be faster.
- Jimenez et al. (2023). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? arXiv. https://arxiv.org/abs/2310.06770 — Benchmark of real GitHub issues in Python repositories.
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, built on multi-head self-attention.
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT, instruction tuning from human preference feedback.
