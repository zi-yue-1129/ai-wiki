---
related:
  - theory/math
  - theory/paradigms/symbolic-ai
  - theory/models/reasoning
aliases:
  - 數學
  - 形式證明
  - 定理證明
---

# Mathematics and Formal Proof

AI is used in mathematics in two distinct ways. Language models solve and write problems in natural language, where the answer may be wrong and hard to check. Formal systems express proofs in a language a computer can verify, so a model's attempt either checks or fails. The most recent progress combines the two.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Formal theorem proving | Proof assistants such as Lean; search and reinforcement learning over proof steps | A checked proof is a reliable reward signal |
| Olympiad geometry | A language model that proposes auxiliary constructions, paired with a symbolic deduction engine | AlphaGeometry (Trinh et al., 2024) |
| Olympiad problem solving | Reinforcement learning on formal problems, with a proof checker as the reward | AlphaProof (Hubert et al., 2025) |
| Program search for discovery | A language model proposes programs, and an evaluator keeps the good ones in a loop | FunSearch (Romera-Paredes et al., 2024) |
| Competition math by language models | Chain-of-thought reasoning, sampling and voting | Measured on MATH and GSM8K benchmarks |
| Conjecture guidance | Learned models suggest patterns that mathematicians then prove | Davies et al. (2021) |
| Symbolic computation | Sequence-to-sequence models for integration and differential equations | Lample & Charton (2019) |

## Why it is hard

- **Verification**: a natural-language proof can look convincing and be wrong. A formal proof is checked by a machine, but writing one requires a formal language and a library of definitions.
- **Scarce data**: formal proof corpora are small compared with web text, so models learn from synthetic problems and from their own successful proofs.
- **Sparse reward**: most proof attempts fail, so the signal for learning is rare.
- **Misformalisation**: a formal proof can be correct about a statement that differs from the intended one.

## Key methods

- [Chain-of-thought reasoning](../../theory/models/reasoning/chain-of-thought.md): step-by-step natural-language reasoning, the usual route for language models on competition mathematics.
- [Test-time scaling](../../theory/models/reasoning/test-time-scaling.md): spending more compute at inference to sample or search over many solutions.
- [Symbolic AI, search and planning](../../theory/paradigms/symbolic-ai/index.md): formal deduction and proof search, the classical side of theorem proving that AlphaGeometry combines with neural models.
- [Reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md): learns proof policies from a checker's verdict, as in AlphaProof-style systems.

## Connections

- The mathematical foundations used in machine learning are on the [Mathematics](../../theory/math/index.md) page.
- Formal proof and symbolic search are the theory side of this page. See [Symbolic AI](../../theory/paradigms/symbolic-ai/index.md).
- How people build proofs, and where intuition comes from, is studied in [Cognitive Science](../../brain-mind/cognitive-science/index.md). Mathematical intuition is one of the questions AI-guided discovery tries to model.
- Competition mathematics is also a benchmark for reasoning models; see [Reasoning models](../../theory/models/reasoning/index.md).

## Applications

- Checking and writing formal proofs in proof assistants such as Lean
- Helping mathematicians find patterns and test conjectures
- Automated verification of software and hardware, which uses the same proof technology
- Tutoring and assessment of mathematical reasoning (see [Education](../education/index.md))

## Risks and limits

- **Benchmark contamination**: problems from public competitions may appear in training data, which inflates scores.
- **Misformalisation**: a machine-checked proof of the wrong statement is a failure that is easy to miss.
- **Overclaiming**: reports of olympiad-level performance cover selected problems and specific formal settings.
- **Attribution**: when a discovery comes from a search over programs, credit and understanding of the result need separate handling.

## Open questions

- Whether formal proof search can scale to research-level mathematics where few formal libraries exist.
- How mathematicians should cite, check and trust results produced with AI assistance.

## References

### Seminal papers

- Hendrycks, D. et al. (2021). Measuring Mathematical Problem Solving With the MATH Dataset. arXiv. https://arxiv.org/abs/2103.03874 — Benchmark of competition-level mathematics problems with step-by-step solutions, used to measure language model reasoning.
- Cobbe, K. et al. (2021). Training Verifiers to Solve Math Word Problems. arXiv. https://arxiv.org/abs/2110.14168 — Introduces the GSM8K benchmark and trains verifiers that rank sampled solutions.
- de Moura, L. & Ullrich, S. (2021). The Lean 4 Theorem Prover and Programming Language. *CADE 2021, Lecture Notes in Computer Science*. https://doi.org/10.1007/978-3-030-79876-5_37 — Describes Lean 4, the proof assistant used by most current formal-mathematics AI systems.
- Trinh, T. H. et al. (2024). Solving olympiad geometry without human demonstrations. *Nature*. https://doi.org/10.1038/s41586-023-06747-5 — Pairs a language model with a symbolic deduction engine to solve olympiad geometry problems.
- Romera-Paredes, B. et al. (2024). Mathematical discoveries from program search with large language models. *Nature*. https://doi.org/10.1038/s41586-023-06924-6 — Uses a language model to propose programs that an evaluator scores, producing new mathematical constructions.
- Hubert, T. et al. (2025). Olympiad-level formal mathematical reasoning with reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-025-09833-y — Describes AlphaProof, which learns to prove formal olympiad problems in Lean with reinforcement learning.

### Surveys and textbooks

- Davies, A. et al. (2021). Advancing mathematics by guiding human intuition with AI. *Nature*. https://doi.org/10.1038/s41586-021-04086-x — Shows how learned models can suggest conjectures that mathematicians then prove, in knot theory and representation theory.
- Lample, G. & Charton, F. (2019). Deep Learning for Symbolic Mathematics. arXiv. https://arxiv.org/abs/1912.01412 — Trains sequence-to-sequence models to solve integration and differential equations.
