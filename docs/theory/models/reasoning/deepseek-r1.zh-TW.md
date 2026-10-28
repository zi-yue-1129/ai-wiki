---
translation_reviewed: 2026-10-28
---

# DeepSeek-R1

DeepSeek-R1 是 DeepSeek 推出的一系列推理模型，見於 2025 年的報告。其核心發現是：以規則式獎勵進行強化學習，就能教會基礎語言模型產生很長、會自我檢查的推理，而不必先用人類撰寫的推理軌跡進行訓練。概述見[推理模型](index.md)頁，該頁並將此方法與思維鏈、自洽性與測試時運算擴展一同比較。

## 概述

過去的推理模型通常在大量逐步示範上微調，這些示範可能由人撰寫，也可能由另一個模型產生。DeepSeek-R1 測試這種監督是否必要。其第一個模型 DeepSeek-R1-Zero 直接從基礎模型開始進行強化學習訓練。主要模型 DeepSeek-R1 則加入一段簡短的監督式起始階段與後續幾個階段，以改善可讀性與一般行為。

## 問題

為每個領域撰寫推理示範的成本很高，而模仿這些示範又會把模型的表現限制在示範的品質之內。報告想知道，僅靠可驗證結果的獎勵，是否就能學會推理。

## 核心想法

只對能以規則檢查的事物給予獎勵：最終答案是否正確，以及推理是否出現在規定的標籤之內。以強化學習最佳化策略。摘要指出，這能在沒有人工標註推理軌跡的情況下改善推理，並且在訓練過程中會出現自我反思、驗證與調整策略等模式。

## 演算法

此論文以群組相對策略最佳化（GRPO）訓練，該方法由 DeepSeekMath（Shao 等人，2024）提出。對每個問題，策略會取樣一組 \(G\) 個輸出，每個輸出各得一個獎勵 \(r_i\)。每個輸出的優勢是它相對於群組的獎勵，因此不需要另外的價值網路：

\[
A_i = \frac{r_i - \mathrm{mean}(r_1,\dots,r_G)}{\mathrm{std}(r_1,\dots,r_G)}
\]

論文中 DeepSeek-R1 的訓練流程分為四個階段：

1. **冷啟動：** 以數千筆精心挑選、可讀性高的長思維鏈範例，微調基礎模型（DeepSeek-V3-Base）。
2. **推理強化學習：** 在推理任務上執行強化學習。在準確率獎勵之外加入語言一致性獎勵，以減少推理過程中混用語言的情形。
3. **拒絕採樣與監督式微調：** 收集約 60 萬筆推理樣本與約 20 萬筆非推理樣本，然後以約 80 萬筆樣本微調基礎模型。
4. **全場景強化學習：** 對數學、程式與邏輯使用規則式獎勵，對一般資料則使用獎勵模型，目標是有幫助且無害。

DeepSeek-R1-Zero 略過第 1 與第 3 階段。其獎勵包括準確率獎勵與格式獎勵，後者要求推理內容出現在 think 標籤之內。

## 結果

- **AIME 2024，pass@1（DeepSeek-R1-Zero）：** 論文報告在強化學習訓練期間，分數從 15.6% 上升到 71.0%。
- **AIME 2024，pass@1（DeepSeek-R1）：** 79.8%。
- **MATH-500，pass@1（DeepSeek-R1）：** 97.3%。
- 摘要也指出，大型模型的推理模式可用來改善較小的模型。

## 限制

- **可讀性：** R1-Zero 的輸出可能混用語言，格式也不佳。冷啟動階段便是為了解決這個問題而加入的。
- **語言：** R1 針對中文與英文調校，遇到其他語言的問題時，可能改以英文推理。
- **提示方式：** 少樣本提示會持續降低其表現，作者建議直接描述問題與輸出格式。
- **軟體工程：** 評估時間很長，限制了這類任務上的大規模強化學習，因此 R1 在這些任務上相對 DeepSeek-V3 的進步不大。
- **一般能力：** R1 在函式呼叫、多輪對話、複雜角色扮演與 JSON 輸出上，表現不如 DeepSeek-V3。

## 關聯

- [思維鏈](chain-of-thought.md)描述了 R1 以訓練所得行為取代的提示方法。
- [自洽性](self-consistency.md)與[測試時運算擴展](test-time-scaling.md)在推論時花費額外運算。R1 則在訓練與生成時花費運算。
- [大型語言模型](../llm/index.md)把此訓練階段放在監督式微調與偏好對齊之後。
- [強化學習](../../paradigms/reinforcement-learning/index.md)提供本頁所用策略梯度方法的一般框架。

## 開放問題

- R1 的行為有多少取決於基礎模型本身已是相當強的模型？
- 規則式獎勵在數學、程式與邏輯之外是否足夠，還是通用階段總需要學習型的獎勵模型？

## 參考文獻

### 開創性論文

- DeepSeek-AI（2025）。*DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv. https://arxiv.org/abs/2501.12948 — 描述 R1-Zero、R1、訓練流程與蒸餾模型的報告。
- Shao, Z., et al.（2024）。*DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models*. arXiv. https://arxiv.org/abs/2402.03300 — 提出 GRPO，這是一種省略價值網路的 PPO 變體，用於訓練 R1。
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — R1 所學會產生、原本靠提示引出的推理方式。
- Lightman, H., et al.（2023）。*Let's Verify Step by Step*. arXiv. https://arxiv.org/abs/2305.20050 — 步驟層級的驗證，R1 的規則式推理獎勵並不依賴這種獎勵方式。

### 綜述與教科書

- Huang, J. & Chang, K. C.-C.（2023）。*Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — 綜述 R1 所建立於其上的推理方法，以及用來評估它們的基準。
