---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
  - theory/paradigms/self-supervised/contrastive-learning
  - theory/models/cnn
---

# BYOL：自我引導的潛在表徵

BYOL 在沒有負樣本對的情況下學習影像表徵。一個網路去預測第二個緩慢移動副本的輸出，而這個副本處理的是同一影像的另一個增強視角。論文透過緩慢更新的目標網路與線上分支上的預測器來維持訓練穩定，而不是靠與其他影像對比。家族層級的全貌見[非對比式方法](index.md)頁。

## 概述

Grill 等人（2020）主張，強的影像表徵不一定需要負樣本對。摘要指出，當時的先進方法依賴負樣本對，而 BYOL 在不使用負樣本的情況下達到新的先進水準。在 ImageNet 的線性評估下，摘要報告 ResNet-50 為 74.3% top-1 準確率，較大的 ResNet 為 79.6%。摘要也指出，BYOL 在轉移與半監督基準上與最佳方法相當或更好，但摘要中並未給出這些基準的數字。

## 核心概念

- **線上網路**：編碼器 \(f_\theta\) 與投影器 \(g_\theta\)，後接預測器 \(q_\theta\)。它是唯一以梯度下降訓練的部分。
- **目標網路**：與線上網路架構相同的編碼器 \(f_\xi\) 與投影器 \(g_\xi\)，但權重 \(\xi\) 不接收梯度，而是線上權重的移動平均。
- **預測器** \(q_\theta\)：只在線上分支上的小型 MLP，架構與投影器相同。
- **Stop-gradient**：梯度不會流入目標分支。

## 運作方式

同一影像產生兩個增強視角。線上網路處理其中一個視角，並預測另一個視角經目標網路得到的投影。損失是 \(\ell_2\) 正規化向量之間的平方距離：

\[
\mathcal{L}_{\theta,\xi} = \big\|\bar q_\theta(z_\theta) - \bar z'_\xi\big\|_2^2 = 2 - 2\cdot\frac{\langle q_\theta(z_\theta), z'_\xi\rangle}{\|q_\theta(z_\theta)\|_2\,\|z'_\xi\|_2}
\]

其中 \(z_\theta\) 與 \(z'_\xi\) 是兩個投影，橫線表示 \(\ell_2\) 正規化。論文透過交換兩個視角來使損失對稱，總損失為兩項之和。只有 \(\theta\) 接收梯度。

目標網路以線上權重的指數移動平均更新：

\[
\xi \leftarrow \tau\,\xi + (1-\tau)\,\theta
\]

衰減係數 \(\tau\) 從 \(\tau_{\text{base}} = 0.996\) 開始，訓練過程中逐漸升至 1，依循

\[
\tau = 1 - (1-\tau_{\text{base}})\cdot\frac{\cos(\pi k/K)+1}{2}
\]

其中 \(k\) 為目前步數，\(K\) 為總步數。

投影器由輸出 4096 維的線性層、批次正規化、ReLU，以及輸出 256 維的線性層組成；預測器架構相同。訓練使用 LARS 最佳化器，學習率採餘弦衰減並有 10 個 epoch 的預熱。基礎學習率為 0.2，依批次大小除以 256 線性縮放。論文的設定使用 512 個 Cloud TPU v3 核心，批次大小 4096，訓練 1000 個 epoch。

## 關鍵方法

### Bootstrap Your Own Latent：自監督學習的新方法（Grill 等人，2020）

- **問題：**對比式方法靠負樣本避免崩塌，而負樣本需要大批次或記憶庫。論文的目標是移除這種依賴。
- **核心想法：**訓練線上網路去預測目標網路對另一視角的表徵。目標網路是線上網路的指數移動平均，不使用負樣本。
- **方程式或演算法：**正規化平方損失、\(\tau\) 從 0.996 向 1 上升的移動平均更新，以及投影器與預測器設計，如「運作方式」所述。
- **結果：**以 ResNet-50 進行 ImageNet 線性評估，得到 74.3% top-1 與 91.6% top-5；ResNet-200（2×）得到 79.6% top-1 與 94.8% top-5。在 ResNet-50 的半監督訓練中，使用 1% 標籤得到 53.2% top-1 與 78.4% top-5；使用 10% 標籤得到 68.8% top-1 與 89.0% top-5。
- **限制：**訓練配方的成本高：1000 個 epoch、批次大小 4096、512 個 TPU 核心。摘要沒有解釋為何訓練能避免崩塌，也沒有給出轉移結果的數字。後續論文 Richemond 等人（2020）指出 BYOL 在沒有批次統計量的情況下仍能運作，因此批次正規化的角色需要另外研究。

## 關聯

- [SimCLR](../contrastive-learning/simclr.md) 與 [MoCo](../contrastive-learning/moco.md) 依賴負樣本。BYOL 是不使用負樣本的方法中最主要的比較對象。
- 目標網路的動量更新與 [MoCo](../contrastive-learning/moco.md) 的動量編碼器想法相同，但 BYOL 沒有佇列。
- [遮罩預測](../masked-prediction/index.md)是另一條自監督路線：預測缺失內容，而非比對視角。
- ResNet 骨幹網路見[CNN 模型](../../../models/cnn/index.md)。
- 上述評估協定在[理論與評估](../theory-and-evaluation/index.md)中討論。

## 開放問題

- 為什麼線上網路與目標網路的設定在沒有負樣本時仍能避免崩塌？批次正規化的角色是其中一部分，後續研究正在檢驗它。
- 設定中的哪些部分（預測器、移動平均排程、正規化）是必要的，哪些主要用於加速或穩定訓練？

## 參考文獻

### 代表性論文

- Grill, J.-B. et al. (2020). *Bootstrap your own latent: A new approach to self-supervised learning*. NeurIPS. https://arxiv.org/abs/2006.07733 — 本頁介紹的論文。
- Chen, X. & He, K. (2021). *Exploring Simple Siamese Representation Learning*. CVPR. https://arxiv.org/abs/2011.10566 — SimSiam，捨棄動量目標，並顯示 stop-gradient 與預測器即可防止崩塌。
- Chen, T., Kornblith, S., Norouzi, M. & Hinton, G. (2020). *A Simple Framework for Contrastive Learning of Visual Representations*. ICML (PMLR 119). https://arxiv.org/abs/2002.05709 — BYOL 所比較的對比式方法。
- He, K., Fan, H., Wu, Y., Xie, S. & Girshick, R. (2020). *Momentum Contrast for Unsupervised Visual Representation Learning*. CVPR. https://arxiv.org/abs/1911.05722 — BYOL 目標網路所依據的動量編碼器。
- Richemond, P. H. et al. (2020). *BYOL works even without batch statistics*. arXiv:2010.10241. https://arxiv.org/abs/2010.10241 — 顯示 BYOL 在沒有批次統計量的情況下仍可運作，檢驗批次正規化是否必要。

### 綜述與教科書

- Balestriero, R. et al. (2023). *A Cookbook of Self-Supervised Learning*. arXiv:2304.12210. https://arxiv.org/abs/2304.12210 — 自監督設計選擇的實務性綜述，包含預測器與目標網路。
