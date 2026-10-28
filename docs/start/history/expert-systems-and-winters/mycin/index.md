---
status: draft
last_reviewed: 2026-10-28
tags:
  - reasoning
  - uncertainty
aliases:
  - MYCIN
  - 確定性因子
  - certainty factors
  - 專家系統
  - Shortliffe
---

# MYCIN and Certainty Factors (1975)

MYCIN was a rule-based expert system that Edward Shortliffe built at Stanford University in the 1970s to identify bacteria causing serious infections and to suggest antibiotic treatment. Its scheme for attaching a certainty factor to each rule, and for combining the factors, was published with Bruce Buchanan in 1975, and it became one of the most copied ideas of the expert-system period.

## Overview

Medical evidence from cultures, symptoms and laboratory tests is incomplete and sometimes contradictory. A physician who takes advice from a program needs to know how sure it is and why it reached its conclusion. MYCIN was built for that setting. It asked the physician for the facts it needed, worked toward a diagnosis and a treatment plan, and could explain its questions in terms of its rules.

Shortliffe's 1976 book describes the system's design and rule base (Shortliffe, 1976). The 1975 paper with Buchanan sets out the certainty-factor model (Shortliffe and Buchanan, 1975). The method keeps the explicit symbols of the [symbolic era](../../symbolic-era/index.md) and adds a numerical measure of belief.

## Key concepts

- **Production rule**: an IF–THEN rule whose premises test facts and whose conclusion adds a new fact or hypothesis.
- **Certainty factor (CF)**: a number between −1 and 1 expressing how strongly the evidence supports a conclusion. Positive values express belief, negative values disbelief, and zero means no information.
- **Backward chaining**: starting from a goal, such as the identity of an organism, finding the rules that could establish it, and working back to their premises.

## How it works

The knowledge base held several hundred production rules, each capturing a piece of medical reasoning. The inference engine worked backward from the goal. To decide which organism was involved, it found the rules that concluded something about organisms, then checked their premises against the facts entered. If a premise was unknown, it asked the physician.

Certainty factors carried the evidence through the chain. A rule contributes its own factor multiplied by the certainty of its premises. When two rules support the same conclusion with positive factors $CF_1$ and $CF_2$, they combine as

$$
CF = CF_1 + CF_2\,(1 - CF_1),
$$

so two moderately supportive rules give a stronger conclusion than either alone, and the value never exceeds 1. The model also handles evidence that counts against a conclusion.

## Results

The main evidence is the system's design and the consultations described in Shortliffe's 1976 book. The result is less a single number than a demonstration: a rule base of a few hundred rules, with an explicit model of uncertainty, could give specialist-level advice in one narrow domain, and the reasoning could be traced. The same inference machinery was reused for other domains by swapping the rules, which led to shell systems such as EMYCIN. The results do not show that the approach would scale to general medicine or be cheap to maintain.

## Limitations

- **Hand-built knowledge.** Each rule had to be elicited from an expert and written down. This is the knowledge acquisition bottleneck, and the cost of building a new rule base was a main reason the expert-system market later contracted (Cullen and Bryman, 1988).
- **Certainty factors are not probabilities.** They were designed to be easy to elicit and combine, and they lack the justification of probability theory. Later systems used probabilistic models such as [graphical models](../../../../theory/paradigms/probabilistic/graphical-models/index.md) instead.
- **Explanations describe rules, not reasons.** Clancey (1983) argued that a trace of the rules that fired shows what the program did, but not the strategic reasons behind its questions and conclusions.
- **Narrow scope.** Knowledge built for one domain did not carry over to another. Attempts to cover common-sense knowledge by hand took a person-century of effort and stayed incomplete (Lenat, 1995).

## Connections

MYCIN extends the symbolic approach rather than abandoning it. Its rule format resembles the production systems used as models of human cognition. [ACT-R](../../../../brain-mind/cognitive-architectures/act-r/index.md) is the best-known example. MYCIN's rules were written to match expert judgement, while ACT-R's are tested against human behaviour. See also the [symbolic AI](../../../../theory/paradigms/symbolic-ai/index.md) pages.

## Open questions

- Can a rule base capture the reasons behind a clinical judgement, or only the conclusions?
- When is a numerical certainty measure a useful approximation to probability, and when does it mislead?

## References

### Seminal papers

- Shortliffe, E. H. & Buchanan, B. G. (1975). A model of inexact reasoning in medicine. *Mathematical Biosciences*. https://doi.org/10.1016/0025-5564(75)90047-4 — Presents the certainty-factor model for combining uncertain evidence, developed for the MYCIN consultation system.
- Shortliffe, E. H. (1976). *Computer-Based Medical Consultations: MYCIN*. Elsevier. https://doi.org/10.1016/b978-0-444-00179-5.x5001-x — The book-length account of the MYCIN system, its design, and its rule-based consultation method.

### Surveys and textbooks

- Nilsson, N. J. (2009). *The Quest for Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/CBO9780511819346 — A history of AI that places the expert-system work of the 1970s and 1980s in the wider story of the field.

### Articles and documentation

- Clancey, W. J. (1983). The epistemology of a rule-based expert system: A framework for explanation. *Artificial Intelligence*. https://doi.org/10.1016/0004-3702(83)90008-5 — Examines the explanations a MYCIN-style rule system can give and what those explanations leave out.
- Cullen, J. & Bryman, A. (1988). The knowledge acquisition bottleneck: Time for reassessment? *Expert Systems*. https://doi.org/10.1111/j.1468-0394.1988.tb00065.x — Questions the common view that knowledge acquisition is the main constraint on expert-system development.
- Lenat, D. B. (1995). CYC. *Communications of the ACM*. https://doi.org/10.1145/219717.219745 — Describes the long effort to build a large common-sense knowledge base by hand, and its lessons for knowledge engineering.
