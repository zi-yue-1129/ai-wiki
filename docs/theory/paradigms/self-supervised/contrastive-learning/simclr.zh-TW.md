---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
  - theory/paradigms/self-supervised/non-contrastive-methods
  - theory/paradigms/self-supervised/masked-prediction
  - theory/models/cnn
---

# SimCLR：視覺表徵對比學習的簡單框架

SimCLR 是一種用於影像的對比式方法，不需要記憶庫，也不需要特殊架構。它對每張影像取兩個隨機增強視角，分別編碼後，訓練這兩個嵌入彼此一致，同時與批次中其他影像的嵌入分開。它是多數以影像為基礎之對比學習的參考框架。家族層級的概觀見[對比學習](index.md)頁面。

## 概述

Chen、Kornblith、Norouzi 與 Hinton（2020）研究對比學習配方中哪些部分真正重要。摘要提出三項發現：資料增強的組合對於定義有用的預測任務至關重要；在表徵與對比損失之間加入可學習的非線性轉換，能提升表徵品質；對比學習比監督式學習更受益於較大的批次與較多的訓練步數。摘要報告，SimCLR 特徵上的線性分類器在 ImageNet 上達到 76.5% top-1 準確率，相較於先前的自監督方法相對提升 7%。論文附錄給出監督式 ResNet-50 的 76.3%，略低於自監督的線性結果。

## 核心概念

- **正樣本對**：同一張影像的兩個增強視角。
- **負樣本**：批次中其他的增強視角。若有 \(N\) 張影像，就有 \(2N\) 個視角，因此每個錨點有 \(2N-2\) 個負樣本。
- **增強策略**：隨機裁切加縮放與翻轉、色彩扭曲，以及高斯模糊。論文將這些增強的組合視為主要的監督來源。
- **投影頭** \(g\)：兩層 MLP，將表徵映射到 128 維空間，損失在該空間計算。訓練後丟棄。
- **溫度** \(\tau\)：在 softmax 之前縮放相似度。論文的掃描顯示，在它測試的數值中 \(\tau = 0.1\) 最好，嵌入經過 \(\ell_2\) 正規化。

## 運作方式

對批次中的每張影像，從增強分布中抽樣兩個視角。編碼器 \(f\)（一個 ResNet）產生表徵 \(h\)，投影頭產生 \(z = g(h)\)。相似度為餘弦相似度 \(\operatorname{sim}(u,v) = u^\top v / (\|u\|\,\|v\|)\)，每一對的損失是正規化、經溫度縮放的交叉熵（NT-Xent）：

\[
\ell_{i,j} = -\log \frac{\exp(\operatorname{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k\neq i]}\exp(\operatorname{sim}(z_i, z_k)/\tau)}
\]

這裡 \(i\) 與 \(j\) 是同一張影像的兩個視角，分母涵蓋批次中所有其他視角。批次損失由這些逐對項組成。下游任務使用 \(h\)，投影頭則被丟棄。

訓練使用 LARS 最佳化器。論文使用的批次大小從 256 到 8192。預設為批次大小 4096、訓練 100 個 epoch，其主要的 ImageNet 比較則使用 1000 個 epoch。裁切面積在影像的 0.08 到 1.0 之間均勻抽樣，之後有一半的機率做隨機水平翻轉。色彩扭曲的強度為 \(s\)（預設 1.0），亮度、對比與飽和度的抖動為 \(0.8s\)，色相為 \(0.2s\)。它以機率 0.8 套用，灰階化以機率 0.2 套用。高斯模糊則套用於一半的影像。

## 關鍵方法

### 視覺表徵對比學習的簡單框架（Chen、Kornblith、Norouzi 與 Hinton，2020）

- **問題：**早期的影像對比方法依賴特殊架構或記憶庫，而且不清楚哪些設計選擇最重要。
- **核心想法：**使用標準 ResNet、強增強、非線性投影頭，以及批次內負樣本的 NT-Xent 損失，然後放大批次大小與訓練長度。
- **方程式或演算法：**上述以餘弦相似度計算的 NT-Xent 損失，加上「運作方式」中所述的增強策略與 LARS 訓練。
- **結果：**論文的表 6 報告，ImageNet 線性評估的 top-1 準確率為：ResNet-50（1×）69.3%、ResNet-50（2×）74.2%、ResNet-50（4×）76.5%。表 7 報告半監督的 top-5 準確率：使用 1% 標籤時 ResNet-50（4×）為 85.8%，使用 10% 標籤時為 92.6%。
- **限制：**論文發現，對比學習受益於大批次（最高 8192）與長時間訓練。負樣本只來自目前的批次，因此其數量受批次大小限制，也就受硬體限制。最佳結果來自最大的編碼器；表 6 中 1× 模型遠低於 4× 模型。[MoCo](moco.md) 以佇列解決批次大小的限制。

## 關聯

- [MoCo](moco.md) 使用非常相近的損失，但負樣本來自佇列，因此數量不受批次大小限制。其後續研究 Improved Baselines with Momentum Contrastive Learning（Chen 等人，2020）採用 SimCLR 的 MLP 投影頭與增強策略。
- [BYOL](../non-contrastive-methods/byol.md) 完全移除負樣本。
- [遮罩自編碼器](../masked-prediction/mae.md)走另一條路：它預測遺失的內容，而不是對比不同視角。
- 上述結果所用的線性評估協定，在[理論與評估](../theory-and-evaluation/index.md)中討論。
- ResNet 骨幹在[CNN 模型](../../../models/cnn/index.md)中說明。

## 開放問題

- SimCLR 的提升有多少來自增強策略，又有多少來自批次大小與訓練長度？論文研究了兩者，但二者會交互作用。
- 為什麼損失前的非線性投影頭能改善下游使用的表徵？論文以實驗展示了這個效果，但摘要沒有給出機制。

## 參考文獻

### 代表性論文

- Chen, T., Kornblith, S., Norouzi, M. & Hinton, G. (2020). A Simple Framework for Contrastive Learning of Visual Representations. ICML (PMLR 119). https://arxiv.org/abs/2002.05709 — 本頁所述的論文。
- Chen, X., Fan, H., Girshick, R. & He, K. (2020). Improved Baselines with Momentum Contrastive Learning. arXiv:2003.04297. https://arxiv.org/abs/2003.04297 — 將 SimCLR 的 MLP 投影頭與增強策略引入 MoCo。
- He, K., Fan, H., Wu, Y., Xie, S. & Girshick, R. (2020). Momentum Contrast for Unsupervised Visual Representation Learning. CVPR. https://arxiv.org/abs/1911.05722 — 以佇列取代批次內負樣本，是取得大量負樣本的另一途徑。
- Wu, Z., Xiong, Y., Yu, S. X. & Lin, D. (2018). Unsupervised Feature Learning via Non-Parametric Instance Discrimination. CVPR. https://arxiv.org/abs/1805.01978 — 以記憶庫儲存負樣本的實例判別，SimCLR 避開了這種做法。
- Oord, A. van den, Li, Y. & Vinyals, O. (2018). Representation Learning with Contrastive Predictive Coding. arXiv:1807.03748. https://arxiv.org/abs/1807.03748 — 提出 NT-Xent 損失所依據的 InfoNCE 損失。
- Grill, J.-B. et al. (2020). Bootstrap your own latent: A new approach to self-supervised learning. arXiv:2006.07733. https://arxiv.org/abs/2006.07733 — 完全移除負樣本，是 SimCLR 設計的主要比較對象。
- He, K., Zhang, X., Ren, S. & Sun, J. (2016). Deep Residual Learning for Image Recognition. CVPR. https://arxiv.org/abs/1512.03385 — 用作編碼器的 ResNet 架構。

### 綜述與教科書

- Balestriero, R. et al. (2023). A Cookbook of Self-Supervised Learning. arXiv:2304.12210. https://arxiv.org/abs/2304.12210 — 自監督學習設計選擇的實務綜述，包含 SimCLR 所研究的內容。
