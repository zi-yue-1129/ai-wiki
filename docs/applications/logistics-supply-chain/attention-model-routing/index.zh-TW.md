---
translation_reviewed: 2026-10-28
---

# 用於路線規劃的注意力模型（Kool 等人，2018）

注意力模型是一種神經網路策略，它利用停靠點集合上的注意力層，一次決定一個停靠點，逐步建構路線。Kool、van Hoof 與 Welling 以強化學習訓練它，並以同一種模型設計與同一組超參數應用於多個路線規劃問題。它是父頁面[物流與供應鏈](../index.md)所介紹的方法之一。

## 概述

旅行推銷員問題（TSP）與車輛路徑問題（VRP）等路線問題，實務上通常由專門的求解器與人工設計的啟發式方法解決，而這些都需要高昂的開發成本。學習型啟發式方法的目標是降低這項成本。Bello 等人（2016）展示了以強化學習訓練的指標網路（pointer network）能產生不錯的 TSP 路線。Kool 等人認為模型與訓練方法都有改進空間，因此提出了以注意力為基礎的模型，以及較簡單的訓練基線。他們宣稱的目標並非擊敗最好的 TSP 求解器，而是說明同一種方法能適用於多種路線變體。

## 關鍵概念

- **編碼器**：類似 [Transformer](../../../theory/models/transformer/index.md) 的注意力層，把每個停靠點與起點轉換為嵌入向量，並以圖嵌入概括整個問題實例。
- **解碼器上下文**：由圖嵌入與最近的停靠點建構的查詢，用來為每個候選停靠點在下一步的選擇評分。
- **REINFORCE**：一種[策略梯度](../../../theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/index.md)方法，會提高成本低於基線之路線的機率。
- **貪婪展開基線**：目前最佳模型以貪婪方式建構的路線成本，用作基線。

## 運作方式

策略 $p_\theta(\pi \mid s)$ 為實例 $s$ 產生解 $\pi$，$L(\pi)$ 為其成本，例如路線長度。訓練以 REINFORCE 梯度最小化期望成本：

$$
\nabla \mathcal{L}(\theta \mid s) = \mathbb{E}_{p_\theta(\pi \mid s)}\big[(L(\pi) - b(s)) \nabla \log p_\theta(\pi \mid s)\big],
$$

其中 $b(s)$ 是目前最佳模型之貪婪解的成本。若抽樣得到的路線比貪婪解更好，其機率便會提高。

1. 以多頭注意力層編碼所有停靠點。
2. 在每一步，由圖嵌入與最後一個停靠點建構解碼器上下文，並計算它與每個停靠點的相容性分數。以 tanh 將分數裁剪到固定範圍。
3. 遮蔽不可行的停靠點，對其餘者取 softmax。訓練時，從此分布中抽出下一個停靠點。
4. 建構完整解後計算其成本，並以目前最佳模型的貪婪展開計算基線成本。
5. 以 Adam 更新參數；當目前模型有所改進時，替換基線模型。

## 結果

在包含 20、50 與 100 個停靠點的 TSP 實例上，注意力模型抽樣版本的目標值為 3.84、5.73 與 7.94，與表中最佳值的差距分別為 0.08%、0.52% 與 2.26%，而最佳值由 Concorde 與 LKH3 等強大求解器取得（Kool 等人，2018）。貪婪版本較快但較不準確；在 100 個停靠點時約需 6 秒，差距為 4.53%。基線包括開源的 OR-Tools 求解器與經典的插入式啟發式方法。摘要報告指出，此模型顯著優於先前的學習型 TSP 啟發式方法，並且在 VRP 變體、定向問題與獎懲式 TSP 上，取得接近專門演算法的結果。

## 限制

- **不能取代求解器。**與最強求解器的差距隨問題規模擴大，在 20 個停靠點時低於 1%，在採用抽樣的 100 個停靠點時超過 2%。
- **抽樣成本。**較好的路線需要更多樣本與時間。貪婪解碼較快，但會犧牲準確度。
- **靜態實例。**基準測試使用固定的實例。時間窗、變動的訂單與隨機需求等實際限制只被部分涵蓋。
- **同一設定不等於同一模型。**單一組超參數設定，並不代表有一個訓練完成的模型能處理所有問題與規模。

## 開放問題

- 學得的策略能在多大程度上泛化到未曾訓練過的實例規模與分布？
- 學習式的建構方法能否與局部搜尋或精確的精修結合，以縮小剩餘的差距？
- 學習型路線規劃器應如何因應在執行期間到達的請求？

## 參考文獻

### 開創性論文

- Kool, W., van Hoof, H. & Welling, M. (2018). Attention, learn to solve routing problems! arXiv (ICLR 2019). https://arxiv.org/abs/1803.08475 — 以 REINFORCE 與貪婪展開基線訓練的注意力模型，應用於 TSP 與數種車輛路徑變體。
- Bello, I. et al. (2016). Neural combinatorial optimization with reinforcement learning. arXiv. https://arxiv.org/abs/1611.09940 — 早期示範：以強化學習訓練的指標網路，能為旅行推銷員問題產生不錯的路線。
- Nazari, M. et al. (2018). Reinforcement learning for solving the vehicle routing problem. arXiv. https://arxiv.org/abs/1802.04240 — 以策略梯度訓練策略，僅依據獎勵信號與可行性規則建構車輛路線。
- Vaswani, A. et al. (2017). Attention is all you need. arXiv. https://arxiv.org/abs/1706.03762 — 提出編碼器與解碼器所依據的 Transformer 注意力層。
- Williams, R. J. (1992). Simple statistical gradient-following algorithms for connectionist reinforcement learning. *Machine Learning*. https://doi.org/10.1007/BF00992696 — 推導出用於訓練此策略的 REINFORCE 估計量。

### 綜述與教科書

- Psaraftis, H. N. (1995). Dynamic vehicle routing: status and prospects. *Annals of Operations Research*. https://doi.org/10.1007/bf02098286 — 較早的綜述，探討車輛在行駛途中才有新資訊到達的路線問題。
