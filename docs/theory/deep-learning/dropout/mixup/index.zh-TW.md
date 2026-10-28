---
translation_reviewed: 2026-10-28
---

# Mixup 與 CutMix

Mixup 與 CutMix 是資料增強方法，它們在兩個訓練樣本的混合上訓練分類器，並以相同比例混合其標籤。Mixup 以加權平均混合整張影像。CutMix 則把另一張影像中的矩形區塊貼到影像上。兩者都在上層[丟棄法與隨機正則化](../index.md)頁面中，被描述為套用在訓練資料而非網路上的隨機性。

## 概述

資料增強透過轉換訓練樣本來擴充訓練集，例如裁切或翻轉影像。大多數轉換都保持標籤不變。Zhang 等人（2017）改變了這一點，把兩個樣本與它們的標籤結合起來。他們的摘要把 mixup 描述為在成對樣本及其標籤的凸組合上訓練，這鼓勵網路在訓練樣本之間表現出線性的行為。

CutMix（Yun 等人，2019）針對較早的一類區域方法的缺點而提出。這些方法會抹除影像中的一塊區域，通常是覆蓋黑色像素或雜訊，這會丟棄資訊並浪費訓練像素。CutMix 則以從另一張影像切下的區塊取代被抹除的區域，並依區塊面積混合標籤。

## 關鍵概念

- **凸組合。** 一種加權平均，權重介於 0 與 1 之間且總和為 1。
- **軟標籤。** 以類別分布表示的目標，例如 70% 屬於某一類、30% 屬於另一類。兩種方法都在軟標籤上訓練。
- **區域丟棄。** 從輸入影像中移除一塊矩形區域。Cutout 是最著名的例子。CutMix 是它的替代方法。
- **定位能力。** 在影像中找出物體位置的能力。CutMix 論文主張，以區塊為基礎的訓練會鼓勵網路注意物體中較不具區分性的部分。

## 運作方式

### Mixup

從參數為 \(\alpha\) 的 Beta 分布中抽取混合權重 \(\lambda\)。對於兩個樣本 \((x_i, y_i)\) 與 \((x_j, y_j)\)，形成

\[
\tilde x = \lambda x_i + (1-\lambda)\,x_j, \qquad \tilde y = \lambda y_i + (1-\lambda)\,y_j.
\]

損失是以混合後的輸入對混合後的標籤計算。參數 \(\alpha\) 控制混合的強度：接近 0 時樣本幾乎不變，較大的值則產生較均勻的混合。

### CutMix

在 \(x_j\) 的影像中抽取一個矩形 \(B\)，其面積取自 Beta 分布的比例，並將它放在隨機位置。令 \(M\) 為二值遮罩，矩形外為 1、矩形內為 0。則

\[
\tilde x = M \odot x_i + (1-M) \odot x_j, \qquad \tilde y = \lambda\, y_i + (1-\lambda)\, y_j,
\]

其中 \(\lambda\) 是仍來自 \(x_i\) 的影像比例，即 1 減去矩形面積除以影像面積。

### 程序

1. 取一個 mini-batch，並把每個樣本與同一批次中的另一個樣本配對，通常透過隨機排列。
2. 為每一對抽取混合權重。
3. 建立混合後的輸入與其混合標籤。
4. 以混合後的樣本計算損失並進行訓練。

## 結果

Mixup 的摘要報告，此方法改善了 ImageNet-2012、CIFAR-10、CIFAR-100、Google commands 與 UCI 資料集上最先進架構的泛化能力。摘要也報告，mixup 減少了對錯誤標籤的記憶，提高了對對抗樣本的穩健性，並穩定了生成對抗網路的訓練。

CutMix 的摘要報告，此方法在 CIFAR 與 ImageNet 分類上持續優於其他增強策略。用來預訓練模型時，以 CutMix 訓練的分類器能改善 Pascal 上的偵測與 MS-COCO 上的影像描述。摘要也報告，它對輸入損壞的穩健性更好，並能改善分布外偵測。

## 限制

- **混合後的影像並非自然影像。** 以混合樣本訓練，會使輸入分布偏離測試時所見的分布，而網路必須同時學會處理兩者。
- **標籤依賴混合規則。** CutMix 以面積作為每張影像應貢獻多少標籤的代理。當物體很小或區塊未覆蓋到物體時，這個代理是粗略的。
- **\(\alpha\) 的選擇。** 混合的強度是一個超參數，其最佳值取決於任務。
- **需要有意義的混合。** 此方法假設組合兩個輸入有合理的意義。對影像與某些隱藏表徵而言成立，但對離散輸入（例如 token）或結構化輸出而言，就不那麼清楚。

## 未解問題

- **為什麼內插有幫助？** Mixup 的動機是偏好樣本之間簡單的線性行為。Verma 等人（2018）把同樣的內插套用到隱藏狀態上，稱為 Manifold Mixup，並報告每個類別的表徵更為平坦。完整的解釋仍然缺乏。
- **標籤應該是什麼？** CutMix 基於面積的標籤是否應依區塊的內容（例如透過顯著性）來決定，是一個開放的設計問題。
- **超越影像。** 把混合推廣到文字、音訊與圖結構，需要選擇要混合什麼，而最佳的選擇尚未確立。

## 關聯

Mixup 從硬標籤產生軟標籤，這使它與[標籤平滑](../label-smoothing/index.md)相關。兩者都降低了網路在訓練樣本上被推向高度自信的程度。Mixup 與 CutMix 是資料增強方法，因此與[上層主題](../index.md)中的其他隨機擾動（例如丟棄法）並列。Shorten 與 Khoshgoftaar（2019）提供了影像增強的綜述。大腦中沒有已確立的、在學習時混合兩個刺激的對應機制，因此這種方法最好被理解為工程上的技巧。更廣泛的連結見[丟棄法](../index.md)頁面與 [NeuroAI](../../../../brain-mind/neuroai/index.md)。

## 應用

- **影像分類。** Mixup 與 CutMix 用於訓練 CIFAR 與 ImageNet 上的分類器，這也是它們論文中的基準測試。
- **偵測與描述的預訓練。** CutMix 論文報告，以 CutMix 訓練的分類器作為偵測與影像描述的預訓練模型時會有增益。
- **穩健性與生成模型。** Mixup 的論文報告了對對抗樣本的穩健性，以及對生成對抗網路訓練的穩定作用。

## 參考文獻

### 開創性論文

- Zhang, H. et al. (2017). *mixup: Beyond Empirical Risk Minimization*. arXiv. https://arxiv.org/abs/1710.09412 — 論文本身：在成對樣本及其標籤的凸組合上訓練，改善泛化與穩健性。
- Yun, S. et al. (2019). *CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features*. arXiv. https://arxiv.org/abs/1905.04899 — 在訓練影像之間貼上區塊，並依區塊面積混合標籤，作為抹除區域的替代方法。
- Verma, V. et al. (2018). *Manifold Mixup: Better Representations by Interpolating Hidden States*. arXiv. https://arxiv.org/abs/1806.05236 — 把內插的想法套用到隱藏表徵上，並報告更平滑的決策邊界。

### 綜述與教科書

- Shorten, C. & Khoshgoftaar, T. M. (2019). *A survey on Image Data Augmentation for Deep Learning*. Journal of Big Data. https://doi.org/10.1186/s40537-019-0197-0 — 綜述影像資料的增強方法，也就是 mixup 與 CutMix 所使用的情境。

### 文章與文件

- Zhang, C. et al. (2016). *Understanding deep learning requires rethinking generalization*. arXiv. https://arxiv.org/abs/1611.03530 — 顯示大型網路可以擬合隨機標籤，這促使人們研究 mixup 等正則化器。
