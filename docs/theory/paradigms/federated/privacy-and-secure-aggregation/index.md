---
related:
- theory/paradigms/unsupervised/index.md
- society/ethics/index.md
tags:
  - federated learning
  - privacy
  - secure aggregation
  - differential privacy
---

# Privacy and Secure Aggregation

Federated learning keeps raw data on devices, but model updates can still leak information about the data they came from. Privacy techniques address this in two ways. Secure aggregation lets the server see only the sum of client updates, and differential privacy limits how much any one client's data can influence the trained model.

## Overview

Two threats matter. An honest but curious server may try to recover a client's update, and a participant may infer whether a particular example was in another client's data. Secure aggregation defends against the first with cryptography, and differentially private training defends against the second by clipping and adding noise to updates. Both add cost, and the two protections combine with a trade-off in accuracy.

## Main techniques

- **Secure aggregation**: clients mask their updates with cryptographic shares so that the server learns only their sum, and it tolerates clients dropping out.
- **Differentially private SGD**: clip per-example gradients and add calibrated noise, which gives a formal privacy guarantee at a cost in accuracy.
- **Client-level privacy**: apply differential privacy to whole client updates rather than to single examples, which suits cross-device settings.
- **Collaborative training across parties**: share selected parameters across institutions without sharing records, as in privacy-preserving deep learning.

## Connections

Privacy trade-offs are part of the wider questions in [ethics and society](../../../../society/ethics/index.md). Differentially private updates interact with [federated averaging](../federated-averaging/index.md) and with the optimisation choices in [supervised learning](../../supervised/loss-functions-and-optimization/index.md).

## Applications

Medical models trained across hospitals, keyboard prediction on phones, and banking models trained across institutions that cannot share customer records.

## Open questions

Formal privacy guarantees often reduce accuracy noticeably, and the guarantees assume threat models that may not hold in practice. Auditing privacy in deployed systems is difficult.

## References

### Seminal papers

- Bonawitz et al. (2017), "Practical secure aggregation for privacy-preserving machine learning", CCS. https://doi.org/10.1145/3133956.3133982 — Protocol that lets the server learn only the sum of client updates, even when clients drop out.
- Abadi et al. (2016), "Deep learning with differential privacy", CCS, [arXiv:1607.00133](https://arxiv.org/abs/1607.00133) — Differentially private SGD, which clips and adds noise to gradients to give a formal guarantee.
- Geyer, Klein & Nabi (2017), "Differentially private federated learning: a client level perspective", [arXiv:1712.07557](https://arxiv.org/abs/1712.07557) — Applies differential privacy to whole client updates, which suits federated settings.
- Shokri & Shmatikov (2015), "Privacy-preserving deep learning", CCS. https://www.comp.nus.edu.sg/~reza/files/Shokri-CCS2015.pdf — Collaborative training in which parties share selected parameter updates instead of data.

### Surveys and textbooks

- Kairouz et al. (2021), "Advances and open problems in federated learning", Foundations and Trends in Machine Learning, [arXiv:1912.04977](https://arxiv.org/abs/1912.04977) — Survey with sections on privacy, secure aggregation and differential privacy.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- McMahan, Ramage, Talwar & Zhang (2018), "Learning differentially private recurrent language models", ICLR. https://arxiv.org/abs/1710.06963 — Trains a language model with differential privacy by adding noise to averaged user updates.
