---
translation_reviewed: 2026-10-28
---

# DARTS：可微分架構搜尋（Liu et al., 2018）

DARTS 把離散的架構選擇換成連續的選擇。每個候選運算都會得到一個可學習的權重，這些權重與網路自身的參數一起，以梯度下降最佳化。與較早的強化學習與演化方法相比，它把[神經架構搜尋](../index.md)的成本降低了約三個數量級。

## 概述

早期的方法，包括 [RL 控制器](../nas-rl/index.md)與[正則化演化](../regularized-evolution/index.md)，都把每個候選者視為黑箱，只回傳一個分數，因此搜尋需要大量已訓練的候選者。Liu、Simonyan 與 Yang（2018）問：能否讓架構本身變成連續的，使梯度可以引導搜尋？

## 關鍵概念

- **胞元。** 被搜尋的區塊是一個小型的有向無環圖。正常胞元保持影像大小，縮減胞元則把影像縮小一半。
- **混合運算。** 在每條邊上，所有候選運算都會被套用，其輸出以 softmax 權重加總；候選者中包含一個表示無連接的零運算。
- **架構權重 \(\alpha\)。** 用來設定混合權重的可學習 logits。所有正常胞元共用一組，所有縮減胞元共用另一組。
- **一階與二階更新。** 一階更新忽略架構步驟之後權重會如何變化。二階更新則以一步前瞻來考慮這點，代價是額外的計算。

## 運作方式

搜尋交替執行兩個梯度步驟（論文的演算法 1）。

1. **架構步驟。** 以 \(\nabla_\alpha \mathcal{L}_{\mathrm{val}}(w - \xi \nabla_w \mathcal{L}_{\mathrm{train}}(w, \alpha), \alpha)\) 的梯度下降更新 \(\alpha\)。一階方法的步長 \(\xi\) 為零。
2. **權重步驟。** 在訓練資料上以 \(\nabla_w \mathcal{L}_{\mathrm{train}}(w, \alpha)\) 的梯度下降更新網路權重 \(w\)。

鬆弛把每條邊上的運算選擇換成 softmax 混合：

\[
\bar{o}^{(i,j)}(x) = \sum_{o \in \mathcal{O}} \frac{\exp\big(\alpha_o^{(i,j)}\big)}{\sum_{o' \in \mathcal{O}} \exp\big(\alpha_{o'}^{(i,j)}\big)}\, o(x),
\]

其中 \(\mathcal{O}\) 為候選運算集合。搜尋結束時，每個節點保留來自不同前驅節點的 \(k\) 個最強運算，並排除零運算。論文在每個節點保留最強的兩個前驅，而且只在搜尋的最後才這麼做。

外層目標是一個雙層問題：選擇 \(\alpha\)，使驗證損失在「對該 \(\alpha\) 使訓練損失最小的 \(w\)」下達到最小。單步近似避免了精確求解內層問題。所有候選者共享同一個過度參數化的網路及其運算權重，這使單次搜尋變得可行，但也會使排名產生偏誤，因為每個候選者的權重都是與許多其他候選者一起訓練的。

## 結果

在 CIFAR-10 上，二階 DARTS 胞元以 3.3M 參數達到 2.76% ± 0.09 的測試誤差，搜尋成本為 4 GPU 天。一階版本達到 3.00% ± 0.14，成本為 1.5 GPU 天。在同一搜尋空間中做隨機取樣，得到 3.29% ± 0.15。論文將這些成本與 NASNet 的 2000 GPU 天（Zoph et al., 2017）及 AmoebaNet 的 3150 GPU 天（Real et al., 2018）相比較。

這個胞元在行動設定下遷移到 ImageNet，top-1 誤差為 26.7%。在 Penn Treebank 上，循環胞元達到 55.7 的測試困惑度，四次執行合計約一個 GPU 天。

兩個消融實驗用來檢驗雙層公式。以座標下降在訓練與驗證資料的聯集上最佳化 \(\alpha\)，得到 4.16% ± 0.16 的誤差；以 SGD 則得到 3.56% ± 0.10。作者推測，這時 \(\alpha\) 會對訓練資料過擬合。

## 限制

- **連續到離散的落差。** 搜尋時使用的是軟混合，但最終架構只保留少數運算。論文指出了這個差異，並建議對 softmax 溫度進行退火，使混合趨於單一選擇。
- **記憶體。** 保留所有運算使超網路比任何單一候選者都大，因此搜尋在八個胞元上進行，然後把胞元放到二十個胞元的網路中評估。
- **搜尋空間受限。** 證據僅涵蓋在同一模板內的卷積與循環胞元。

## 開放問題

- **離散化。** 能否在保持梯度效率的同時，縮小鬆弛網路與離散架構之間的落差？
- **穩健性。** 在共同協定下，這個優勢還能保留多少？Yang et al.（2019）主張應以隨機架構來衡量增益。
- **隨機搜尋。** Li and Talwalkar（2019）發現，附權重共享的隨機搜尋在 PTB 上勝過附提前停止的隨機搜尋，在 CIFAR-10 上則極具競爭力。部分增益可能來自共享方案與搜尋空間，而不僅僅來自梯度。

## 參考文獻

### 開創性論文

- Liu, H., Simonyan, K. & Yang, Y. (2018). *DARTS: Differentiable Architecture Search*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — 論文本身：以梯度下降訓練的架構選擇連續鬆弛。
- Zoph, B., et al. (2017). *Learning Transferable Architectures for Scalable Image Recognition*. arXiv:1707.07012. https://arxiv.org/abs/1707.07012 — NASNet，DARTS 比較其約 2000 GPU 天成本的搜尋胞元。
- Pham, H., et al. (2018). *Efficient Neural Architecture Search via Parameter Sharing*. arXiv:1802.03268. https://arxiv.org/abs/1802.03268 — ENAS，DARTS 所比較的低成本權重共享基準。
- Real, E., et al. (2018). *Regularized Evolution for Image Classifier Architecture Search*. arXiv:1802.01548. https://arxiv.org/abs/1802.01548 — AmoebaNet 的搜尋，成本約 3150 GPU 天，DARTS 與之比較。

### 綜述與教科書

- Elsken, T., Metzen, J. H. & Hutter, F. (2018). *Neural Architecture Search: A Survey*. arXiv:1808.05377. https://arxiv.org/abs/1808.05377 — 依搜尋空間、搜尋策略與效能估計組織 NAS。

### 文章與文件

- Li, L. & Talwalkar, A. (2019). *Random Search and Reproducibility for Neural Architecture Search*. arXiv:1902.07638. https://arxiv.org/abs/1902.07638 — 附權重共享的隨機搜尋，在 PTB 上勝過附提前停止的隨機搜尋。
- Yang, A., Esperança, P. M. & Carlucci, F. M. (2019). *NAS evaluation is frustratingly hard*. arXiv:1912.12522. https://arxiv.org/abs/1912.12522 — 主張在共同協定下，並與隨機架構比較，來評估 NAS 方法。
