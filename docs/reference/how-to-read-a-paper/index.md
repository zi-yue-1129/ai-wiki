---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - brain-mind/neuroai
tags:
  - evaluation
  - benchmarks
aliases:
  - 如何閱讀 AI 論文
  - 論文閱讀
  - How to read a paper
  - Reading machine learning papers
---

# How to Read an AI Paper

A research paper makes claims, and a reader's job is to see which of them the evidence supports. This page describes how machine learning papers are usually laid out, a reading order that makes the main claims visible, and the checks on baselines, test data, seeds and code that show whether a headline result is likely to hold.

## Overview

Most AI research reaches readers first as a paper, often posted on arXiv and later published at a conference or in a journal (see [Conferences & Journals](../venues/index.md)). A paper is an argument. It says that a method does something better, faster or more clearly than before, and it supports that statement with tables, plots and, increasingly, code. The reader decides how much of the argument to accept and for what purpose.

Reading papers well is rarely taught. Keshav (2007) sets out a practical three-pass method, and the advice here builds on it with the checks that machine learning papers often need. The aim is not to find fault with every paper, but to know which claims are well supported.

## Key concepts

- **Claim**: a statement the paper asks readers to accept, such as "our method outperforms the previous best method on benchmark X".
- **Baseline**: a method the new one is compared with. A weak or under-tuned baseline can make a modest gain look large.
- **Ablation**: a run with one component removed or changed, used to show which part of the method produces the gain.
- **Seed and variance**: results of neural networks depend on random initialisation, data order and hardware noise. A single run is one sample from a spread of possible results.
- **Contamination**: test items, or close copies of them, appearing in the data a model was trained on (see [Benchmark Contamination](../../engineering/evaluation/contamination.md)).
- **Reproducibility**: whether another group, using the paper together with its code and data, can obtain similar results.

## How it works

### Structure of an ML paper

Most machine learning papers follow a common layout. The **title and abstract** state the problem, the approach and the headline result. The **introduction** usually ends with a list of contributions, which is the most useful single summary of the claims. **Related work** places the paper among earlier methods. The **method** section defines the model or algorithm, often with equations or pseudocode. The **experiments** section names the datasets, baselines, metrics and training settings, and reports results, often with ablations. A **limitations** or **discussion** section may follow, then the conclusion, references and an **appendix**. NeurIPS, for example, has asked authors to complete a reproducibility checklist with each submission.[^pineau]

### Reading order

A practical order is to read the abstract and introduction, look at the figures and tables, read the method, and then the experiments. Treat the contribution list as a set of claims and find the table that tests each one. The appendix can wait.

Keshav's method fits this order. A first pass covers the title, abstract, introduction, section headings and conclusions, and ends with a decision about whether the paper deserves more time. A second pass reads the paper with care, noting figures and unclear points while skipping details that do not matter for the main argument. A third pass asks the reader to rebuild the work mentally, so that its assumptions and missing pieces become visible.[^keshav]

### Judging claims and baselines

For each headline claim, ask what would have to be true for it to be false. In particular, check whether:

- **the baselines are recent, strong and tuned with similar effort.** Dacrema and colleagues attempted to reproduce 18 neural recommendation methods from major conferences. Only 7 could be reproduced with reasonable effort, and six of those were often outperformed by simple heuristic methods such as nearest-neighbour rules.[^dacrema]
- **the gain is larger than the variation across runs.** Henderson and colleagues show that reported deep reinforcement learning results can vary enough, through seeds and implementation details, that small differences are hard to interpret. They call for significance metrics and more standardised reporting.
- **the ablation removes the component the paper credits.** Lipton and Steinhardt list failing to identify the sources of empirical gains among recurring problems in machine learning papers. One example they give is a gain that comes from hyperparameter tuning but is credited to an architectural change.[^lipton]
- **the search effort was matched.** In a large comparison of generative adversarial networks, Lucic and colleagues found that most models could reach similar scores given enough hyperparameter search and random restarts. Reported differences may therefore reflect search effort as much as the algorithm.

### Contamination and cherry-picking

Two problems can make a headline number look better than it is. **Contamination** means the test items, or near copies of them, appeared in training data, so the score partly measures recall. Brown and colleagues reported an overlap analysis between benchmarks and training data for GPT-3, and rescored a subset with the overlapping items removed. Sainz and colleagues argue that contamination should be measured for each benchmark rather than assumed to be absent.[^brown] A decontamination filter that finds no shared word sequences is not proof of a clean test set, because rephrased or translated items can pass it (Yang et al., 2023).[^yang] Jain and colleagues built LiveCodeBench from contest problems published over time, so that models can be tested on problems released after their training cut-off.[^jain] When reading a paper, compare the model's training cut-off with the benchmark's publication date, and look for a statement about decontamination or a private or dynamic test set.

**Cherry-picking** is selective reporting. It includes showing the best of many seeds, choosing datasets, subsets or metrics after seeing the results, or tuning the new method on the test set while baselines keep their defaults. Signs include a small number of seeds, no error bars, no failure cases and a metric that the task does not normally use. Reporting a clean subset alongside the full benchmark, as the GPT-3 authors did, is a sign of disclosure rather than proof that the result is sound. [Benchmark Suites](../../engineering/evaluation/benchmark-suites.md) explains how a saturated suite magnifies small, selectively reported differences.

### Code and reproducibility signals

Public code is a strong signal, but its presence alone is not enough. Look for code linked from the paper that matches the method described; configuration files or scripts giving the hyperparameters, seeds and data splits; a statement of compute used; and a README that explains how to reproduce the main table. Weaker signals include "code available on request" and repositories without training or evaluation scripts.

The evidence on documentation is sobering. Gundersen and Kjensmo surveyed 400 papers from two major AI conferences and found that none documented every variable they grouped as necessary for reproduction. Between 20 and 30 percent of the variables in each group were documented.[^gundersen] Kapoor and Narayanan found data leakage across 17 fields that use machine learning, affecting 329 papers. They proposed model info sheets for reporting scientific claims, so that leakage can be caught before publication.[^kapoor] The NeurIPS 2019 reproducibility program combined a code submission policy, a community reproducibility challenge and a checklist in the submission process, and its report describes what the organisers learned from it.[^pineau]

## Key methods

Reading strategies differ in where they start and what they are for. The table compares four common approaches. They are not exclusive, and careful readers often combine a quick first pass with a claims-focused check.

| Strategy | Starts with | Best for | Main risk |
|---|---|---|---|
| Three-pass reading (Keshav) | Title, abstract and figures, then a careful read, then a mental rebuild of the method | Deciding whether a paper matters, then understanding it | The third pass is slow and is often skipped |
| Claims-first check | The contribution list and the table that tests each claim | Judging whether the evidence supports the headline | Misses the method details needed to reimplement the work |
| Code-first check | The repository, its configuration files and the script behind the main table | Checking reproducibility and hidden tuning | Code may be missing, partial, or a different version from the paper |
| Citation trail | The reference list, then later papers that cite the work | Placing a result in context and finding its rivals | Citing a paper is not endorsing it, and popularity is not evidence |

## Connections

[Conferences & Journals](../venues/index.md) explains review models and preprints, [Landmark Papers](../papers/index.md) lists the papers that shaped several fields, and the [Glossary](../glossary/index.md) gives Chinese equivalents for common terms.

For the evaluation side, [Evaluation & Benchmarks](../../engineering/evaluation/index.md) sets out the pitfalls and a protocol for designing a test, and [Evaluation and Validation](../../theory/paradigms/supervised/evaluation-and-validation/index.md) covers splits, metrics and uncertainty for supervised models. [Benchmark Suites](../../engineering/evaluation/benchmark-suites.md) explains how saturation changes the meaning of a score, and [Benchmark Contamination](../../engineering/evaluation/contamination.md) covers detection and prevention in more depth.

The brain-and-mind angle raises the same questions in a particular form. A paper that reports a resemblance between a network's activity and brain recordings needs controls, such as untrained networks or alternative models, before the resemblance counts as evidence. [NeuroAI](../../brain-mind/neuroai/index.md) covers this area. [Building Machines That Learn and Think Like People](../../brain-mind/cognitive-science/building-machines-like-people/index.md) is an example of a target article published with open peer commentary, which lets readers see the disagreement as well as the claim.

## Applications

- **Literature reviews.** A three-pass read lets a researcher screen many papers quickly and reserve careful reading for the few that matter.
- **Refereeing.** The claims-first check and the questions about baselines and seeds form the core of a review.
- **Building on a result.** The code-first check shows which settings matter before a method is reproduced.
- **Summaries.** A generated summary can miss the baseline details and seed counts that matter most. Check claims against the tables they cite.

## Open questions

- Most fields do not require every input needed to reproduce a result. How can readers check claims at scale? Kapoor and Narayanan's model info sheets are one proposal.
- Can contamination be detected for closed models that do not publish their training data? Duan et al. (2024) found that membership inference barely outperforms random guessing on large language models trained on the Pile, and many methods depend on access to the corpus (see [Benchmark Contamination](../../engineering/evaluation/contamination.md)).
- Should venues reward reproduction work, and how should a reader weigh a result that few other groups have repeated?

[^pineau]: Pineau et al. (2020), listed in References. The report describes the three components of the NeurIPS 2019 program: a code submission policy, a reproducibility challenge and a checklist.
[^keshav]: Keshav (2007), listed in References. The paper describes the three-pass method and how to use it for a literature survey.
[^dacrema]: Dacrema et al. (2019), listed in References. Of 18 algorithms, 7 could be reproduced with reasonable effort, and 6 of those were often outperformed by simple heuristics.
[^lipton]: Lipton and Steinhardt (2018), listed in References. The paper names four patterns, including failure to identify the sources of empirical gains.
[^brown]: Brown et al. (2020), listed in References. The GPT-3 paper reports an analysis of overlap between its benchmarks and training data.
[^yang]: Yang et al. (2023), listed in References. The paper shows that rephrased and translated test samples can evade n-gram decontamination.
[^jain]: Jain et al. (2024), listed in References. The benchmark uses problems released over time so that results can be compared against each model's cut-off.
[^gundersen]: Gundersen and Kjensmo (2018), listed in References. The survey covered 400 papers from IJCAI and AAAI, and found that 20 to 30 percent of the variables in each group were documented.
[^kapoor]: Kapoor and Narayanan (2022), listed in References. The survey covered 17 fields and 329 papers with data leakage errors, and proposed model info sheets.

## References

### Seminal papers

- Keshav, S. (2007). *How to read a paper*. ACM SIGCOMM Computer Communication Review. https://doi.org/10.1145/1273445.1273458 — Describes a three-pass method for reading research papers efficiently, and how to use it when surveying the literature.
- Lipton, Z. C. & Steinhardt, J. (2018). *Troubling Trends in Machine Learning Scholarship*. arXiv. https://arxiv.org/abs/1807.03341 — Lists four recurring problems in machine learning papers, including misattributed empirical gains and misuse of mathematics and language.
- Henderson, P. et al. (2018). *Deep Reinforcement Learning that Matters*. arXiv. https://arxiv.org/abs/1709.06560 — Shows how non-determinism and variance make reported deep reinforcement learning results hard to interpret, and recommends better reporting.
- Lucic, M. et al. (2018). *Are GANs Created Equal? A Large-Scale Study*. arXiv. https://arxiv.org/abs/1711.10337 — Large empirical comparison of GAN models, finding that most reach similar scores once hyperparameters and restarts are sufficiently tuned.
- Dacrema, M. F., Cremonesi, P. & Jannach, D. (2019). *Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches*. arXiv. https://arxiv.org/abs/1907.06902 — Attempts to reproduce 18 neural recommendation methods and compares them with simpler, well-tuned baselines.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The GPT-3 paper, whose evaluation section analyses overlap between benchmarks and training data and rescores clean subsets.

### Surveys and textbooks

- Gundersen, O. E. & Kjensmo, S. (2018). *State of the Art: Reproducibility in Artificial Intelligence*. Proceedings of the AAAI Conference on Artificial Intelligence. https://doi.org/10.1609/aaai.v32i1.11503 — Surveys 400 AI papers for the variables needed to reproduce them, and finds that documentation is incomplete.
- Kapoor, S. & Narayanan, A. (2022). *Leakage and the Reproducibility Crisis in ML-based Science*. arXiv. https://arxiv.org/abs/2207.07048 — Surveys data leakage across fields that use machine learning, proposes a taxonomy of leakage types, and suggests model info sheets for reporting.

### Articles and documentation

- Pineau, J. et al. (2020). *Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)*. arXiv. https://arxiv.org/abs/2003.12206 — Report on the NeurIPS 2019 reproducibility program, covering its code policy, challenge and checklist.
- Sainz, O. et al. (2023). *NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark*. arXiv. https://arxiv.org/abs/2310.18018 — Argues that contamination must be measured for each benchmark because it can inflate reported scores.
- Yang, S. et al. (2023). *Rethinking Benchmark and Contamination for Language Models with Rephrased Samples*. arXiv. https://arxiv.org/abs/2311.04850 — Shows that rephrased and translated test samples can bypass n-gram decontamination.
- Duan, M. et al. (2024). *Do Membership Inference Attacks Work on Large Language Models?*. arXiv. https://arxiv.org/abs/2402.07841 — Finds that membership inference attacks barely outperform random guessing on language models trained on the Pile, which limits how contamination can be detected.
- Jain, N. et al. (2024). *LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code*. arXiv. https://arxiv.org/abs/2403.07974 — Builds a coding benchmark from contest problems published over time, to limit contamination.
