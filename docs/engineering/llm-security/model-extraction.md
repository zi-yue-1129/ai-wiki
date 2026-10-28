---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/model-compression/knowledge-distillation
  - society/open-vs-closed
  - society/privacy
tags:
  - security
  - knowledge distillation
  - large language models
aliases:
  - Model extraction
  - Model stealing
  - Model theft
  - 模型竊取
  - 模型萃取
  - 蒸餾攻擊
---

# Model Extraction and Theft

Model extraction is an attack in which someone who can only query a deployed model builds a copy of its behaviour, or recovers part of its parameters, without receiving the weights, which threatens both the owner's investment and the model's confidentiality.

## Overview

Training a large model is expensive, and many providers recover that cost by selling API access. The API is also the attack surface: each reply reveals a label, a probability or a sentence of text, and an adversary who collects enough replies can train a second model on them.

Tramèr et al. (2016) showed that simple prediction services could be copied with near-perfect fidelity. Language models raise the stakes, because their replies are rich text, and the same procedure, distillation, is an ordinary method when the teacher is one's own model.

Two aims are worth separating. *Functionality stealing* aims at a copy that behaves similarly. *Parameter extraction* aims at the weights, which needs outputs with a particular structure.

## Key concepts

- **Victim and substitute**: the deployed model and the copy the adversary trains.
- **Fidelity and accuracy**: fidelity is how often the copy matches the victim; accuracy is how well it does the true task.
- **Soft outputs**: probabilities or logits, which carry more information than a single label.
- **Distillation**: training a student on a teacher's outputs, introduced by Hinton et al. (2015). See [Knowledge distillation](../../theory/model-compression/knowledge-distillation/index.md).

## How it works

Most attacks follow one loop: send queries, record the replies, train a substitute on the pairs, and measure how closely it matches the victim.

```mermaid
flowchart LR
  Q[Chosen queries] --> V[Victim API]
  V --> O[Labels, probabilities or text]
  O --> D[Query and reply pairs]
  D --> S[Substitute trained to match]
  S --> E[Measured fidelity and accuracy]
```

The substitute $f_\theta$ is fitted to minimise a loss over the queries $x_i$, where $f_V$ is the victim:

$$\hat\theta = \arg\min_\theta \sum_i \mathcal{L}\big(f_\theta(x_i),\, f_V(x_i)\big)$$

Three choices decide how well this works. The first is the query distribution: Orekondy et al. (2019) found that random images from an unrelated distribution could still yield a working copy of an image API. The second is the output, since probabilities reveal more than labels. The third is the architecture, which the substitute need not share with the victim.

Gudibande et al. (2023) fine-tuned open models on replies from a proprietary chat model. The imitators copied its style and looked competitive to crowd raters, but closed little of the gap on tasks the imitation data did not cover.

Carlini et al. (2024) pursued parameter recovery. The logit vectors a transformer produces for many prompts lie in a subspace of dimension at most its hidden size. Linear algebra on such outputs can reveal that dimension and recover the final embedding projection up to symmetries.[^1]

## Key methods

The variants below differ in what the adversary learns and what the API must return. None has a page of its own.

| Variant | What the adversary gets | What the API returns | Main limit |
|---|---|---|---|
| Label-only substitute (Papernot et al., 2017) | Adversarial examples that transfer to the victim | Labels | Depends on the substitute's fit |
| Confidence-based extraction (Tramèr et al., 2016) | Near-perfect copies of simple models | Confidence values | Hiding confidences is not enough |
| Text imitation (Krishna et al., 2020; Gudibande et al., 2023) | Copies that match style and some behaviour | Generated text | Style copies easily; facts do not |
| Log-probability recovery (Carlini et al., 2024) | The final projection layer of a production model | Log-probabilities | Recovers one layer only |

## Defences

No single control is enough, and most have been tested only in part.

- **Limit the output.** Returning only the top label removes information per query, but Tramèr et al. (2016) show this is not sufficient.
- **Detect query patterns.** PRADA (Juuti et al., 2019) flags clients whose queries depart from benign use. Its evaluation predates adaptive attackers.
- **Rate limits and access control.** Limits on volume and accounts raise the cost of a campaign, but an attacker can spread queries across accounts.
- **Perturb the replies.** Orekondy et al. (2020) perturb predictions to mislead an attacker's training, at a small cost to benign users.
- **Watermarks and fingerprints.** Peng et al. (2023) implant a backdoor in embeddings so that a stolen embedding model can be checked. Krishna et al. (2020) found API watermarking ineffective against more sophisticated adversaries. Xu et al. (2024) implant a private instruction trigger as an LLM fingerprint. Maini et al. (2021) test whether a suspect model has learned from the owner's training data.[^2]

## Connections

- **Distillation.** Extraction and [knowledge distillation](../../theory/model-compression/knowledge-distillation/index.md) share a mechanism and differ in consent and ownership. See also [LLM distillation](../../theory/model-compression/knowledge-distillation/llm-distillation/index.md).
- **Privacy attacks.** [Training data extraction](../../society/privacy/training-data-extraction.md) recovers memorised text; model extraction recovers behaviour or weights. Compare [membership inference](../../society/privacy/membership-inference.md).
- **Backdoors.** Fingerprints and watermarks rely on backdoors planted on purpose, the mechanism in [data poisoning and backdoors](data-poisoning-and-backdoors.md).
- **Closed and open models.** Access control separates many closed providers from open-weight releases, and extraction blurs that line. See [Open versus closed models](../../society/open-vs-closed/index.md).
- **Guardrails.** A copy made elsewhere escapes the [guardrails](guardrails.md) of the original service.

## Applications

- **Competing products** that imitate a commercial model's behaviour cheaply (Gudibande et al., 2023).
- **Evasion.** A substitute gives an attacker a stand-in for crafting adversarial examples that transfer to the victim (Papernot et al., 2017).

## Open questions

- **Scope of parameter recovery.** Carlini et al. (2024) recover one projection layer. Whether comparable methods recover deeper structure is not known.
- **Legitimate or extractive?** Competitor traffic can look like ordinary use, so query-based detectors may not separate the two.
- **Capability gap.** Whether imitation can close a gap on tasks outside the imitation data is unsettled; Oliynyk et al. (2023) survey the field.
- **Durability and law.** Fine-tuning may remove marks, and the legal status of model outputs under terms of service and copyright law is unsettled.

## References

### Seminal papers

- Tramèr, F. et al. (2016). *Stealing Machine Learning Models via Prediction APIs*. USENIX Security Symposium. https://arxiv.org/abs/1609.02943 — Near-perfect extraction of simple models, including from live cloud prediction services.
- Papernot, N. et al. (2017). *Practical Black-Box Attacks against Machine Learning*. ACM ASIA CCS. https://arxiv.org/abs/1602.02697 — Trains a substitute on labels from a remote DNN and shows its adversarial examples transfer.
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — Introduces distillation, training a small model on a larger model's soft outputs.
- Orekondy, T., Schiele, B. & Fritz, M. (2019). *Knockoff Nets: Stealing Functionality of Black-Box Models*. CVPR. https://arxiv.org/abs/1812.02766 — Shows that random out-of-distribution query images can yield a functional copy of an image API.
- Krishna, K. et al. (2020). *Thieves on Sesame Street! Model Extraction of BERT-based APIs*. ICLR. https://arxiv.org/abs/1910.12366 — Extracts BERT-based NLP APIs using random word sequences as queries, and tests two defences.
- Carlini, N. et al. (2024). *Stealing Part of a Production Language Model*. ICML. https://arxiv.org/abs/2403.06634 — Recovers the embedding projection layer of production language models through API access, at low cost.
- Gudibande, A. et al. (2023). *The False Promise of Imitating Proprietary LLMs*. arXiv:2305.15717. https://arxiv.org/abs/2305.15717 — Finds that imitating a proprietary chat model copies its style more than its factual capability.
- Juuti, M. et al. (2019). *PRADA: Protecting against DNN Model Stealing Attacks*. IEEE EuroS&P. https://arxiv.org/abs/1805.02628 — Detects extraction by analysing the distribution of each client's consecutive queries.
- Orekondy, T., Schiele, B. & Fritz, M. (2020). *Prediction Poisoning: Towards Defenses Against DNN Model Stealing Attacks*. ICLR. https://arxiv.org/abs/1906.10908 — Perturbs predictions to mislead an attacker's training while barely affecting benign users.
- Peng, W. et al. (2023). *Are You Copying My Model? Protecting the Copyright of Large Language Models for EaaS via Backdoor Watermark*. arXiv:2305.10036. https://arxiv.org/abs/2305.10036 — Implants a backdoor watermark in embeddings so that a stolen embedding model can be verified.
- Xu, J. et al. (2024). *Instructional Fingerprinting of Large Language Models*. arXiv:2401.12255. https://arxiv.org/abs/2401.12255 — Implants a private instruction trigger as a fingerprint, tested on eleven popular LLMs.
- Maini, P., Yaghini, M. & Papernot, N. (2021). *Dataset Inference: Ownership Resolution in Machine Learning*. ICLR. https://arxiv.org/abs/2104.10706 — Tests whether a suspect model holds knowledge of the owner's training data, as an ownership defence.

### Surveys and textbooks

- Oliynyk, D., Mayer, R. & Rauber, A. (2023). *I Know What You Trained Last Summer: A Survey on Stealing Machine Learning Models and Defences*. ACM Computing Surveys. https://arxiv.org/abs/2206.08451 — Taxonomy of extraction attacks and defences, with an analysis of which defences current attacks weaken.

[^1]: Carlini et al. (2024) report extracting the full projection matrix of two OpenAI models for under 20 US dollars, per the abstract.

[^2]: Maini et al. (2021) report owner confidence above 99% from 50 training points, per the abstract.
