---
translation_reviewed: 2026-10-28
---

# 能量分數

能量分數是一種從分類器 logit 計算的分布外分數。它以 logit 的 log-sum-exp 取代 softmax 信心，保留了 softmax 會丟棄的 logit 整體大小資訊。Liu 等人（2020）提出它，作為比 softmax 更可靠的分數，同時也作為訓練目標。它是[分布外偵測](../index.md)頁面所描述的分數之一。

## 概述

[最大 softmax 機率](../max-softmax-probability/index.md)基準讀取的是最大的類別機率。softmax 正規化使得當所有 logit 加上同一個常數時，該機率保持不變，因此這個基準看不到 logit 的大小。Liu 等人（2020）主張，這使得 softmax 分數在 OOD 資料上過度自信。他們的能量分數則保留了 logit 的大小。作者指出，能量在理論上與輸入的機率密度一致。此方法可以套用在任何預先訓練的分類器上，論文也提出以能量為基礎的訓練目標。

## 關鍵概念

- **Logit。** 網路給每個類別的原始分數。softmax 把 logit 轉為機率。
- **Log-sum-exp。** 函數 $\log \sum_i \exp(a_i)$。它的行為接近 $a_i$ 的最大值，但保持平滑，並保留輸入的尺度。
- **能量。** 由 logit 計算出的純量。在此方法中，能量越低代表輸入越符合訓練資料的典型。
- **以能量為基礎的訓練。** 一種改變訓練目標的變體，使訓練輸入的能量低，離群值輸入的能量高。

## 運作方式

對於分類器的 logit $f_i(x)$，輸入 $x$ 的能量在溫度 $T$ 下定義為

$$
E(x; f) = -T \log \sum_i \exp\!\big(f_i(x)/T\big).
$$

當 $T = 1$ 時，這就是 logit 的 log-sum-exp 取負。當能量高於在驗證資料上選定的門檻 $\tau$ 時，輸入會被標記為分布外。

與 softmax 相比，能量保留了 logit 的大小。若每個 logit 都加上同一個常數 $c$，softmax 機率不變，但能量改變 $-c$。因此，即使兩個輸入的 softmax 分布相同，logit 較大的輸入能量也較低。這正是作者所利用的性質。

程序如下。

1. 照常訓練分類器，或使用已預先訓練的分類器。
2. 對保留的分布內輸入與 OOD 測試輸入計算 $E(x; f)$。
3. 在驗證資料上選定 $\tau$，並回報 AUROC 與 95% 真陽性率時的偽陽性率。

## 結果

在 CIFAR-10 預先訓練的 WideResNet 上，論文回報，能量分數使 95% 真陽性率下的平均偽陽性率比 softmax 分數降低了 18.03%。[^1] 作者也回報，他們以能量為基礎的訓練在常見基準上勝過目前的最先進方法。論文把此方法與多種事後與訓練式的方法做比較。確切的表格見論文，本頁沒有重新執行。

## 限制

- **仍是單一數字。** 能量把 logit 壓縮為一個值。與 softmax 分數一樣，它忽略了特徵空間的結構，而[馬氏距離](../mahalanobis-distance/index.md)等方法則利用了這個結構。
- **對 logit 尺度敏感。** 此分數取決於 logit 的整體大小，因此它的可靠性受制於產生這些 logit 的訓練。若網路對每個輸入都把 logit 放大，分數的資訊量會下降。
- **訓練變體需要離群值。** 論文中以能量為基礎的訓練使用離群值資料，這類資料很難事先定義。事後使用能量則不需要它。

## 開放問題

- 在標準基準上的進步，能否延續到自然的分布偏移上？
- 什麼時候 logit 的大小真的提供了不熟悉的證據，什麼時候它只反映訓練的假象？

## 與其他主題的連結

能量分數把分類器與密度模型連結起來：負能量是輸入之未正規化密度的對數。[密度與生成模型](../../../paradigms/unsupervised/density-and-generative-models/index.md)頁面涵蓋了這個概念的一般面向。以能量為基礎的變體以類似 Outlier Exposure 的方式使用離群值（Hendrycks 等人，2018）。

Liu 等人（2020）把此分數視為對 softmax 從訓練繼承而來之過度自信的回應，這也是[不確定性量化與校準](../../uncertainty-and-calibration/index.md)所關心的問題。

[^1]: 數字取自 Liu 等人（2020）的摘要。

## 參考文獻

### 開創性論文

- Liu, W., Wang, X., Owens, J. D. & Li, Y. (2020). *Energy-based Out-of-distribution Detection*. arXiv. https://arxiv.org/abs/2010.03759 — 提出用於 OOD 偵測的能量分數，以及以能量為基礎的訓練目標（NeurIPS 2020）。
- Hendrycks, D. & Gimpel, K. (2016). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. arXiv. https://arxiv.org/abs/1610.02136 — 提出能量分數所比較的最大 softmax 機率基準（ICLR 2017）。
- Liang, S., Li, Y. & Srikant, R. (2017). *Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks*. arXiv. https://arxiv.org/abs/1706.02690 — 提出 ODIN，這是一種使用溫度縮放與輸入擾動的事後分數（ICLR 2018）。
- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. arXiv. https://arxiv.org/abs/1807.03888 — 提出特徵空間中的馬氏距離分數，能量分數與之比較（NeurIPS 2018）。

### 綜述與教科書

- Yang, J., Zhou, K., Li, Y. & Liu, Z. (2021). *Generalized Out-of-Distribution Detection: A Survey*. arXiv. https://arxiv.org/abs/2110.11334 — 綜述分類式、密度式與距離式的 OOD 偵測方法。

### 文章與文件

- Hendrycks, D., Mazeika, M. & Dietterich, T. (2018). *Deep Anomaly Detection with Outlier Exposure*. arXiv. https://arxiv.org/abs/1812.04606 — 以輔助離群值訓練偵測器，與以能量為基礎的變體相關（ICLR 2019）。
