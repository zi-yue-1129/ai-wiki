---
related:
  - theory/paradigms/probabilistic
  - theory/paradigms/supervised
  - society/ethics
aliases:
  - 保險
  - 精算
  - 精算科學
---

# Insurance and Actuarial Science

Insurance is built on pricing risk. Actuaries have used statistical models for centuries, and machine learning now extends them with richer data, such as telematics and claims text. Fraud detection and claims handling are older, well-tested uses. The same models that improve price accuracy can also create new forms of unfair discrimination, and regulators increasingly examine them.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Risk pricing | Generalised linear models; gradient-boosted trees; neural networks | Regulators expect transparent, explainable models |
| Claims triage and reserving | Classifiers for claim severity; neural reserving models | Speeds up routing to the right handler |
| Fraud detection | Supervised classifiers; anomaly detection; network analysis | Heavy class imbalance is the core difficulty |
| Telematics and usage-based insurance | Models of driving data from vehicle sensors or phones | Data consent and privacy questions |
| Document and claims text | Language models for reading medical and repair reports | New source of error and bias |
| Underwriting and eligibility | Automated decisions on coverage | Governed by consumer-protection rules |

## Why it is hard

- **Rare events**: fraud and large claims are rare, so models must be calibrated carefully and evaluated with the right metrics.
- **Long horizons**: a policy's losses appear years later, so feedback is slow.
- **Price sensitivity**: small differences in predicted risk change who buys, which changes the risk pool.
- **Proxies for protected traits**: features that predict risk can also stand in for race, sex or disability.

## Key methods

- [Trees and ensembles](../../theory/paradigms/supervised/trees-and-ensembles/index.md): gradient-boosted trees are the workhorse for pricing and fraud models.
- [Anomaly detection](../../theory/paradigms/unsupervised/anomaly-detection/index.md): flags claims that differ from normal patterns, used alongside supervised fraud models.
- [Probabilistic and Bayesian methods](../../theory/paradigms/probabilistic/index.md): give calibrated risk estimates and uncertainty, which pricing requires.
- [Interpretability](../../society/interpretability/index.md): methods that explain a price or a decision, which regulators increasingly require.

## Connections

- Credit scoring and fraud in banking share many methods; see [Finance](../finance/index.md).
- Fairness constraints on pricing are the same problem as in other automated decisions. See [Ethics & Fairness](../../society/ethics/index.md).
- Human judgement under uncertainty, and how people perceive and accept risk, is covered in [Cognitive Science](../../brain-mind/cognitive-science/index.md).

## Applications

- Pricing motor, home and health insurance
- Claims triage and automated first notice of loss
- Fraud screening
- Usage-based pricing from telematics
- Reserve estimation and portfolio monitoring

## Risks and limits

- **Discriminatory pricing**: a model can raise prices for a group through correlated features, even without using a protected attribute.
- **Explanation gaps**: a customer or regulator may not be able to see why a price changed.
- **Model risk**: a model that works in one market or product can fail in another.
- **Strategic behaviour**: customers adjust what they report or how they drive once they know a device is measuring them.

## Open questions

- Whether fairness constraints can be added to pricing without destroying the risk pooling that insurance depends on.
- How to validate models whose main outcomes take years to show up.

## References

### Seminal papers

- Dal Pozzolo, A. et al. (2015). Calibrating Probability with Undersampling for Unbalanced Classification. *2015 IEEE Symposium Series on Computational Intelligence*. https://doi.org/10.1109/SSCI.2015.33 — Shows how undersampling distorts predicted probabilities on rare-event data and how to correct for it, a central issue in fraud models.
- Bhattacharyya, S. et al. (2011). Data mining for credit card fraud: A comparative study. *Decision Support Systems*. https://doi.org/10.1016/j.dss.2010.08.008 — Compares learning methods for detecting fraudulent transactions on highly imbalanced data.
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS*. https://arxiv.org/abs/1705.07874 — Introduces SHAP values, which attribute a model's prediction to its input features.

### Surveys and textbooks

- Wüthrich, M. V. & Merz, M. (2023). *Statistical Foundations of Actuarial Learning and its Applications*. Springer. https://doi.org/10.1007/978-3-031-12409-9 — Textbook connecting actuarial statistics with modern machine learning, including pricing and reserving.
- European Union. Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (AI Act). *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj — The binding text; its recitals name AI used for risk assessment and pricing in health and life insurance as a high-risk use.
