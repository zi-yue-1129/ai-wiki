---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
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

# 主要模型目錄

本目錄依據介紹各模型家族的技術報告，列出主要模型家族。每一項記錄開發者、報告首次公開的時間，以及報告本身所述的規模。它不是所有發布版本的完整清單。沒有公開技術報告的模型（例如部分閉源商用系統）不列入，除非開發者曾公布附有日期的規模聲明。更廣的歷史脈絡見[時間軸](../timeline/index.zh-TW.md)，本頁則提供模型層級的細節。

## 如何閱讀表格

- **報告日期**指技術報告首次在 arXiv 發布的時間，而不是產品上市的時間。
- **報告所述規模**照錄報告摘要或概述中的數字。若摘要未給數字，該欄會註明。
- **開放程度**只在報告有所說明時才標示。空白並不代表權重是封閉的。

## 架構源頭

| 模型 | 開發者 | 報告 | 報告所述規模 | 備註 |
|---|---|---|---|---|
| Transformer | Google Brain 與 Google Research | Vaswani 等人，2017 年 6 月 | 並非有規模的模型；論文報告 WMT 2014 英譯德的 BLEU 為 28.4 | 以下各家族都以此為基礎。見 [Transformer](../../theory/models/transformer/index.zh-TW.md)。 |

## GPT 家族（OpenAI）

| 模型 | 報告 | 報告所述規模 | 備註 |
|---|---|---|---|
| GPT-3 | Brown 等人，2020 年 5 月 | 1,750 億參數 | 摘要描述為具 1,750 億參數的自迴歸語言模型。摘要並未說明權重是否釋出。 |
| GPT-4 | OpenAI，2023 年 3 月 | 摘要未揭露 | 報告描述為基於 Transformer 的下一個 token 預測模型，但未給出參數數量。 |

## Llama 家族（Meta）

| 模型 | 報告 | 報告所述規模 | 備註 |
|---|---|---|---|
| LLaMA | Touvron 等人，2023 年 2 月 | 70 億至 650 億參數 | 依摘要，訓練資料來自公開可得的來源，共數兆 token。 |
| Llama 2 | Touvron 等人，2023 年 7 月 | 70 億至 700 億參數 | 在基礎模型之外，另有微調後的聊天版本。 |

## Gemini 家族（Google DeepMind）

| 模型 | 報告 | 報告所述規模 | 備註 |
|---|---|---|---|
| Gemini | Gemini Team，2023 年 12 月 | Ultra、Pro 與 Nano 等級；摘要未給參數數量 | 多模態家族。報告列出作者團隊而非個人。 |

## Qwen 家族（阿里巴巴）

| 模型 | 報告 | 報告所述規模 | 備註 |
|---|---|---|---|
| Qwen | Bai 等人，2023 年 9 月 | 多種規模；摘要未給數量 | Qwen 系列的技術報告。 |

## Mistral 家族（Mistral AI）

| 模型 | 報告 | 報告所述規模 | 備註 |
|---|---|---|---|
| Mistral 7B | Jiang 等人，2023 年 10 月 | 70 億參數 | 依摘要，為 70 億參數的語言模型。 |

## DeepSeek 家族（DeepSeek）

| 模型 | 報告 | 報告所述規模 | 備註 |
|---|---|---|---|
| DeepSeek-V3 | DeepSeek-AI，2024 年 12 月 | 總參數 6,710 億，每個 token 啟動 370 億 | 為混合專家模型，因此每個 token 實際啟動的規模遠小於總參數。見[混合專家](../../theory/models/mixture-of-experts/index.zh-TW.md)。 |

## Claude 與其他閉源模型

Anthropic 的 Claude 模型並沒有上述形式的單一公開技術報告，因此本表不列其規模。需要相關資料的讀者，請查閱開發者的模型文件，以取得發布日期與公布的能力。

## 本表的限制

- 規模取自報告摘要，並非逐篇完整閱讀報告。引用前請查看報告原文。
- 這裡的發布日期是報告日期，產品的可用時間可能不同。
- 隨著新家族發布，本表會逐漸過時。加入新列時，請附上報告連結，並在合併前查看摘要。

## 參考文獻

### 重要論文

- Vaswani、Shazeer、Parmar、Uszkoreit、Jones、Gomez、Kaiser 與 Polosukhin，*Attention Is All You Need*（2017）。https://arxiv.org/abs/1706.03762 — 提出本目錄各家族所使用的 Transformer 架構。
- Brown 等人，*Language Models are Few-Shot Learners*（2020）。https://arxiv.org/abs/2005.14165 — GPT-3 的報告，包含 1,750 億參數的數字。
- Touvron 等人，*LLaMA: Open and Efficient Foundation Language Models*（2023）。https://arxiv.org/abs/2302.13971 — LLaMA 的報告，規模從 70 億到 650 億參數。

### 文章與文件

- Touvron 等人，*Llama 2: Open Foundation and Fine-Tuned Chat Models*（2023）。https://arxiv.org/abs/2307.09288 — Llama 2 的報告，規模從 70 億到 700 億參數。
- OpenAI，*GPT-4 Technical Report*（2023）。https://arxiv.org/abs/2303.08774 — GPT-4 的報告；其摘要未給出參數數量。
- Gemini Team，*Gemini: A Family of Highly Capable Multimodal Models*（2023）。https://arxiv.org/abs/2312.11805 — Gemini 的報告，包含 Ultra、Pro 與 Nano 等級。
- Bai 等人，*Qwen Technical Report*（2023）。https://arxiv.org/abs/2309.16609 — Qwen 的技術報告。
- Jiang 等人，*Mistral 7B*（2023）。https://arxiv.org/abs/2310.06825 — Mistral 7B 的報告，模型為 70 億參數。
- DeepSeek-AI，*DeepSeek-V3 Technical Report*（2024）。https://arxiv.org/abs/2412.19437 — 報告總參數 6,710 億、每個 token 啟動 370 億參數。
