---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - agents
  - reasoning
  - tool use
aliases:
  - ReAct
  - Reasoning and Acting
  - 推理與行動
---

# ReAct（Yao 等人，2022）

ReAct 是一種提示方法，讓語言模型在同一段交錯的序列中寫下它的推理與行動。推理幫助模型規劃與修正，行動則讓它查詢外部來源。Yao 等人（2022）提出此方法，並在問答、事實查核與兩個互動式決策基準上展示了進步。

本頁是[代理工程](index.zh-TW.md)的一部分，也是[工具呼叫與模型上下文協定](tool-calling-and-mcp.zh-TW.md)背後的命名方法之一。

## 概述

在 ReAct 之前，推理與行動通常分開研究。思維鏈提示（Wei 等人，2022）會引出推理步驟，但不會查詢模型以外的資訊，因此這些步驟中的錯誤不會被證據修正。純行動的做法可以蒐集事實，卻不說明如何運用它們。ReAct 把兩者合併在同一個序列中。

## 問題

只依靠記憶作答的模型會產生幻覺；從未查核事實的推理鏈，則可能讓早期錯誤延續到之後每一步。論文要處理的問題是：模型如何在環境中蒐集資訊，同時保留能告訴它下一步該找什麼的推理。

## 核心想法

在每一步，模型先寫一段簡短的思考，也就是對目前狀態的推理，然後寫出一個行動，也就是對外部來源或環境的呼叫。行動所回傳的觀察結果會加入上下文，下一段思考會利用它。思考幫助模型推導、追蹤與更新計畫，並處理例外狀況；行動則讓它取得權重中沒有的知識或狀態。論文把這套方法應用在一個簡單的維基百科 API 上，用於問答與事實驗證。

## 方程式或演算法

這個程序是對三種文字的迴圈：

1. 寫下關於已知事項與下一步要做什麼的思考。
2. 從允許的行動集合中寫出一個行動，並執行它。
3. 附加環境回傳的觀察結果，然後回到第 1 步，直到模型給出最終答案。

提示中的範例會展示這三種文字，因此模型只需少量示範就能學會此模式。

## 結果

摘要指出，在 HotpotQA 與 FEVER 上，ReAct 克服了幻覺與錯誤傳遞的問題，並產生比沒有推理軌跡之基線更容易解讀的軌跡。在兩個互動式決策基準 ALFWorld 與 WebShop 上，它分別以絕對成功率高出模仿學習與強化學習方法 34% 與 10%，而且只用一到兩個上下文範例作為提示。

## 限制

- **依賴環境。**效果取決於外部來源的品質。搜尋結果不佳或觀察錯誤，仍會誤導模型。
- **以提示為基礎。**此方法透過提示運作，論文的比較也只使用少量範例。之後的代理常改為在軌跡上訓練或微調模型。
- **可解讀性是關於軌跡的主張。**可讀的軌跡讓執行過程更容易檢查，但並不證明所述的推理導致了行動。
- **成本。**每一步都增加一次模型呼叫，以及上下文中的一段觀察，因此長的情節會變得昂貴。

## 關聯

- 在環境中行動的強化學習觀點，見[強化學習](../../theory/paradigms/reinforcement-learning/index.zh-TW.md)。ReAct 不學習權重也能做到這點。
- Reflexion 以跨次嘗試的語言回饋擴充此迴圈，見 [Reflexion](reflexion.zh-TW.md)。
- Toolformer 學習何時呼叫工具，而非依提示決定，見 [Toolformer](toolformer.zh-TW.md)。
- 為這類代理建立的評估環境包括 [WebArena](../../theory/evaluation/benchmarks/reasoning-agents/webarena.zh-TW.md)。

## 應用

- 在推理過程中搜尋知識庫的問答系統。
- 把觀察與規劃交錯進行的網頁與居家任務代理。

## 開放問題

- 環境雜亂時，模型能否讓思考與行動保持一致？
- 當模型經過訓練而非提示時，交錯式推理是否仍然有效？

## 參考文獻

### 開創性論文

- Yao, S. 等人（2023）。*ReAct: Synergizing Reasoning and Acting in Language Models*。ICLR。https://arxiv.org/abs/2210.03629 — 提出 ReAct，並報告在 HotpotQA、FEVER、ALFWorld 與 WebShop 上的結果。
- Wei, J. 等人（2022）。*Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*。arXiv。https://arxiv.org/abs/2201.11903 — 顯示寫出中間推理步驟能改善複雜推理，是 ReAct 所延伸的基線。
- Shridhar, M. 等人（2020）。*ALFWorld: Aligning Text and Embodied Environments for Interactive Learning*。arXiv。https://arxiv.org/abs/2010.03768 — 以文字描述的居家環境，代理在其中行動並觀察，是 ReAct 的測試場景之一。
- Yao, S. 等人（2022）。*WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents*。arXiv。https://arxiv.org/abs/2207.01206 — 模擬的線上購物環境，用於有根基的語言代理，是 ReAct 的第二個測試場景。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，說明推理與行動方法的脈絡。
