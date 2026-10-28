---
translation_reviewed: 2026-10-28
---

# 最大 softmax 機率

最大 softmax 機率（MSP）是分布外偵測中最簡單的事後分數。當分類器最大的 softmax 輸出很低時，輸入會被視為不熟悉。Hendrycks 與 Gimpel（2016）把它提出作為基準，後來的方法都以它為比較的起點。它是[分布外偵測](../index.md)頁面所描述的分數之一。

## 概述

在已知類別上訓練的分類器，對每個類別都會產生一個機率。MSP 基準假設：網路對它認識的輸入，會比對不認識的輸入更有信心。Hendrycks 與 Gimpel（2016）發現，被正確分類的樣本，其最大 softmax 機率往往高於被誤分類或分布外的樣本。這使它在電腦視覺、自然語言處理與語音辨識任務上都能作為可用的偵測器。此方法不需要改動網路、不需要額外訓練，也不需要離群值資料。該論文也指出，這個基準有時可以被超越，這為後續的研究留下了空間。

## 關鍵概念

- **Logit。** 網路在 softmax 把分數轉為機率之前，給每個類別的原始分數。
- **誤分類偵測。** 同一個分數也可能標記出分布內、但分類器會答錯的輸入；Hendrycks 與 Gimpel 把這個問題與 OOD 偵測一起處理。
- **門檻。** 在驗證資料上選定的數值。它決定遺漏的 OOD 輸入與被誤標的 ID 輸入之間的權衡。

## 運作方式

令 $f(x)$ 為輸入 $x$ 的 logit 向量，$p_k(x)$ 為類別 $k$ 的 softmax 機率。MSP 分數與決策規則為

$$
s_{\text{MSP}}(x) = \max_k p_k(x), \qquad \hat{o}(x) = \mathbb{1}\big[s_{\text{MSP}}(x) < \tau\big].
$$

程序如下。

1. 照常在分布內資料上訓練分類器。
2. 在保留的分布內集合與 OOD 測試集上計算 $s_{\text{MSP}}$。
3. 在驗證資料上選定 $\tau$，例如使 95% 的分布內輸入被接受。
4. 回報 AUROC（衡量兩組分數排序得多好）與 95% 真陽性率時的偽陽性率。

## 結果

論文在電腦視覺、自然語言處理與自動語音辨識任務上評估這個基準。在每一項任務中，作者都發現被正確分類的樣本，其最大 softmax 機率比被誤分類或分布外的樣本更大，因此分數能在某種程度上區分它們。摘要把這個基準描述為在這些任務上都有效，並指出它有時可以被超越。後續研究會回報基準在特定資料集上的錯誤率；Liang 等人（2017）給出一個這樣的比較：在 CIFAR-10 上訓練的 DenseNet 上，95% 真陽性率時的偽陽性率從基準的 34.7% 降到他們方法的 4.3%。[^1]

## 限制

- **繼承而來的過度自信。** 此分數是網路正規化後的輸出。softmax 正規化會迫使機率總和為一，因此即使輸入遠離訓練資料，最大值仍可能很大。Liu 等人（2020）認為，基於 softmax 的分數在 OOD 資料上有過度自信的後驗機率。
- **依賴校準。** 若網路在分布內就校準不良，MSP 也會繼承這個問題。Guo 等人（2017）指出，現代網路往往校準得很差；參見[溫度縮放](../../uncertainty-and-calibration/temperature-scaling/index.md)。
- **只有一個數字。** 此分數只保留最大的類別機率，忽略 logit 的整體大小，以及後來方法所使用的特徵空間形狀。

## 開放問題

- 為什麼有些 OOD 資料集會騙過最大 softmax 機率，而其他看似同樣困難的資料集卻不會？
- 誤分類偵測與 OOD 偵測應該共用同一個分數，還是只是看起來相似？

## 與其他主題的連結

[能量分數](../energy-score/index.md)保留了 softmax 會消去的 logit 大小，部分也是對 MSP 過度自信的回應。[馬氏距離](../mahalanobis-distance/index.md)則轉而查看特徵空間，不依賴最終的機率。ODIN（Liang 等人，2017）保留 MSP 分數，但加入溫度縮放與小幅輸入擾動，有助於分開兩組分數的分布。

此分數也是[不確定性量化與校準](../../uncertainty-and-calibration/index.md)的一部分。溫度縮放會改變 softmax 的數值，因此可能改變 MSP 分數的排序。

## 參考文獻

### 開創性論文

- Hendrycks, D. & Gimpel, K. (2016). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. arXiv. https://arxiv.org/abs/1610.02136 — 提出最大 softmax 機率基準，並在視覺、語言與語音任務上測試（ICLR 2017）。
- Liang, S., Li, Y. & Srikant, R. (2017). *Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks*. arXiv. https://arxiv.org/abs/1706.02690 — 提出 ODIN，這是一種修改 softmax 分數的方法，使用溫度縮放與輸入擾動（ICLR 2018）。
- Liu, W., Wang, X., Owens, J. D. & Li, Y. (2020). *Energy-based Out-of-distribution Detection*. arXiv. https://arxiv.org/abs/2010.03759 — 主張 softmax 信心在 OOD 資料上過度自信，並提出能量分數（NeurIPS 2020）。
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks*. arXiv. https://arxiv.org/abs/1706.04599 — 顯示現代網路校準不良，這會影響 softmax 信心的可靠性（ICML 2017）。

### 綜述與教科書

- Yang, J., Zhou, K., Li, Y. & Liu, Z. (2021). *Generalized Out-of-Distribution Detection: A Survey*. arXiv. https://arxiv.org/abs/2110.11334 — 綜述分類式、密度式與距離式的 OOD 偵測方法。

### 文章與文件

- Ovadia, Y. et al. (2019). *Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift*. arXiv. https://arxiv.org/abs/1906.02530 — 在資料集偏移下評估基於 softmax 的不確定性，結果顯示其可靠性會下降。

[^1]: 數字取自 Liang 等人（2017）的摘要。該文中的基準即為最大 softmax 機率方法。
