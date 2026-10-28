---
references: not-required  # lists and meta pages cite through their entries
last_reviewed: 2026-10-28
tags:
  - large language models
  - transformers
aliases:
  - 主要模型目錄
  - 主要模型
  - Major models
  - Model catalogue
---

# Catalogue of Major Models

A model-card style list of the large language model families that most readers meet, grouped by vendor. Each row gives the release month, the size class, the openness and a one-line note, and links to the report that supports the row. Rows whose source could not be checked are left out, and the page gives no benchmark scores.

## Overview

The tables below group models by family: GPT, Claude, Gemini (with the open Gemma line), Llama, Qwen, DeepSeek, Mistral and a set of other models. Each family has its own table, so the rows can be compared within a family before comparing across families.

The columns mean the following:

- **Released** is the month the cited report was first posted to arXiv, or the publication date of the vendor's announcement for the Claude models. In most cases this is within days of public release, but the two dates are not always the same.
- **Size class** is the parameter count given in the cited source. Where a source gives no count, the cell says so. For mixture-of-experts (MoE) models both the total and the active count are shown, because the active count is what each token uses.
- **Openness** states what the source says about access, as described in the next section.
- **Source** links to the report or announcement used for the row.

Model names change quickly and new versions appear often. The list therefore records what each cited source says and does not claim to be complete. For current comparisons, use a live leaderboard, and check the vendor's own page for the latest versions. The overview of the [LLM topic](../../theory/models/llm/index.md) lists the families in the same broad groups.

## Key concepts

- **Open weights**: the trained parameters can be downloaded and run. The licence may still restrict commercial use, so the licence is named when the source names it.
- **Fully open**: the weights are released together with the training data and the training and evaluation code. The OLMo report makes this distinction, noting that most earlier releases shared weights and inference code but not the training data.[^1]
- **Hosted only**: the model is used through a vendor's product or API, and the cited source describes no download of weights.
- **Active parameters**: in a mixture-of-experts model, only some parameters process each token. A model can therefore be large in total and modest in cost per token, as the [Glossary](../glossary/index.md) entry for mixture of experts explains.
- **Technical report, model card and system card**: the documents a vendor or lab publishes with a model. A technical report usually gives architecture and training detail, a system card focuses on safety evaluation, and a model card summarises both. Where a vendor publishes none of these, a dated announcement may be the only source.

## GPT (OpenAI)

| Model | Released | Size class | Openness | Note | Source |
|---|---|---|---|---|---|
| GPT-4 | Mar 2023 | Not disclosed | Closed; the report gives no architecture or size | Accepts image and text input; the report says it withholds architecture and training details | [arXiv:2303.08774](https://arxiv.org/abs/2303.08774) |
| GPT-4o | Oct 2024 | Not stated | Hosted only (API access described) | One network for text, audio, image and video input, with text, audio and image output | [arXiv:2410.21276](https://arxiv.org/abs/2410.21276) |
| gpt-oss-120b and gpt-oss-20b | Aug 2025 | 116.8B total, 5.1B active; 20.9B total, 3.6B active | Open weights, Apache 2.0 | Two open-weight reasoning models using mixture of experts | [arXiv:2508.10925](https://arxiv.org/abs/2508.10925) |

The earlier GPT-3 model is described on the [GPT-3 page](../../theory/models/llm/gpt-3-few-shot/index.md). It is not in the table because the status of its weights could not be confirmed from the paper.

## Claude (Anthropic)

| Model | Released | Size class | Openness | Note | Source |
|---|---|---|---|---|---|
| Claude 2 | Jul 2023 | Not stated | Hosted only (API and beta website) | Improved performance and longer responses | [Anthropic](https://www.anthropic.com/news/claude-2) |
| Claude 3 (Haiku, Sonnet, Opus) | Mar 2024 | Three tiers; sizes not stated | Hosted only (API) | Opus and Sonnet available through the API at launch | [Anthropic](https://www.anthropic.com/news/claude-3-family) |
| Claude 3.5 Sonnet | Jun 2024 | Not stated | Hosted only (API and cloud platforms) | Available through the Anthropic API and two cloud platforms | [Anthropic](https://www.anthropic.com/news/claude-3-5-sonnet) |
| Claude 3.7 Sonnet | Feb 2025 | Not stated | Hosted only (API) | Extended thinking, with a thinking budget that API users can set | [Anthropic](https://www.anthropic.com/news/claude-3-7-sonnet) |
| Claude Sonnet 4.5 | Sep 2025 | Not stated | Hosted only (API) | Context editing and a memory tool added to the Claude API | [Anthropic](https://www.anthropic.com/news/claude-sonnet-4-5) |
| Claude Opus 4.5 | Nov 2025 | Not stated | Hosted only (apps, API and cloud platforms) | Available in Anthropic's apps, the API and three major clouds | [Anthropic](https://www.anthropic.com/news/claude-opus-4-5) |

Anthropic publishes announcements for these models rather than arXiv technical reports, so the sources are the announcement pages. The pages give no parameter counts, and none of the models has open weights in the sources checked.

## Gemini and Gemma (Google)

| Model | Released | Size class | Openness | Note | Source |
|---|---|---|---|---|---|
| Gemini 1.0 | Dec 2023 | Ultra, Pro and Nano tiers | Hosted only (products and APIs) | Three tiers, from cloud reasoning to on-device use | [arXiv:2312.11805](https://arxiv.org/abs/2312.11805) |
| Gemini 1.5 Pro and Flash | Mar 2024 | Not stated | Hosted only (API) | Long context, with recall tested up to ten million tokens | [arXiv:2403.05530](https://arxiv.org/abs/2403.05530) |
| Gemini 2.5 Pro and Flash | Jul 2025 | Not stated | Hosted only (API) | Pro is a thinking model that can process up to three hours of video | [arXiv:2507.06261](https://arxiv.org/abs/2507.06261) |
| Gemma | Mar 2024 | 2B and 7B | Open weights | First Gemma release, built from Gemini research, with pretrained and tuned checkpoints | [arXiv:2403.08295](https://arxiv.org/abs/2403.08295) |
| Gemma 2 | Jul 2024 | 2B to 27B | Open weights | Knowledge distillation used to train the 2B and 9B models | [arXiv:2408.00118](https://arxiv.org/abs/2408.00118) |
| Gemma 3 | Mar 2025 | 1B to 27B | Open weights | Adds vision understanding and at least 128K tokens of context | [arXiv:2503.19786](https://arxiv.org/abs/2503.19786) |

## Llama (Meta)

| Model | Released | Size class | Openness | Note | Source |
|---|---|---|---|---|---|
| LLaMA | Feb 2023 | 7B to 65B | Released to the research community | Trained on publicly available datasets only, according to the report | [arXiv:2302.13971](https://arxiv.org/abs/2302.13971) |
| Llama 2 | Jul 2023 | 7B to 70B | Open weights, custom commercial licence | Base models and Llama 2-Chat, a version tuned for dialogue | [arXiv:2307.09288](https://arxiv.org/abs/2307.09288) |
| Llama 3 | Jul 2024 | Largest model 405B, dense | Open weights (405B publicly released) | A family with multilingual, coding, reasoning and tool-use support; multimodal extensions were not broadly released | [arXiv:2407.21783](https://arxiv.org/abs/2407.21783) |

## Qwen (Alibaba)

| Model | Released | Size class | Openness | Note | Source |
|---|---|---|---|---|---|
| Qwen | Sep 2023 | 7B and 14B open-sourced | Open weights for the 7B and 14B base and chat models | The report also covers coding and mathematics variants | [arXiv:2309.16609](https://arxiv.org/abs/2309.16609) |
| Qwen2 | Jul 2024 | 0.5B to 72B, dense and MoE | Open weights (Hugging Face and ModelScope) | Instruction-tuned variants included | [arXiv:2407.10671](https://arxiv.org/abs/2407.10671) |
| Qwen2.5 | Dec 2024 | Up to 72B (open flagship) | Open weights for the open sizes; Turbo and Plus hosted only | Pretraining scaled to 18 trillion tokens | [arXiv:2412.15115](https://arxiv.org/abs/2412.15115) |
| Qwen3 | May 2025 | 0.6B to 235B, dense and MoE | Open weights, Apache 2.0 | One model supports both a thinking and a non-thinking mode | [arXiv:2505.09388](https://arxiv.org/abs/2505.09388) |

## DeepSeek

| Model | Released | Size class | Openness | Note | Source |
|---|---|---|---|---|---|
| DeepSeek LLM | Jan 2024 | 7B and 67B | Open-source | A scaling-law study behind the 7B and 67B models, trained on 2 trillion tokens | [arXiv:2401.02954](https://arxiv.org/abs/2401.02954) |
| DeepSeek-V2 | May 2024 | 236B total, 21B active (MoE) | Open weights (checkpoints on GitHub) | Multi-head latent attention and DeepSeekMoE for cheaper training and inference | [arXiv:2405.04434](https://arxiv.org/abs/2405.04434) |
| DeepSeek-V3 | Dec 2024 | 671B total, 37B active (MoE) | Open weights (checkpoints on GitHub) | Trained on 14.8 trillion tokens without irrecoverable loss spikes | [arXiv:2412.19437](https://arxiv.org/abs/2412.19437) |
| DeepSeek-R1 | Jan 2025 | Built on the V3 base; distilled models from 1.5B | Open weights (MIT licence, per the report) | Reasoning trained with reinforcement learning; the distilled models are a separate release, see [R1 distillation](../../theory/model-compression/knowledge-distillation/llm-distillation/deepseek-r1/index.md) | [arXiv:2501.12948](https://arxiv.org/abs/2501.12948) |

## Mistral AI

| Model | Released | Size class | Openness | Note | Source |
|---|---|---|---|---|---|
| Mistral 7B | Oct 2023 | 7B | Open weights, Apache 2.0 | Grouped-query and sliding-window attention; instruction-tuned variant | [arXiv:2310.06825](https://arxiv.org/abs/2310.06825) |
| Mixtral 8x7B | Jan 2024 | 47B total, 13B active (sparse MoE) | Open weights, Apache 2.0 | Eight experts per layer, with two chosen for each token | [arXiv:2401.04088](https://arxiv.org/abs/2401.04088) |

Mistral's later models are documented on its own news pages. Those pages could not be reached from the environment used to write this page, so they are not listed.

## Other models

| Model | Released | Size class | Openness | Note | Source |
|---|---|---|---|---|---|
| BERT | Oct 2018 | BASE 110M; LARGE 340M | Open (code and pre-trained models released) | Bidirectional encoder, pre-trained and then fine-tuned; see [BERT](../../theory/models/transformer/architecture-families/bert/index.md) | [arXiv:1810.04805](https://arxiv.org/abs/1810.04805) |
| T5 | Oct 2019 | Up to 11B | Open (code, data and pre-trained models released) | Casts every task as text in and text out; see [T5](../../theory/models/transformer/architecture-families/t5/index.md) | [arXiv:1910.10683](https://arxiv.org/abs/1910.10683) |
| Falcon | Nov 2023 | 7B, 40B and 180B | Open weights under a permissive licence | Trained on web data, with an extract of the web dataset released | [arXiv:2311.16867](https://arxiv.org/abs/2311.16867) |
| OLMo | Feb 2024 | 1B and 7B | Fully open (weights, training data, code) | Released with its training data and code, unlike most earlier open releases | [arXiv:2402.00838](https://arxiv.org/abs/2402.00838) |
| Kimi K2 | Jul 2025 | 1T total, 32B active (MoE) | Open weights (base and post-trained checkpoints) | Agentic model trained with the MuonClip optimizer | [arXiv:2507.20534](https://arxiv.org/abs/2507.20534) |
| GLM-4.5 | Aug 2025 | 355B total, 32B active (MoE); Air 106B | Open-source | Hybrid reasoning, with thinking and direct response modes | [arXiv:2508.06471](https://arxiv.org/abs/2508.06471) |

## Connections

The language models above are built on the [Transformer](../../theory/models/transformer/index.md), and the [Scaling Laws](../../theory/models/llm/scaling-laws/index.md) page covers why their sizes were chosen. [Knowledge distillation](../../theory/model-compression/knowledge-distillation/index.md) can make smaller models from larger ones, as in the distilled DeepSeek-R1 models. The [open-source survey](../../start/open-source-survey/index.md) describes the tools and resources around open models. The venues where these reports appear are listed in [Conferences & Journals](../venues/index.md), and the datasets behind pretraining are in [Datasets](../datasets/index.md). The labs behind the models are in [People & Labs](../people-and-labs/index.md).

## Open questions

- When a vendor gives no parameter count, what is the fairest way to compare models of different families?
- Should a model count as open when only its weights are released, or only when its data and code are released too, as OLMo does?
- How should mixture-of-experts models be compared, using total parameters, active parameters, or the cost of a request?

## References

### Seminal papers

- OpenAI (2023). *GPT-4 Technical Report*. arXiv. https://arxiv.org/abs/2303.08774 — Describes GPT-4 and states that the report gives no further details of architecture, model size or training.
- OpenAI (2024). *GPT-4o System Card*. arXiv. https://arxiv.org/abs/2410.21276 — System card for GPT-4o, an omni model covering text, audio, image and video, with its safety evaluations.
- OpenAI (2025). *gpt-oss-120b & gpt-oss-20b Model Card*. arXiv. https://arxiv.org/abs/2508.10925 — Model card for two open-weight mixture-of-experts reasoning models released under Apache 2.0.
- Gemini Team (2023). *Gemini: A Family of Highly Capable Multimodal Models*. arXiv. https://arxiv.org/abs/2312.11805 — Introduces the Ultra, Pro and Nano Gemini models and how they are deployed.
- Gemini Team (2024). *Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context*. arXiv. https://arxiv.org/abs/2403.05530 — Describes Gemini 1.5 Pro and Flash and their long-context recall up to ten million tokens.
- Gemini Team (2025). *Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities*. arXiv. https://arxiv.org/abs/2507.06261 — Covers the Gemini 2.X family, including Gemini 2.5 Pro and Flash and the earlier 2.0 models.
- Gemma Team (2024). *Gemma: Open Models Based on Gemini Research and Technology*. arXiv. https://arxiv.org/abs/2403.08295 — Introduces the first Gemma models, at 2B and 7B parameters, with pretrained and fine-tuned checkpoints.
- Gemma Team (2024). *Gemma 2: Improving Open Language Models at a Practical Size*. arXiv. https://arxiv.org/abs/2408.00118 — Describes Gemma 2 from 2B to 27B parameters, with knowledge distillation for the smaller models.
- Gemma Team (2025). *Gemma 3 Technical Report*. arXiv. https://arxiv.org/abs/2503.19786 — Describes Gemma 3 from 1B to 27B parameters, adding vision understanding and longer context.
- Touvron, H. et al. (2023). *LLaMA: Open and Efficient Foundation Language Models*. arXiv. https://arxiv.org/abs/2302.13971 — The LLaMA family from 7B to 65B parameters, trained on publicly available datasets.
- Touvron, H. et al. (2023). *Llama 2: Open Foundation and Fine-Tuned Chat Models*. arXiv. https://arxiv.org/abs/2307.09288 — Llama 2 from 7B to 70B parameters, with chat models and the custom commercial licence.
- Grattafiori, A. et al. (2024). *The Llama 3 Herd of Models*. arXiv. https://arxiv.org/abs/2407.21783 — Describes the Llama 3 family, whose largest model is a 405B-parameter dense Transformer.
- Bai, J. et al. (2023). *Qwen Technical Report*. arXiv. https://arxiv.org/abs/2309.16609 — Introduces the first Qwen models and the open-sourced 7B and 14B base and chat versions.
- Qwen Team (2024). *Qwen2 Technical Report*. arXiv. https://arxiv.org/abs/2407.10671 — Describes the Qwen2 series from 0.5B to 72B parameters, with weights released on Hugging Face and ModelScope.
- Qwen Team (2024). *Qwen2.5 Technical Report*. arXiv. https://arxiv.org/abs/2412.15115 — Describes Qwen2.5, its open-weight sizes and the hosted Turbo and Plus variants.
- Qwen Team (2025). *Qwen3 Technical Report*. arXiv. https://arxiv.org/abs/2505.09388 — Describes Qwen3 dense and mixture-of-experts models from 0.6B to 235B parameters, released under Apache 2.0.
- DeepSeek-AI (2024). *DeepSeek LLM: Scaling Open-Source Language Models with Longtermism*. arXiv. https://arxiv.org/abs/2401.02954 — Scaling study behind the open-source DeepSeek LLM models at 7B and 67B parameters.
- DeepSeek-AI (2024). *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*. arXiv. https://arxiv.org/abs/2405.04434 — Describes a 236B-parameter mixture-of-experts model with 21B active parameters and its checkpoints.
- DeepSeek-AI (2024). *DeepSeek-V3 Technical Report*. arXiv. https://arxiv.org/abs/2412.19437 — Describes a 671B-parameter mixture-of-experts model with 37B active parameters and its checkpoints.
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv. https://arxiv.org/abs/2501.12948 — Describes a reasoning model built on the DeepSeek-V3 base and the distilled models released with it.
- Jiang, A. Q. et al. (2023). *Mistral 7B*. arXiv. https://arxiv.org/abs/2310.06825 — Describes the 7B Mistral model, released under Apache 2.0, with grouped-query and sliding-window attention.
- Jiang, A. Q. et al. (2024). *Mixtral of Experts*. arXiv. https://arxiv.org/abs/2401.04088 — Describes a sparse mixture-of-experts model with 47B total and 13B active parameters.
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv. https://arxiv.org/abs/1810.04805 — Introduces the BERT encoder, pre-trained bidirectionally and fine-tuned for language understanding tasks.
- Raffel, C. et al. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. arXiv. https://arxiv.org/abs/1910.10683 — Introduces T5, a text-to-text model up to 11B parameters, with its pre-trained models and code released.
- Almazrouei, E. et al. (2023). *The Falcon Series of Open Language Models*. arXiv. https://arxiv.org/abs/2311.16867 — Describes Falcon models at 7B, 40B and 180B parameters, released under a permissive licence.
- Groeneveld, D. et al. (2024). *OLMo: Accelerating the Science of Language Models*. arXiv. https://arxiv.org/abs/2402.00838 — Describes OLMo, released with its training data and training and evaluation code as well as its weights.
- Kimi Team (2025). *Kimi K2: Open Agentic Intelligence*. arXiv. https://arxiv.org/abs/2507.20534 — Describes a trillion-parameter mixture-of-experts model with 32B active parameters and released checkpoints.
- GLM-4.5 Team (2025). *GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models*. arXiv. https://arxiv.org/abs/2508.06471 — Describes an open-source 355B mixture-of-experts model and the 106B GLM-4.5-Air version.

### Articles and documentation

- Anthropic (2023). *Claude 2*. Anthropic news. https://www.anthropic.com/news/claude-2 — Announcement of Claude 2 on 11 July 2023, with API and beta website access.
- Anthropic (2024). *Introducing the next generation of Claude*. Anthropic news. https://www.anthropic.com/news/claude-3-family — Announcement of the Claude 3 family of Haiku, Sonnet and Opus, with API availability at launch.
- Anthropic (2024). *Introducing Claude 3.5 Sonnet*. Anthropic news. https://www.anthropic.com/news/claude-3-5-sonnet — Announcement of Claude 3.5 Sonnet and its availability through the API and two cloud platforms.
- Anthropic (2025). *Claude 3.7 Sonnet and Claude Code*. Anthropic news. https://www.anthropic.com/news/claude-3-7-sonnet — Announcement of Claude 3.7 Sonnet, with extended thinking and a thinking budget set through the API.
- Anthropic (2025). *Introducing Claude Sonnet 4.5*. Anthropic news. https://www.anthropic.com/news/claude-sonnet-4-5 — Announcement of Claude Sonnet 4.5 and its use through the Claude API.
- Anthropic (2025). *Introducing Claude Opus 4.5*. Anthropic news. https://www.anthropic.com/news/claude-opus-4-5 — Announcement of Claude Opus 4.5 and its availability in apps, the API and three major cloud platforms.

[^1]: Groeneveld et al. (2024), arXiv:2402.00838, abstract: most prior efforts released only model weights and inference code, while OLMo also releases its open training data and training and evaluation code.
