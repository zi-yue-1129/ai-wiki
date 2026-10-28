---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
  - theory/paradigms/self-supervised/non-contrastive-methods
  - theory/models/cnn
---

# MoCo：無監督視覺表徵學習的動量對比

MoCo 是一種對比式方法，它把大量負樣本的鍵保存在佇列中，並以編碼器的慢速移動副本來編碼這些鍵。這使負樣本數量與批次大小脫鉤。家族層級的全貌見[對比學習](index.md)頁。

## 概述

He、Fan、Wu、Xie 與 Girshick（2020）把無監督視覺學習看成字典查找：一個經編碼的查詢，應該與一組經編碼的鍵中的正樣本鍵相符。摘要指出，此方法以「佇列與動量平滑編碼器」建立「動態字典」，因此能即時建立大型且一致的字典。論文顯示，無標籤學到的特徵能良好地轉移到偵測與分割任務。摘要也指出，在七項偵測與分割任務上，MoCo 能超越其監督式 ImageNet 預訓練的對應版本。

## 核心概念

- **查詢與鍵**：同一影像的兩個視角，一個由查詢編碼器編碼，另一個由鍵編碼器編碼。兩者的嵌入構成正樣本對。
- **佇列**：先進先出的儲存區，保存最近幾個小批次的鍵，作為負樣本來源。論文使用 \(K = 65{,}536\) 個鍵。
- **動量編碼器**：鍵編碼器不以梯度訓練，其權重是查詢編碼器權重的指數移動平均，動量 \(m = 0.999\)。
- **溫度**：損失中的 \(\tau = 0.07\)。
- **Shuffling BN**：多 GPU 訓練的細節。批次正規化的統計量是每張 GPU 各自計算；鍵編碼器的小批次在分配到各 GPU 前會先打亂，避免查詢與其正樣本鍵共用同一子集的統計量。

## 運作方式

每個小批次（論文的 ImageNet 設定為 256 張影像，分散到 8 張 GPU）都會被編碼兩次。查詢編碼器以梯度下降更新，鍵編碼器則以動量規則更新：

\[
\theta_k \leftarrow m\,\theta_k + (1-m)\,\theta_q
\]

對每個查詢 \(q\)，正樣本鍵 \(k_+\) 是同一影像另一視角的鍵，負樣本則是佇列中的 \(K\) 個鍵。損失為 InfoNCE：

\[
\mathcal{L}_q = -\log \frac{\exp(q\cdot k_+/\tau)}{\sum_{i=0}^{K}\exp(q\cdot k_i/\tau)}
\]

每一步之後，最新的鍵加入佇列，最舊的鍵移出。由於佇列中的鍵來自緩慢變化的編碼器狀態，字典在遠大於批次大小的情況下仍保持一致。

## 關鍵方法

### 無監督視覺表徵學習的動量對比（He、Fan、Wu、Xie 與 Girshick，2020）

- **問題：**對比學習在負樣本多時效果較好，但端到端訓練時，負樣本只限於當前批次。摘要所設定的目標是既大又一致的字典。
- **核心想法：**把鍵保存在佇列中，並由動量更新的編碼器產生，使字典可以很大，而鍵編碼器的變化保持緩慢。
- **方程式或演算法：**\(\tau = 0.07\) 的 InfoNCE 損失、\(m = 0.999\) 的動量更新、\(K = 65{,}536\) 的佇列，以及 Shuffling BN，如「運作方式」所述。
- **結果：**在 ImageNet 的線性評估協定下，以 ResNet-50 訓練 200 個 epoch 的 MoCo 達到 60.6% 的 top-1 準確率。在 PASCAL VOC 以 Faster R-CNN 進行偵測時，監督式 ImageNet 預訓練的 AP 為 53.5，以 ImageNet-1M 預訓練的 MoCo 為 55.9。在 COCO 以 Mask R-CNN（R50-FPN，框 AP）評估時，監督式預訓練為 40.6，以 ImageNet-1M 預訓練的 MoCo 為 40.8。
- **限制：**在 COCO 上，MoCo 相對監督式預訓練的增益很小（R50-FPN 為 40.8 對 40.6）。論文沒有提供線性協定下的監督式基準，因此線性結果無法直接與監督式訓練比較。Shuffling BN 是多 GPU 批次統計量的工程解法，並非目標函數本身的性質。佇列中的鍵來自較早的編碼器狀態，因此方法依賴動量值的設定。

## 關聯

- [SimCLR](simclr.md) 使用相近的損失，但負樣本取自當前批次。MoCo 的佇列消除了對批次大小的依賴。
- [BYOL](../non-contrastive-methods/byol.md) 保留動量更新編碼器的想法，但完全不使用負樣本。
- 線性評估與轉移評估協定，在[理論與評估](../theory-and-evaluation/index.md)中討論。
- ResNet 骨幹網路見[CNN 模型](../../../models/cnn/index.md)。

## 開放問題

- 佇列長度與動量如何互動？論文選擇 \(K = 65{,}536\) 與 \(m = 0.999\)，但摘要並未說明結果對這兩者的敏感度。
- 相對監督式預訓練的優勢，是否也適用於本文未報告的偵測與分割任務，以及非 ImageNet 類型的資料？

## 參考文獻

### 代表性論文

- He, K., Fan, H., Wu, Y., Xie, S. & Girshick, R. (2020). *Momentum Contrast for Unsupervised Visual Representation Learning*. CVPR. https://arxiv.org/abs/1911.05722 — 本頁介紹的論文。
- Chen, X., Fan, H., Girshick, R. & He, K. (2020). *Improved Baselines with Momentum Contrastive Learning*. arXiv:2003.04297. https://arxiv.org/abs/2003.04297 — 後續研究，以改良的訓練配方重新檢視 MoCo 作為基準。
- Chen, T., Kornblith, S., Norouzi, M. & Hinton, G. (2020). *A Simple Framework for Contrastive Learning of Visual Representations*. ICML (PMLR 119). https://arxiv.org/abs/2002.05709 — 使用批次內負樣本的對比方法，MoCo 的佇列即是取代它。
- Wu, Z., Xiong, Y., Yu, S. X. & Lin, D. (2018). *Unsupervised Feature Learning via Non-Parametric Instance Discrimination*. CVPR. https://arxiv.org/abs/1805.01978 — 以記憶庫儲存特徵進行個體判別，是更早取得大量負樣本的方法。
- Oord, A. van den, Li, Y. & Vinyals, O. (2018). *Representation Learning with Contrastive Predictive Coding*. arXiv:1807.03748. https://arxiv.org/abs/1807.03748 — 提出 MoCo 所用的 InfoNCE 損失。

### 綜述與教科書

- Balestriero, R. et al. (2023). *A Cookbook of Self-Supervised Learning*. arXiv:2304.12210. https://arxiv.org/abs/2304.12210 — 自監督設計選擇的實務性綜述，包含動量編碼器與佇列。
- Liu, X. et al. (2020). *Self-supervised Learning: Generative or Contrastive*. arXiv:2006.08218. https://arxiv.org/abs/2006.08218 — 比較生成式與對比式自監督學習的綜述。
