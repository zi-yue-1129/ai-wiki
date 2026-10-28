---
status: draft
last_reviewed: 2026-10-28
tags:
  - reasoning
  - search
  - evaluation
aliases:
  - FunSearch
  - 函數空間搜尋
  - 程式搜尋
---

# FunSearch (Romera-Paredes et al. 2024)

FunSearch is an evolutionary procedure that pairs a pretrained large language model with an automatic evaluator. The model writes candidate programs, the evaluator scores them, and the best programs seed the next round. Its central choice is to search over programs that construct solutions rather than over the solutions themselves. Romera-Paredes and colleagues reported the method in Nature in 2024. It is one of the three landmark methods described on the parent page [Mathematics and Formal Proof](../index.md).

## Overview

Large language models can produce plausible but wrong statements, which Romera-Paredes et al. (2024) identify as a barrier to their use in scientific discovery. FunSearch sidesteps this by making every candidate testable. The language model proposes; the evaluator decides. A wrong idea gets a low score and is discarded, so the system never needs to be trusted about any single output.

The method was applied to two problems. The first is the cap set problem in extremal combinatorics, which asks for large sets of points in a finite grid with no three points on a common line. The second is online bin packing, where an algorithm must place arriving items into bins as they come. In both cases the output is a program, which experts can read, test and generalise.

## Key concepts

- **Evolutionary search.** A population of programs is improved over generations. Each generation, new programs are produced from high-scoring parents and kept only if they run and score well.
- **Program versus solution.** A solution is one object, such as a particular set of points. A program is a recipe that builds solutions, and it can be run on larger instances. Searching over programs lets a found pattern generalise.
- **Evaluator.** A problem-specific function that returns a score for a program, and rejects programs that fail or run too long. It is the source of trust in the system.
- **Pretrained language model.** It supplies the variation step: given example programs and their scores, it writes a new program that may improve on them.

## How it works

The search loop has five steps:

1. Write a problem-specific evaluator and a simple initial program.
2. Store the initial program in a database of scored programs.
3. Select several high-scoring programs from the database and prompt the language model to write an improved variant.
4. Run each new program through the evaluator under a time limit, and store the valid ones with their scores.
5. Repeat for many generations, then inspect the best program. A researcher reads it, checks why it works and tries to generalise it.

The language model is never asked for an answer. It is asked for code, and the evaluator is the only judge.

## Results

For the cap set problem, FunSearch found large cap sets beyond the best known ones, in finite dimensions and asymptotically. For online bin packing, it found heuristics that improve on widely used baselines. The abstract gives no figures, and this page quotes none, so readers should consult the paper for the exact numbers.

## Limitations

- **Evaluator required.** The method needs a cheap, automatic way to score a candidate. Problems whose quality is hard to measure in code are poor fits.
- **Interpretation.** A discovered program is more readable than a raw object, but understanding why it works is still an expert task.
- **Scope of claims.** The paper's successes are on a small number of problems. The method does not, by itself, produce proofs that such constructions are optimal.
- **Compute and variance.** Each run needs many model calls, and runs can find different programs.

## Open questions

- FunSearch finds objects and algorithms but not proofs. The AlphaEvolve work extended the approach to a wider set of problems, and combined it with proof systems (Georgiev et al., 2025).
- How much of the performance comes from the language model's prior knowledge and how much from the search itself? The answer determines how far the method transfers.
- Which open problems have evaluators that are cheap enough to make search practical?

## Connections

- The evolutionary structure belongs to the [evolutionary methods](../../../theory/paradigms/evolutionary/index.md) family of optimisation.
- Search over candidate objects is the classical theme of [symbolic AI search](../../../theory/paradigms/symbolic-ai/index.md), here guided by a language model rather than a hand-written heuristic.
- Davies et al. (2021) take a complementary route: machine learning suggests patterns that mathematicians then turn into conjectures. In FunSearch, the program search itself produces the candidate.
- Yang et al. (2024) argue that formal, machine-checkable reasoning is indispensable for AI mathematics, the principle FunSearch applies through its evaluator.

## Applications

The abstract notes that programs of this kind, such as the bin-packing heuristics, can be deployed in real applications. A later system, AlphaEvolve, applied the same idea to a range of problems. It reports a first improvement, after 56 years, over Strassen's algorithm for multiplying two 4 × 4 complex-valued matrices, using 48 scalar multiplications (Novikov et al., 2025). Georgiev et al. (2025) applied the system to 67 mathematical problems.

## References

### Seminal papers

- Romera-Paredes, B. et al. (2024). *Mathematical discoveries from program search with large language models*. Nature. https://doi.org/10.1038/s41586-023-06924-6 — Introduces FunSearch, an evolutionary search over LLM-written programs scored by an evaluator.
- Novikov, A. et al. (2025). *AlphaEvolve: A coding agent for scientific and algorithmic discovery*. arXiv. https://arxiv.org/abs/2506.13131 — Extends the evolutionary coding approach to many scientific and computing problems.
- Davies, A. et al. (2021). *Advancing mathematics by guiding human intuition with AI*. Nature. https://doi.org/10.1038/s41586-021-04086-x — Uses machine learning to suggest patterns for new conjectures, a complementary approach.

### Surveys and textbooks

- Yang, K. et al. (2024). *Formal Mathematical Reasoning: A New Frontier in AI*. arXiv. https://arxiv.org/abs/2412.16075 — Argues that machine-checkable reasoning is needed for trustworthy AI mathematics.

### Articles and documentation

- Georgiev, B. et al. (2025). *Mathematical exploration and discovery at scale*. arXiv. https://arxiv.org/abs/2511.02864 — Applies AlphaEvolve to 67 mathematical problems with mathematicians.
