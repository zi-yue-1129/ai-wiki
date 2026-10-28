---
tags:
  - supervised learning
  - evaluation
  - metrics
---

# Evaluation and Validation

Measuring how well a supervised model will do on new data, and avoiding fooling yourself.

## Splitting data

- **Train / validation / test**: tune on validation, report once on test.
- **k-fold cross-validation** averages over $k$ splits, useful for small data. Use **stratified** folds for imbalanced classes.
- **Group and time splits**: keep all samples from one patient, user or session in one fold; for forecasting always validate on later time than training. Random splits there leak information.
- **Nested cross-validation** separates hyperparameter selection from performance estimation.

## Metrics

| Task | Metric | Caution |
|---|---|---|
| Classification | Accuracy | Misleading with imbalance |
| Classification | Precision, recall, F1 | Depend on the threshold |
| Classification | ROC-AUC, PR-AUC | PR-AUC is more informative for rare positives |
| Probabilistic | Log-loss, Brier score, calibration error | Reward honest probabilities |
| Regression | RMSE, MAE, $R^2$ | RMSE penalises large errors |
| Ranking | NDCG, MAP | Position-weighted |
| Segmentation | IoU, Dice | |

**Calibration** asks whether predictions of 80% are right 80% of the time; temperature scaling (Guo et al., 2017) is a simple fix for deep networks.

## Common failures

- **Data leakage**: preprocessing fitted on all data, duplicates across splits, features that encode the label.
- **Test-set reuse**: repeatedly choosing models by test score overfits the test set; benchmark leaderboards suffer from this.
- **Shortcut learning**: high accuracy for the wrong reason; test on out-of-distribution and counterfactual sets.
- **Subgroup gaps**: report metrics per group, not only the average (see [Ethics & Fairness](../../../../society/ethics/index.md)).
- **Statistical noise**: report confidence intervals or seeds, not single runs.

## Connections

LLM evaluation adds benchmark contamination and judge-model bias; see [Large Language Models](../../../models/llm/index.md). Related: [Landmark Papers](../../../../reference/papers/index.md).

## References

### Seminal papers

- Saito & Rehmsmeier (2015), "The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets", *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — Shows why precision-recall curves are more informative than ROC curves for rare positives.
- Niculescu-Mizil & Caruana (2005), "Predicting good probabilities with supervised learning", ICML. https://doi.org/10.1145/1102351.1102430 — Compares probability calibration across common classifiers and the effect of calibration methods.
- Guo et al. (2017), "On calibration of modern neural networks", ICML, arXiv:1706.04599 — Shows that modern networks are overconfident and that temperature scaling corrects it.
- Zhang, C. et al. (2017). Understanding deep learning requires rethinking generalization. ICLR. arXiv:1611.03530. https://arxiv.org/abs/1611.03530 — Shows that networks can memorise random labels, so held-out tests are essential.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

- Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters*, 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010 — Explains how ROC curves and the AUC are built, read and commonly misused.

### Articles and documentation

- Grinsztajn, Oyallon & Varoquaux (2022), "Why do tree-based models still outperform deep learning on tabular data?", arXiv:2207.08815 — Careful benchmark design, useful as a model for fair comparisons between methods.

## Further learning

- StatQuest with Josh Starmer, episodes on ROC curves and AUC, YouTube. https://www.youtube.com/@statquest — Visual explanation of how ROC curves and AUC are built and what they measure.
