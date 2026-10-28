---
translation_reviewed: 2026-10-28
related:
- theory/models/cnn
tags:
- neuroscience
- vision
- neuroai
aliases:
  - Performance-Optimised Networks Predict IT Cortex
  - Yamins 2014
  - 效能最佳化網路預測皮質
---

# 以效能最佳化的網路預測視覺皮質（Yamins 等人，2014）

針對物件辨識最佳化的深度卷積網路，能預測猴子高階視覺皮質中神經元的反應。模型越擅長辨識物件，通常也越能預測這些反應，把工程上的表現與生物上的吻合連結了起來。

本頁屬於 [NeuroAI：大腦與 AI 的雙向啟發](../index.md)。它詳細說明一種方法。

## 概述

視覺皮質很難直接建模，因為許多候選模型大致能擬合早期階段，但在後期階段彼此差異很大。Yamins 等人問的是：哪一類計算模型，最能解釋腹側視覺路徑上的反應；該路徑經過 V4 與下顳葉（IT）皮質，支撐物件辨識。他們發現，答案取決於是否把模型針對大腦所執行的任務加以最佳化。

## 核心概念

- **腹側視覺路徑（ventral visual stream）**：從初級視覺皮質經 V4 到 IT 皮質的路徑，攜帶物件資訊。
- **任務最佳化模型（task-optimised model）**：權重是為某項任務（例如物件分類）而訓練的網路，而不是直接擬合神經資料。
- **預測力（predictivity）**：模型的特徵經映射後，能在新影像上預測神經元活動的程度。
- **階層式模型（hierarchical model）**：多層堆疊的結構，每一層建立在下層之上，因此較高層的感受野較大。

## 問題

哪一種計算模型，最能預測高階視覺皮質的神經反應？早期模型多為人工設計，或直接擬合神經資料；而良好的物件辨識本身，是否就代表與大腦的良好吻合，並不清楚。

## 核心想法

針對物件辨識最佳化深度卷積網路，再測試其特徵對 V4 與 IT 記錄到的反應有多少預測力。論文比較了許多架構，其核心結果是：物件分類的表現與模型預測 IT 反應的能力相符。表現最好的模型，預測這些反應的能力也優於較早期、未針對此任務最佳化的模型。

## 方法

1. 訓練一族階層式卷積網路，使其能對影像中的物件進行分類。
2. 依其在物件辨識任務上的表現挑選模型。
3. 記錄獼猴 V4 與 IT 神經元對一組影像的反應。
4. 把模型特徵對應到神經反應，並以自然影像評估此對應預測反應的準確度。摘要未說明對應的方法。

## 結果

論文指出，各模型的物件辨識表現，與其預測 IT 反應的能力相符。論文也指出，表現最好的模型，預測這些反應的能力優於較早期、針對此任務最佳化程度較低的模型。論文的結果來自固定的影像集與記錄位置；本頁不引用數值分數，應以原論文為準。

## 限制

- **預測不等於機制。**一個能良好預測神經群體的模型，並不代表大腦以相同方式計算其特徵。
- **固定的刺激集。**測試使用特定的影像集與記錄位置，結果可能取決於這些選擇。
- **模型族有限。**比較的是卷積階層結構，其他架構可能以不同方式預測相同的資料。

## 與其他主題的關聯

- **卷積網路**：所測試的模型是卷積網路，見[卷積神經網路](../../../theory/models/cnn/index.md)。
- **視覺知覺**：物件辨識的生物學面向見[視覺知覺](../../visual-perception/index.md)，包括 [Hubel 與 Wiesel](../../neuroscience/receptive-fields-hubel-wiesel/index.md) 所研究的簡單到複雜階層。
- **母主題**：[NeuroAI](../index.md)。同一主題的另一方法是[導航網路中的格狀單元](../grid-like-units/index.md)。

## 應用

- **神經科學的模型選擇**：以神經資料上的預測力，在視覺系統的候選模型之間做選擇。
- **工程上的啟示**：任務表現與大腦吻合度同步提升，是視覺模型也會與神經資料相比較的原因之一。

## 開放問題

- **這種連結在 IT 之外是否成立？**早期與中間區域可能需要不同的模型，而與 V4 的連結也不那麼明確。
- **哪些特徵才是關鍵？**預測力並未說明訓練後網路的哪一部分造成了吻合。
- **訓練資料有多重要？**在不同影像集上訓練的模型，對神經反應的預測可能不同，這仍在研究中。

## 參考文獻

### 開創性論文

- Yamins, D. L. K., 等人（2014）。Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*。https://doi.org/10.1073/pnas.1403112111 — 顯示為物件辨識訓練的深度網路，能預測高階視覺皮質的神經反應，且辨識越好，預測也越好。
- Krizhevsky, A., Sutskever, I. & Hinton, G. E.（2012）。ImageNet Classification with Deep Convolutional Neural Networks. *Advances in Neural Information Processing Systems 25*。https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — 使深度模型在大規模物件辨識中變得實用的卷積網路。
- Cadieu, C. F., 等人（2014）。Deep Neural Networks Rival the Representation of Primate IT Cortex for Core Visual Object Recognition. *PLoS Computational Biology*。https://doi.org/10.1371/journal.pcbi.1003963 — 報告針對物件辨識訓練的深度網路，其表徵與靈長類 IT 皮質相當，是與 Yamins 等人研究同時期的發現。

### 綜述與回顧

- Kriegeskorte, N.（2008）。Matching categorical object representations in inferior temporal cortex of man and monkey. *Neuron*。https://doi.org/10.1016/j.neuron.2008.10.043 — 提出表徵相似度分析，這是本研究所用來比較模型與大腦表徵的方法。
- Schrimpf, M., 等人（2021）。The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*。https://doi.org/10.1073/pnas.2105646118 — 顯示預測下一個詞的語言模型能預測語言網路的大腦反應，而預測得越好，與大腦的吻合度也越高。
