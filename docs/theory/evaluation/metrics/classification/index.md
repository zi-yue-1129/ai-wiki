---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# Classification Metrics

Classification metrics score a model whose output is a class label or a score for each class. Some metrics read the labels at one decision threshold: accuracy, precision, recall and F1. Others read the scores across all thresholds and ask how well positives are ranked above negatives: ROC-AUC and PR-AUC. The two groups answer different questions, so a model can look strong on one and weak on the other.

## Key metrics

| Metric | What it measures | Fixed label-decision rule? | Use when |
|---|---|---|---|
| [Accuracy](accuracy.md) | Fraction of correct labels | Yes | Classes are balanced and every error costs the same |
| [Precision](precision.md) | Share of predicted positives that are correct | Yes | False alarms are costly |
| [Recall](recall.md) | Share of true positives that are found | Yes | Missed cases are costly |
| [F1](f1.md) | Harmonic mean of precision and recall | Yes | One number for the positive class |
| [ROC-AUC](roc-auc.md) | Ranking of positives above negatives | No | Comparing models without fixing a threshold |
| [PR-AUC](pr-auc.md) | Precision across recall levels | No | Positives are rare |

For a score-based **binary** classifier, label metrics generally change when the cutoff changes. Multiclass predictions may instead use `argmax`, and models may supply labels directly; neither case requires a single numeric cutoff. Report the label-decision rule (and any relevant cutoff) alongside accuracy, precision, recall and F1. ROC-AUC and PR-AUC aggregate across score thresholds rather than choosing one operating point; inspect precision and class prevalence when positives are rare.

## Shared synthetic 100-case example

The worked examples for [accuracy](accuracy.md), [precision](precision.md), [recall](recall.md), and [F1](f1.md) all use **the same** binary-classification confusion matrix. Rows are **actual** classes; columns are **predicted** classes. The entries are nonnegative integer counts, not probabilities.

| Actual class | Predicted positive | Predicted negative | Total |
|---|---:|---:|---:|
| Positive | 40 (TP) | 20 (FN) | 60 |
| Negative | 10 (FP) | 30 (TN) | 40 |
| **Total** | **50** | **50** | **100** |

From these *identical* 100 cases, accuracy is **70/100 = 0.700**, precision is **40/50 = 0.800**, recall is **40/60 ≈ 0.667**, and F1 is **80/110 ≈ 0.727**. This is a **constructed count example, not measured classifier performance**. The animations linked in the metric pages use their own explicitly stated synthetic score sets or population parameters and **must not be read as sequential results from these 100 cases**.

## Guided animations: two different evaluation questions

The following **synthetic**, bilingual demonstrations are shared with the detailed metric pages. They explain different decisions; neither displays measured classifier outcomes.

- **Does a changing base rate move the ROC point?** The [ROC/PR prevalence animation](roc-auc.md) holds TPR = 0.80 and FPR = 0.10 constant while positive prevalence varies from 5% to 60%. Its ROC point stays fixed, but precision rises from about 0.296 to 0.923. The same animation is explained in [PR-AUC](pr-auc.md). [GitHub static preview](../../../../assets/concept-animations/roc-pr-prevalence-still.svg).
- **Which threshold should be deployed?** The [Youden-J versus expected-loss animation](roc-auc.md) compares seven cutoffs on six distinct-score ranked cases. Maximum J occurs at k = 2; for hypothetical prevalence 0.40, false-positive cost 1 and false-negative cost 5, minimum expected loss instead occurs at k = 6. If false-negative cost were 1, the loss minimum would move back to k = 2. [GitHub static preview](../../../../assets/concept-animations/roc-youden-cost-still.svg).

On MkDocs, use the keyboard-accessible Play/Pause control. With reduced motion the static frame is shown; on narrow screens focus and scroll horizontally.

## Connections

Whether the scores behave like probabilities is a separate question, covered in [Probabilistic Metrics](../probabilistic/index.md). The procedure for splitting data and validating a classifier is in [Evaluation and Validation](../../../paradigms/supervised/evaluation-and-validation/index.md).

## References

### Surveys and documentation

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — Shows why precision-recall curves are more informative than ROC curves for rare positives.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Reference for the standard classification scorers and their definitions.
- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Defines precision, recall, the F measure and average precision for retrieval, which carry over to classification.

### Additional sources

- Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters* 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010 — Explains how ROC curves and the AUC are built, read and commonly misused.
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — Standard textbook on statistical learning and its evaluation.
