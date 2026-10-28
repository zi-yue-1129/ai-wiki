---
status: draft
last_reviewed: 2026-10-28
tags:
  - reasoning
  - knowledge representation
aliases:
  - DreamCoder
  - 夢想編碼器
  - Wake-sleep Bayesian program learning
  - 覺醒-睡眠貝氏程式學習
  - Library learning
  - 程式庫學習
  - Program induction
  - 程式歸納
---

# DreamCoder

DreamCoder is a system that learns to solve problems by writing programs, and that grows the programming language it writes in as it learns. Ellis and colleagues introduced it as a preprint in 2020. Its wake-sleep procedure alternates between solving tasks with a neural search and extending a library of reusable abstractions. It is the program-induction landmark of the [neuro-symbolic AI overview](../index.md).

## Overview

Expert problem solvers depend on the languages they think in. A mathematician writes with well-chosen notation, and a programmer builds up functions that are reused. DreamCoder asks whether a machine can acquire such a language. It starts from a basic domain-specific language, solves tasks by writing programs in it, and adds new abstractions when they recur across solutions. The abstract says that acquiring expertise means learning these languages, together with the skills to use them.[^1]

Program induction from examples has a long history, from string transformations in spreadsheets onward.[^2]

## Key concepts

- **Domain-specific language (DSL)**: a set of primitives and a grammar in which programs for one domain are written.
- **Library**: learned abstractions added to the DSL as new primitives. Solutions can then reuse them.
- **Recognition model**: a neural network that, given a task, predicts which primitives a solution is likely to use, so that the search can be guided.
- **Generative model**: a probability distribution over programs in the current library. It is used to sample programs and tasks during sleep.

## How it works

The abstract describes the procedure as a wake-sleep algorithm that "alternately extends the language with new symbolic abstractions and trains the neural network on imagined and replayed problems."[^1] In outline:

1. **Wake.** For each task in a batch, the recognition model ranks the library's primitives, and a search enumerates programs in order of their probability. Each program that solves its task is kept, and the solved tasks are stored for replay.
2. **Abstraction sleep.** The solutions are examined for subprograms that recur. Useful ones are added to the library as new primitives, and the solutions are rewritten to use them.
3. **Dream sleep.** Programs are sampled from the generative model and turned into imagined tasks. The recognition model is trained on these and on the replayed solved tasks, so that it learns which primitives to predict for a given task.
4. The loop repeats with the updated library and recognition model.

The underlying objective is Bayesian. A simplified form of the score being maximised is

$$
\log P[L] + \sum_{x} \log \sum_{\rho} P[\rho \mid L]\, P[x \mid \rho]
$$

where $L$ is the library, $\rho$ a program and $x$ a task, with $P[x \mid \rho]$ equal to 1 when $\rho$ solves $x$ and 0 otherwise. This is a simplification; the paper gives the exact prior over libraries and the approximations it uses.

## Results

The abstract reports that DreamCoder solves both classic inductive programming tasks and creative tasks. It also reports that the system rediscovers the basics of modern functional programming, vector algebra and classical physics, including Newton's and Coulomb's laws, and that its concepts are built compositionally from earlier ones, which yields layered representations that transfer to new tasks.[^1] The benchmark-level figures are in the paper's experiments and are not reproduced here.

## Limitations

- **Search cost.** Enumerating programs is expensive, and the recognition model only narrows the search.
- **Designer's choices.** The starting DSL, the task families and the training schedule shape what the system can learn. Rediscovering a known law means reaching it with the primitives given, not discovering it from nothing.
- **Readability needs review.** A learned library is readable as code, but judging whether an abstraction is the right one still requires a person.
- **Domain fit.** The approach relies on tasks whose solutions are programs with checkable outputs.

## Open questions

- Can library learning work over the much larger and less structured program spaces that language models explore?
- Does a language model that writes code directly make a learned DSL unnecessary, or does a learned library supply the reuse that such models lack?

## Connections

Code-trained language models write programs without a learned DSL,[^4] and the mechanics of executing model-written code are covered in [CodeAct](../../../../engineering/agents/sandboxing-and-computer-use/codeact/index.md). DreamCoder's layered libraries are one attempt at the compositional, learned-to-learn ingredients that Lake and colleagues argue human-like learning requires.[^3] The abstract makes no claim about the brain. Its "imagined and replayed" training is a loose analogy to offline replay, which is discussed in [Hippocampal Replay](../../../../brain-mind/sleep-and-consolidation/hippocampal-replay/index.md). For the wider picture, see [Neuro-Symbolic AI](../index.md).

## References

### Seminal papers

- Ellis, K. et al. (2020). *DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning*. arXiv. https://arxiv.org/abs/2006.08381 — Learns domain-specific programming languages and neural search guides through alternating wake and sleep phases.
- Gulwani, S. (2011). *Automating string processing in spreadsheets using input-output examples*. Proceedings of POPL. https://doi.org/10.1145/1926385.1926423 — Learns string-transformation programs in spreadsheets from a few input-output examples.
- Lake, B. M. et al. (2016). *Building Machines That Learn and Think Like People*. arXiv. https://arxiv.org/abs/1604.00289 — Argues that human-like learning needs causal models, intuitive theories and compositionality.

### Articles and documentation

- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces Codex, a language model trained on code, and evaluates it on writing programs from docstrings.
- Gao, L. et al. (2022). *PAL: Program-aided Language Models*. arXiv. https://arxiv.org/abs/2211.10435 — Has a language model write programs that a Python interpreter executes, so that the solving step is exact.

[^1]: Ellis et al. (2020), listed above. The description of the procedure, scope and results is taken from the abstract.
[^2]: Gulwani (2011), listed above.
[^3]: Lake et al. (2016), listed above.
[^4]: Chen et al. (2021) on Codex and Gao et al. (2022) on PAL, both listed above.
