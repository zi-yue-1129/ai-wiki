---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - theory/evaluation/protocols/index.md
tags:
  - evaluation
  - protocols
  - llm-as-judge
---

# LLM 作為評審

LLM 作為評審是一種評估協定，由語言模型依書寫的評分準則為另一個模型的輸出打分，或直接比較兩個輸出。它讓開放式答案能以人類評分者無法達到的規模來衡量，但評審本身有偏誤，因此分數必須與人類判斷對照（Zheng et al., 2023）。

## 程序

這個協定有三個部分：定義好答案標準的評分準則、要求給分或偏好的評審提示，以及把回覆轉成數字的解析器。成對比較會請評審判斷兩個答案何者較好；單一答案評分則依固定尺度為每個答案給分（Zheng et al., 2023）。

## 主要方法

本頁提到的三種評審方法各有獨立頁面。它們都在回答同一個問題：如何從模型取得可靠的判斷，只是做法不同。

- [MT-Bench](mt-bench.md)：以固定提示、交換答案順序並計入平手的成對與單一答案評分。它與人類專家的一致度，是支持模型評審最主要的證據。
- [長度控制 AlpacaEval](length-controlled-alpacaeval.md)：以迴歸修正自動評審偏好較長答案的傾向，並報告它與 Chatbot Arena 有更高的相關性。
- [Elo 評分與競技場](elo-rating.md)：把大量成對判定（來自人或模型）轉為排名，這是 Chatbot Arena 採用的彙總步驟。

## 已知偏誤

Zheng et al.（2023）報告了位置偏誤（評審偏好成對中的第一個答案）、冗長偏誤（較長的答案得分較高），以及自我偏好（評審偏好與自身風格相近的答案）。交換兩個答案的順序後取兩次判定的平均，可以減少位置偏誤；其餘偏誤則需與人類評分的樣本比對才能發現。

## 報告

報告評審模型與版本、確切的評分準則與提示、順序交換的政策、在標明樣本上與人類評分者的一致程度，以及每個項目的判定次數。評分準則或評審一旦改變，分數也會改變，因此基線必須重新評分。

## 限制

- **循環性。** 若評審訓練時使用的偏好與它被要求應用的偏好相同，它可能獎勵自身的風格。
- **評分準則過窄。** 評審可以前後一致，卻衡量錯誤的東西。
- **成本與漂移。** 託管的評審模型會隨時間改變，因此結果需要記錄版本與日期。

## 相關

- [評估協定概述](../index.md) 列出其他協定方法。
- [Elo 評分與競技場](elo-rating.md) 從大量判定中彙總偏好。
- [人工評估](human-evaluation.md) 提供評審必須對齊的參考判斷。

## 參考文獻

### 開創性論文

- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. arXiv. https://arxiv.org/abs/2306.05685 — 研究以模型為基礎的評審、其與人類的一致性以及偏誤。
- Wang, P. et al. (2023). *Large Language Models are not Fair Evaluators*. arXiv. https://arxiv.org/abs/2305.17926 — 顯示候選答案的順序會改變 LLM 評估者的判定。
- Dubois, Y. et al. (2024). *Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators*. arXiv. https://arxiv.org/abs/2404.04475 — 為自動評審提出長度控制的勝率，並報告其與 Chatbot Arena 的相關性。

### 文章與文件

- Chiang, W.-L. et al. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*. arXiv. https://arxiv.org/abs/2403.04132 — 在公開平台上結合人類成對偏好與以模型為基礎的評審。
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估語言模型，揭露其取捨。

### 補充來源

- Gehrmann, S. et al. (2022). *Repairing the Cracked Foundation: A Survey of Obstacles in Evaluation Practices for Generated Text*. arXiv. https://arxiv.org/abs/2202.06935 — 調查生成文本的評估實務與其效度問題。
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。
