---
translation_reviewed: 2026-10-28
---

# 格點搜尋

格點搜尋在由每個超參數的候選值所形成的固定格點上，每一點都訓練一次模型，並保留最好的一點。它簡單且可重現，但成本隨超參數數目呈指數成長。本頁是[超參數最佳化](index.md)的一部分。

## 概述

格點搜尋是人工調校模型時最常見的方法，因為格點容易寫下，結果也容易閱讀。Bergstra 與 Bengio（2012）指出，當只有少數超參數重要時，它的效率不佳：格點把大部分執行次數花在只在不重要維度上不同的組合上。此方法仍然是有用的基準，也是隨機取樣的比較對象。

## 關鍵概念

- **格點**：每個超參數的候選值集合，其乘積即為所有要嘗試的設定。
- **格點點**：格點中的一組設定。
- **解析度**：每個超參數的候選值數目。

## 問題

在只有少數超參數、且預算已知的情況下，應該在規則格點上嘗試哪些設定，才能在其中找到最好的一組？

## 運作方式

若超參數的候選集合大小為 \(n_1, \dots, n_d\)，則格點的點數為 \(|\mathcal G| = \prod_{i=1}^{d} n_i\)。每個點都經過訓練並評分，回傳最好的一點。因此執行次數隨超參數數目 \(d\) 呈指數成長，若每個超參數有 \(n\) 個值，則執行次數為 \(n^d\)。

## 主要方法

本頁只涵蓋一種方法：全因子格點，每個點都以完整預算訓練。

1. 為每個超參數選擇候選值集合，對乘性的超參數，常在對數尺度上等距排列。
2. 取這些集合的乘積，得到格點。
3. 訓練每個點，並記錄其驗證分數。
4. 回傳最好的點。

## 變體

- **由粗到細的格點**先執行粗格點，再在最佳區域附近執行較細的格點。
- **隨機格點子集**從完整格點中隨機取出子集，是格點與隨機搜尋之間的中間步驟。

## 結果與限制

- Bergstra 與 Bengio（2012）顯示，格點可能只給出重要超參數的少數不同值，因為大部分執行都在重複不重要超參數的值。相同的執行次數下，隨機取樣能為每個維度提供更多不同的值。
- 執行次數以 \(n^d\) 成長，因此超過少數超參數時格點便不切實際。
- 格點搜尋不會利用先前執行的結果來選擇後續設定，因此無法把執行集中在分數較好的區域。
- 其結果可重現，也容易平行化，因為每個點都彼此獨立。

## 應用

- **小型搜尋**，針對兩到三個超參數，例如學習率與正則化強度。
- **模型的健全性檢查**，完整格點能讓每個設定的效果一目了然。
- **比較新搜尋方法的基準**，在相同預算下進行比較。

## 開放問題

- 當某超參數的最佳值依賴其他超參數時，格點應如何安排間距？
- 考慮到隨機搜尋幾乎總是效率至少相當，何時格點仍勝過隨機搜尋？

## 與其他頁面的連結

- 上層主題：[超參數最佳化](index.md)
- 取樣的替代方案：[隨機搜尋](random-search.md)
- 以模型為基礎的替代方案：[貝氏最佳化](bayesian-optimisation.md)

## 參考文獻

### 奠基性論文

- Bergstra, J. & Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research* 13, 281–305. https://jmlr.org/papers/v13/bergstra12a.html — 比較格點搜尋與隨機取樣，並顯示當只有少數超參數重要時格點的低效率。
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). Practical Bayesian Optimization of Machine Learning Algorithms. In *NeurIPS 2012*. arXiv:1206.2944. https://arxiv.org/abs/1206.2944 — 以先前結果選擇後續設定的以模型為基礎替代方案，與固定格點不同。

### 綜述與教科書

- Feurer, M. & Hutter, F. (2019). Hyperparameter Optimization. In *Automated Machine Learning*, Springer, 3–33. https://doi.org/10.1007/978-3-030-05318-5_1 — 把格點搜尋描述為該領域基準的章節。
- Shahriari, B. et al. (2016). Taking the Human Out of the Loop: A Review of Bayesian Optimization. *Proceedings of the IEEE* 104(1), 148–175. https://doi.org/10.1109/JPROC.2015.2494218 — 比較格點搜尋與以模型為基礎搜尋的綜述。
- Hutter, F., Kotthoff, L. & Vanschoren, J. (eds.) (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer. https://doi.org/10.1007/978-3-030-05318-5 — 與其他調校方法一併討論格點搜尋的書籍章節。
- Li, L. et al. (2017). Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization. *Journal of Machine Learning Research* 18(185). arXiv:1603.06560. https://arxiv.org/abs/1603.06560 — 在相同執行次數下，與格點與隨機搜尋比較其預算分配。
