---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 訓練資料萃取
  - 從語言模型萃取訓練資料
  - Training data extraction
---

# Training Data Extraction

!!! info "Part of Privacy and Data Protection"
    This method page belongs to [Privacy and Data Protection](index.md). It explains the attack in detail; the parent page compares it with other risks.

Training data extraction is an attack that recovers text a language model memorised during training. Carlini et al. (2021) showed that a large language model can emit verbatim training sequences when sampled in the right way. This is a stronger leak than membership inference, because it reveals the content itself rather than only whether a record was used.

## Problem

A language model is trained on text gathered from the web, which may include names, contact details or private messages. The question is whether that text can come back out when an outside user queries the model, and how much of it can be recovered in practice.

## Core idea

Generate a large number of samples from the model, rank them by signs of memorisation, and check the top candidates against sources. Memorised text tends to have unusually high likelihood under the model compared with a reference, and it can be confirmed by searching for it in the training data or on the web.

## How the attack works

1. **Sample.** Generate many continuations from the model, using a range of prompts or from an empty prompt.
2. **Score.** Rank each sample by a memorisation signal, such as the model's likelihood compared with a reference model.
3. **Keep the top candidates.** Select the samples with the strongest signal.
4. **Verify.** Check each candidate against a source to confirm that it is memorised text rather than fluent generation.

The paper describes the scoring and verification in detail. The steps here are a summary; read the paper before reuse.

## Results

The abstract of Carlini et al. (2021) reports that the attack extracts hundreds of verbatim text sequences from the training data of GPT-2. Carlini et al. (2022) find that memorisation grows with model size, with how often an example is duplicated in the training data, and with the amount of context used to prompt the model. The 2022 abstract gives no specific numbers for these relationships.

## Limitations

- **One model family.** The 2021 study targets GPT-2. The 2021 abstract also reports that larger models are more vulnerable than smaller ones, but results do not transfer automatically to other families.
- **Sampling cost.** The attack depends on how many samples an attacker can afford, so success is a matter of resources.
- **Verification.** Confirming that a sequence is memorised text, and not a common phrase, requires a reliable check against the source data.
- **Mitigations change the picture.** Deduplication and differentially private training reduce extraction, but the 2022 abstract warns that memorisation is likely to increase with scale without active mitigations.

## Connections

- The same mechanism applies to image models, where training images can be extracted. See [Extracting training data from diffusion models](../copyright/diffusion-extraction.md).
- The weaker leak of membership is covered on the [Membership Inference](membership-inference.md) page.
- Protection in training is the subject of [Differential Privacy](differential-privacy.md).

## Open questions

- How can memorisation be measured reliably as training sets and models grow?
- Which kinds of personal data are most at risk, and how should they be filtered?
- Do safety tuning and unlearning remove extractable text, or only hide it?

## References

### Seminal papers

- Carlini, N. et al. (2021). Extracting training data from large language models. *USENIX Security Symposium*. https://arxiv.org/abs/2012.07805 — The study described on this page, which extracts verbatim training sequences from GPT-2.
- Carlini, N., Liu, C., Erlingsson, Ú., Kos, J. & Song, D. (2019). The secret sharer: Evaluating and testing unintended memorization in neural networks. arXiv:1802.08232. https://arxiv.org/abs/1802.08232 — A methodology for quantifying the risk of unintended memorisation of uncommon training data.
- Carlini, N. et al. (2022). Quantifying memorization across neural language models. arXiv:2202.07646. https://arxiv.org/abs/2202.07646 — Shows that memorisation grows with model size, duplication and prompt context.
- Carlini, N. et al. (2023). Extracting training data from diffusion models. arXiv:2301.13188. https://arxiv.org/abs/2301.13188 — The same kind of extraction applied to image models.
- Yeom, S., Giacomelli, I., Fredrikson, M. & Jha, S. (2018). Privacy risk in machine learning: Analyzing the connection to overfitting. arXiv:1709.01604. https://arxiv.org/abs/1709.01604 — Links overfitting, which drives memorisation, to privacy risk.
