---
related:
- theory/paradigms/transfer/fine-tuning-and-adaptation/index.md
- theory/paradigms/meta-learning/optimisation-based/index.md
tags:
  - federated learning
  - non-IID data
  - personalisation
---

# Heterogeneity and Personalisation

Devices and institutions rarely hold data drawn from the same distribution. One user's photos or one hospital's patients differ from another's, and this non-IID data makes local updates drift and the global model fit some clients better than others. Methods in this subtopic correct the drift, or give each client a model adapted to its own data.

## Overview

Heterogeneity affects both optimisation and fairness. Local steps push each client toward its own optimum, so averaging can converge slowly or to a poor point. Personalisation accepts that a single global model may be the wrong target, and it builds client-specific models on top of shared knowledge.

## Main approaches

- **Proximal and drift-correcting methods**: keep local updates close to the global model (FedProx), or subtract an estimate of each client's drift using control variates (SCAFFOLD).
- **Analysis of non-IID data**: studies how label and feature skew degrade federated averaging, and which settings are most harmful.
- **Personalised federated learning**: fine-tune the global model on each client, or learn a shared representation with client-specific heads.
- **Meta-learning for personalisation**: use gradient-based meta-learning so that each client adapts quickly from the shared initialisation.

## Connections

Personalisation is closely related to [fine-tuning and adaptation](../../transfer/fine-tuning-and-adaptation/index.md) in transfer learning, and its initialisation idea follows [optimisation-based meta-learning](../../meta-learning/optimisation-based/index.md). The basic averaging algorithm is in [federated averaging](../federated-averaging/index.md).

## Applications

Keyboard and recommendation models that adapt to each user, hospital networks where each site has a different patient mix, and sensor models that must work across different devices and environments.

## Open questions

It is hard to measure heterogeneity in practice, and personalised models can be unfair to clients with little data. Trade-offs between personalisation, privacy and communication are not well understood.

## References

### Seminal papers

- Li, Sahu, Zaheer, Sanjabi, Talwalkar & Smith (2020), "Federated optimization in heterogeneous networks", MLSys, arXiv:1812.06127 — FedProx, which limits client drift with a proximal term in local training.
- Karimireddy, Kale, Mohri, Reddi, Stich & Suresh (2020), "SCAFFOLD: stochastic controlled averaging for federated learning", ICML, arXiv:1910.06378 — Uses control variates to correct the drift of each client's local updates.
- Zhao, Li, Lai, Suda, Civin & Chandra (2018), "Federated learning with non-IID data", arXiv:1806.00582 — Shows that label skew across clients can reduce accuracy substantially, and studies a small amount of shared data as a remedy.
- McMahan et al. (2017), "Communication-efficient learning of deep networks from decentralized data", AISTATS, arXiv:1602.05629 — The federated averaging paper, whose experiments include non-IID partitions.

### Surveys and textbooks

- Kairouz et al. (2021), "Advances and open problems in federated learning", Foundations and Trends in Machine Learning, arXiv:1912.04977 — Survey that discusses heterogeneity and personalisation as open problems.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Tan et al. (2022), "Towards personalized federated learning", IEEE Transactions on Neural Networks and Learning Systems. No link checked.
