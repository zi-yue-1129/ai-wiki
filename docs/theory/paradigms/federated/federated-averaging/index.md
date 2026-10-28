---
related:
- theory/paradigms/supervised/loss-functions-and-optimization/index.md
- engineering/training/index.md
tags:
  - federated learning
  - FedAvg
  - distributed optimisation
---

# Federated Averaging

Federated averaging is the basic algorithm of federated learning. Each participating device trains a copy of the model on its own data for a few local steps, and a server averages the resulting models. The raw data never leaves the devices, and only model updates are communicated.

## Overview

A round of training picks a subset of clients, sends them the current global model, has each run local stochastic gradient descent, and averages the returned weights, usually weighted by the number of local examples. Local steps reduce communication, but they also make the local models drift apart when the data differs between clients.

## Key ideas

- **Local updates**: several local steps per round trade extra computation on devices for fewer communication rounds.
- **Weighted averaging**: combine client models in proportion to their data sizes, which is the simplest form of aggregation.
- **Client sampling**: train on a random subset of devices each round, which keeps the cost manageable with millions of phones.
- **Proximal regularisation**: add a term that keeps local models close to the global model, which stabilises training when clients are heterogeneous.

## Connections

Federated averaging is distributed [supervised learning](../../supervised/loss-functions-and-optimization/index.md) with stochastic gradient descent on each client. Engineering details of distributed training appear in [training](../../../../engineering/training/index.md). The heterogeneity problem that local updates create is the subject of [heterogeneity and personalisation](../heterogeneity-and-personalisation/index.md).

## Applications

Next-word prediction on mobile keyboards, on-device health and activity models, and hospital networks that train a shared model without sharing patient records.

## Open questions

Averaging can slow or prevent convergence when client data is very different. Communication, client availability and fairness across devices remain practical limits.

## References

### Seminal papers

- McMahan, Moore, Ramage, Hampson & Agüera y Arcas (2017), "Communication-efficient learning of deep networks from decentralized data", AISTATS, arXiv:1602.05629 — Introduces federated averaging and shows that it trains deep networks with far less communication.
- Konečný, McMahan, Yu, Richtárik, Suresh & Bacon (2016), "Federated learning: strategies for improving communication efficiency", arXiv:1610.05492 — Early paper that proposes structured and sketched updates to reduce communication.
- Li, Sahu, Zaheer, Sanjabi, Talwalkar & Smith (2020), "Federated optimization in heterogeneous networks", MLSys, arXiv:1812.06127 — FedProx, a proximal extension of federated averaging for heterogeneous clients.

### Surveys and textbooks

- Kairouz et al. (2021), "Advances and open problems in federated learning", Foundations and Trends in Machine Learning, arXiv:1912.04977 — Broad survey of federated learning with a list of open problems.
- Yang, Liu, Chen & Tong (2019), "Federated machine learning: concept and applications", ACM Transactions on Intelligent Systems and Technology, arXiv:1902.04885 — Introduces the taxonomy of horizontal and vertical federated learning.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Bonawitz et al. (2019), "Towards federated learning at scale: system design", SysML. No link checked.
