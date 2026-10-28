---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/continual/regularisation-based
  - theory/paradigms/continual/replay-and-memory
  - theory/paradigms/transfer/fine-tuning-and-adaptation
---

# EWC：彈性權重鞏固

EWC 是持續學習中的一種正則化方法。網路學習新任務時，會加上一項懲罰，把每個權重拉回舊任務結束時的數值。每個權重的懲罰強度，取決於該權重對舊任務的重要程度。家族層級的全貌見[基於正則化的持續學習](index.md)頁。

## 概述

Kirkpatrick 等人（2017）從災難性遺忘出發：依序訓練多個任務的網路，會逐漸失去在較早任務上的表現。他們的解法是減慢對舊任務重要權重的學習，同時讓其他權重自由移動。方法的名稱借自神經科學中的突觸鞏固概念。論文在一系列置換 MNIST 任務，以及依序學習數款 Atari 2600 遊戲的實驗上測試此方法，並宣稱單一網路可以在長時間未見的任務上保有其能力。預印本（arXiv）為 2016 年 12 月，正式發表於 2017 年的 PNAS。

## 核心概念

- **災難性遺忘**：在新任務上做梯度下降，會覆寫編碼舊任務的權重。
- **錨點** \(\theta^*_{A}\)：在舊任務 A 上學到的參數值。
- **費雪資訊** \(F_i\)：每個參數 \(i\) 對應的一個數值，衡量舊任務的概似對該權重變化的敏感程度。論文只使用對角線。論文指出，它在損失接近極小值處等於二階導數，可以只用一階導數計算，而且是半正定的。
- **強度** \(\lambda\)：決定相對於新任務，舊任務受保護的程度。
- **拉普拉斯式近似**：論文把舊任務參數的後驗視為以 \(\theta^*_A\) 為中心的高斯分布，其精度由對角費雪矩陣給出。作者把這個點估計列為限制（見下文）。

## 運作方式

學習任務 B 時，從任務 A 找到的參數出發。任務 B 的損失再加上一項二次懲罰：

\[
L(\theta) = L_B(\theta) + \sum_i \frac{\lambda}{2}\,F_i\,(\theta_i - \theta^*_{A,i})^2
\]

每個權重都像一根連在舊值上的彈簧，剛度為 \(\lambda F_i\)。費雪值小的權重可以自由移動，費雪值大的權重則留在任務 A 結束時的位置附近。任務 A 學完後，會計算對角費雪值，並與錨點一起儲存。有更多任務時，每個較早的任務各加一項懲罰，並把這些懲罰加總。

在 Atari 實驗中，論文在每次切換任務時，用重播緩衝區中的 100 個小批次重新計算對角費雪值。正文並未說明費雪值是由模型的抽樣預測估計，還是由經驗梯度估計。

## 關鍵方法

### Overcoming catastrophic forgetting in neural networks（Kirkpatrick 等人，2017）

- **問題：**對一系列任務進行基於梯度的訓練，會覆寫早期任務所依賴的權重，因此網路會遺忘。論文把依序學習任務視為人工智慧的關鍵，並把遺忘視為障礙。
- **核心想法：**依每個權重對舊任務的估計重要性，懲罰其改變量，並以 Fisher 資訊作為重要性的度量。重要的權重維持在舊值附近，不重要的權重則適應新任務。
- **方程式或演算法：**即上方的受懲罰損失，在每個任務之後計算對角 Fisher。每個舊任務各加一項懲罰，即可把方法推廣到多個任務。
- **結果：**在 MNIST 排列任務上，結果只以圖形呈現，文字中沒有準確率數值。在依序的 Atari 2600 遊戲上，論文繪製的是上限為 10 的總人類正規化分數曲線，逐遊戲的分數也只在圖中，因此本頁不引用這些數值。論文的設定包括每個序列十個遊戲，從 DQN 達到人類水準或以上的遊戲中隨機抽取，並在附錄中使用 400 的 EWC 懲罰縮放係數。論文報告，EWC 單一網路的分數不及十個分開訓練的 DQN。
- **限制：**論文對權重採用的對角、點估計處理是一種近似。論文指出 EWC 能讓「大量任務依序學習，錯誤率僅適度增加」，但其圖形只呈現少數任務序列，因此擴展性的說法是定性的。

## 關聯

- 同一家族中的其他懲罰與蒸餾方法，例如突觸智慧與無遺忘學習，列於[基於正則化的持續學習](index.md)頁。它們是線上估計重要性，或改用蒸餾舊輸出，而非使用費雪資訊。
- 保留舊資料的主要替代方案是[重播與記憶](../replay-and-memory/index.md)。
- 從預訓練模型出發，如[微調與適應](../../transfer/fine-tuning-and-adaptation/index.md)所述，是許多實際情境中較簡單的減少遺忘方式。
- 學習快速適應的起始點，而非保護舊任務的方法，是 [MAML](../../meta-learning/optimisation-based/maml.md)。

## 開放問題

- 更完整的後驗，或對權重做貝氏處理，能否在可接受的成本下修正被低估的不確定性？論文提出這個方向，但未加以測試。
- 費雪估計器（抽樣或經驗）的選擇，會對結果造成多大影響？
- 對角重要性估計在許多任務上的可靠程度如何？

## 參考文獻

### 開創性論文

- Kirkpatrick, J. et al. (2017). Overcoming catastrophic forgetting in neural networks. *PNAS* 114(13), 3521–3526. https://pmc.ncbi.nlm.nih.gov/articles/PMC5380101 — 提出 EWC。預印本為 [arXiv:1612.00796](https://arxiv.org/abs/1612.00796)。
- Zenke, F., Poole, B. & Ganguli, S. (2017). Continual Learning Through Synaptic Intelligence. arXiv:1703.04200. https://arxiv.org/abs/1703.04200 — 每個連接在訓練中追蹤自己對早期任務的貢獻，是基於 Fisher 懲罰的替代方法。
- Li, Z. & Hoiem, D. (2016). Learning without Forgetting. arXiv:1606.09282. https://arxiv.org/abs/1606.09282 — 以在新資料上蒸餾舊模型的輸出來保留早期行為，因此不需要舊的訓練資料。

### 綜述與教科書

- De Lange, M. et al. (2021). A continual learning survey: Defying forgetting in classification tasks. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2021.3057446 (arXiv:1909.08383, https://arxiv.org/abs/1909.08383) — 在常見基準上比較正則化、重播與架構方法。
- Parisi, G. I. et al. (2019). Continual Lifelong Learning with Neural Networks: A Review. arXiv:1802.07569. https://arxiv.org/abs/1802.07569 — 回顧減少災難性遺忘的持續學習方法，以及它們與生物學習的關聯。
