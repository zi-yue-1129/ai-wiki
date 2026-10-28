---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - security
  - provenance
  - detection
aliases:
  - Watermarking
  - LLM Watermark
  - Text Watermark
  - 浮水印
  - 語言模型浮水印
---

# 模型輸出浮水印

浮水印（watermarking）會在生成的文字中嵌入一個統計訊號，使偵測器日後能判斷某段文字來自特定模型。這個訊號對讀者不可見，但能從一小段詞元中被偵測出來。浮水印是一種來源追溯工具，其效力弱於「保證能偵測」：有決心的人通常能移除或改寫這個訊號。

本頁是[LLM 應用安全](index.zh-TW.md)的一部分。

## 概述

隨著生成文字越來越流暢，人們與平台都想知道它的來源。大致有兩種做法。被動偵測在事後，依文字的風格或統計特徵，對段落進行分類。浮水印則改變生成過程本身，使輸出帶有來源的證據。浮水印需要模型擁有者配合，被動偵測則不需要。兩者的失敗模式不同。

## 關鍵概念

- **浮水印：**引入生成過程中的統計偏差，偵測器可以檢驗它。
- **偵測器：**判斷一段文字是否帶有浮水印的程序，通常預先設定誤判率。
- **穩健性：**浮水印能否在編輯、改寫或翻譯後保留。
- **不可偵測性：**對於沒有金鑰的人，浮水印文字是否與一般文字無法區分。

## 運作方式

浮水印方法通常會在取樣每個詞元時，修改所用的機率分布。一個秘密金鑰與前面的詞元共同決定一組被偏好的詞元。在一段文字中，被偏好的詞元出現的次數會高於隨機，偵測器持有金鑰，就能檢驗這種超額出現。Kirchenbauer 等人（2023）為專有語言模型提出一套浮水印框架，訊號以很小的品質代價嵌入，並能從一小段詞元中偵測。Christ 等人（2023）追問浮水印能否在沒有金鑰時不可偵測、而有金鑰時仍可偵測，並以形式化方法研究此問題。Zhao 等人（2023）研究在編輯下仍保持穩健的浮水印，並為偵測器提供可證明的保證。

被動偵測也有人研究。Mitchell 等人（2023）提出 DetectGPT，它利用模型的對數機率判斷一段文字是否來自該模型，不需要訓練分類器，也不需要浮水印。Sadasivan 等人（2023）探討 AI 生成的文字究竟能否被可靠地偵測。

## 限制

- **以改寫移除。**Krishna 等人（2023）顯示，改寫可以規避包括浮水印在內的數種偵測器，而以檢索為基礎的防禦對改寫較有效。
- **開放模型。**浮水印只適用於由提供者控制生成過程的情況；開放權重的模型可以在沒有浮水印的情況下運行。
- **誤判。**偵測器必須把被錯誤標記的人類文字比例壓低，這限制了它能使用的訊號有多弱。
- **範圍。**文字浮水印無法解決影像、音訊或經編輯內容的歸屬問題。

## 關聯

- 浮水印可以協助追蹤透過 API 複製的輸出，見[模型萃取與竊取](model-extraction.zh-TW.md)。
- 生成內容與訓練內容的所有權與再利用問題，見[版權與 AI](../../society/copyright/index.zh-TW.md)。
- 對模型應用程式的威脅，見[LLM 應用安全](index.zh-TW.md)。

## 應用

- 在託管生成文字的平台上加註來源標籤。
- 在偵測器錯誤率可接受的情況下，偵測大量生產的內容。

## 開放問題

- 浮水印能否在強力改寫下存活，同時不提高誤判率？
- 在教育等情境中，錯誤的標記後果嚴重，偵測應如何使用？

## 參考文獻

### 開創性論文

- Kirchenbauer, J. 等人（2023）。*A Watermark for Large Language Models*。ICML。https://arxiv.org/abs/2301.10226 — 為語言模型提出一套浮水印框架，能從一小段詞元中偵測。
- Christ, M.、Gunn, S. 與 Zamir, O.（2023）。*Undetectable Watermarks for Language Models*。arXiv。https://arxiv.org/abs/2306.09194 — 研究沒有金鑰時不可偵測的浮水印及其形式化保證。
- Zhao, X. 等人（2023）。*Provable Robust Watermarking for AI-Generated Text*。arXiv。https://arxiv.org/abs/2306.17439 — 提出在編輯下保持穩健、並具可證明偵測器的浮水印。
- Mitchell, E. 等人（2023）。*DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature*。ICML。https://arxiv.org/abs/2301.11305 — 以機率曲率為基礎的被動偵測器，不需要浮水印。
- Krishna, K. 等人（2023）。*Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense*。arXiv。https://arxiv.org/abs/2303.13408 — 顯示改寫可以規避包括浮水印在內的偵測器。
- Sadasivan, V. S. 等人（2023）。*Can AI-Generated Text be Reliably Detected?*。arXiv。https://arxiv.org/abs/2303.11156 — 探討 AI 生成文字能否被可靠地偵測。
