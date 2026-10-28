---
status: draft
last_reviewed: 2026-10-28
related:
  - society/governance
  - society/safety-alignment
  - start/open-source-survey
tags:
  - open source
  - open weights
  - release policy
aliases:
  - 開放權重
  - 開源模型
  - 封閉模型
  - Open-weight models
  - Open-source AI
---

# Open versus Closed Models

A model can be released in very different ways. It can be kept behind an API or a product, released with its weights for anyone to download under a licence with conditions, or released with its code, weights and data information under an open-source licence. These choices decide who can study, adapt and audit a model, and who can misuse it. This page covers the distinction, the arguments on each side, and what the main definitions require.

## Overview

The debate is not only about whether software is free. A closed model can be used but not inspected or changed. An open-weight model can be run and fine-tuned on local hardware, but its training data, code and usage terms may be partly withheld. A fully open model makes most of its parts available, which makes it easier to reproduce and harder to monitor once copies have spread.

Open-source software resources, such as courses and tools, are a separate question. They are surveyed in [Open-Source Resource Survey](../../start/open-source-survey/index.md) and are not repeated here.

## Key concepts

- **Closed model**: the weights are not released. People use the model through an API or a product, and the provider can monitor and change it.
- **Open-weight model**: the weights can be downloaded. The licence and use policy vary, and the code or training data may not be released.
- **Open-source AI**: under the Open Source AI Definition 1.0 (2024), the system must allow people to use it for any purpose, study it, modify it and share it, and it must be available with data information, code and parameters in the form preferred for modification.
- **Licence**: the legal terms of use. Released weights do not by themselves mean an open licence.

## How it works

Release policy changes three things.

1. **Access.** Researchers and developers can inspect a model, fine-tune it and run it locally when the weights are available. A closed model limits this to what the provider allows.
2. **Distribution.** Once weights are downloaded, the people who hold them control where and how the model runs. The provider cannot easily recall them.
3. **Monitoring.** A provider can watch and restrict usage of an API. For downloaded weights, that control is much weaker. Kapoor et al. (2024) describe open foundation models as easier to adapt and harder to monitor, and they count both as sources of advantage and danger.

## Release positions

The table compares the main positions in the literature. The positions are arguments about policy, not algorithms, so each is summarised here rather than given its own method page.

| Position | Main claim | Source |
|---|---|---|
| Open release by default | Open models bring innovation, competition, transparency and a more distributed share of decision-making power, and their extra risk should be judged at the margin | [Kapoor et al. (2024)](https://arxiv.org/abs/2403.07918) |
| Restrict the most capable models | For some powerful models expected in the near future, the risks could outweigh the benefits, so they should not be released openly at first; alternative sharing methods should be explored | [Seger et al. (2023)](https://arxiv.org/abs/2311.09227) |
| Define openness precisely | Open-source AI requires data information, code and parameters, so that a skilled person can modify the system | [Open Source AI Definition 1.0 (2024)](https://opensource.org/ai) |
| Measure transparency | Developers disclose too little about data, compute, distribution and downstream impact, and an index can make this visible | [Bommasani et al. (2023)](https://arxiv.org/abs/2310.12941) |

## Responses

| Approach | What it does | Limits |
|---|---|---|
| Staged or restricted release | Releases the most capable models gradually or under controlled access | Hard to judge the risks in advance; may reduce the benefits of openness |
| Open definitions | Gives a shared test of what counts as open-source AI | A definition does not settle licence terms or usage policies |
| Transparency indices | Scores developers on what they disclose | Measures disclosure, not the safety of the model itself |
| Marginal-risk analysis | Asks whether an open release adds risk beyond existing technology | Current evidence is not yet enough to judge the added risk for misuse such as cyberattacks or bioweapons |

Regulation also treats open release as a policy question. See [Law, Policy & Governance](../governance/index.md) for how the rules differ across jurisdictions.

## Connections

- Risks of misuse and loss of control are discussed in [Safety & Alignment](../safety-alignment/index.md). Open release is one of the main ways those risks are argued about.
- The governance side, including reporting duties and standards, is covered in [Law, Policy & Governance](../governance/index.md).
- Foundation models, the category that most open-weight releases belong to, are introduced by Bommasani et al. (2021) (see References).

## Applications

- **Research on model internals** needs access to weights, for example for interpretability work.
- **Local deployment** of a model where data cannot leave the premises.
- **Adaptation to languages or domains** that a closed provider does not serve well, through fine-tuning of open weights.

## Open questions

- How should marginal risk be measured for open models, given the evidence that exists today?
- Can a model be released in stages or under restrictions without losing the benefits that Kapoor et al. (2024) describe?
- Should openness depend on the weights alone, or also on the data information and code that the Open Source AI Definition asks for?

## References

### Seminal papers

- Bommasani, R. et al. (2021). On the opportunities and risks of foundation models. arXiv:2108.07258. https://arxiv.org/abs/2108.07258 — Names foundation models, large models adapted to many tasks, and sets out their opportunities and risks; the abstract argues that their flaws spread to every downstream application.
- Kapoor, S. et al. (2024). On the societal impact of open foundation models. arXiv:2403.07918. https://arxiv.org/abs/2403.07918 — Analyses the benefits and risks of openly released foundation models, using a marginal-risk framework.
- Seger, E. et al. (2023). Open-sourcing highly capable foundation models. arXiv:2311.09227. https://arxiv.org/abs/2311.09227 — Argues that some powerful models may be too risky to release openly, and explores alternative ways to share them.
- Bommasani, R. et al. (2023). The Foundation Model Transparency Index. arXiv:2310.12941. https://arxiv.org/abs/2310.12941 — Scores major developers on 100 transparency indicators and finds that disclosure is shrinking.

### Articles and documentation

- Open Source Initiative. *The Open Source AI Definition, version 1.0* (2024). https://opensource.org/ai — Defines the freedoms and the components an AI system must provide to be called open source.
