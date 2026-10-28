---
translation_reviewed: 2026-10-28
---

# 稀疏自編碼器與特徵字典

稀疏自編碼器是一種網路，訓練目標是用一個寬的編碼重建模型的內部激活，而在任何輸入下，這個編碼中只有少數項目會活躍。每一項（即一個特徵）都對應到一個可辨識的概念，因此學到的整組特徵就構成一本字典，用來讀取模型所表示的內容。

## 概述

神經網路的某一層很難直接讀懂。它的神經元通常會對許多不相干的事物產生反應，也就是[機械式可解釋性與電路](mechanistic-interpretability.md)中所描述的多義性問題。一種解釋是疊加：網路把比神經元數量更多的概念，塞進近似正交的方向中。若此說成立，自然的單位就是方向而非單一神經元，而任務便是找出這些方向。

稀疏自編碼器（SAE）嘗試在沒有標籤的情況下找出這些方向。Cunningham et al. (2023) 報告的特徵，比其他方法得到的方向更易解讀。這個想法有較早的淵源：自然影像的稀疏編碼（見[稀疏編碼](../../brain-mind/computational-neuroscience/sparse-coding/index.md)），以及訊號處理中的字典學習（Mairal et al., 2009）。

## 核心概念

- **激活（activation）**：某一層對一個 token 產生的向量。SAE 以激活作為輸入。
- **過完備字典（overcomplete dictionary）**：特徵方向的數量多於輸入維度，這是疊加所要求的。
- **稀疏性（sparsity）**：對於一個輸入，有多少特徵是活躍的（即 L0 範數），通常會以其可解的替代形式 L1 範數加以懲罰。
- **權衡（trade-off）**：字典可以靠使用許多特徵來重建得很好，也可以靠丟棄資訊來保持稀疏。訓練的目的，就是在兩者之間取得平衡。
- **失活潛在特徵（dead latent）**：在訓練資料上從不活躍的特徵，會白白浪費容量。
- **單義性（monosemanticity）**：一個特徵只追蹤單一概念的性質，判斷方式是其最強烈的輸入所對應的解釋是否連貫。

## 運作方式

對於一個激活 $x$，編碼器把它映射到更寬的編碼 $f(x)$，解碼器則以特徵方向的加權和重建它：

$$f(x) = \sigma(W_{\text{enc}}\,x + b_{\text{enc}}), \qquad \hat{x} = W_{\text{dec}}\,f(x) + b_{\text{dec}}$$

訓練時最小化重建誤差加上對編碼的懲罰：

$$\mathcal{L} = \lVert x - \hat{x} \rVert_2^2 + \lambda\,\lVert f(x) \rVert_1$$

```mermaid
flowchart LR
    A["層激活 x"] --> B["編碼器：寬的稀疏編碼 f(x)"]
    B --> C["解碼器：特徵方向的加總"]
    C --> D["重建結果 x-hat"]
    D --> E["損失：誤差加上稀疏懲罰"]
```

訓練完成後，每個特徵會透過收集最強烈啟動它的輸入來加以解讀。Cunningham et al. (2023) 以自動化方法而非人工來為特徵評分。由於模型有許多層，完整的研究需要每一層各一個 SAE，通常還要每個子層各一個。

## 關鍵方法

這些變體的差別在於如何實施稀疏性，以下逐一在文中比較。

| 變體 | 稀疏性的實施方式 | 針對的問題 |
|---|---|---|
| 搭配 L1 懲罰的 ReLU（Cunningham et al., 2023） | 對編碼大小施加懲罰 | 基準方法。懲罰同時也會使特徵的量值收縮 |
| 門控 SAE（Rajamanoharan et al., 2024a） | 一條路徑決定哪些特徵啟動，另一條路徑估計其大小；L1 懲罰只作用於前者 | 收縮（shrinkage），即激活被系統性地低估 |
| TopK 或 k-sparse（Makhzani & Frey, 2013；Gao et al., 2024） | 每個輸入只保留最大的 k 個激活 | 直接設定稀疏程度；Gao et al. 加入的修改使失活潛在特徵很少 |
| BatchTopK（Bussmann et al., 2024） | top-k 規則套用於整個批次，因此每個輸入的數量會變動 | 固定的 k 讓容易與困難的輸入使用相同數量的特徵 |
| JumpReLU（Rajamanoharan et al., 2024b） | 每個特徵有自己學到的閾值；L0 計數以直通估計器（straight-through estimator）訓練 | 在給定稀疏程度下的重建品質；Gemma Scope 採用此變體 |

論文通常在固定的稀疏程度下比較各變體，因為越稀疏的編碼通常重建得越差。Rajamanoharan et al. (2024b) 報告，在 Gemma 2 9B 的激活上，於給定稀疏程度下達到最佳的重建。Gao et al. (2024) 則在 GPT-4 的激活上訓練了一個含 1,600 萬個潛在變數的自編碼器，並報告了清晰的擴展趨勢。

## 連結

- 上層總覽為[可解釋性](index.md)。此處找到的特徵，正是[機械式可解釋性與電路](mechanistic-interpretability.md)中電路分析所依託的單位。SAE 也是一種稀疏、過完備的[自編碼器](../../theory/paradigms/unsupervised/autoencoders-and-representations/index.md)。
- 探測需要帶標籤的概念；SAE 則在沒有標籤的情況下提出概念，而這些概念仍須檢驗。見[探測分類器與表徵分析](probing.md)。
- 與神經科學的連結十分直接。Olshausen 與 Field（1996）透過學習自然影像的稀疏編碼，解釋了 V1 的感受野；SAE 則把同樣的目標套用到已訓練網路的激活上。見[NeuroAI](../../brain-mind/neuroai/index.md)。

## 應用

- **開放的研究工具。** Gemma Scope 釋出了 Gemma 2 2B 與 9B 每一層與每個子層的 SAE，因為訓練完整的一套對產業以外的研究者而言成本過高（Lieberum et al., 2024）。
- **引導（steering）。** Arad et al. (2025) 發現，依特徵對輸出的效果來篩選，而非依啟動它的輸入來篩選，能讓引導效果提升兩到三倍，使 SAE 足以與有監督的方法競爭。引導是[安全與對齊](../safety-alignment/index.md)所討論的控制途徑之一。

## 開放問題

### 這些特徵是真正的基本單位嗎？

Leask et al. (2025) 以 SAE 縫合（stitching）顯示字典並不完整，並以元 SAE（meta-SAE）顯示其特徵並非不可再分。一組正典的基本分析單位至今尚未確立。

### 特徵分裂與吸收

當概念形成階層時，稀疏字典可能會把父概念分裂成多個子概念。Chanin et al. (2024) 發現，父概念因此可能在應該啟動的地方卻不啟動，其含義被子特徵吸收。改變 SAE 的大小或稀疏程度並無法消除此現象。

### 對下游任務有幫助嗎？

Kantamneni et al. (2025) 在資料稀少、類別不平衡、標籤有雜訊與分布偏移的情境下，把 SAE 特徵當作探測器來測試。SAE 有時在單一資料集上勝過基準，但與 SAE 的集成並不能可靠地勝過不含 SAE 的集成，而且簡單的非 SAE 基準在多項任務上與之持平。

### 規模與評估

沒有人知道模型內部真正的概念，因此評分仰賴自動化的代理指標。Gao et al. (2024) 顯示重建與特徵品質會隨規模提升，但特徵能否解釋前沿模型的運算，而不只是重建其激活，仍是開放問題。

## 參考文獻

### 開創性論文

- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*. https://doi.org/10.1038/381607a0 — 顯示自然影像的稀疏編碼會產生類似 V1 的定向濾波器。
- Mairal, J., Bach, F., Ponce, J. & Sapiro, G. (2009). Online learning for matrix factorization and sparse coding. arXiv. https://arxiv.org/abs/0908.0050 — 提出在大型資料集上線上學習字典的演算法。
- Makhzani, A. & Frey, B. (2013). k-Sparse Autoencoders. arXiv. https://arxiv.org/abs/1312.5663 — 提出 k-sparse 自編碼器，只保留最大的 k 個隱藏活動。
- Cunningham, H., et al. (2023). Sparse Autoencoders Find Highly Interpretable Features in Language Models. arXiv. https://arxiv.org/abs/2309.08600 — 將稀疏自編碼器套用於語言模型激活，並找到比其他分解方法更具單義性的特徵。
- Rajamanoharan, S., et al. (2024a). Improving Dictionary Learning with Gated Sparse Autoencoders. arXiv. https://arxiv.org/abs/2404.16014 — 提出門控變體，消除 L1 懲罰所造成的收縮。
- Rajamanoharan, S., et al. (2024b). Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU Sparse Autoencoders. arXiv. https://arxiv.org/abs/2407.14435 — 提出 JumpReLU SAE，在給定稀疏程度下，對 Gemma 2 9B 激活的重建優於門控與 TopK 變體。
- Gao, L., et al. (2024). Scaling and evaluating sparse autoencoders. arXiv. https://arxiv.org/abs/2406.04093 — 大規模訓練 TopK SAE，包括在 GPT-4 激活上訓練的 1,600 萬潛在變數模型，並提出特徵品質指標。
- Bussmann, B., Leask, P. & Nanda, N. (2024). BatchTopK Sparse Autoencoders. arXiv. https://arxiv.org/abs/2412.06410 — 把 TopK 限制放寬到批次層級，使每個輸入啟動的特徵數量可以變動。
- Chanin, D., et al. (2024). A is for Absorption: Studying Feature Splitting and Absorption in Sparse Autoencoders. arXiv. https://arxiv.org/abs/2409.14507 — 顯示在為稀疏性而訓練的 SAE 中，階層特徵會被子特徵吸收。
- Leask, P., et al. (2025). Sparse Autoencoders Do Not Find Canonical Units of Analysis. arXiv. https://arxiv.org/abs/2502.04878 — 以 SAE 縫合與元 SAE 顯示 SAE 特徵並不完整，也非不可再分。
- Kantamneni, S., et al. (2025). Are Sparse Autoencoders Useful? A Case Study in Sparse Probing. arXiv. https://arxiv.org/abs/2502.16681 — 在困難情境中把 SAE 特徵當作探測器來測試，發現它們只偶爾勝過簡單基準。
- Arad, D., Mueller, A. & Belinkov, Y. (2025). SAEs Are Good for Steering -- If You Select the Right Features. arXiv. https://arxiv.org/abs/2505.20063 — 區分輸入特徵與輸出特徵，並顯示依輸出分數篩選能改善引導效果。

### 綜述與教科書

- Sharkey, L., et al. (2025). Open Problems in Mechanistic Interpretability. arXiv. https://arxiv.org/abs/2501.16496 — 對機械式可解釋性未解問題的合作式綜述，也是評判 SAE 成果的背景。

### 文章與文件

- Lieberum, T., et al. (2024). Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2. arXiv. https://arxiv.org/abs/2408.05147 — 為 Gemma 2 2B 與 9B 的每一層釋出 JumpReLU SAE，並附權重與評估結果。
