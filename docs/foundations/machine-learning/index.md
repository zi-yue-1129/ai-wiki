---
related:
- foundations/paradigms
- foundations/paradigms/supervised
- foundations/probabilistic
- engineering/evaluation
---

# Machine Learning

## Intuition

Traditional programming: humans write rules; the computer turns inputs into outputs.
Machine learning: humans provide examples of inputs and outputs; the computer finds the rules (model parameters).

Formally, given data \( D = \{(x_i, y_i)\} \), find \( f_\theta \) in a hypothesis space \( \mathcal{H} \) minimising expected loss:

\[
\theta^* = \arg\min_\theta \; \mathbb{E}_{(x,y)\sim P}\big[L(f_\theta(x), y)\big] \approx \arg\min_\theta \frac{1}{n}\sum_i L(f_\theta(x_i), y_i) + \lambda R(\theta)
\]

See [Learning Paradigms](../paradigms/index.md) for the different kinds of learning signal.

## Task types

| Task | Description | Example | Common algorithms |
|---|---|---|---|
| Classification | Predict a category | Spam, tumour benign/malignant | Logistic regression, trees, SVMs, neural nets |
| Regression | Predict a number | House price, drug dose | Linear regression, gradient boosting |
| Clustering | Find groups | Customer segments, cell types | k-means, DBSCAN, hierarchical clustering |
| Dimensionality reduction | Compress features | Visualisation, denoising | PCA, t-SNE, UMAP |
| Anomaly detection | Find unusual samples | Fraud, machine faults | Isolation Forest, autoencoders |
| Ranking and recommendation | Order by preference | Search, e-commerce | Matrix factorisation, two-tower models |
| Forecasting | Predict the future | Demand, load | ARIMA, gradient boosting, RNNs, Transformers |

## Classic algorithms

- **Linear / logistic regression**: interpretable, fast, the baseline in many fields.
- **k-nearest neighbours**: memorise everything, let neighbours vote.
- **Decision trees**: a cascade of if–else; interpretable but prone to overfitting.
- **Random forests**: bagging many trees.
- **Gradient-boosted trees (XGBoost, LightGBM, CatBoost)**: kings of tabular data.
- **Support vector machines**: maximise the margin; kernels handle nonlinearity.
- **Naive Bayes**: assumes conditionally independent features; a fast text baseline.
- **PCA**: directions of maximal variance.
- **Gaussian mixtures and EM**: soft clustering.

!!! tip "Try trees first on tables"
    On small and medium tabular datasets, gradient-boosted trees often beat deep learning (Grinsztajn et al., 2022). Tabular foundation models such as TabPFN have recently become strong on small data and are worth trying too.

## Generalisation: the central problem

### Underfitting and overfitting

- **Underfitting**: the model is too simple; training error is already high.
- **Overfitting**: the model memorises noise; low training error, high test error.

### Bias–variance trade-off

\[
\text{Expected error} = \text{bias}^2 + \text{variance} + \text{irreducible noise}
\]

Classical view: complexity reduces bias and increases variance, so there is a sweet spot.
Modern view: **double descent** — very large models, past the point where they can exactly fit the training data, see test error fall again. This helps explain why deep networks with far more parameters than examples generalise (Belkin et al., 2019; Nakkiran et al., 2019).

### Regularisation

L1 (sparsity), L2 (weight decay), early stopping, data augmentation, dropout, ensembling.

## Experimental method

1. **Split data**: train / validation / test. Touch the test set once, at the end.
2. **Cross-validation**: essential with small data.
3. **Split time series by time**, never letting the future predict the past.
4. **Avoid leakage**: fit preprocessing (scaling, feature selection) on training data only; split by patient/user, not by row.
5. **Choose metrics that fit the task**:

| Metric | When |
|---|---|
| Accuracy | Balanced classes |
| Precision / recall / F1 | Imbalanced classes (screening favours recall, spam filters favour precision) |
| ROC-AUC, PR-AUC | Threshold-free comparison; PR-AUC under heavy imbalance |
| MAE, RMSE, R² | Regression |
| Calibration (ECE) | When probabilities must be trustworthy (medicine, finance) |

## Learning theory in brief

- **PAC learning**: how many samples are needed to learn an approximately correct hypothesis with high probability.
- **VC dimension**: a capacity measure for hypothesis classes.
- **No free lunch**: no algorithm is best on all problems; inductive bias is necessary.
- **Inductive bias**: translation equivariance in CNNs, temporal structure in RNNs, permutation invariance in GNNs all build domain knowledge into models. The brain's evolved architecture can be seen as a powerful inductive bias (see [NeuroAI](../../brain-mind/neuroai/index.md)).

## Links to cognitive science

- **Concept learning**: humans learn new concepts from a few examples; Bayesian program learning (Lake et al., 2015) models this.
- **Prototype vs exemplar theories** of categorisation correspond to class-centroid classifiers and kNN-style memory.
- **Statistical learning**: infants segment words using syllable transition probabilities (Saffran et al., 1996) — in some ways like a language model.

## Resources

- Microsoft [ML-For-Beginners](https://github.com/microsoft/ML-For-Beginners) (MIT)
- Andrew Ng, *Machine Learning Specialization* (Coursera)
- *The Elements of Statistical Learning* (free PDF)
- [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html)
- Hsuan-Tien Lin, *Machine Learning Foundations/Techniques* (NTU, Mandarin)

## References

### Seminal papers

- Zhang, C., et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — Shows that large models can memorise random labels, which undermines simple capacity-based accounts of generalisation.
- Hastie, T., Tibshirani, R. & Friedman, J. *The Elements of Statistical Learning*, 2nd ed. https://hastie.su.domains/ElemStatLearn/ — The standard graduate reference on supervised and unsupervised methods, with the statistical theory behind them. Free PDF from the authors.

### Lectures and videos

- Abu-Mostafa, Y. S. *Learning From Data*. Caltech. https://work.caltech.edu/telecourse — A free introductory course on the theory and practice of learning from data, covering the VC dimension, bias–variance and regularisation.

### Articles and documentation

- Domingos, P. (2012). A Few Useful Things to Know About Machine Learning. *Communications of the ACM*, 55(10). https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf — Twelve practical lessons for practitioners on generalisation, features and overfitting.
- scikit-learn developers. *User Guide*. https://scikit-learn.org/stable/user_guide.html — The practical reference for standard algorithms, model evaluation and common pitfalls, with runnable examples.
