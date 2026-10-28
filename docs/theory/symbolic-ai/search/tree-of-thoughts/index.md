---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/reasoning
  - theory/models/agents
tags:
  - reasoning
  - search
  - planning
aliases:
  - Tree of Thoughts
  - ToT
  - 思維樹
  - 思想樹
  - Chain of thought
  - 思維鏈
---

# Tree of Thoughts

Tree of Thoughts (ToT) is a framework in which a language model proposes several intermediate reasoning steps, scores them, and searches the resulting tree, with backtracking when a branch looks unpromising. It generalises chain-of-thought prompting, which follows a single path. It is an application of the [search algorithms](../index.md) family to language-model reasoning, introduced by Yao and colleagues in 2023.[^1]

## Overview

Chain-of-thought prompting asks a model to write its reasoning as one sequence of steps. If an early step is wrong, the model rarely returns to it. Many problems need exploration: trying an option, seeing that it fails, and choosing another. ToT treats partial solutions as states in a search problem. The model proposes candidate next steps, the same model judges which states are promising, and a search procedure decides where to go next.

The authors evaluated ToT on three tasks chosen because they need planning or search: Game of 24, creative writing and mini crosswords.[^1] The framework is general, but its gains depend on how the tasks are split into steps and how the states are judged.

## Key concepts

- **Thought**: a coherent unit of text, such as one arithmetic step or one plan sentence, that serves as an intermediate result.
- **State**: the problem together with the thoughts produced so far.
- **Thought generator**: proposes candidate next thoughts from a state, either by sampling or by asking for several at once.
- **State evaluator**: scores a state, either by rating each one on its own or by voting between candidates.
- **Search procedure**: breadth-first search keeps the best few states at each level. Depth-first search follows the most promising branch and backtracks when it fails.

## How it works

ToT can be described as a search over a tree whose nodes are states. A breadth-first version runs the following loop.

1. Start from the problem as the root state.
2. For each state in the current frontier, ask the model to generate $k$ candidate thoughts, giving $k$ new states.
3. Ask the model to evaluate each new state, for example by rating how likely it is to lead to a solution.
4. Keep the $b$ highest-rated states and discard the rest.
5. Repeat until a state solves the problem or the search budget is spent.

A depth-first version instead continues from the most promising state, and when the evaluator marks a state as impossible, it backtracks to the previous level. Both versions use the language model for all three roles: proposing, judging and deciding which path to follow. This makes ToT a closed loop in which the model's own judgement drives the search.

## Results

The clearest result is on Game of 24, a puzzle in which four numbers must be combined with arithmetic to reach 24. The abstract reports that GPT-4 with chain-of-thought prompting solved 4% of tasks, while ToT achieved a success rate of 74%.[^1] The abstract reports gains on all three tasks.

Later work extended the idea. Language Agent Tree Search combines Monte Carlo tree search with language-model value functions and environment feedback. Its abstract reports 92.7% pass@1 accuracy on HumanEval programming tasks with GPT-4.[^2] Reasoning via Planning uses the language model as both reasoning agent and world model, with Monte Carlo tree search over reasoning steps. Its abstract reports that LLaMA-33B with this method surpasses chain-of-thought prompting on GPT-4 by 33% relative improvement on plan generation.[^3] These results come from different tasks, so they are not directly comparable.

## Limitations

- **Cost.** A search makes many model calls for each problem, so inference compute and latency rise sharply compared with a single chain.
- **Self-evaluation.** The evaluator is a language model. If it judges a flawed step as promising, the search follows that error.
- **Task design.** The tasks were chosen where look-ahead matters, and the prompts were designed for them. It is not yet clear how to split an open-ended task into steps.
- **Verification.** The method works best when subgoals can be checked. Without a verifier the search has little to stop it drifting.

## Open questions

- Does training a model to reason longer, as in current reasoning models, internalise a kind of search that explicit tree search otherwise provides?
- How should test-time compute be allocated? Snell and colleagues find that the best strategy depends on prompt difficulty, which suggests that fixed budgets may be wasteful on some prompts.[^4]
- Which search procedure works best for language models: breadth-first, depth-first, or Monte Carlo methods that balance exploration and exploitation?

## Connections

ToT is the language-model counterpart of the classical methods in the [parent overview](../index.md), with the model playing the roles of heuristic and successor generator. See also the [reasoning models](../../../models/reasoning/index.md) page, which covers training, and [AI agents](../../../models/agents/index.md). [ReAct](../../../../engineering/agents/react/index.md) interleaves reasoning with acting, and [Reflexion](../../../../engineering/agents/reflexion/index.md) uses verbal feedback after failure, both of which address the same weakness of single-pass reasoning. The analogy with human thought is loose; dual-process theories contrast fast intuition with slow deliberation (see [Psychology and AI](../../../../brain-mind/psychology/index.md)).

## Applications

- **Puzzles and mathematical problems**, where a partial solution can be checked, as in Game of 24.
- **Programming**, in agent systems that search over candidate code and use test results as feedback.[^2]
- **Planning in simulated environments**, such as plan generation tasks studied with Reasoning via Planning.[^3]

## References

### Seminal papers

- Yao, S. et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. arXiv. https://arxiv.org/abs/2305.10601 — Introduces ToT, a search over tree-structured reasoning steps with model-based proposal and evaluation.
- Yao, S. et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. arXiv. https://arxiv.org/abs/2210.03629 — Interleaves reasoning traces and actions in a language model, an agent pattern that search-based work builds on.
- Kocsis, L. & Szepesvári, C. (2006). Bandit Based Monte-Carlo Planning. *Lecture Notes in Computer Science*. https://doi.org/10.1007/11871842_29 — Introduces UCT, a selection rule for Monte Carlo tree search that some language-model search systems use.

### Surveys and textbooks

- Browne, C. B. et al. (2012). A Survey of Monte Carlo Tree Search Methods. *IEEE Transactions on Computational Intelligence and AI in Games*. https://doi.org/10.1109/TCIAIG.2012.2186810 — Surveys Monte Carlo tree search and its variants, the family behind the language-model systems discussed here.

### Articles and documentation

- Hao, S. et al. (2023). Reasoning with Language Model is Planning with World Model. arXiv. https://arxiv.org/abs/2305.14992 — Uses Monte Carlo tree search over reasoning steps, with the language model acting as both world model and reasoning agent.
- Zhou, A. et al. (2023). Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models. arXiv. https://arxiv.org/abs/2310.04406 — Combines Monte Carlo tree search, language-model value functions and environment feedback for agents.
- Snell, C. et al. (2024). Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. arXiv. https://arxiv.org/abs/2408.03314 — Studies how searching against verifiers and adaptive sampling at test time trade off against model size, depending on prompt difficulty.

[^1]: Yao et al. (2023), listed above. The success rates are as reported in the abstract.
[^2]: Zhou et al. (2023), listed above. The figure is the abstract's reported pass@1 with GPT-4.
[^3]: Hao et al. (2023), listed above. The 33% figure is the relative improvement reported in the abstract.
[^4]: Snell et al. (2024), listed above.
