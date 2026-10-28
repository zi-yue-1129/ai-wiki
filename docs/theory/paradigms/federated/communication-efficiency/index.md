---
related:
- theory/paradigms/federated/federated-averaging/index.md
- engineering/training/index.md
tags:
  - federated learning
  - communication efficiency
  - gradient compression
---

# Communication Efficiency

In federated learning the network connection to each client is often the bottleneck, not computation. Communication-efficient methods reduce how many rounds are needed and how many bytes each round sends, usually by compressing model updates or by sending them less often.

## Overview

Each round sends model updates from clients to the server and back. Compression can quantise updates to fewer bits, sparsify them so that only the largest values are sent, or use structured low-dimensional updates. Accuracy usually drops as compression increases, so the aim is to reach the same accuracy with fewer bytes overall.

## Main techniques

- **Structured and sketched updates**: restrict updates to a structured form, such as a low-rank or random-mask subspace, so they can be sent in fewer values.
- **Quantisation**: send gradients with a small number of bits, using an encoding that keeps the expected update unbiased.
- **Gradient sparsification with local accumulation**: send only the largest gradient values and keep the rest locally until they grow large enough.
- **Fewer communication rounds**: do more local computation per round, the basic trade-off of federated averaging.

## Connections

These methods build on the averaging scheme of [federated averaging](../federated-averaging/index.md). The same compression ideas are used for speeding up distributed training in [engineering: training](../../../../engineering/training/index.md). Sparsity and quantisation of model weights also appear in the parameter-efficient methods of [transfer learning](../../transfer/fine-tuning-and-adaptation/index.md).

## Applications

Phones on slow or metered networks, sensors that send updates over low-bandwidth radio, and clinics with limited connectivity that still need to take part in joint training.

## Open questions

Compression interacts with privacy and with heterogeneous clients, and its effect on convergence is not fully understood. Measuring real communication cost, including overheads and retries, is harder than counting bytes in simulations.

## References

### Seminal papers

- Konečný et al. (2016), "Federated learning: strategies for improving communication efficiency", arXiv:1610.05492 — Proposes structured and sketched updates that reduce the bytes sent per round.
- Alistarh, Grubic, Li, Tomioka & Vojnovic (2017), "QSGD: communication-efficient SGD via gradient quantization and encoding", NeurIPS, arXiv:1610.02132 — Quantises gradients with an unbiased encoding that trades accuracy for communication.
- Lin, Han, Mao, Wang & Dally (2018), "Deep gradient compression: reducing the communication bandwidth for distributed training", ICLR, arXiv:1712.01887 — Sparsifies gradients and accumulates the unsent values locally, which keeps accuracy high at high compression.

### Surveys and textbooks

- Kairouz et al. (2021), "Advances and open problems in federated learning", Foundations and Trends in Machine Learning, arXiv:1912.04977 — Survey with a section on communication costs and compression.
- Yang, Liu, Chen & Tong (2019), "Federated machine learning: concept and applications", ACM Transactions on Intelligent Systems and Technology, arXiv:1902.04885 — Overview that discusses the communication constraints of federated systems.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Bernstein, Wang, Azizzadenesheli & Anandkumar (2018), "signSGD: compressed optimisation for non-convex problems", ICML. No link checked.
