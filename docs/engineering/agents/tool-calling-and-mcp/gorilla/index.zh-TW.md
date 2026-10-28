---
translation_reviewed: 2026-10-28
---

# Gorilla：連結大量 API 的大型語言模型

Gorilla（Patil 等人，2023）是一個以 LLaMA 為基礎、參數量為 70 億的模型，經過微調以撰寫機器學習 API 的呼叫，並經過訓練以閱讀檢索器放入提示中的 API 文件。它是 [工具呼叫與 Model Context Protocol](../index.md)概述頁所列的三個方法頁之一。

## 概述

被要求呼叫某個 API 時，語言模型常寫出看似合理、但引數錯誤的呼叫，或是提到一個並不存在的 API。論文把後者稱為幻覺。文件也會隨時間改變，因此從固定快照中學到的內容很快就會過時。Gorilla 以一項設計同時處理這兩個問題：模型經過訓練，會使用推論時提供的文件，使其答案依循文件，而非記憶。

作者聚焦於機器學習模型平台，因為那裡有許多功能相近的 API，差異卻很重要。

## 關鍵概念

- **APIBench**：作者建立的資料集，收錄來自三個模型平台的 API 呼叫，分別是 TorchHub、HuggingFace 與 TensorFlow Hub。每一筆資料都是把模型卡片轉成結構化紀錄，欄位包括領域、框架、API 名稱、呼叫方式與引數等。論文報告共有 1,645 個此類呼叫。
- **Self-instruct 生成**：GPT-4 根據少量範例配對與該 API 的文件，撰寫需要該 API 的使用者請求，且不得提及 API 名稱。手寫的資料只有每個平台六組範例配對。
- **檢索感知訓練**：訓練時，提示中包含檢索到的文件，使模型學會閱讀並依據文件作答。
- **AST 子樹比對**：將生成的呼叫解析為抽象語法樹，並檢查它是否為參考呼叫的子樹。此檢查用來辨識使用了哪一個 API。
- **幻覺**：依論文的定義，指一個不是資料庫中任何 API 之子樹的呼叫，也就是說，該 API 並不存在。

## 運作方式

1. **收集文件。** 把每個模型卡片轉成結構化的 API 紀錄。
2. **生成指令。** 請 GPT-4 為每個 API 撰寫需要它的使用者請求，每個 API 保留十組指令與 API 配對。
3. **微調。** 以這些配對，將 LLaMA-7B 基礎模型訓練成使用者與代理人的對話，採用一般的指令微調。檢索感知版本在訓練時，會在使用者提示後附加「請參考此 API 文件」以及檢索到的紀錄。
4. **檢索並作答。** 推論時，由檢索器（BM25、以 GPT 為基礎的索引，或總能回傳正確文件的理想檢索器）提供最新文件，模型再撰寫呼叫。
5. **評分。** 以 AST 比對檢查每個輸出，並計算三種結果：正確、幻覺，或選錯了真實存在的 API。

## 結果

論文在 APIBench 的 TorchHub 上進行主要比較，不使用檢索器（零樣本）。Gorilla 的整體準確率為 59.13%，幻覺率為 6.98%；GPT-4 的整體準確率為 38.70%，幻覺率為 36.55%（表 1）。[^1]摘要指出，經過微調的模型在撰寫 API 呼叫方面超越了 GPT-4。

另有兩項值得注意的發現。作者觀察到，在他們的各種設定中，GPT-3.5 的幻覺比 GPT-4 少，並認為這反映了人類回饋強化學習在使模型誠實方面的作用。他們也發現，推論時加入檢索器並不總是有幫助：配對不佳的檢索器可能誤導模型，並增加錯誤。最後，由於模型受過閱讀文件的訓練，當模型的文件改變時，它能夠適應，論文以一個改變後的模型登錄檔為例說明。

## 限制

- **領域狹窄。** 作者選擇機器學習平台，是因為其中的 API 功能相近，任務因而困難，但這些 API 並不能代表一般的 API。論文也指出，機器學習 API 若以偏頗的資料訓練，可能產生有偏見的預測。
- **一次只呼叫一個 API。** 論文只考慮每個輸出一次 API 呼叫。
- **指標衡量的內容。** AST 比對檢查呼叫是否與參考 API 相符，但它不檢查呼叫能否執行，也不檢查其結果是否回答了使用者的問題。
- **依賴檢索器。** 效果取決於檢索器，而配對不佳的檢索器會降低準確率，論文中也有此報告。

## 開放問題

- 檢索感知訓練能否推廣到一般的 REST API，那些文件較不一致的情況？[ToolLLM](../toolllm/index.md) 以規模更大的 API 集合來處理這個問題。
- 當任務需要多個 API 時，模型應如何結合多份檢索到的文件？
- 訓練能否適應從未見過的文件，還是需要檢索器提供變動的內容？

## 參考文獻

### 奠基性論文

- Patil, S. G. et al. (2023). *Gorilla: Large Language Model Connected with Massive APIs*. arXiv. https://arxiv.org/abs/2305.15334 — 本頁所述的論文，介紹 APIBench、檢索感知微調與以 AST 為基礎的評估。
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. arXiv. https://arxiv.org/abs/2005.11401 — 提出結合檢索器與生成器的架構，是 Gorilla 把 API 文件納入提示時所套用的一般模式。
- Wang, Y. et al. (2022). *Self-Instruct: Aligning Language Models with Self-Generated Instructions*. arXiv. https://arxiv.org/abs/2212.10560 — 說明如何從模型自身的輸出生成指令資料，作者據此改寫出 API 請求的生成方法。
- Touvron, H. et al. (2023). *LLaMA: Open and Efficient Foundation Language Models*. arXiv. https://arxiv.org/abs/2302.13971 — 介紹 Gorilla 所微調的開放基礎模型。
- Schick, T. et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv. https://arxiv.org/abs/2302.04761 — 另一種做法，讓模型在自己標註的工具呼叫上訓練，而非使用生成的指令。

[^1]: Patil 等人（2023），Gorilla 論文的表 1，https://arxiv.org/abs/2305.15334 — Gorilla 與 GPT-4 在 TorchHub 零樣本準確率與幻覺數據的來源。
