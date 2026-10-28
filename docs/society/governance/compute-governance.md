---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/hardware
  - theory/models/llm/scaling-laws
  - society/open-vs-closed
tags:
  - regulation
  - compute
  - export controls
aliases:
  - 運算治理
  - 算力治理
  - 出口管制
  - Compute governance
  - Export controls
  - Know-your-customer
---

# Compute Governance and Export Controls

Compute governance tries to regulate AI through the hardware and infrastructure that training and running models require. Its main tools are export controls on advanced chips, thresholds based on training compute, and identity checks on the cloud providers that rent out computing capacity.

!!! info "Part of Law, Policy & Governance"
    This page belongs to [Law, Policy & Governance](index.md). It explains one policy approach in detail; the parent page covers the wider legal landscape.

## Overview

Most AI policy works on models, data or uses. Compute governance works one step earlier, on the physical resources needed to build a capable model. Its argument is that compute is easier to see, measure and control than data or algorithms: it can be detected, withheld and counted, and its production depends on a small number of firms and countries. Sastry et al. (2024) make this case and also list the risks of using compute as a policy lever.

## Key concepts

- **Export control**: a legal restriction on sending specified goods, software or technology to certain countries or users. Applied to AI, it covers advanced accelerator chips and chipmaking equipment, and in some proposals access to cloud computing.
- **Training compute**: the total number of arithmetic operations used to train a model, usually counted in floating-point operations (FLOP). Heim and Koessler (2024) describe it as the metric regulators use to decide which models deserve oversight.
- **Compute threshold**: a level of training compute above which a model triggers obligations, such as notification, reporting or a presumption of extra risk.
- **Know-your-customer (KYC)**: procedures a service provider uses to verify who its customers are and to keep records. Egan and Heim (2023) propose applying the banking version of this idea to providers of compute.

## How it works

Compute governance acts through three levers.

1. **Restricting supply.** Export controls limit which chips, and which tools for making them, can be sold to a given country. Gupta et al. (2024) describe the US strategy as an attempt to keep advanced accelerators away from Chinese AI developers. The [AI Hardware](../../engineering/hardware/index.md) page describes the supply chain that makes this a chokepoint: a few designers, a few foundries and a few equipment makers.
2. **Setting thresholds.** Laws define a level of training compute that triggers extra duties. Heim and Koessler (2024) argue that training compute is currently the most suitable metric for this filter, because it correlates with capability, can be measured early and can be checked by outside parties. It is an imperfect proxy for risk, so it should start a review rather than end one.
3. **Monitoring and identifying users.** Shavit (2023) proposes that chip firmware could save snapshots of model weights for inspectors, and that the chip supply chain could be watched so that no actor gathers large numbers of untracked chips, without restricting consumer devices. Know-your-customer schemes add a further step: the provider checks who the customer is before access is granted.

These levers keep returning because compute grows quickly. Sevilla et al. (2022) found that training compute doubled roughly every six months after deep learning took off.[^1] A threshold fixed at one level becomes less selective over time, which is one reason thresholds are contested.

## Key methods

The four instruments below are compared briefly. Most real policies combine several of them.

| Instrument | Who it targets | Main advantage | Main weakness |
|---|---|---|---|
| Chip export controls (Gupta et al., 2024) | Chip suppliers and buyers abroad | Acts on a concentrated supply chain | Chips that leak out of the controlled market and efficiency gains reduce its effect |
| Compute thresholds (Heim & Koessler, 2024) | Developers training large models | Measurable before a model is deployed | A proxy for capability and risk; compute-saving techniques can avoid it |
| Hardware-enabled verification (Shavit, 2023; Brundage et al., 2020) | Chips, firmware and their owners | Lets outsiders check claims about training | Mostly still at the design stage; raises privacy and cost concerns |
| Know-your-customer for compute providers (Egan & Heim, 2023) | Customers of cloud compute | Shows who is using compute and can suspend access | Needs dynamic thresholds, record-keeping and government capacity |

## Connections

- The hardware supply chain that makes export controls possible is covered in [AI Hardware](../../engineering/hardware/index.md).
- Thresholds rely on training compute tracking capability. The empirical side of that link is in [Scaling laws and emergent abilities](../../theory/models/llm/scaling-laws/index.md).
- Open-weight models are hard to control once downloaded, which is one reason policymakers look at compute instead. See [Open versus Closed Models](../open-vs-closed/index.md).
- Neuromorphic and analogue hardware counts events or physical quantities rather than dense arithmetic. It is unclear how FLOP-based thresholds would apply to such systems; see [Spiking Neural Networks & Neuromorphic Computing](../../brain-mind/snn-neuromorphic/index.md).

## Applications

- **Export licensing.** Chip sales to restricted destinations require a government licence. Gupta et al. (2024) examine how this has worked in one case, the sale of a chip designed to comply with the rules.
- **Reporting on large training runs.** Pistillo and Villalobos (2025) describe how a 2023 US executive order instructed the Commerce Department to require reporting from developers of models above a training-compute threshold, and how the EU AI Act presumes that such models carry systemic risk.[^2] The US order has since been revoked, so the current position should be checked on the [parent page](index.md).

## Open questions

- Can a compute threshold keep its meaning as algorithms become more efficient and models use more computation at inference time?
- Can verification work without revealing a developer's data, weights or hyperparameters?
- Should access controls cover remote use of cloud compute as well as the sale of chips?

### Criticisms

- **Thresholds are shortsighted.** Hooker (2024) argues that compute thresholds, as implemented, are unlikely to reduce risk, because the link between compute and risk is uncertain and changing.
- **Thresholds have loopholes.** Pistillo and Villalobos (2025) show that fine-tuning, model reuse, model expansion and extra inference compute can raise capability while using less training compute, which could keep developers below a threshold.
- **Export controls are porous.** Gupta et al. (2024) present evidence that Chinese labs have obtained restricted chips and used software and modelling techniques to get more from weaker hardware. Their argument centres on one company's model, so it should be weighed as a strong case rather than a settled finding.
- **Broad scope has costs.** Sastry et al. (2024) warn that poorly scoped compute governance carries risks for privacy, economic activity and the concentration of power.

[^1]: Sevilla et al. (2022) report separate doubling times for each period; exact estimates depend on the sample of models.
[^2]: Both the EU presumption and the US reporting duty are set by reference to training compute. The exact figures are in the legal texts; check the current version of each law.

## References

### Seminal papers

- Sastry, G. et al. (2024). *Computing Power and the Governance of Artificial Intelligence*. arXiv preprint. https://arxiv.org/abs/2402.08797 — Argues that compute is a practical point of intervention for AI governance, and lists its uses and risks.
- Shavit, Y. (2023). *What does it take to catch a Chinchilla? Verifying Rules on Large-Scale Neural Network Training via Compute Monitoring*. arXiv preprint. https://arxiv.org/abs/2303.11341 — Proposes hardware-level monitoring so that governments can verify rules on large training runs.
- Brundage, M. et al. (2020). *Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims*. arXiv preprint. https://arxiv.org/abs/2004.07213 — Analyses ten mechanisms, including hardware-based ones, for making claims about AI systems verifiable.
- Heim, L. & Koessler, L. (2024). *Training Compute Thresholds: Features and Functions in AI Regulation*. arXiv preprint. https://arxiv.org/abs/2405.10799 — Argues that training compute is a suitable filter for regulatory oversight, and that it should not be used alone.
- Egan, J. & Heim, L. (2023). *Oversight for Frontier AI through a Know-Your-Customer Scheme for Compute Providers*. arXiv preprint. https://arxiv.org/abs/2310.13625 — Proposes that compute providers verify their customers, and discusses the design issues this raises.
- Sevilla, J. et al. (2022). *Compute Trends Across Three Eras of Machine Learning*. arXiv preprint. https://arxiv.org/abs/2202.05924 — Measures the growth of training compute across the history of machine learning, the trend data behind compute-based policy.

### Articles and documentation

- Hooker, S. (2024). *On the Limitations of Compute Thresholds as a Governance Strategy*. arXiv preprint. https://arxiv.org/abs/2407.05694 — Essay that questions whether training compute predicts risk, and recommends a better approach.
- Pistillo, M. & Villalobos, P. (2025). *Defending Compute Thresholds Against Legal Loopholes*. arXiv preprint. https://arxiv.org/abs/2502.00003 — Examines compute-saving techniques that could let developers avoid thresholds in US and EU law.
- Gupta, R., Walker, L. & Reddie, A. W. (2024). *Whack-a-Chip: The Futility of Hardware-Centric Export Controls*. arXiv preprint. https://arxiv.org/abs/2411.14425 — Presents a case study of Chinese developers working around chip export controls, and assesses the strategy.
