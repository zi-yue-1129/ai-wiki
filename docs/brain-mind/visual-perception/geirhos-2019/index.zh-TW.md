---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- theory/models/cnn
tags:
- neuroscience
- perception
aliases:
  - Geirhos 2019
  - 形狀偏好
  - Shape Bias
  - Stylized-ImageNet
---

# CNN 的形狀偏好（Geirhos 等人，2019）

Geirhos 等人（2019）問了一個簡單、答案卻很明確的問題：在 ImageNet 上訓練的卷積網路，是像人一樣依形狀辨識物體，還是依紋理？他們發現，一般網路主要依賴紋理；而以強調形狀的資料集訓練，能使網路轉向形狀。這篇論文對 NeuroAI 很重要，因為它給出了網路與人類之間一個具體的行為差異，以及一種檢驗訓練改變能否消除這種差異的方法。

本頁是[知覺與視覺系統](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 問題

人類主要依形狀辨識物體，即使紋理具有誤導性，也是如此。在 ImageNet 上，網路可以在沒有學到相同線索的情況下達到高準確度，因為在自然照片中，紋理往往是可靠的捷徑。如果如此，網路可能是因錯誤的理由而成功，這會限制它作為人類視覺模型的價值。

## 方法

作者建立了一個衝突資料集，稱為 Stylized-ImageNet。每張影像保留原始物體的形狀，但套用了另一張影像的紋理，透過風格轉換產生。於是形狀與紋理指向不同的類別，分類器的選擇便顯示它用了哪一種線索。

步驟如下：

1. 對 ImageNet 影像做風格轉換，使物體形狀與紋理互相衝突。
2. 在衝突影像上測試一般的 ImageNet 網路與人類觀察者。
3. 以標準與風格化影像的混合資料，訓練同一架構（ResNet-50）。
4. 測量依形狀的分類、物體偵測，以及對影像失真的穩健性。

第 3 步是介入。固定架構，便能分離出訓練資料的效果。

## 結果

論文報告：

- 在 ImageNet 上訓練的一般網路主要依賴紋理，與人類不同。
- 以風格化資料訓練後，同一架構轉向依形狀辨識，與人類行為更為接近。
- 具形狀偏好的網路改善了物體偵測與對影像失真的穩健性。

本頁所用的摘要以定性方式給出這些結果。引用數字前請查閱全文。

## 限制

- 風格化資料只介入了一種捷徑。它不是人類視覺的完整解釋，也無法確定人們在所有任務中如何權衡形狀與紋理。
- 形狀偏好並不能消除其他失敗模式。網路仍可能對人類忽略的微小對抗性變化脆弱。
- 比較依賴所選的架構與資料集，效果的大小可能因其他模型而異。

## 與其他主題的關聯

- **模型比較**：本研究使用與 [Yamins 等人（2014）](../yamins-2014/index.md)所檢驗的相同卷積家族，但它探問的是網路學到什麼，而非它們對神經元的預測能力有多好。
- **CNN 架構**：架構家族見 [CNN](../../../theory/models/cnn/index.md)。
- **知覺**：塑造人類辨識的腹側與背側路徑，見[知覺與視覺系統](../index.md)。

## 開放問題

- **形狀偏好是否讓網路更像大腦？** 它讓網路在這項測試上更接近人類行為，但是否也匹配內部運算，尚未得到證明。
- **哪些訓練訊號會產生形狀偏好？** 論文改變的是資料。目標函數、架構或發展式訓練是否也能產生相同的偏好，仍是開放問題。

## 參考文獻

### 開創性論文

- Geirhos, R., Rubisch, P., Michaelis, C., Bethge, M., Wichmann, F. A. & Brendel, W.（2019）。ImageNet-trained CNNs are biased towards texture. *ICLR*。https://arxiv.org/abs/1811.12231 — 顯示一般 CNN 依賴紋理，風格化訓練可使其轉向形狀。
- Krizhevsky, A., Sutskever, I. & Hinton, G. E.（2012）。ImageNet Classification with Deep Convolutional Neural Networks. *NeurIPS*。https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 論文，使深度卷積網路成為影像辨識的標準模型。
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J.（2014）。Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*。https://doi.org/10.1073/pnas.1403112111 — 顯示物體辨識效能能預測網路對 IT 反應的解釋力。

### 綜述與回顧

- Lindsay, G. W.（2021）。Convolutional Neural Networks as a Model of the Visual System: Past, Present, and Future. *Journal of Cognitive Neuroscience*。https://doi.org/10.1162/jocn_a_01544 — 回顧 CNN 作為視覺系統模型的用法，以及它能解釋與無法解釋的部分。
- Goodale, M. A. & Milner, A. D.（1992）。Separate visual pathways for perception and action. *Trends in Neurosciences*。https://pubmed.ncbi.nlm.nih.gov/1374953/ — 腹側與背側路徑，為人類側的對照提供背景。
