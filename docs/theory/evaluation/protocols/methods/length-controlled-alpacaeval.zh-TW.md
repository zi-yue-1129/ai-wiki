---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - theory/evaluation/protocols/methods/llm-as-judge.md
tags:
  - evaluation
  - protocols
  - llm-as-judge
aliases:
  - 長度控制 AlpacaEval
  - Length-controlled AlpacaEval
  - AlpacaEval-LC
---

# 長度控制 AlpacaEval

!!! info "屬於 LLM 作為評審"
    本方法頁隸屬於 [LLM 作為評審](llm-as-judge.zh-TW.md)。它詳細說明長度修正；上層頁面則比較各種評審方法。

AlpacaEval 是一個自動基準：由一個強大的模型判斷某模型對一組指令的答案，是否勝過基線的答案。Dubois et al. (2024) 顯示，其原始勝率會獎勵較長的答案，並提出一種迴歸方法，用來估計當兩則答案長度相同時會得到的勝率。

## 問題

自動評審成本低，與人類偏好的一致性也相當不錯，但它偏好較長的答案。模型因此可能藉由寫得更多而非答得更好來提高分數，排行榜也可能反映的是冗長程度。問題在於：能否在不做新的人類研究的情況下，修正自動基準的長度偏誤。

## 核心想法

建立一個評審偏好的模型，把三種效應分開：兩個模型之間的品質差異、經正規化的長度差異項，以及指令項。接著把長度項設為零，預測偏好。這些預測在各指令上的平均值，就是長度控制的勝率。

## 程序

作者對評審的偏好擬合一個邏輯斯迴歸模型。模型有三部分：兩模型之間的品質差異、一個長度項（以長度差異正規化後的 tanh 作為縮放），以及一個指令專屬項。長度控制的勝率會移除長度項：

$$\text{winrate}^{\text{LC}}(m, b) = 100 \cdot \mathbb{E}_x\left[\sigma\left(\theta_m - \theta_b + (\psi_m - \psi_b)\gamma_x\right)\right]$$

其中 $m$ 是被評分的模型，$b$ 是基線，$\sigma$ 是邏輯斯函數，$\gamma_x$ 是先在聯合迴歸中估計的指令項。訓練使用交叉熵損失、五摺交叉驗證與 L2 正則化。長度係數只做輕度正則化，以防止模型藉由截斷來操弄迴歸。

## 結果

- **與 Chatbot Arena 的一致性。** 排行榜與 Chatbot Arena 之間的 Spearman 相關係數，從 AlpacaEval 的 0.94 提高到長度控制版本的 0.98，計算所用為 38 個模型（圖 1 與第 4.2 節）。作者報告，與原始版本相比的 bootstrap p 值為 0.07，因此這項改進仍屬暗示性，而非確定的結論。
- **長度操弄。** 改變提示中的冗長指令後，gpt4_1106_preview 的原始勝率在 22.9% 至 64.3% 之間變動；長度控制後的勝率則介於 41.9% 與 51.6% 之間（第 4.1 節）。論文以定性方式指出，較弱的模型（例如 claude-2.1）只要被要求寫得冗長，就能獲得大幅提升。
- **跨提示的穩定性。** 勝率在各提示變體之間的正規化標準差，由約 25% 降至約 10%（第 4.1 節）。表 1 則列為 26% 至 10%。
- **截斷攻擊。** 對被截斷的輸出，在 AlpacaEval 2.0 上勝率為 3.7，未正則化的 AlpacaEval-LC 上升至 25.9，正則化後降至 12.2（第 4.3 節）。表 1 將正則化後的增益列為 8.5 個百分點。

## 限制

- 作者只在 AlpacaEval 上測試了去偏方法。本頁的結果不能說明它能推廣到其他基準。
- 這個方法回答的是一個反事實問題：若兩個模型的答案長度相同，它們會如何比較。長度有時本身就是好答案的一部分，因此這是建模上的選擇，而非使用者真實偏好的事實。
- 此方法不處理 LLM 評審的其他已知偏誤，例如位置偏誤與自我偏好。這些可見 [MT-Bench](mt-bench.zh-TW.md)。
- 參考模型與自動標註者固定為某個 GPT-4 Turbo 變體，因此該評審本身的偏誤也會延續到結果中。

## 關聯

- 評審的位置與自我偏好偏誤，以及記錄這些偏誤的一致性研究，見 [MT-Bench](mt-bench.zh-TW.md)。
- 長度控制分數所對照的競技場，以及把投票轉為分數的排名方法，見 [Elo 評分與競技場](elo-rating.zh-TW.md)。
- 更完整的協定，包括評分準則與報告建議，見 [LLM 作為評審](llm-as-judge.zh-TW.md)。

## 開放問題

- 長度控制在長篇寫作、多輪對話與非英文答案上是否仍然有效？
- 自動基準是否也應控制格式（例如清單與標題）的影響，因為評審可能同樣偏好這些格式？

## 參考文獻

### 開創性論文

- Dubois, Y., Galambosi, B., Liang, P. & Hashimoto, T. B. (2024). *Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators*. arXiv. https://arxiv.org/abs/2404.04475 — 提出長度控制的勝率，並報告其與 Chatbot Arena 的相關性。
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. NeurIPS Datasets and Benchmarks Track. https://arxiv.org/abs/2306.05685 — 記錄 LLM 評審的冗長偏誤與其他偏誤，以及 GPT-4 與人類評分者的一致性。
- Chiang, W.-L. et al. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*. arXiv. https://arxiv.org/abs/2403.04132 — 長度控制基準所對照的人類偏好競技場。
- Wang, P. et al. (2023). *Large Language Models are not Fair Evaluators*. arXiv. https://arxiv.org/abs/2305.17926 — 顯示候選答案的順序會改變 LLM 評估者的判定；這種偏誤不會因長度修正而消失。
- Liu, Y. et al. (2023). *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*. arXiv. https://arxiv.org/abs/2303.16634 — 另一種使用思維鏈與表單填寫的評審方法，可與原始自動評分比較。
