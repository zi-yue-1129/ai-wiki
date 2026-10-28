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

- **問題：** 在一連串任務上做基於梯度的訓練，會覆寫較早任務所依賴的權重，因此網路遺忘。論文把依序學習任務視為人工智慧的關鍵能力，並把遺忘視為主要障礙。
- **核心想法：** 依舊任務的估計重要性，懲罰每個權重的改變幅度，並以費雪資訊作為重要性的衡量。重要的權重留在舊值附近，不重要的權重則可以適應新任務。
- **公式或演算法：** 上節的懲罰損失，以及每個任務後計算的對角費雪值。每個舊任務一項懲罰，即可擴展到多個任務。
- **結果：** 在 MNIST 置換任務上，結果只以圖形呈現，正文未給出準確率數值。在依序 Atari 2600 遊戲上，各遊戲的分數只以曲線呈現，因此本頁不引用具體數字。論文的設定包括：每個序列使用 19 款遊戲的池中抽出的 10 款（這 19 款是獨立 DQN 能達到人類水準或以上的遊戲），以及費雪縮放係數 400。論文描述，給予網路真實任務標籤（而非學到的標籤）的好處只是「適度」的。
- **限制：** 作者表示，點估計（對角拉普拉斯）的處理方式「確實是一項重大弱點」，而且實作「低估了參數的不確定性」。使用單一網路時，EWC 「未能達到」十個獨立 DQN 的分數。此方法還需要為每個突觸儲存三個數值：權重、其費雪值與錨點。論文沒有獨立的限制一節，以上內容取自其討論。

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

- Kirkpatrick, J. 等人 (2017). Overcoming catastrophic forgetting in neural networks. PNAS. https://doi.org/10.1073/pnas.1611835114 — 提出 EWC。arXiv 預印本為 [arXiv:1612.00796](https://arxiv.org/abs/1612.00796)。
- Zenke, F., Poole, B. & Ganguli, S. (2017). Continual Learning Through Synaptic Intelligence. arXiv:1703.04200. https://arxiv.org/abs/1703.04200 — 每個連結在訓練中追蹤它對較早任務的有用程度，是基於費雪的懲罰的另一種選擇。
- Li, Z. & Hoiem, D. (2016). Learning without Forgetting. arXiv:1606.09282. https://arxiv.org/abs/1606.09282 — 在新資料上蒸餾舊模型的輸出，以保留先前的行為，因此不需要舊的訓練資料。

### 綜述與教科書

- De Lange, M. 等人 (2021). A continual learning survey: Defying forgetting in classification tasks. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2021.3057446（arXiv:1909.08383，https://arxiv.org/abs/1909.08383）— 在共同的基準上比較正則化、重播與架構方法。
- Parisi, G. I. 等人 (2019). Continual lifelong learning with neural networks: a review. Neural Networks. https://doi.org/10.1016/j.neunet.2019.01.012（arXiv:1802.07569，https://arxiv.org/abs/1802.07569）— 回顧減少災難性遺忘的持續學習方法，並討論其與生物學習的關聯。
