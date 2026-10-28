---
translation_reviewed: 2026-10-28
---

# 自洽性

自洽性以多條取樣的思維鏈取代單一的貪婪思維鏈，然後回傳大多數鏈條所得出的答案。此方法不需訓練，適用於任何能產生思維鏈文字的模型。概述見[推理模型](index.md)頁，它所延伸的方法是[思維鏈](chain-of-thought.md)。

## 概述

思維鏈提示通常只解碼一條推理路徑，也就是每一步最可能的那一條。這條路徑可能含有錯誤，而模型在另一次嘗試中未必會犯同樣的錯。此方法的依據是 Wang 等人（2022）提出的直覺：一個問題通常有數條通往同一答案的有效推理路線，而錯誤則會分散到不同的答案上。因此，取樣多樣的路徑並投票，會偏向一致的答案。

## 問題

貪婪的思維鏈解碼很脆弱。一個錯誤步驟就足以導致錯誤答案，而且此方法無法告訴我們這條鏈是否可靠。

## 核心想法

對同一個問題取樣多樣的推理路徑，而不只取貪婪的一條。接著對這些路徑做邊際化：依最終答案將推理鏈分組，選出獲得最多支持的答案。作者的描述是：透過對取樣的推理路徑做邊際化，選出最一致的答案。

## 演算法

1. 以思維鏈範例提示模型，如[思維鏈](chain-of-thought.md)方法所述。
2. 對同一個問題取樣 \(k\) 條推理路徑。使用大於零的取樣溫度，使各路徑有所不同。
3. 從每條路徑中擷取最終答案。
4. 回傳出現次數最多的答案 \(a^\*\)：\(a^\* = \arg\max_a \sum_{i=1}^{k} \mathbf{1}[\,a_i = a\,]\)。

此方法需要能在不同路徑之間比較的答案。對自由格式的文字做聚合較為困難，摘要並未涵蓋這一點。

## 結果

Wang 等人（2022）報告，在算術與常識基準上，此方法勝過貪婪的思維鏈解碼。摘要列出以下準確率提升：

- GSM8K：+17.9%
- SVAMP：+11.0%
- AQuA：+12.2%
- StrategyQA：+6.4%
- ARC-challenge：+3.9%

摘要並未說明取樣數 \(k\) 為多少，因此若要重用這個設定，應先查閱完整論文。

## 限制

- 成本隨 \(k\) 增加。每多一個樣本就是一次完整的生成，因此此方法直接以運算換取準確率。這正是[測試時運算](test-time-scaling.md)頁所描述的取捨。
- 投票需要可比較的最終答案。對於開放式問題沒有簡單的多數決，因此需要另一種分組答案的方式。
- 當模型系統性地犯錯時，多數決可能一致地選中錯誤答案。取樣無法修補缺少的能力。
- 論文的增益是在答案簡短的基準上報告的，在長篇文字任務上的幅度並未顯示。

## 關聯

- [思維鏈](chain-of-thought.md)是自洽性所重複解碼的提示方法。
- [測試時運算擴展](test-time-scaling.md)將此想法加以推廣：花費額外的樣本或搜尋步驟，並以驗證器而非投票來決定保留哪些結果。
- [DeepSeek-R1](deepseek-r1.md)在產生訓練資料時，取樣多個候選解，也使用了相關的想法。

## 開放問題

- 應如何為每個查詢選擇取樣數？容易的問題需要的樣本較少。
- 對於精確比對會失敗的自由格式輸出，能否學到答案分組的方式？

## 參考文獻

### 開創性論文

- Wang, X., et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv. https://arxiv.org/abs/2203.11171 — 原始方法：取樣多樣的推理路徑，並保留最一致的最終答案。
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 自洽性所取代的貪婪思維鏈基準。
- Snell, C., Lee, J., Xu, K. & Kumar, A. (2024). *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv. https://arxiv.org/abs/2408.03314 — 研究增加推論運算（包括取樣）如何能與更大的模型相抗衡。
- Lightman, H., et al. (2023). *Let's Verify Step by Step*. arXiv. https://arxiv.org/abs/2305.20050 — 以步驟層級的驗證器為候選解排序，是投票之外的另一種選擇。

### 綜述與教科書

- Huang, J. & Chang, K. C.-C.（2023）。*Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — 綜述推理的解碼與提示方法，包括以取樣投票的做法。
