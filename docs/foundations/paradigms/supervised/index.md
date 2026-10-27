# Supervised Learning

## Idea

Learn a mapping \(f: X \to Y\) from labelled examples \((x_i, y_i)\). The label tells the learner exactly what the right answer was, so the error can be computed and minimised directly:

\[
\min_\theta \frac{1}{n}\sum_{i=1}^n L\big(f_\theta(x_i), y_i\big) + \lambda R(\theta)
\]

## Task types

| Task | Output | Typical loss |
|---|---|---|
| Binary classification | {0, 1} | Binary cross-entropy, hinge |
| Multi-class classification | One of K classes | Softmax cross-entropy |
| Multi-label classification | Any subset of K labels | Per-label sigmoid cross-entropy |
| Regression | Real value | Mean squared error, MAE, Huber |
| Ordinal regression | Ordered categories (e.g. disease grade) | Cumulative link losses |
| Structured prediction | Sequences, trees, segmentations | CRF loss, sequence cross-entropy, Dice |
| Ranking | Ordering of items | Pairwise / listwise losses |
| Survival analysis | Time-to-event with censoring | Cox partial likelihood |

## Algorithms

Linear and logistic regression, k-nearest neighbours, decision trees, random forests, gradient-boosted trees (XGBoost, LightGBM, CatBoost), support vector machines, naive Bayes, Gaussian processes, and neural networks of every kind. See [Machine Learning](../../machine-learning/index.md) for details.

## Where labels come from

- **Human annotation** (crowdsourcing, domain experts) — expensive, slow, sometimes inconsistent; measure inter-annotator agreement (Cohen's κ).
- **Natural labels** — logs of what actually happened (clicks, purchases, diagnoses, prices).
- **Programmatic labels** — heuristics and rules (see [weak supervision](../semi-supervised/index.md)).
- **Model-generated labels** — LLMs as annotators or distillation from a larger model; validate against human labels.

## Pitfalls

| Problem | Symptom | Remedy |
|---|---|---|
| Overfitting | Train ≫ test performance | Regularisation, more data, early stopping, augmentation |
| Label noise | Plateaued accuracy, memorised errors | Noise-robust losses, relabelling, confident learning |
| Class imbalance | High accuracy, useless minority-class recall | Re-weighting, resampling, focal loss, PR-AUC |
| Leakage | Suspiciously good validation scores | Fit preprocessing on train only; split by patient / time / user |
| Shortcut learning | Model uses spurious cues (e.g. hospital watermark on X-rays) | Stress tests, counterfactual data, domain-shift evaluation |
| Distribution shift | Performance drops in deployment | Monitoring, [domain adaptation](../transfer/index.md) |

## Supervised learning inside modern AI

Even "self-supervised" foundation models rely on supervised steps: **supervised fine-tuning (SFT)** of LLMs on instruction–response pairs is supervised learning (and also a form of [imitation learning](../imitation/index.md)); reward models in RLHF are trained with supervised preference labels.

## Brain and behaviour

- **Cerebellum**: climbing fibres from the inferior olive carry error signals that drive plasticity at Purkinje-cell synapses — the classic Marr–Albus–Ito theory of cerebellar supervised learning.
- **Delta rule and Rescorla–Wagner**: the Widrow–Hoff delta rule (1960) and the Rescorla–Wagner model of classical conditioning (1972) have the same mathematical form — learning proportional to prediction error.
- **Category learning** in psychology studies how people learn labelled categories; prototype and exemplar models map onto centroid classifiers and kNN.

## Further reading

- Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning* (free PDF)
- [scikit-learn supervised learning guide](https://scikit-learn.org/stable/supervised_learning.html)
- Geirhos et al. (2020), "Shortcut learning in deep neural networks", *Nature Machine Intelligence*

## Subtopics

- [Linear models and GLMs](linear-models/index.md): regression, logistic and regularised linear models.
- [Decision trees and ensembles](trees-and-ensembles/index.md): random forests and gradient boosting.
- [Support vector machines and kernels](kernel-methods-svm/index.md): maximum margin and the kernel trick.
- [Instance-based and probabilistic classifiers](instance-based-and-probabilistic/index.md): kNN, naive Bayes, discriminant analysis, Gaussian processes.
- [Loss functions and optimisation](loss-functions-and-optimization/index.md): what "wrong" means and how parameters are found.
- [Generalisation theory](generalization-theory/index.md): why fitting a sample transfers to new data.
- [Evaluation and validation](evaluation-and-validation/index.md): splits, metrics and common leakage errors.

## References

- Cortes & Vapnik (1995), "Support-vector networks", *Machine Learning* 20. https://link.springer.com/doi/10.1007/BF00994018 — Introduces the soft-margin SVM, the classic supervised classifier.
- Boser, Guyon & Vapnik (1992), "A training algorithm for optimal margin classifiers", COLT. https://mlanthology.org/colt/1992/boser1992colt-training — The first kernel SVM paper, combining margins with the kernel trick.
- Breiman (2001), "Random forests", *Machine Learning* 45(1). https://mlanthology.org/mlj/2001/breiman2001mlj-random — Random forests, the strongest general-purpose tree ensemble of its era.
- Friedman (2001), "Greedy function approximation: a gradient boosting machine", *Annals of Statistics* 29(5). https://doi.org/10.1214/AOS/1013203451 — Gradient boosting, the basis of most modern tabular models.
- Zhang et al. (2017), "Understanding deep learning requires rethinking generalization", ICLR, arXiv:1611.03530. https://mlanthology.org/iclr/2017/zhang2017iclr-understanding — Shows why classical generalisation theory does not explain deep networks.
