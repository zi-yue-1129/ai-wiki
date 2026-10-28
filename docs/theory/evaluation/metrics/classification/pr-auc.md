---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# PR-AUC

PR-AUC summarises the precision-recall curve, which plots precision against recall as the decision threshold changes. It is the metric to prefer when positives are rare, because it focuses on how the positives are ranked.

## Definition

Average precision (AP) is the usual PR-AUC estimate. It sums the precision at each threshold, weighted by the gain in recall from the previous threshold:

$$AP = \sum_n (R_n - R_{n-1})\, P_n$$

where $P_n$ and $R_n$ are precision and recall at the $n$-th threshold. scikit-learn's `average_precision_score` uses this step-wise form, which does not interpolate between points. It warns that the trapezoidal area under the same curve can be overly optimistic.

## Interpretation

A random classifier has precision equal to the positive rate, so PR-AUC for a random ranking equals the prevalence of positives. Unlike ROC-AUC, the baseline changes with the data, so PR-AUC values are not comparable across datasets with different prevalence. Compare models on the same dataset.

## When to use it

Use PR-AUC when positives are rare, as in fraud or fault detection, and when the scores will be used to pick the top of a ranked list. Saito and Rehmsmeier (2015) show that on imbalanced data the precision-recall plot is more informative than the ROC plot.

## Worked example

Use the same four scores. Sorted by score, the list is 0.9 (positive), 0.8 (negative), 0.6 (positive), 0.3 (negative). Precision at the two positives is $1/1$ and $2/3$, so average precision is $(1 + 2/3) / 2 \approx 0.83$, which matches the value `average_precision_score` returns. A random ranking would score 0.5 here, the prevalence of positives.

## Properties and variants

- **Baseline.** A random ranking gives PR-AUC equal to the prevalence, so the value should be read against that baseline, as described in the interpretation section.
- **Interpolation variants.** Older benchmarks, such as early PASCAL VOC evaluations, used 11-point interpolated average precision. At recall levels $0, 0.1, \ldots, 1$ it takes the maximum precision at or above each level and averages those. This differs from the step-wise average precision used here.
- **Single-point summaries.** Precision at a fixed recall, such as 90%, is a single-point summary that some applications prefer.
- **Limit.** Like ROC-AUC it judges the ranking but not calibration, and its value depends on prevalence.

## Pitfalls

- **Prevalence.** Two datasets with different positive rates give different PR-AUC baselines. Report the prevalence next to the score.
- **Interpolation.** Trapezoidal and step-wise estimates of the same curve differ. State which one is used.

## Related metrics

[ROC-AUC](roc-auc.md) is the threshold-free metric that uses the true and false positive rates instead. [Precision](precision.md) and [recall](recall.md) are the points on the curve. The family overview is [Classification Metrics](index.md).

## References

### Seminal papers

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — Shows why precision-recall curves are more informative than ROC curves for rare positives.

### Articles and documentation

- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — API reference giving the step-wise formula for average precision and the warning about the trapezoidal rule.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of threshold-free classification scorers and how they are used.

### Additional sources

- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Defines precision, recall, the F measure and average precision for retrieval.
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
