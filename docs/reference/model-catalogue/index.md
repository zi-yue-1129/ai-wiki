---
status: draft
last_reviewed: 2026-10-28
related:
  - reference/timeline
  - theory/models/transformer
tags:
  - models
  - catalogue
  - reference
aliases:
  - 模型目錄
  - 主要模型一覽
  - Model catalogue
---

# Catalogue of major models

This catalogue lists major model families by the technical report that introduced them. Each entry gives the developer, when the report was first posted, and the size the report itself states. It does not list every release. Models without a public technical report, such as several closed commercial systems, are left out unless their developer published a dated statement of their size. The [timeline](../timeline/index.md) gives the wider history, and this page gives the model-level detail.

## How to read the table

- **Report date** is the first arXiv posting of the technical report, not the date of the product launch.
- **Size as stated** copies the figure in the report's abstract or summary. Where the abstract gives no figure, the cell says so.
- **Openness** is only noted where the report states it. A blank note does not mean the weights are closed.

## Architecture root

| Model | Developer | Report | Size as stated | Note |
|---|---|---|---|---|
| Transformer | Google Brain and Google Research | Vaswani et al., June 2017 | Not a sized model; the paper reports a BLEU score of 28.4 on WMT 2014 English-to-German | The architecture every family below builds on. See [Transformer](../../theory/models/transformer/index.md). |

## GPT family (OpenAI)

| Model | Report | Size as stated | Note |
|---|---|---|---|
| GPT-3 | Brown et al., May 2020 | 175 billion parameters | The abstract describes an autoregressive language model with 175 billion parameters. It does not state a release of weights. |
| GPT-4 | OpenAI, March 2023 | Not disclosed in the abstract | The report gives a Transformer-based next-token model but no parameter count. |

## Llama family (Meta)

| Model | Report | Size as stated | Note |
|---|---|---|---|
| LLaMA | Touvron et al., February 2023 | 7B to 65B parameters | Trained on trillions of tokens from publicly available sources, according to the abstract. |
| Llama 2 | Touvron et al., July 2023 | 7B to 70B parameters | Introduces a fine-tuned chat variant alongside the base models. |

## Gemini family (Google DeepMind)

| Model | Report | Size as stated | Note |
|---|---|---|---|
| Gemini | Gemini Team, December 2023 | Ultra, Pro and Nano tiers; the abstract gives no parameter counts | A family of models in Ultra, Pro and Nano tiers. |

## Qwen family (Alibaba)

| Model | Report | Size as stated | Note |
|---|---|---|---|
| Qwen | Bai et al., September 2023 | Several sizes; the abstract gives no counts | The technical report for the Qwen series. |

## Mistral family (Mistral AI)

| Model | Report | Size as stated | Note |
|---|---|---|---|
| Mistral 7B | Jiang et al., October 2023 | 7 billion parameters | A 7-billion-parameter language model, per the abstract. |

## DeepSeek family (DeepSeek)

| Model | Report | Size as stated | Note |
|---|---|---|---|
| DeepSeek-V3 | DeepSeek-AI, December 2024 | 671 billion total parameters, 37 billion activated per token | A mixture-of-experts model, so the active size per token is much smaller than the total. See [Mixture of experts](../../theory/models/mixture-of-experts/index.md). |

## Claude and other closed models

Anthropic's Claude models have no single public technical report in the form above, so they are not listed with a size. Readers who need them should check the developer's model documentation for the release date and the stated capabilities.

## Limits of this table

- Sizes were checked against each report's abstract, not the full report. Check the report before relying on a size beyond the abstract.
- Release dates here are report dates. Product availability can differ.
- The table will drift as new families are released. Add rows with a report link and check the abstract before merging.

## References

### Seminal papers

- Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser and Polosukhin, *Attention Is All You Need* (2017). https://arxiv.org/abs/1706.03762 — Introduces the Transformer architecture used by the families in this catalogue.
- Brown et al., *Language Models are Few-Shot Learners* (2020). https://arxiv.org/abs/2005.14165 — The GPT-3 report, with the 175 billion parameter figure.
- Touvron et al., *LLaMA: Open and Efficient Foundation Language Models* (2023). https://arxiv.org/abs/2302.13971 — The LLaMA report, with sizes from 7B to 65B.

### Articles and documentation

- Touvron et al., *Llama 2: Open Foundation and Fine-Tuned Chat Models* (2023). https://arxiv.org/abs/2307.09288 — The Llama 2 report, with sizes from 7B to 70B.
- OpenAI, *GPT-4 Technical Report* (2023). https://arxiv.org/abs/2303.08774 — The GPT-4 report; its abstract gives no parameter count.
- Gemini Team, *Gemini: A Family of Highly Capable Multimodal Models* (2023). https://arxiv.org/abs/2312.11805 — The Gemini report, with Ultra, Pro and Nano tiers.
- Bai et al., *Qwen Technical Report* (2023). https://arxiv.org/abs/2309.16609 — The first Qwen technical report, introducing the model family listed in this catalogue.
- Jiang et al., *Mistral 7B* (2023). https://arxiv.org/abs/2310.06825 — The Mistral 7B report, with a 7-billion-parameter model.
- DeepSeek-AI, *DeepSeek-V3 Technical Report* (2024). https://arxiv.org/abs/2412.19437 — Reports 671 billion total and 37 billion activated parameters.
