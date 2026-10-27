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

LLM evaluation adds benchmark contamination and judge-model bias; see [Large Language Models](../../../../models/llm/index.md). Related: [Landmark Papers](../../../../reference/papers/index.md).

## References

### Seminal papers

- Saito & Rehmsmeier (2015), "The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets", *PLoS ONE* 10(3). https://pmc.ncbi.nlm.nih.gov/articles/PMC4349800
- Niculescu-Mizil & Caruana (2005), "Predicting good probabilities with supervised learning", ICML. https://mlanthology.org/icml/2005/niculescumizil2005icml-predicting
- Guo et al. (2017), "On calibration of modern neural networks", ICML, arXiv:1706.04599. Temperature scaling.
- Zhang et al. (2017), "Understanding deep learning requires rethinking generalization", ICLR, arXiv:1611.03530. Models can memorise, so held-out tests matter. https://mlanthology.org/iclr/2017/zhang2017iclr-understanding

### Surveys and textbooks

- (none checked for this page)

### Lectures and videos

- StatQuest with Josh Starmer, episodes on ROC curves and AUC, YouTube. https://www.youtube.com/@statquest

### Articles and documentation

- Grinsztajn, Oyallon & Varoquaux (2022), "Why do tree-based models still outperform deep learning on tabular data?", arXiv:2207.08815. A careful benchmark design.
