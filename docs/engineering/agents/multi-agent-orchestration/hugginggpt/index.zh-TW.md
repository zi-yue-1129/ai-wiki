---
translation_reviewed: 2026-10-28
---

# HuggingGPT

HuggingGPT（Shen 等人，2023）使用大型語言模型擔任規劃者。它把使用者的請求拆成子任務，把每個子任務指派給 Hugging Face 上的專門模型，執行這些模型，再根據其輸出撰寫最終答案。它是[多代理人編排](../index.md)概述頁中的規劃者與工作者方法。

## 概述

許多 AI 任務同時需要數種專門模型。單一請求可能結合多種模型，例如先偵測照片中的姿勢，再依此姿勢生成新的圖像。Shen 等人提出，應由語言模型擔任控制者：它讀取請求，決定要使用哪些模型以及順序，並以語言作為模型之間的介面。

這個設計把「決定要做什麼、以什麼順序做」，與「以最適合的工具完成每個部分」分開。規劃者本身不執行專門任務。

## 關鍵概念

- **規劃者（planner）**：把請求解析為任務與其相依關係的語言模型。
- **工作者（workers）**：專門模型，各自以一段簡短的功能文字描述。
- **任務圖（task graph）**：計畫本身。論文把請求視為有向無環圖，因此一項任務可以把另一項任務的輸出當作輸入。

## 運作方式

論文描述四個階段，每個階段都以提示交給語言模型執行：

1. **任務規劃。** 規劃者把請求轉為任務清單，每項任務有識別碼，以及它所相依的任務的識別碼。
2. **模型選擇。** 對每項任務，規劃者從功能描述與任務類型相符的候選模型中挑選一個。
3. **任務執行。** 被選中的模型依相依順序執行，每個輸出都會保存，供需要它的任務使用。
4. **回應生成。** 規劃者讀取請求、計畫、所選模型與其輸出，撰寫一則同時說明答案與過程的回覆。

在作者的例子中，先執行姿勢偵測，其輸出再作為圖像生成的條件，因此規劃者必須正確處理這個相依關係。

## 關鍵方法

[MetaGPT](../metagpt/index.md) 讓代理人擔任固定角色，[多代理人辯論](../debate/index.md)則完全不指定角色。[ReAct](../../react/index.md) 則是規劃系統所延伸的單一代理人迴圈。

## 結果

論文的主要證據是一組示範，以及對規劃階段的評估，因為計畫的品質限制了後續的所有步驟。作者在三類請求上評估規劃：單一任務、順序任務與圖形任務。以 GPT-3.5 作為規劃者時，單一任務規劃的準確率分數為 52.62。[^1] 在圖形任務上，由 GPT-4 擔任評審判斷計畫是否正確，GPT-3.5 的分數為 50.48，相對地，Alpaca-7b 為 13.14，Vicuna-7b 為 19.17，顯示較強與較弱規劃者之間的差距。[^2] 論文未在標準基準上報告端到端的準確率。

## 限制

- **單點失敗。** 錯誤的計畫會傳播到之後的每一步。錯誤的模型選擇會產生種類錯誤的輸出。
- **規劃分數不高。** 報告中 GPT-3.5 的規劃準確率約為一半，因此這類規劃者在複雜請求上遠不可靠。作者的人工標註資料只有 46 個複雜請求，其餘標籤則來自 GPT-4。[^2]
- **依賴描述文字。** 模型選擇取決於每個模型所帶的功能文字，描述不佳會導致選擇不佳。

## 開放問題

- **計畫檢查。** 規劃者能否自行驗證計畫，還是需要第二個模型來做？論文對此未作定論。
- **重新規劃。** 步驟失敗時，計畫必須修改。何時修改、如何修改，是實務上的問題。

## 相關連結

先規劃再行動的想法，也是 Plan-and-Solve 提示的基礎，它要求模型先擬定計畫再執行（Wang 等人，2023）。在較新的系統中，主導代理人會一邊規劃、追蹤進度並重新規劃，一邊指揮專門代理人，例如 Magentic-One（Fourney 等人，2024）。從認知的角度看，這與 [ACT-R](../../../../brain-mind/cognitive-architectures/act-r/index.md) 的目標模組相近，後者保存當前目標，並為其他模組設定子目標。

## 參考文獻

### 奠基性論文

- Shen, Y. et al. (2023). *HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face*. arXiv. https://arxiv.org/abs/2303.17580 — 語言模型規劃任務，從 Hugging Face 選出專門模型，並依其輸出撰寫最終答案。
- Wang, L. et al. (2023). *Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models*. arXiv. https://arxiv.org/abs/2305.04091 — 要求模型在執行前先擬定子任務計畫，以減少零樣本推理中遺漏步驟的錯誤。

### 綜述與教科書

- Guo, T. et al. (2024). *Large Language Model based Multi-Agents: A Survey of Progress and Challenges*. arXiv. https://arxiv.org/abs/2402.01680 — 綜述以 LLM 為基礎的多代理人系統，涵蓋代理人設定檔、溝通方式及其背後的機制。

### 文章與文件

- Fourney, A. et al. (2024). *Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks*. arXiv. https://arxiv.org/abs/2411.04468 — 一個主導代理人負責規劃、追蹤進度並重新規劃，同時指揮負責網頁、檔案與程式碼任務的專門代理人。
- Anthropic (2025). *How we built our multi-agent research system*. Anthropic Engineering. https://www.anthropic.com/engineering/multi-agent-research-system — 主導代理人為各個研究任務建立子代理人，並整合其結果，是實際上線的規劃者與工作者設計。
- Kim, Y. et al. (2025). *Towards a Science of Scaling Agent Systems*. arXiv. https://arxiv.org/abs/2512.08296 — 顯示集中式協調在限制錯誤傳播上，比獨立代理人更有效，效果取決於任務。

[^1]: Shen et al. (2023)，表 3（單一任務規劃），https://arxiv.org/abs/2303.17580 — 以 GPT-3.5、Alpaca-7b 與 Vicuna-7b 作為規劃者的任務規劃準確率。
[^2]: Shen et al. (2023)，表 5（圖形任務）與資料集說明，https://arxiv.org/abs/2303.17580 — 圖形任務規劃的 GPT-4 評審分數，以及人工標註資料集的規模與標註方式。
