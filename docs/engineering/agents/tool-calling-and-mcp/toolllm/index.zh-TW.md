---
translation_reviewed: 2026-10-28
---

# ToolLLM：讓大型語言模型掌握 16000 多個真實 API

ToolLLM（Qin 等人，2023）是為開放語言模型進行工具使用的框架。它提供一個涵蓋真實 REST API 的大型指令資料集、一種用來找出有效呼叫鏈的深度優先搜尋、一個自動評估器，以及以這些資料訓練的模型 ToolLLaMA。它是 [工具呼叫與 Model Context Protocol](../index.md)概述頁所列的三個方法頁之一。

## 概述

LLaMA 等開放模型的工具使用能力很弱。作者認為，指令微調主要著重於語言能力，忽略了工具使用，而 ChatGPT 等封閉模型則表現得好得多。ToolLLM 從整體處理這個問題：教導工具使用所需的資料、在這些資料上訓練模型，以及評估結果的方法。其目標是涵蓋真實應用所使用的眾多 API，而不只是為了基準測試挑選的幾個工具。

## 關鍵概念

- **ToolBench**：指令資料集。作者從 RapidAPI Hub 收集了 49 個類別中的 16,464 個 RESTful API，生成使用這些 API 的指令，並為每個指令標註解題路徑。
- **單一工具與多工具指令**：需要一個 API 的請求，或需要同一類別或同一集合中多個 API 的請求。
- **解題路徑**：完成一個指令所需的 API 呼叫序列與最終答案。
- **深度優先搜尋決策樹（DFSDT）**：對推理步驟進行的搜尋，模型可以捨棄某個分支，改試另一個分支。
- **ToolEval**：自動評估器，回報通過率（即指令是否在預算內完成）與勝率（由 ChatGPT 判斷兩條解題路徑的優劣）。
- **API 檢索器**：稠密檢索器，為每個指令從龐大的 API 池中推薦相關的 API。

## 運作方式

1. **收集 API。** 蒐集 RESTful API 及其文件，並依類別分組。
2. **生成指令。** 提示 ChatGPT 撰寫使用一個或多個 API 的指令。
3. **以 DFSDT 標註解題路徑。** 對每個指令，搜尋會展開推理節點，每個節點是一個提出行動的推理步驟。模型可呼叫「放棄並結束」函式，捨棄某個節點並展開新的節點。搜尋偏好深度，並只保留通過的路徑。
4. **訓練 ToolLLaMA。** 以指令與解題路徑配對微調 LLaMA-2 7B。
5. **以 ToolEval 評估。** 評分通過率與勝率。作者報告，ChatGPT 的判斷與人類標註者在通過率上有 87.1% 的一致性，在勝率上則為 80.3%。

作者認為 DFSDT 針對簡單迴圈的兩個弱點而設計。早期的錯誤可能擴散成錯誤的迴圈，而單一路徑所探索的行動空間也很有限。

## 結果

論文在三種指令類型上比較 ChatGPT 使用 ReAct 與 DFSDT 的表現。ReAct 的平均通過率為 35.3%，DFSDT 為 63.8%。另有一個基線，會重複執行 ReAct 直到耗用與 DFSDT 相同的預算，其通過率為 44.5%，因此 DFSDT 的提升並非只是嘗試次數較多（Qin 等人，2023，表 3）。

在主要實驗中，DFSDT 提高了所測試每一個模型的通過率與勝率，包括 ChatGPT、GPT-4、Claude-2 與 Text-Davinci-003。使用 DFSDT 的 ChatGPT 在通過率上超越了使用 ReAct 的 GPT-4。Vicuna 與 Alpaca 一個指令也無法通過。使用 DFSDT 的 ToolLLaMA 通過率僅次於使用 DFSDT 的 GPT-4，並能泛化到未見過的指令與工具。摘要另指出，它也能以零樣本方式遷移到 APIBench 資料集，並可與神經網路 API 檢索器搭配使用。[^1]

## 限制

- **依賴教師模型。** 指令與解題路徑都由 ChatGPT 生成，因此學生模型會繼承教師模型的盲點。
- **評估器的限制。** ToolEval 與人類判斷常常一致，但並非總是一致，而且它以 ChatGPT 作為評審。
- **搜尋成本。** DFSDT 比 ReAct 需要更多次模型呼叫。作者以預算相同的 ReAct 基線進行比較，但在實際部署中，搜尋的成本會隨決策樹的規模增長。
- **即時服務。** 通過率取決於真實 API 能否依文件正常回應，而這類服務會隨時間改變。
- **預言式檢索。** 主要表格的大多數列使用正確答案的 API 集合。只有一列使用經過訓練的檢索器，因此從大型 API 池中選擇的情況只得到部分測試。

## 開放問題

- 這種搜尋能否推廣到所研究的工具使用任務之外？作者把 DFSDT 描述為一般的決策策略，這一點是否成立仍待確認。
- 需要多少來自較強模型的合成資料？較小的學生模型又能保留多少品質？
- 搜尋能否便宜到足以用於互動式應用？

## 參考文獻

### 奠基性論文

- Qin, Y. et al. (2023). *ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs*. arXiv. https://arxiv.org/abs/2307.16789 — 本頁所述的論文，包含 ToolBench 資料集、DFSDT、ToolEval 與 ToolLLaMA。
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — 論文中與 DFSDT 比較的推理與行動迴圈。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 提出在提示中逐步推理，作者把這種單一路徑的推理與樹狀搜尋相對照。
- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. arXiv. https://arxiv.org/abs/2303.11366 — 代理人在失敗嘗試後撰寫語言式反思，是另一種從錯誤中復原的相關方法。
- Touvron, H. et al. (2023). *LLaMA: Open and Efficient Foundation Language Models*. arXiv. https://arxiv.org/abs/2302.13971 — 介紹 ToolLLaMA 所微調的開放基礎模型。

### 綜述與教科書

- Qin, Y. et al. (2023). *Tool Learning with Foundation Models*. arXiv. https://arxiv.org/abs/2304.08354 — 工具學習的框架，模型在其中分解任務、規劃並選擇工具，並以實驗回顧此領域。

[^1]: Qin 等人（2023），ToolLLM 論文的摘要與表 4，https://arxiv.org/abs/2307.16789 — 零樣本遷移到 APIBench 的結果，以及主要實驗中通過率排序的來源。
