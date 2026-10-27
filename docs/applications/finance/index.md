---
related:
- foundations/paradigms/online
- foundations/paradigms/federated
- society/ethics
- applications/cybersecurity
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
- **Backtest overfitting**: testing many strategies guarantees some look good by chance (López de Prado's deflated Sharpe ratio)
- **Adversaries**: fraudsters adapt to detectors
- **Explainability requirements**: e.g. US Equal Credit Opportunity Act adverse-action notices; EU AI Act classifies creditworthiness assessment as high-risk

## LLMs in finance

- BloombergGPT (2023) — a finance-specific LLM — was soon matched by general models on many tasks, a common pattern
- Uses: summarising filings and calls, research assistants, code for quants, compliance review, customer support
- Risks: hallucinated numbers, data leakage, herding if many firms use similar models

## Systemic risk

Regulators (FSB, BIS, IMF) warn that widespread use of similar models and vendors could increase correlation, procyclicality and concentration risk; flash-crash dynamics show how automated strategies can interact.

## Resources

- López de Prado, *Advances in Financial Machine Learning*
- Dixon, Halperin & Bilokon, *Machine Learning in Finance*
- Financial Stability Board (2024), "The Financial Stability Implications of Artificial Intelligence"
- [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) and FinRL open-source projects
