---
status: draft
last_reviewed: 2026-10-28
tags:
  - reasoning
  - knowledge representation
aliases:
  - Neural theorem prover
  - Neural theorem proving
  - 神經定理證明器
  - 神經定理證明
  - End-to-end differentiable proving
  - 端到端可微分證明
  - Soft unification
  - 軟合一
---

# Neural Theorem Prover

A neural theorem prover answers queries against a knowledge base by backward chaining, but matches symbols with a differentiable similarity between learned vectors instead of exact unification. Rocktäschel and Riedel introduced the end-to-end differentiable version as a preprint in 2017. It is the neural-proving landmark of the [neuro-symbolic AI overview](../index.md).

## Overview

Classical proving and knowledge-base reasoning rely on discrete matching: two symbols either unify or they do not. That prevents learning symbol representations from data by gradient descent. Prolog's backward chaining shows the classical procedure. To prove a goal, the system finds a rule whose conclusion matches it and recursively proves that rule's premises.

Rocktäschel and Riedel replace exact matching with a soft one. Their networks prove queries by operating on dense vector representations of symbols, built recursively in the style of Prolog backward chaining. Because every step is differentiable, gradient descent can learn that two symbols are similar and use that similarity in proofs.[^1]

## Key concepts

- **Backward chaining**: starting from a goal, looking for rules whose conclusion matches it, and recursively proving their premises.
- **Unification**: finding substitutions that make two terms equal. Classical provers use it exactly.
- **Soft unification**: a degree of match between two symbols, computed from their embeddings with a radial basis function kernel.
- **Proof score**: a value in $[0,1]$ for a proof, built from the soft matches along it, so that a query receives a score rather than a yes or no answer.

## How it works

The procedure for a single query runs as follows.

1. **Embed the symbols.** Each predicate and constant has a learnable vector representation.
2. **Find candidate steps.** For the goal, consider each fact and each rule whose head could match it.
3. **Match softly.** Score each candidate match with a radial basis function kernel on the two embeddings, for example the Gaussian $k(\mathbf{a}, \mathbf{b}) = \exp(-\lVert \mathbf{a} - \mathbf{b} \rVert^2 / \mu)$ with bandwidth $\mu$.
4. **Recurse.** Prove the rule's body in the same way and multiply the match scores along the chain.
5. **Combine alternatives.** Combine the scores of different proofs, here by taking a maximum, to obtain the score of the query.
6. **Train.** Adjust the embeddings and rule parameters by gradient descent, so that facts the knowledge base supports receive high scores.

The same machinery also induces rules. The abstract says the network learns to place similar symbols close together, to use those similarities in proofs, to induce logical rules, and to combine provided and induced rules for multi-hop reasoning.[^1]

## Results

The abstract reports that the architecture outperforms ComplEx, a state-of-the-art neural link-prediction model, on three of four benchmark knowledge bases, while inducing interpretable, function-free first-order logic rules.[^1] The benchmark names and detailed figures are in the paper and are not reproduced here.

## Limitations

- **Cost of recursion.** Backward chaining explores candidate rules and matches, and its cost grows with proof depth and the number of rules. In practice the search over alternative proofs has to be bounded.
- **Similarity is not identity.** Two symbols with close embeddings can be treated as equal, so a proof can look plausible while relying on a false match.
- **Function-free rules.** The induced rules are function-free, which excludes structures that build new terms, such as lists.
- **Narrow scope.** The results concern knowledge-base completion and query answering. The approach does not address open-ended language or perception.

## Open questions

- Can soft unification be paired with exact checking, so that a learned similarity cannot produce an invalid proof?
- How far does the approach scale to large knowledge bases and unbounded proof search?
- Can the rules it induces be checked by a formal proof assistant?

## Connections

The neural theorem prover and [∂ILP](../differentiable-ilp/index.md) both learn rules, but in different directions. ∂ILP learns rules from examples, while the neural theorem prover proves queries and induces rules as a side effect of proving. Later neural provers work on formal mathematics instead of knowledge bases. GPT-f generates Metamath proofs with a transformer language model,[^2] LeanDojo adds retrieval to a prover for Lean,[^3] and AlphaProof searches for Lean proofs with reinforcement learning.[^4] In the Lean-based systems, a proof is written as text and accepted only if Lean 4 checks it.[^5] See [Mathematics and Formal Proof](../../../../applications/mathematics/index.md) and [AlphaProof](../../../../applications/mathematics/alphaproof/index.md).

## Applications

- **Knowledge-base completion.** Inferring facts missing from an incomplete knowledge base, as in the abstract's experiments.[^1]
- **Multi-hop queries.** Answering questions that require chaining several facts and rules.

[^1]: Rocktäschel and Riedel (2017), listed above. The results and capabilities are taken from the abstract.
[^2]: Polu and Sutskever (2020), listed above.
[^3]: Yang et al. (2023), listed above.
[^4]: Hubert et al. (2025), listed above.
[^5]: de Moura and Ullrich (2021), listed above.

## References

### Seminal papers

- Rocktäschel, T. & Riedel, S. (2017). *End-to-End Differentiable Proving*. arXiv. https://arxiv.org/abs/1705.11040 — Builds neural networks that prove knowledge-base queries by backward chaining, with soft symbol matching learned from data.
- Polu, S. & Sutskever, I. (2020). *Generative Language Modeling for Automated Theorem Proving*. arXiv. https://arxiv.org/abs/2009.03393 — Introduces GPT-f, a transformer-based prover for Metamath whose proofs were accepted into the main library.

### Articles and documentation

- Yang, K. et al. (2023). *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models*. arXiv. https://arxiv.org/abs/2306.15626 — An open Lean toolkit with data, models and benchmarks, including a retrieval-augmented prover.
- Hubert, T. et al. (2025). *Olympiad-level formal mathematical reasoning with reinforcement learning*. Nature. https://doi.org/10.1038/s41586-025-09833-y — Describes AlphaProof, which learns to find formal Lean proofs through reinforcement learning, with test-time adaptation.
- de Moura, L. & Ullrich, S. (2021). *The Lean 4 Theorem Prover and Programming Language*. Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-030-79876-5_37 — Describes Lean 4, the proof assistant and programming language used by AlphaProof.
