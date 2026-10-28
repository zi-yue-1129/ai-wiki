---
translation_reviewed: 2026-10-28
---

# 神經符號 AI

神經符號 AI 結合從資料學習的神經網路，以及表示與推理結構的符號元件，例如邏輯、規則與知識圖譜。目標是在同一系統中兼顧學習的穩健性與推理的明確性。本頁是[符號 AI、搜尋與規劃](../index.md)的一部分。

## 概述

神經網路能從大量資料學習，但不容易檢視，而且對概念的新組合往往泛化不佳。符號系統能精確推理結構，但需要人工撰寫知識。神經符號的研究問的是如何兼得兩者。Garcez 與 Lamb（2023）把此領域描述為繼統計學習之後的第三波 AI。

## 關鍵概念

- **以邏輯作為約束**：把邏輯規則轉為訓練訊號，使網路違反規則時受到懲罰。
- **以邏輯作為表示**：邏輯公式在連續、模糊的真值上求值，因此可以微分，並與網路一起訓練（Serafini 與 Garcez，2016）。
- **規則抽取**：分析已訓練的網路，產生描述其行為的符號規則。
- **機率邏輯**：帶權重的邏輯公式定義可能世界上的分布，是邏輯與學習最早的結合方式之一（Richardson 與 Domingos，2006）。

## 運作方式

文獻中有三種主要模式。第一種是以包含邏輯約束的損失函數訓練神經模型，以先驗知識引導學習。第二種是把邏輯結構內建到網路中，使其輸入與輸出為謂詞或關係。第三種是端到端地學習邏輯或機率模型，並以可微分的運算表示規則，例如可微分的歸納邏輯程式設計（Evans 與 Grefenstette，2018）。

## 主要方法

- [馬可夫邏輯網路](markov-logic-networks.md)：帶權重的一階公式，定義可能世界上的對數線性分布。它把邏輯與[圖模型](../../probabilistic/graphical-models/index.md)所述的機率圖模型結合起來。

其他結合方式，包括邏輯張量網路（Serafini 與 Garcez，2016）與可微分歸納邏輯（Evans 與 Grefenstette，2018），在此僅作摘要，目前尚無專頁。

## 與其他頁面的連結

- [知識圖譜與知識表示](../knowledge-graphs/index.md)提供神經符號系統所要推理的結構化事實。
- [機率圖模型](../../probabilistic/graphical-models/index.md)提供馬可夫邏輯網路所用的機率模型。
- [監督式學習](../../supervised/index.md)涵蓋神經訓練方法，是多數此類系統的學習端。

## 應用

- **關係資料的推理**：以邏輯規則與學得的權重進行實體解析與關係分類（Richardson 與 Domingos，2006）。
- **帶先驗知識的學習**：在已知少數規則而資料有限的任務中訓練模型。
- **可解釋的學習**：從資料中歸納出的規則，人可以逐條檢查（Evans 與 Grefenstette，2018）。

## 開放問題

- 把邏輯建立在連續表示上並不唯一，不同的模糊語意可能得到不同結果。
- 把精確或近似的機率邏輯擴展到大型領域，成本仍然很高。
- 神經符號系統是否在哪些任務上比純神經系統泛化得更好，需要系統性的評估（Garcez 與 Lamb，2023）。

## 參考文獻

### 奠基性論文

- Richardson, M. & Domingos, P. (2006). Markov logic networks. *Machine Learning* 62(1–2), 107–136. https://doi.org/10.1007/s10994-006-5833-1 — 提出馬可夫邏輯網路，把帶權重的一階公式作為可能世界上馬可夫網路的模板。
- Serafini, L. & Garcez, A. d'A. (2016). Logic tensor networks: deep learning and logical reasoning from data and knowledge. arXiv:1606.04422. https://arxiv.org/abs/1606.04422 — 提出實數值邏輯，使一階公式能與神經模型一起訓練。
- Evans, R. & Grefenstette, E. (2018). Learning explanatory rules from noisy data. *Journal of Artificial Intelligence Research* 61, 1–64. https://doi.org/10.1613/jair.5714 — 以可微分的歸納邏輯程式設計，從雜訊資料中學習規則。

### 綜述與教科書

- Garcez, A. d'A. & Lamb, L. C. (2023). Neurosymbolic AI: the 3rd wave. *Artificial Intelligence Review* 56(11), 12387–12406. https://doi.org/10.1007/s10462-023-10448-w — 神經符號領域的綜述與主要方向。
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — 神經符號研究所結合的邏輯與機率推理背景。
