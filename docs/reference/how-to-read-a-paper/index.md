---
status: draft
last_reviewed: 2026-10-28
related:
  - reference/papers
  - reference/style-guide
tags:
  - reading
  - research methods
  - reproducibility
aliases:
  - 如何閱讀 AI 論文
  - 讀論文
  - Reading papers
---

# How to read an AI paper

AI papers can be long, dense and sometimes hard to trust. A good reading method lets you find the central claim quickly, judge whether the evidence supports it, and decide whether the result is worth building on. This page gives a reading order, the questions to ask of baselines and experiments, and the signs that a result will or will not reproduce.

## Overview

Most machine learning papers share a structure: an abstract, an introduction that states the problem and the claim, a related-work section, a method, experiments, and a discussion. The structure is a convenience, not a guarantee. Some papers bury the key limitation in an appendix, and some results depend on details that are only in the code. The aim of a reading method is to separate what the authors claim from what they show.

## Key concepts

- **Claim**: the sentence the paper wants you to believe, usually stated in the abstract and the introduction.
- **Evidence**: the experiments that support the claim, including the setup, the data and the metric.
- **Baseline**: the comparison method. A result is only as informative as its baseline.
- **Ablation**: an experiment that removes a component to show that it matters.
- **Contamination**: a test item that was seen during training, which inflates the reported score.

## How to read: a reading order

Read in three passes rather than linearly.

1. **First pass (ten minutes).** Read the title, abstract, introduction and conclusion. Write down the claim in one sentence and the setting in which it applies. Look at the figures and the main results table.
2. **Second pass (an hour).** Read the method and experiments. Check whether the experiments test the claim, whether the baselines are strong and fairly tuned, and whether the metric measures what the claim needs. Read the ablations and note what they remove.
3. **Third pass (only for papers that matter).** Re-derive the key equation, rerun a small part of the code, and check the appendices for hyperparameters, data splits and failed settings.

Papers that are strong on the first two passes can still be wrong in the third, so decide how far you will go before you start.

## Questions to ask

- Does the claim hold for the setting the authors tested, or does the abstract imply a wider scope?
- Are the baselines recent, well tuned and run under the same budget? A weak baseline can make any method look good.
- Are the results averaged over several random seeds, and is the variance reported?
- Is the test set separate from the data used for tuning? Were any test items seen during pre-training?
- Does the paper report negative results, such as settings where the method failed?
- Are the reported gains large compared with the variance across runs?

## Reproducibility signals

Good signs include code and data released with the paper, exact hyperparameters, the compute used, and a clear description of data splits. Warning signs include results reported only as a single number, missing ablations, and a method described in prose that cannot be implemented from the text.

A paper that makes these signals easy to find is not necessarily right, but it is much easier to check. Lipton and Steinhardt discuss common problems in the machine learning literature, including unjustified claims, confusion of explanation with speculation, and the use of mathematics where it adds nothing [(Lipton and Steinhardt, 2018)](https://arxiv.org/abs/1807.03341). Pineau and colleagues report on the NeurIPS 2019 Reproducibility Program, which covers what makes machine learning results sound and reproducible [(Pineau et al., 2020)](https://arxiv.org/abs/2003.12206).

## A worked example

The Transformer paper is a useful exercise. Its claim is that an attention-only architecture can replace recurrence and convolution for sequence transduction. Its evidence is a set of machine translation experiments, and the headline result is a BLEU score of 28.4 on WMT 2014 English-to-German, which the abstract says improves on prior results including ensembles by more than 2 BLEU [(Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762). A careful reader would ask which baselines were tuned to the same degree, how well the result transfers beyond translation, and what the training cost was. The paper's later influence does not answer those questions for it.

## Connections

Reading methods matter most where claims are contested, such as in [Evaluation](../../theory/evaluation/index.md), where benchmarks and protocols determine what results mean. The notation used in equations is covered in [Notation and symbols](../notation/index.md). The collection of papers cited across the wiki is in [Papers](../papers/index.md).

## Applications

Students use a reading method to prepare for a seminar or a literature review. Practitioners use it to decide whether to adopt a method. Reviewers use it to check whether a submitted paper's claims are supported.

## Open questions

- Which reproducibility checks predict whether a result will hold up in practice?
- How should readers weigh a method's influence against the strength of its evidence?
- Can automated tools help readers find missing baselines and unreported variance, without replacing judgement?

## References

### Seminal papers

- Keshav, *How to Read a Paper*, ACM SIGCOMM Computer Communication Review (2007). https://doi.org/10.1145/1273445.1273458 — A three-pass method for reading research papers, from computer systems but widely used beyond it.
- Goodfellow, Bengio and Courville, *Deep Learning*, MIT Press (2016). https://www.deeplearningbook.org/ — A textbook that defines the notation and terms many papers assume.
- Lipton and Steinhardt, *Troubling Trends in Machine Learning Scholarship* (2018). https://arxiv.org/abs/1807.03341 — Catalogues common problems in machine learning papers and how they distort the literature.
- Pineau, Vincent-Lamarre, Sinha, Larivière, Beygelzimer, d'Alché-Buc, Fox and Larochelle, *Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)* (2020). https://arxiv.org/abs/2003.12206 — Reports on the reproducibility program and its practical recommendations.
- Vaswani et al., *Attention Is All You Need* (2017). https://arxiv.org/abs/1706.03762 — The paper used as the worked example above.
