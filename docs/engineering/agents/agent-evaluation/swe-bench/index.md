---
status: draft
last_reviewed: 2026-10-28
tags:
- agents
- evaluation
- benchmarks
aliases:
- SWE-bench
- 真實 GitHub 議題
- 軟體工程基準
---

# SWE-bench: Resolving Real GitHub Issues

SWE-bench (Jimenez et al., 2023) tests whether a language-model agent can change a real software repository so that a reported GitHub issue is resolved, with the project's own tests as the judge. It is one of three landmark methods on the [Agent Evaluation](../index.md) page.

## Overview

Software engineering suits agent evaluation: it involves reading a large codebase, locating code, editing it and running tests. Earlier code benchmarks such as HumanEval asked for a single function written from a docstring (Chen et al., 2021). That tests generation, but not navigation across a whole project.

SWE-bench assembles 2,294 issues and their pull requests from 12 popular Python repositories (Jimenez et al., 2023). The model receives the issue text and a copy of the repository at the state before the fix, and must produce a change that the project's tests accept.

## Key concepts

- **Issue**: a bug report or feature request, written by a user, that a later pull request in the original project resolved.
- **Base commit**: the repository state just before that pull request. The agent starts here.
- **Patch**: the diff the agent produces. It is applied to the base commit.
- **FAIL_TO_PASS tests**: tests that fail before the fix and must pass after the patch.
- **PASS_TO_PASS tests**: tests that pass before and after the fix and must still pass.
- **Resolve rate**: the share of instances in which both sets of tests behave as required. It is the headline metric.

## How it works

Grading follows a fixed procedure:

1. Check out the repository at the base commit, with its dependencies installed in an isolated environment.
2. Give the model the issue text and the codebase. In the original setting, the model received retrieved parts of the repository in one prompt and returned a patch. Later agent systems let the model navigate the repository through tools in a loop.
3. Collect the patch the model produces.
4. Apply the patch to the base commit and run the FAIL_TO_PASS and PASS_TO_PASS tests.
5. Count the instance as resolved only if every FAIL_TO_PASS test passes and no PASS_TO_PASS test fails.

The check is automatic and repeatable, but the criterion depends entirely on the quality of the tests.

## Results

The paper's headline result is low. Its abstract reports that the best-performing model, Claude 2, solved only 1.96 percent of the issues, and that the fine-tuned SWE-Llama resolved only the simplest ones (Jimenez et al., 2023).

Later agent systems scored far higher on the same benchmark. SWE-agent, which adds a custom interface for editing files, navigating repositories and running tests, reports a pass@1 rate of 12.5 percent on SWE-bench (Yang et al., 2024). Scores depend on the model, scaffold and benchmark version, so compare them only within one protocol.

Grading errors also change the picture. Aleithan et al. (2024) examined the patches that passed the tests and found many with leaked solutions or weak tests. After problematic instances were removed, the resolution rate of one SWE-agent configuration fell from 12.47 to 3.97 percent.[^1]

## Limitations

- **Narrow scope.** All instances come from Python projects, and the 12 repositories are popular open-source projects whose code and discussions are widely available on the web.
- **Weak tests.** A patch can pass tests that do not check the real behaviour. Aleithan et al. report that 31.08 percent of the passed patches they inspected were suspicious for this reason.
- **Solution leakage.** Some issues or comments contain the fix itself, so a model can succeed by copying it. The same analysis finds this in 32.67 percent of successful patches.
- **Contamination.** Over 94 percent of the issues predate the knowledge cutoffs of LLMs, so a model may have seen them in training (Aleithan et al., 2024).
- **Test-passing is not merging.** A patch that passes the tests may still be rejected by maintainers for style, scope or design.

## Open questions

- **Robust grading.** Curated subsets, such as SWE-bench Verified, aim to improve quality, yet Zhu et al. (2025) still report insufficient test cases in that subset. Whether test-based grading can be made robust at scale is unresolved.
- **Skill or interface.** Yang et al. (2024) show that interface design changes results. Whether a score measures the model's engineering ability or the quality of its tools is hard to separate.
- **Other languages and tasks.** Results on Python issues may not transfer to other languages, to feature requests or to large system changes.

## References

### Seminal papers

- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv. https://arxiv.org/abs/2310.06770 — Benchmark of 2,294 issues from 12 Python repositories, graded by the projects' own tests.
- Yang, J. et al. (2024). *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. arXiv. https://arxiv.org/abs/2405.15793 — Shows how a custom agent-computer interface changes an agent's SWE-bench performance.
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces HumanEval, the single-function benchmark that SWE-bench extends to whole repositories.

### Surveys and textbooks

- Yehudai, A. et al. (2025). *Survey on Evaluation of LLM-based Agents*. arXiv. https://arxiv.org/abs/2503.16416 — Survey of agent evaluation that covers software-engineering agents among its application benchmarks.

### Articles and documentation

- Aleithan, R. et al. (2024). *SWE-Bench+: Enhanced Coding Benchmark for LLMs*. arXiv. https://arxiv.org/abs/2410.06992 — Manual analysis of SWE-bench that finds solution leakage and weak tests among successful patches.
- Zhu, Y. et al. (2025). *Establishing Best Practices for Building Rigorous Agentic Benchmarks*. arXiv. https://arxiv.org/abs/2507.02825 — Reports insufficient test cases in SWE-bench Verified and proposes a checklist for benchmark builders.

[^1]: Aleithan et al. (2024), abstract, https://arxiv.org/abs/2410.06992 — Reports the drop from 12.47 to 3.97 percent for SWE-Agent with GPT-4 after filtering problematic instances.
