---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
  - theory/paradigms/self-supervised/non-contrastive-methods
  - theory/paradigms/self-supervised/masked-prediction
  - theory/models/cnn
---

# SimCLR：視覺表徵對比學習的簡單框架

SimCLR 是一種用於影像的對比式方法，不需要記憶庫，也不需要特殊架構。它對每張影像取兩個隨機增強視角並加以編碼，訓練這兩個嵌入彼此靠近，同時與批次中其他影像的嵌入保持距離。它是多數影像對比學習的參照框架。家族層級的全貌見[對比學習](index.md)頁。

## 概述

Chen、Kornblith、Norouzi 與 Hinton（2020）研究對比學習配方中哪些部分真正重要。摘要提出三項發現：資料增強的組合對於定義有效的預測任務至關重要；表徵與對比損失之間加入可學習的非線性轉換，能明顯提升表徵品質；對比學習比監督式學習更受益於較大的批次與較多的訓練步數。摘要指出，在 SimCLR 表徵上訓練的線性分類器在 ImageNet 上達到 76.5% 的 top-1 準確率，相較先前的自監督方法相對提升 7%，並與監督式 ResNet-50 相當。

## 核心概念

- **正樣本對**：同一影像的兩個增強視角。
- **負樣本**：批次中其他的增強視角。N 張影像共有 \(2N\) 個視角，因此每個錨點有 \(2N-2\) 個負樣本。
- **增強策略**：隨機裁切後縮放並水平翻轉、顏色失真與高斯模糊。論文把這些增強的組合視為主要的監督來源。
- **投影頭** \(g\)：兩層 MLP，把表徵映射到 128 維空間，損失在該空間計算。訓練結束後丟棄。
- **溫度** \(\tau\)：在 softmax 前縮放相似度。論文的掃描實驗顯示，在使用 \(\ell_2\) 正規化嵌入時，\(\tau = 0.1\) 是所測試數值中最好的。

## 運作方式

每張批次中的影像都從增強分布中抽取兩個視角。編碼器 \(f\)（ResNet）產生表徵 \(h\)，投影頭產生 \(z = g(h)\)。相似度採用餘弦，\(\operatorname{sim}(u,v) = u^\top v / (\|u\|\,\|v\|)\)，每一對的損失是正規化溫度縮放交叉熵（NT-Xent）：

\[
\ell_{i,j} = -\log \frac{\exp(\operatorname{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k\neq i]}\exp(\operatorname{sim}(z_i, z_k)/\tau)}
\]

其中 \(i\) 與 \(j\) 是同一影像的兩個視角，分母涵蓋批次中所有其他視角。批次損失由這些逐對的項組成。下游任務使用 \(h\)，投影頭則丟棄。

訓練使用 LARS 最佳化器。論文使用的批次大小從 256 到 8192。預設為批次大小 4096、訓練 100 個 epoch；ImageNet 的主要比較則使用 1000 個 epoch。裁切面積在影像的 0.08 到 1.0 之間均勻抽樣，有一半的情況會再做水平翻轉。顏色失真的強度為 \(s\)（預設 1.0），亮度、對比與飽和度的抖動為 \(0.8s\)，色調為 \(0.2s\)。顏色失真以機率 0.8 施加，灰階以機率 0.2 施加，高斯模糊約作用於一半的影像。

## 關鍵方法

### 視覺表徵對比學習的簡單框架（Chen、Kornblith、Norouzi 與 Hinton，2020）

- **問題：**早期影像對比方法依賴特殊架構或記憶庫，而且不清楚哪些設計選擇最關鍵。
- **核心想法：**使用標準 ResNet、強增強、非線性投影頭，以及在批次內負樣本上計算的 NT-Xent 損失，再擴大批次大小與訓練長度。
- **方程式或演算法：**上述以餘弦相似度計算的 NT-Xent 損失，以及「運作方式」中描述的增強策略與 LARS 訓練。
- **結果：**論文表 6 報告 ImageNet 線性評估的 top-1 準確率：ResNet-50（1×）為 69.3%，ResNet-50（2×）為 74.2%，ResNet-50（4×）為 76.5%。表 7 報告半監督的 top-5 準確率：使用 1% 標籤時，ResNet-50（4×）為 85.8%；使用 10% 標籤時為 92.6%。
- **限制：**論文發現對比學習受益於大批次（最高到 8192）與長時間訓練。負樣本只來自當前批次，因此負樣本數量受批次大小限制，也就受硬體限制。最佳結果來自最大的編碼器；表 6 中的 1× 模型明顯低於 4× 模型。[MoCo](moco.md) 以佇列處理批次大小的限制。

## 關聯

- [MoCo](moco.md) 使用相近的損失，但負樣本來自佇列，因此數量不受批次大小限制。
- [BYOL](../non-contrastive-methods/byol.md) 完全不使用負樣本。
- [遮罩自編碼器](../masked-prediction/mae.md) 走另一條路：預測缺失的內容，而不是對比視角。
- 上述結果所用的線性評估協定，在[理論與評估](../theory-and-evaluation/index.md)中討論。
- ResNet 骨幹網路見[CNN 模型](../../../models/cnn/index.md)。

## 開放問題

- SimCLR 的增益有多少來自增強策略，又有多少來自批次大小與訓練長度？論文兩者都有研究，但兩者互相影響。
- 損失前的非線性投影頭為什麼能提升下游使用的表徵？論文以實驗說明此效果，摘要並未給出機制解釋。

## 參考文獻

### 代表性論文

- Chen, T., Kornblith, S., Norouzi, M. & Hinton, G. (2020). *A Simple Framework for Contrastive Learning of Visual Representations*. ICML (PMLR 119). https://arxiv.org/abs/2002.05709 — 本頁介紹的論文。
- Chen, T. et al. (2020). *Big Self-Supervised Models are Strong Semi-Supervised Learners*. NeurIPS. https://arxiv.org/abs/2006.10029 — 後續研究，將 SimCLR 的做法擴展到大型模型以進行半監督學習。
- Wu, Z., Xiong, Y., Yu, S. X. & Lin, D. (2018). *Unsupervised Feature Learning via Non-Parametric Instance Discrimination*. CVPR. https://arxiv.org/abs/1805.01978 — 以記憶庫中的負樣本進行個體判別，SimCLR 避開了這個記憶庫。
- Oord, A. van den, Li, Y. & Vinyals, O. (2018). *Representation Learning with Contrastive Predictive Coding*. arXiv:1807.03748. https://arxiv.org/abs/1807.03748 — 提出 InfoNCE 損失，NT-Xent 損失即以此為基礎。
- Wang, T. & Isola, P. (2020). *Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere*. ICML (PMLR 119). https://arxiv.org/abs/2005.10242 — 以對齊性與均勻性解釋對比目標。
- He, K., Zhang, X., Ren, S. & Sun, J. (2016). *Deep Residual Learning for Image Recognition*. CVPR. https://arxiv.org/abs/1512.03385 — 本頁方法所用編碼器的 ResNet 架構。

### 綜述與教科書

- Balestriero, R. et al. (2023). *A Cookbook of Self-Supervised Learning*. arXiv:2304.12210. https://arxiv.org/abs/2304.12210 — 自監督設計選擇的實務性綜述，包含 SimCLR 研究的各項選擇。
