---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
tags:
  - alignment
  - oversight
aliases:
  - Debate cross-examination
  - Cross-examination
  - 辯論交叉詰問
  - 交叉詰問
---

# Debate cross-examination

Cross-examination is a mechanism added to [AI debate](debate.md) so that a debater cannot change the meaning of a statement after it has been challenged. In the machine-learning version, the opponent may question a saved copy of the debater that knows only what was said up to that point. The idea comes from Barnes and Christiano (2020), in an informal post, and it targets one specific weakness of debate: ambiguity.

## Problem

Debate assumes that a false claim can be exposed by the opposing debater. A dishonest debater can exploit this by making an ambiguous statement early, then choosing whichever meaning suits the part of the argument under discussion. A judge who sees only the final exchange may not notice the switch. Barnes and Christiano frame this ambiguity as the problem cross-examination is meant to solve.

## Key concepts

- **Saved copy**: for a machine debater, a snapshot taken when it makes a statement. The copy does not know which branch of the debate was pursued afterwards.
- **Clarifying question**: a question from the opponent to the copy about the terms and details of the statement.
- **Commitment**: the debater must either fix the details in advance or give answers that can be checked against each other later.

## How it works

1. Debater A makes a statement $s$ in the debate.
2. For a machine debater, the system saves a copy of A as it stood at that point.
3. Later, debater B may question the copy about $s$. The copy answers from the transcript up to $s$ only.
4. Either debater may quote these answers. If A's later claims contradict what the copy said, the contradiction counts against A.
5. The judge then decides as in ordinary debate.

For human debaters, who cannot be copied, the post suggests backtracking to the point where a term was introduced, or bringing in a teammate who sees only the debate up to that statement. This version depends on good-faith play, because the debater must answer honestly about what was said earlier.

## Evidence

The formal studies of debate test related features, but not this copy-based mechanism. Each one is a useful comparison point:

- Khan et al. (2024) test an interactive debate in which the judge makes statements after each round, such as asking clarifying questions. With LLM judges, interactive debate did not improve accuracy over static debate. With human judges, the two matched.
- Michael et al. (2023) let the judge ask questions and set burdens on the debaters. With human judges, debate reached 84% accuracy against 74% for consultancy. With AI debaters, debate reached 78% against 80% for consultancy, which is not a significant difference.
- Kenton et al. (2024) explicitly choose not to evaluate interactive debate, in which the judge asks questions in each round.
- Brown-Cohen et al. (2025) propose a formal protocol in which a prover decomposes a claim and an estimator assigns probabilities to the subclaims. Its structure is close in spirit to cross-examination, but the paper does not use that term. It gives theoretical soundness and completeness results and no experiments.

Taken together, these results show that interactive questioning can help some judges, but they do not establish the cross-examination mechanism itself.

## Limitations

- **Ambiguity only.** The post says the mechanism does not solve the obfuscated-argument problem, and that the authors do not have a fix for it.
- **Good-faith dependence.** The human version works only if the debater answers honestly when backtracking.
- **Copy fidelity.** The mechanism assumes that a saved copy reflects the debater's reasoning at the time of the statement. The formal literature does not test this assumption.
- **Indirect evidence.** No formal experiment tests a copy-based cross-examination protocol.

## Connections

Cross-examination borrows its name from courtroom practice, where an advocate's claims are tested by questions from the other side. The analogy explains the design, but a debater copy is not a witness, and the analogy does not guarantee that the mechanism works. The method belongs to the debate family in [scalable oversight](scalable-oversight.md), alongside [AI debate](debate.md) and the decomposition approaches. Judges in these protocols face the same risk of being exploited that is discussed in [reward hacking](reward-hacking.md).

## Applications

These are research uses, not deployed systems.

- Designing debate protocols for machine debaters that must commit to the details of their claims.
- Training human debaters and judges to check whether a claim stays consistent under questioning.
- Building evaluation setups that test whether a model's explanation survives follow-up questions.

## Open questions

- Does a saved copy reproduce the reasoning of the original debater, or only its words?
- Does cross-examination reduce ambiguity-based deception in practice, and does it help with obfuscated arguments?
- How can the copy-based mechanism be combined with formal protocols such as the prover-estimator structure?

## References

### Seminal papers

- Irving, G., Christiano, P. & Amodei, D. (2018). *AI safety via debate*. arXiv:1805.00899. https://arxiv.org/abs/1805.00899 — Proposes two-agent debate judged by a human, the protocol that cross-examination modifies.
- Khan, A. et al. (2024). *Debating with More Persuasive LLMs Leads to More Truthful Answers*. Proceedings of ICML 2024 (PMLR 235). https://arxiv.org/abs/2402.06782 — Compares static and interactive debate with human and LLM judges on QuALITY.
- Michael, J. et al. (2023). *Debate Helps Supervise Unreliable Experts*. arXiv:2311.08702. https://arxiv.org/abs/2311.08702 — Tests debate with judges who can ask questions, against a consultancy baseline.

### Surveys and textbooks

- Kenton, Z. et al. (2024). *On scalable oversight with weak LLMs judging strong LLMs*. arXiv:2407.04622. https://arxiv.org/abs/2407.04622 — Compares debate and consultancy with weak LLM judges, and states that interactive debate is not evaluated.
- Brown-Cohen, J. et al. (2025). *Avoiding Obfuscation with Prover-Estimator Debate*. arXiv:2506.13609. https://arxiv.org/abs/2506.13609 — Proposes a prover-estimator debate protocol, with theoretical soundness and completeness results.

## Further learning

- Barnes, E. & Christiano, P. (2020). [Debate update: Obfuscated arguments problem](https://www.alignmentforum.org/posts/PJLABqQ962hZEqhdB/debate-update-obfuscated-arguments-problem). AI Alignment Forum. The original description of cross-examination, in an informal post.
