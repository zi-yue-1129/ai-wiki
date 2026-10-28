---
related:
- foundations/paradigms/federated/privacy-and-secure-aggregation/index.md
- foundations/paradigms/transfer/index.md
tags:
  - federated learning
  - vertical federated learning
  - cross-silo
---

# Vertical and Cross-silo Federated Learning

Most federated learning work assumes many phones that hold the same features but different users, which is called horizontal federated learning. Cross-silo settings are different: a few organisations, such as banks or hospitals, each hold different features about overlapping people. Vertical federated learning trains a model across these feature partitions without any party sharing its raw records.

## Overview

In vertical learning, parties first align their records by identifiers, often through private entity resolution, and then train jointly on their own feature blocks. Intermediate values are exchanged under encryption or secret sharing, and each party keeps its own features. The cost is higher than horizontal training because every step needs cross-party computation.

## Main approaches

- **Entity resolution and alignment**: find shared individuals without revealing the non-shared ones, usually with private set intersection or hashed identifiers.
- **Vertical logistic regression and linear models**: train with homomorphic encryption or secret sharing so that each party computes its share of the gradient.
- **Split learning and embeddings**: each party trains its own lower layers and sends embeddings to a shared top model, which limits what is exchanged.
- **Cross-silo secure training**: apply secure aggregation and privacy techniques to a small number of reliable, well-connected participants.

## Connections

Cross-silo settings use the protections described in [privacy and secure aggregation](../privacy-and-secure-aggregation/index.md). The idea of learning from distributed sources with different features is related to [transfer learning](../../transfer/index.md), and the joint models are ordinary [supervised learning](../../supervised/index.md) problems.

## Applications

Credit scoring across banks with different customer data, medical research across hospitals that hold different test results for shared patients, and advertising models across companies with different user signals.

## Open questions

Entity alignment leaks information, and encrypted training is slow for large models. Incentives for participation and fair sharing of value between parties are as important as the technical protocol.

## References

### Seminal papers

- Hardy et al. (2017), "Private federated learning on vertically partitioned data via entity resolution and additively homomorphic encryption", arXiv:1711.10677 — Trains a vertical logistic regression with entity resolution and homomorphic encryption.
- Shokri & Shmatikov (2015), "Privacy-preserving deep learning", CCS. https://www.comp.nus.edu.sg/~reza/files/Shokri-CCS2015.pdf — Early collaborative training in which parties share selected parameters rather than data.
- Bonawitz et al. (2017), "Practical secure aggregation for privacy-preserving machine learning", CCS, arXiv:1611.04482 — Secure aggregation protocol that applies to cross-party gradient sums.

### Surveys and textbooks

- Yang, Liu, Chen & Tong (2019), "Federated machine learning: concept and applications", ACM Transactions on Intelligent Systems and Technology, arXiv:1902.04885 — Introduces the horizontal, vertical and transfer categories of federated learning.
- Kairouz et al. (2021), "Advances and open problems in federated learning", Foundations and Trends in Machine Learning, arXiv:1912.04977 — Survey that covers cross-silo settings and their open problems.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

