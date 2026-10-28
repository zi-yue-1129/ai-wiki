---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - agents
  - tool use
  - self-supervised learning
aliases:
  - Toolformer
  - 自學工具使用
  - 工具增強語言模型
---

# Toolformer（Schick 等人，2023）

Toolformer 是一種讓語言模型自行學會呼叫外部工具的方法。模型從自己的文字中學習，在有助於預測後續文字的位置插入 API 呼叫，因此它能自行決定呼叫哪個 API、何時呼叫、使用什麼參數，以及如何運用結果。Schick 等人（2023）提出此方法，所涵蓋的工具包括計算機、問答系統、兩個搜尋引擎、翻譯系統與行事曆。

本頁是[代理工程](index.zh-TW.md)的一部分，也是[工具呼叫與模型上下文協定](tool-calling-and-mcp.zh-TW.md)背後的命名方法之一。

## 概述

語言模型擅長語言，但在算術或查找事實等基本功能上較弱，而小型的專用工具在這些方面表現更好。常見的做法是以工具使用的範例來提示模型。Toolformer 則在訓練期間就教模型使用工具，使工具使用成為模型自身決策的一部分，而非固定的提示模式。

## 問題

以人工方式訓練模型使用工具，需要大量標註的工具使用資料，而為每個 API 建立這些資料成本很高。問題是：模型能否從每個 API 的少量示範中，產生自己的工具使用訓練資料，同時不喪失一般的語言能力？

## 核心想法

此方法分三步。首先，模型在文字中取樣可能有助於 API 呼叫的候選位置，並在那裡提出一個呼叫。其次，它執行這些呼叫，並只保留那些使後續詞元更容易預測的呼叫，這是論文用來衡量有用性的標準。第三，它以插入了保留之呼叫的文字進行微調。結果是一個能在自己生成的文字串流中產生呼叫與參數，並利用回傳結果繼續生成的模型。

## 方程式或演算法

對每個 API，使用少量示範：

1. 以模型在文字中取樣候選 API 呼叫的位置。
2. 執行每個呼叫，並把其結果插入呼叫之後。
3. 只有當插入呼叫與其結果後，後續詞元的損失下降至少一個門檻值（預設 1.0，計算機與翻譯工具為 0.5），且相較於兩個基線中較低者（不呼叫，以及呼叫但不提供結果）仍有此下降時，才保留該呼叫。
4. 以過濾後的文字微調模型，並保留語言建模的目標。

在推論時，當模型判斷需要某個工具，就寫出呼叫的詞元序列，由外部程式執行。

## 結果

摘要指出，Toolformer 在多種下游任務上的零樣本表現顯著提升，常可與大得多的模型相抗衡，且不犧牲其核心的語言建模能力。論文以 GPT-J（67 億參數）進行微調。所涵蓋的工具涉及算術、事實查找、搜尋、翻譯與日期。

## 限制

- **訓練時的工具集固定。**新工具需要新的訓練資料與新的微調。
- **篩選設計。**有用性標準依賴損失，因此在損失無法衡量的方面有幫助的呼叫，可能被丟棄。
- **工具錯誤。**工具的錯誤結果與正確結果以相同的權威被插入。
- **模型層級的訓練。**此方法會改變權重，除非供應者支援，否則難以用於封閉模型。

## 關聯

- ReAct 採取的、以提示為基礎的工具使用，見 [ReAct](react.zh-TW.md)。
- 標準化工具提供方式的協定，見[工具呼叫與模型上下文協定](tool-calling-and-mcp.zh-TW.md)。
- Toolformer 所微調的模型家族，見 [Transformer](../../theory/models/transformer/index.zh-TW.md)。
- 本文中作為工具之一的檢索，見[檢索增強生成](../rag/index.zh-TW.md)。

## 應用

- 在回答過程中呼叫計算機或搜尋引擎的模型。
- 透過專用服務檢查日期、單位或翻譯的助理。

## 開放問題

- 一個模型能學會多少種工具，之後才會混淆它們？
- 工具使用能否從最終答案的回饋學習，而不是從損失下降學習？

## 參考文獻

### 開創性論文

- Schick, T. 等人（2023）。*Toolformer: Language Models Can Teach Themselves to Use Tools*。arXiv。https://arxiv.org/abs/2302.04761 — 提出 Toolformer，以自我監督方式、從每個工具的少量示範中學會呼叫 API。
- Yao, S. 等人（2023）。*ReAct: Synergizing Reasoning and Acting in Language Models*。ICLR。https://arxiv.org/abs/2210.03629 — 以提示為基礎的替代做法，把工具使用與推理交錯。
- Parisi, A.、Zhao, Y. 與 Fiedel, N.（2022）。*TALM: Tool Augmented Language Models*。arXiv。https://arxiv.org/abs/2205.12255 — 較早的做法，以工具呼叫擴充語言模型。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，涵蓋工具使用作為其元件之一。

### 文章與文件

- Model Context Protocol。*Specification, revision 2025-06-18*。https://modelcontextprotocol.io/specification/2025-06-18 — 後來用來連接模型與工具的標準，走的是與把工具使用訓練進模型不同的路線。
