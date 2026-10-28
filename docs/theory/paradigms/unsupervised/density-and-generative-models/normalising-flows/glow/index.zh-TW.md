---
translation_reviewed: 2026-10-28
---

# Glow

Glow（Kingma 與 Dhariwal，2018）是一種用於影像的[正規化流](../index.md)。流的每一步結合三個部分：actnorm 層、混合通道的可逆 1×1 卷積，以及仿射耦合層。它保留了 [RealNVP](../realnvp/index.md) 的多尺度設計，在相同的影像基準上改善了對數似然，並展示了大型影像的逼真合成與操控。

## 概述

RealNVP 在耦合層之間反轉通道的順序。Glow 則以可學習的可逆 1×1 卷積取代這種固定的反轉。論文顯示，與反轉或固定的隨機置換相比，它能降低負對數似然並加快收斂。

Glow 也以 actnorm 取代批次正規化。作者的理由是，批次正規化的效能在每個處理單元的小批次時會下降，而大型影像迫使批次大小只能是一。Actnorm 是逐通道的縮放與偏移，以第一個小批次初始化，使激活值一開始具有零均值與單位變異數。

## 核心概念

- **流的一步**：依序套用 actnorm、一次 1×1 卷積與一個仿射耦合層。消融實驗使用每一層級 \(K = 32\) 步、共 \(L = 3\) 個層級。
- **可逆 1×1 卷積**：在每個空間位置上套用到通道向量的一個可學習矩陣 \(W\)。只要 \(W\) 非奇異，它就是可逆的。
- **LU 參數化**：把 \(W\) 寫成一個置換矩陣、一個對角線為一的下三角矩陣與一個上三角矩陣的乘積。對於 \(c\) 個通道，這把其對數行列式的成本從 \(O(c^3)\) 降為 \(O(c)\)。
- **多尺度架構**：與 RealNVP 相同，每個層級中張量先被壓縮，執行各步後，一半的通道被分出，送入潛在向量。

## 運作方式

對於高為 \(h\)、寬為 \(w\)、通道數為 \(c\) 的張量，論文給出每個元件的前向映射與對數行列式：

| 元件 | 前向映射 | 對數行列式 |
|---|---|---|
| Actnorm | \(y_{i,j} = s \odot x_{i,j} + b\) | \(h \cdot w \cdot \sum \log\lvert s\rvert\) |
| 可逆 1×1 卷積 | \(y_{i,j} = W x_{i,j}\) | \(h \cdot w \cdot \log\lvert\det W\rvert\) |
| 仿射耦合 | 與 RealNVP 相同，其縮放 \(s\) 與平移 \(t\) 由一半的通道計算 | 被耦合那一半上 \(\sum_j s_j\) |

總對數行列式是所有步驟之和。縮放與平移網路為卷積網路，隱藏層有 512 個通道。

訓練步驟如下：

1. 以第一個小批次初始化每個 actnorm 層。
2. 在每個層級中，壓縮張量、執行各步，然後分出一半的通道。
3. 加總對數行列式，並計算潛在向量在高斯先驗下的對數密度，接著最大化平均對數似然。

取樣時，從先驗抽取潛在向量，再反向執行各步。論文發現，從降溫的模型 \(p_{\theta,T}(x) \propto p_\theta(x)^T\) 取樣，通常能得到較好的樣本；對於加性耦合層，這相當於把先驗的標準差乘以 \(T\)。論文的隨機樣本使用 \(T = 0.7\)。

## 結果

在影像基準上，Glow 在每個資料集都報告了比 RealNVP 更低的每維位元數，使用相同的預處理：

| 資料集 | RealNVP | Glow |
|---|---|---|
| CIFAR-10 | 3.49 | 3.35 |
| ImageNet 32 × 32 | 4.28 | 4.09 |
| ImageNet 64 × 64 | 3.98 | 3.81 |
| LSUN（bedroom） | 2.72 | 2.38 |
| LSUN（tower） | 2.81 | 2.46 |
| LSUN（church outdoor） | 3.08 | 2.67 |

在 CIFAR-10 的消融實驗中，學到的 1×1 卷積在加性與仿射耦合兩種情況下都優於另外兩種選擇，且收斂最快。論文報告，它只增加約 0.2% 的參數與約 7% 的牆鐘時間。論文也展示了 CelebA-HQ 上 256 × 256 的樣本，以及沿著從 CelebA 標籤（例如微笑）學得的方向移動潛在編碼所做的屬性編輯。

## 限制

- **高解析度的成本。**論文報告，在單一 GPU 上以批次大小一生成 256 × 256 的影像約需 130 毫秒。在此規模下訓練，需要梯度檢查點，且每個裝置只能處理一張影像。
- **深度帶來的記憶體。**激活值的記憶體隨步數增加，可逆性原則上能降低這項成本；作者把這留待未來的工作。
- **去量化。**Glow 繼承了影像密度模型的離散化問題，Ho 等人（2019）表明，它會影響流所能達到的似然。
- **適用範圍。**屬性實驗使用具有二元標籤的人臉，論文並未測試其他影像領域。

## 未解問題

- 哪些通道混合與耦合設計，能以最少的參數得到最佳的似然？Flow++（Ho 等人，2019）與神經樣條流（Durkan 等人，2019）藉由改變耦合變換本身，部分回答了這個問題。
- 如同可逆性的論證所暗示，深層流的記憶體成本能否在實務上降低，同時不失去精確的似然？

## 參考文獻

### 開創性論文

- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS. https://arxiv.org/abs/1807.03039 — 論文本身：actnorm、可逆 1×1 卷積、影像基準，以及本頁討論的人臉編輯實驗。
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2016). *Density estimation using Real NVP*. arXiv. https://arxiv.org/abs/1605.08803 — Glow 所延伸的耦合架構與多尺度設計，也是上述各項比較的基準。
- Ho, J., Chen, X., Srinivas, A., Duan, Y. & Abbeel, P. (2019). *Flow++: Improving Flow-Based Generative Models with Variational Dequantization and Architecture Design*. ICML. https://arxiv.org/abs/1902.00275 — 顯示均勻去量化與仿射耦合的選擇會限制流，並在此基礎上加以改進。
- Durkan, C., Bekasov, A., Murray, I. & Papamakarios, G. (2019). *Neural Spline Flows*. NeurIPS. https://arxiv.org/abs/1906.04032 — 以仍可解析求逆的樣條取代仿射耦合變換。

### 綜述與教科書

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 綜述正規化流，並討論 Glow 各元件所處理的設計取捨。
