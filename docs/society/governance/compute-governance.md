---
status: draft
last_reviewed: 2026-10-28
related:
  - society/governance
  - society/safety-alignment
  - theory/evaluation
tags:
  - compute
  - export controls
  - AI governance
aliases:
  - 算力治理
  - 運算治理
  - 出口管制
  - Export controls
---

# Compute governance and export controls

Compute governance treats the computing power used to train and run AI systems as a point where policy can act. Because chips, data centres and training runs are physical, concentrated and countable, governments have begun to use them as levers. This page explains why compute is attractive as a lever, how export controls and regulatory thresholds use it, and what critics say.

## Overview

Training a frontier model requires large amounts of computing power, which is produced by a small number of chip designers, foundries and equipment makers. Sastry and colleagues argue that compute is a strong point of intervention for AI governance because it has three properties. It is **detectable**, since large clusters are visible. It is **excludable**, since access can be restricted to some actors and not others. And it is **quantifiable**, so a rule can refer to a number [(Sastry et al., 2024)](https://arxiv.org/abs/2402.08797).

## Key concepts

- **Compute**: the number of arithmetic operations a computer performs, usually counted in floating-point operations (FLOP). Training compute is the total used to train one model.
- **Export controls**: government restrictions on selling or transferring advanced chips, chipmaking equipment or model weights to particular countries or entities.
- **Compute threshold**: a number of FLOP above which a legal duty applies, such as a safety evaluation or a notification.
- **Know-your-customer (KYC) for compute**: checks on who is renting large amounts of computing capacity, for example from cloud providers.

## How it works

Governments act on compute at several points in the supply chain. Export controls restrict who can buy advanced chips and the equipment to make them. Regulations set thresholds so that the largest training runs face more obligations. Some proposals would require cloud providers to verify the identity of customers who rent large clusters.

The rationale for thresholds is that the most capable models are expensive to train, so a compute line can capture a small number of developers without regulating every system. Sastry and colleagues note the risk that poorly scoped compute rules could affect privacy, economic activity and the concentration of power, so the design of the threshold matters as much as its existence [(Sastry et al., 2024)](https://arxiv.org/abs/2402.08797).

## Regulatory thresholds

The EU AI Act sets obligations for general-purpose AI models. A model is presumed to pose systemic risk when its cumulative training compute exceeds 10^25 floating-point operations, and such models face additional duties such as evaluation and incident reporting [(Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj). The threshold is a proxy: it counts compute and does not directly measure capability or risk.

Frontier-AI proposals in the policy literature use similar logic. Anderljung and colleagues describe frontier AI regulation that would require developers of the most capable models to manage emerging risks, with registration, evaluation and safety standards as possible tools [(Anderljung et al., 2023)](https://arxiv.org/abs/2307.03718). Shevlane and colleagues argue that evaluations for dangerous capabilities are needed before deployment, which is a precondition for any threshold-based regime to be useful [(Shevlane et al., 2023)](https://arxiv.org/abs/2305.15324).

## Export controls

The United States has restricted exports of advanced computing chips and chipmaking tools to some countries since 2022, and has changed the scope of those restrictions several times. Their stated aims combine national security with the goal of slowing the spread of the most capable systems. Trend data show how quickly the compute used in machine learning has grown, which is why many policymakers treat the frontier as a moving target [(Sevilla et al., 2022)](https://arxiv.org/abs/2202.05924).

## Criticisms

Critics point to several problems. Thresholds can become outdated as efficiency improves, so a model may need less compute to reach the same capability later. Export controls can push development toward other suppliers or toward smaller, less visible clusters. Compute rules also say little about data, algorithms or how a system is deployed, so they cannot replace safety evaluations. Finally, governance by compute could concentrate influence in the few firms that control chips and cloud capacity.

## Connections

Compute governance connects to the safety discussion of [AI safety and alignment](../safety-alignment/index.md), to the evaluation methods in [Evaluation](../../theory/evaluation/index.md), and to the energy questions in [Environmental impact](../environment/index.md). Its wider legal context is in [Law, policy and governance](index.md).

## Applications

Export controls are applied by trade agencies, and thresholds are applied by regulators to model developers. Cloud providers apply customer checks when they sell large capacity. Research groups use the same counting logic to estimate the size of training runs, which lets outside observers compare systems.

## Open questions

- Will compute thresholds remain a useful signal as algorithms become more efficient?
- Can verification of compute use be made reliable without invasive monitoring?
- How should controls balance security goals with access for researchers and firms in other countries?
- Should governance shift toward evaluations of what models can do rather than how much compute they used?

## References

### Seminal papers

- Sastry, Heim, Belfield, Anderljung, Brundage, Hazell, O'Keefe, Hadfield, Ngo, Pilz, Gor, Bluemke, Shoker, Egan, Trager, Avin, Weller, Bengio and Coyle, *Computing Power and the Governance of Artificial Intelligence* (2024). https://arxiv.org/abs/2402.08797 — Argues that compute is a strong lever for AI governance and discusses its risks.
- Shevlane, Farquhar, Garfinkel, Phuong, Whittlestone, Leung, Kokotajlo, Marchal, Anderljung, Kolt, Ho, Siddarth, Avin, Hawkins, Kim, Gabriel, Bolina, Clark, Bengio, Christiano and Dafoe, *Model evaluation for extreme risks* (2023). https://arxiv.org/abs/2305.15324 — Proposes dangerous-capability evaluations as a basis for oversight.
- Anderljung, Barnhart, Korinek, Leung, O'Keefe, Whittlestone, Avin, Brundage and colleagues, *Frontier AI Regulation: Managing Emerging Risks to Public Safety* (2023). https://arxiv.org/abs/2307.03718 — Sets out a regulatory approach for frontier models.
- Sevilla, Heim, Ho, Besiroglu, Hobbhahn and Villalobos, *Compute Trends Across Three Eras of Machine Learning* (2022). https://arxiv.org/abs/2202.05924 — Measures the growth of training compute across the history of machine learning.

### Articles and documentation

- European Union, *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*, Official Journal of the European Union (2024). https://eur-lex.europa.eu/eli/reg/2024/1689/oj — Sets the compute-based presumption of systemic risk for general-purpose AI models.
