---
related:
- theory/paradigms/online
- theory/paradigms/federated
- society/ethics
- applications/cybersecurity
aliases:
  - 金融
  - 財務
---

# Finance

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Fraud detection | Gradient-boosted trees, graph neural networks over transaction networks, anomaly detection | One of the oldest and most successful ML uses |
| Credit scoring and underwriting | Logistic regression, boosting; alternative data | Regulated; explanations required for adverse decisions |
| Anti-money laundering (AML) / KYC | Network analysis, entity resolution, document AI | High false-positive rates are a major cost |
| Algorithmic and quantitative trading | Statistical arbitrage, ML signals, RL for execution | Low signal-to-noise; overfitting and regime change dominate |
| Market making and execution | Optimal execution, RL, microstructure models | |
| Risk management | Stress testing, VaR models, scenario generation | Model-risk management (SR 11-7 in the US) |
| Customer service and advice | Chatbots, robo-advisors, LLM copilots for advisers | Suitability and disclosure rules apply |
| Document processing | Earnings calls, filings, contracts, insurance claims | LLMs widely adopted |
| Insurance | Pricing, claims triage, telematics | Fairness and discrimination concerns |

## Why finance is hard for ML

- **Non-stationarity**: relationships change as markets adapt — including to the models themselves
- **Low signal-to-noise**: tiny predictable components
- **Backtest overfitting**: testing many strategies guarantees some look good by chance (Bailey & López de Prado, 2014)
- **Adversaries**: fraudsters adapt to detectors
- **Explainability requirements**: lending and insurance rules in many jurisdictions require reasons for adverse decisions

## LLMs in finance

- BloombergGPT (Wu et al., 2023) is a finance-specific LLM.
- Uses: summarising filings and calls, research assistants, code for quants, compliance review, customer support
- Risks: hallucinated numbers, data leakage, herding if many firms use similar models

## Systemic risk

Widespread use of similar models and vendors could increase correlation, procyclicality and concentration risk, and automated strategies can interact in flash-crash dynamics.

## Key methods

Three methods are most relevant here. Each links to the page that explains it.

- [Graph neural networks](../../theory/models/gnn/message-passing/index.md): message passing over transaction networks, used to flag suspicious accounts (Weber et al., 2019).
- [Anomaly detection](../../theory/paradigms/unsupervised/anomaly-detection/index.md): models of normal activity that flag deviations, used for fraud detection.
- [Online learning](../../theory/paradigms/online/index.md): models updated as data arrive, a response to the non-stationarity of markets.

## References

### Seminal papers

- Weber et al. (2019). Anti-Money Laundering in Bitcoin: Experimenting with Graph Convolutional Networks for Financial Forensics. arXiv. https://arxiv.org/abs/1908.02591 — Graph convolutional networks for detecting illicit transactions in Bitcoin.
- Chen & Guestrin (2016). XGBoost: A Scalable Tree Boosting System. arXiv. https://arxiv.org/abs/1603.02754 — Gradient-boosted trees, the workhorse of fraud and credit models.
- Wu et al. (2023). BloombergGPT: A Large Language Model for Finance. arXiv. https://arxiv.org/abs/2303.17564 — A finance-specific large language model trained on financial and general data.
- Bailey & López de Prado (2014). The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality. *The Journal of Portfolio Management*. https://doi.org/10.3905/jpm.2014.40.5.094 — Adjusts Sharpe ratios for the number of strategies tested.

### Surveys and textbooks

- Dixon, Halperin & Bilokon (2020). *Machine Learning in Finance*. Springer. https://doi.org/10.1007/978-3-030-41068-1 — Textbook on machine learning methods used in finance.
