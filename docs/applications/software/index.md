---
related:
- models/agents
- models/llm
- applications/cybersecurity
- engineering/evaluation
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
| HumanEval / MBPP | Writing short functions from docstrings (now saturated) |
| SWE-bench / SWE-bench Verified | Resolving real GitHub issues in Python repositories |
| LiveCodeBench, Codeforces ratings | Competitive programming, contamination-resistant |
| Terminal-Bench, other agentic suites | Working in real environments |

Scores on SWE-bench Verified rose from a few percent in 2023 to well over half of tasks by 2025 for leading agents.

## Productivity evidence

- Controlled task studies found large speedups on well-defined tasks (e.g. ~56% faster on an HTTP-server task with Copilot, Peng et al., 2023)
- Field experiments at large companies found meaningful increases in completed tasks, larger for less experienced developers (Cui et al., 2024)
- A randomised trial with experienced open-source developers on their own mature repositories found they were ~19% *slower* with early-2025 AI tools despite believing they were faster (METR, 2025) — effects depend heavily on task, codebase and experience

## Practices that work

- Give agents clear specifications, tests and repository context (e.g. a CLAUDE.md / AGENTS.md describing conventions)
- Keep humans reviewing diffs; require tests to pass
- Break work into small, verifiable steps
- Use sandboxes and least-privilege credentials for agents
- Track defect and security rates, not only velocity

## Risks

- Subtle bugs and insecure code; hallucinated package names ("slopsquatting")
- Licence and provenance concerns for generated code
- Skill atrophy, especially for learners
- Maintainability debt from large volumes of generated code
- Agent security: prompt injection via issues, comments or dependencies (see [Cybersecurity](../cybersecurity/index.md))

## Beyond coding

Requirements analysis, test generation, code review, migration of legacy code (e.g. COBOL to Java), documentation, incident response, formal verification assistance.

## Resources

- [SWE-bench](https://www.swebench.com/)
- Anthropic, "Building effective agents"; Claude Code and OpenAI Codex documentation
- METR (2025), "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity"
