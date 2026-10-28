---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - theory/evaluation/protocols/methods/contamination-detection.md
tags:
  - evaluation
  - protocols
  - contamination
aliases:
  - LiveBench
  - 持續更新的基準
  - 抗污染基準
---

# LiveBench and Refreshed Benchmarks

!!! info "Part of Contamination Detection"
    This method page belongs to [Contamination Detection](contamination-detection.md). It explains the refreshed-benchmark approach in detail; the parent page compares it with the detection methods.

A refreshed benchmark avoids contamination by changing its questions over time, so that new test items come from sources published after the models' training cutoffs. LiveBench is a benchmark designed this way: White et al. (2024) add and update questions monthly, draw them from recent material, and score answers automatically. Unlike a private test set, LiveBench releases all of its questions.

## Problem

A static benchmark becomes contaminated as soon as its questions are posted. Once they are in a web crawl, a later model can learn them, and the score then measures memory. Detection methods can flag the damage after the fact, but they cannot make a fixed benchmark clean again. The problem is to keep the test items out of the training data in the first place.

## Core idea

Use test items that did not exist when the models were trained. Take questions from recent sources, and keep adding new ones on a fixed schedule, so that each release contains items newer than the training cutoffs of the models being compared. Score the answers with objective ground truth rather than with an LLM judge, so that the scoring cannot drift with a judge model.

## Procedure

As White et al. (2024) describe the design, a LiveBench release is produced in this way:

1. Collect new questions each month from recent math competitions, arXiv papers, news articles and datasets.
2. Add harder, contamination-limited versions of older tasks, such as Big-Bench Hard, AMPS and IFEval.
3. Score each answer automatically against an objective ground-truth value.
4. Publish the questions, the code and the model answers, so that others can rerun the benchmark.

## Results

The abstract of White et al. (2024) describes the design and the goals; it does not report a headline score for any model, and this page does not give one. The abstract states that questions are "added and updated on a monthly basis," and that all questions, code and model answers are released.

## Limitations

- **Cutoffs are not public.** A refreshed benchmark assumes that the newest items postdate the training data of each model. For models with unknown cutoffs, this assumption cannot be checked.
- **Cost of maintenance.** Monthly collection needs people or pipelines, and older releases can still be copied.
- **Narrow sources.** Questions from competitions, papers and news suit some skills better than others.
- **Public release.** Publishing all questions means that once an item is out, it is no longer clean for models trained afterwards. That is intended, but it limits how far a score from an old release can be compared with a new one.

## Connections

- The methods that detect contamination in a static benchmark are on [N-gram Overlap Decontamination](ngram-overlap-decontamination.md) and [Min-K% Prob](min-k-percent-prob.md).
- Private test sets are an alternative that keeps the items hidden. They trade openness for control over who sees them.
- The benchmark families where this design is used are listed under [Evaluation](../../../../theory/evaluation/index.md).

## Open questions

- How often must a benchmark be refreshed to stay clean as training corpora grow?
- Can new items be made comparable to old ones, so that scores can be tracked over time?

## References

### Seminal papers

- White, C. et al. (2024). *LiveBench: A Challenging, Contamination-Limited LLM Benchmark*. arXiv. https://arxiv.org/abs/2406.19314 — Describes a monthly-updated benchmark with objective scoring, designed to limit test set contamination.
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — A large static benchmark whose task files carry canary strings against web scraping, a different approach to the same problem.
- Dodge, J. et al. (2021). *Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus*. arXiv. https://arxiv.org/abs/2104.08758 — Shows that benchmark examples can appear in web corpora, the reason refreshed benchmarks exist.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Reports the 13-gram overlap analysis that motivated careful benchmark cleaning.
