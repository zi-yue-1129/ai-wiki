---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/meta-learning/optimisation-based
  - theory/paradigms/transfer/fine-tuning-and-adaptation
  - theory/paradigms/continual/regularisation-based
---

# MAML：模型無關元學習

MAML 學習網路參數的初始化，使模型在新任務上只需少數幾次梯度步驟，就能取得良好表現。它在許多小型任務上訓練，其目標函數評估的是適應之後的參數，而非適應之前的參數。它是[基於最佳化的元學習](index.md)家族的代表方法。

## 概述

Finn、Abbeel 與 Levine（2017）在 ICML 2017（PMLR 70）發表 MAML。此方法不依賴特定架構：只要是以梯度下降訓練且損失可微分的模型都能使用。論文將它應用於 Omniglot 與 miniImageNet 上的少樣本分類、正弦函數回歸，以及強化學習。與一般訓練的差異在於，外層更新會對內層適應步驟求導，因此學到的起點是依據它適應的效果來選擇的。

## 核心概念

- **任務** \(\mathcal T_i\)：從任務分布 \(p(\mathcal T)\) 抽出的一個小型學習問題。每個任務有少量用於適應的範例，以及用來衡量結果的其他範例。
- **內層更新**：在單一任務上，從共享參數 \(\theta\) 出發，以步長 \(\alpha\) 做一次或多次梯度步驟。
- **元目標**：對抽樣的各任務，適應之後損失的總和。
- **元梯度**：元目標對 \(\theta\) 的梯度。它會穿過內層更新，因此包含二階導數。論文把它描述為「梯度的梯度」。
- **一階 MAML（FOMAML）**：一種近似，捨棄二階導數項，並使用適應後參數處的梯度。

## 運作方式

對任務 \(\mathcal T_i\)，一次內層步驟得到適應後的參數

\[
\theta_i' = \theta - \alpha\,\nabla_\theta \mathcal L_{\mathcal T_i}(f_\theta)
\]

元目標是各任務上適應後參數的損失總和，

\[
\min_\theta \sum_{\mathcal T_i \sim p(\mathcal T)} \mathcal L_{\mathcal T_i}\big(f_{\theta_i'}\big)
\]

共享參數則以元步長 \(\beta\) 更新：

\[
\theta \leftarrow \theta - \beta\,\nabla_\theta \sum_{\mathcal T_i \sim p(\mathcal T)} \mathcal L_{\mathcal T_i}\big(f_{\theta_i'}\big)
\]

論文的演算法 1 重複這些步驟：抽樣一批任務；對每個任務，用少量範例計算梯度並得到適應後的參數 \(\theta_i'\)；最後以加總的元梯度更新 \(\theta\)。論文實驗中的內層步長包括：miniImageNet 使用 \(\alpha = 0.01\)、訓練時 5 步內層更新；5-way Omniglot 使用 \(\alpha = 0.4\)、訓練時 1 步內層更新。論文並未為每個實驗說明元步長 \(\beta\)。它在不同領域也使用不同的最佳化器：正弦回歸使用 Adam，強化學習使用 TRPO。

## 關鍵方法

### Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks（Finn、Abbeel 與 Levine，2017）

- **問題：** 深度網路需要大量範例才能學會新任務，而少樣本學習只提供少數範例。論文要求一個初始化，使新任務只需少數梯度步驟就能學會。
- **核心想法：** 在許多任務上訓練共享的初始化，並以它在每個任務上經過幾次梯度步驟後的損失來評分。學到的初始化對任務變化敏感，因此小幅梯度步驟就能帶來大幅改善。
- **公式或演算法：** 如上所述的內層更新、元目標與演算法 1。一階變體 FOMAML 則捨棄二階導數。
- **結果：**
  - Omniglot，卷積網路（表 1）：5-way 準確率在 1-shot 為 98.7 ± 0.4%，在 5-shot 為 99.9 ± 0.1%。20-way 準確率在 1-shot 為 95.8 ± 0.3%，在 5-shot 為 98.9 ± 0.2%。
  - miniImageNet，5-way（表 1）：1-shot 為 48.70 ± 1.84%，5-shot 為 63.11 ± 0.92%。微調基準分別為 28.86 ± 0.54% 與 49.79 ± 0.79%。FOMAML 為 48.07 ± 1.75% 與 63.15 ± 0.91%，與完整 MAML 幾乎相同。
  - 正弦回歸，5-shot（表 2）：一次梯度步驟後的均方誤差為 0.67，十步後為 0.35。該表中最佳的基準（在所有任務上預訓練）分別為 2.41 與 2.19。
  - 論文指出，由於早期研究的資料切分無法取得，Omniglot 的比較結果「可能無法嚴格比較」。
- **限制：** 論文沒有獨立的限制一節。作者在正文中寫道，「MAML 的一項重大計算成本來自二階導數」。在策略上的強化學習中，每個適應步驟都需要來自當前策略的新樣本。結果也取決於內層步長與內層步數，而這些設定在各實驗之間，以及訓練與測試之間都有所不同。

## 關聯

- 更廣泛的家族，包括 Reptile 與潛在嵌入最佳化，見[基於最佳化的元學習](index.md)頁。
- 度量式方法（例如匹配網路）在 Omniglot 上與 MAML 比較。它們列於[基於度量的元學習](../metric-based/index.md)頁。
- 內層迴圈與[微調](../../transfer/fine-tuning-and-adaptation/index.md)是同一種操作，但 MAML 學習的是這種操作的起點。miniImageNet 表中的微調基準，在 1-shot 時遠低於 MAML（28.86% 對 48.70%）。
- 基於記憶的元學習器見[記憶與模型式方法](../memory-and-model-based/index.md)頁。
- 持續學習使用相似的參數空間想法，但目標是避免遺忘。見[基於正則化的持續學習](../../continual/regularisation-based/index.md)與 [EWC](../../continual/regularisation-based/ewc.md)。

## 開放問題

- 二階梯度的成本很高。一階近似在 miniImageNet 上保留了大部分準確率，但它在什麼情況下會失效？
- 內層步長與步數很重要。能否在差異很大的任務間可靠地學習它們？
- 機率式與潛在空間的延伸方法，例如機率式 MAML 與潛在嵌入最佳化，處理了不確定性與規模問題。它們在相同基準上的表現如何比較？

## 參考文獻

### 開創性論文

- Finn, C., Abbeel, P. & Levine, S. (2017). Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks. ICML (PMLR 70). https://arxiv.org/abs/1703.03400 — 提出 MAML，並報告本頁使用的 Omniglot 與 miniImageNet 結果。
- Nichol, A., Achiam, J. & Schulman, J. (2018). On First-Order Meta-Learning Algorithms. arXiv:1803.02999. https://arxiv.org/abs/1803.02999 — 分析一階 MAML 並提出 Reptile。
- Rusu, A. A. et al. (2018). Meta-Learning with Latent Embedding Optimization. arXiv:1807.05960. https://arxiv.org/abs/1807.05960 — 在學到的低維潛在空間中進行基於梯度的適應，而非在原始參數空間。
- Finn, C., Xu, K. & Levine, S. (2018). Probabilistic Model-Agnostic Meta-Learning. arXiv:1806.02817. https://arxiv.org/abs/1806.02817 — 對初始化參數放置分布，使適應時能為模糊的任務抽樣合理的模型。
- Antoniou, A., Edwards, H. & Storkey, A. (2018). How to train your MAML. arXiv:1810.09502. https://arxiv.org/abs/1810.09502 — 列出使 MAML 訓練更穩定、成本更低的改進。

### 綜述與教科書

- Hospedales, T. et al. (2020). Meta-Learning in Neural Networks: A Survey. arXiv:2004.05439. https://arxiv.org/abs/2004.05439 — 綜述元學習，並把基於梯度的方法置於其他方法家族之中。
