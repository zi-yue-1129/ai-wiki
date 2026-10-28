---
translation_reviewed: 2026-10-28
---

# 分布外偵測與分布偏移

分布偏移是指訓練與部署之間資料的改變。分布外（OOD）偵測則是問某個特定輸入是否來自模型訓練分布之外，好讓系統把它標記出來、拒絕處理，或交給人處理。這兩件事都很重要，因為在自己的測試集上準確的分類器，一旦輸入改變，就可能非常自信地答錯。本頁是[機器學習](../index.md)的一部分。

## 概述

監督式學習通常假設訓練與部署的資料來自同一分布。實際上，兩者往往並不相同：不同醫院的掃描儀不同、季節會變、相機會被移動、語言也會漂移。Recht 等人（2019）依照原始的建構流程重新建立了 CIFAR-10 與 ImageNet 的測試集，發現準確率在 CIFAR-10 上下降 3% 到 15%，在 ImageNet 上下降 11% 到 14%。[^1]

這裡有兩個相關的問題。第一個是模型在偏移下能否保持準確；領域適應與穩健訓練都處理這個問題，[領域適應](../../paradigms/transfer/domain-adaptation/index.md)頁面涵蓋遷移的一面。第二個是模型能否察覺某個輸入並不熟悉。偵測器不會讓分類器在這些輸入上變得更準確，但它讓系統可以拒絕對這些輸入採取行動。

OOD 偵測與異常偵測、新穎性偵測、離群值偵測以及開放集辨識有大量重疊。Yang 等人（2021）指出，這些領域各自獨立發展，常用同樣的詞彙卻有不同的意義。開放集辨識（Scheirer 等人，2013）是最直接的變體：分類器必須正確辨識已知類別，並拒絕來自從未見過之類別的輸入。[異常偵測](../../paradigms/unsupervised/anomaly-detection/index.md)頁面涵蓋更廣的家族。

## 關鍵概念

- **分布內（ID）與分布外（OOD）。** 若輸入來自模型所訓練的分布，它就是分布內的。一張貓的照片對貓分類器而言是分布內的；但對只在汽車上訓練的模型而言，它就是分布外的。
- **協變量偏移。** 輸入的分布改變，而輸入與標籤之間的對應規則保持不變（Shimodaira，2000）。
- **標籤偏移與概念偏移。** 標籤偏移改變各類別的出現頻率；概念偏移則改變把輸入對應到標籤的規則。Moreno-Torres 等人（2012）對分類問題中的這些資料集偏移提供了統一的觀點。
- **評分函數。** 對每個輸入計算的一個數值，數值越高代表越典型。門檻會把分數轉為接受或拒絕的決定。
- **AUROC 與 95% TPR 時的 FPR。** AUROC 衡量 ID 與 OOD 的分數排序得有多好。95% TPR 時的 FPR 則是當 95% 的 ID 輸入被接受時，被誤接受的 OOD 輸入比例。
- **捷徑學習。** 模型依賴一個在基準測試上有效、但在更困難條件下失效的規則（Geirhos 等人，2020）。例如背景在訓練時能預測標籤，就是這類規則的常見來源，也就是虛假相關。

## 運作方式

典型的偵測器取一個已訓練的分類器，並在測試時加上一個評分步驟。分數會與在驗證資料上選定的門檻比較。

```mermaid
flowchart LR
  A[在分布內資料上訓練] --> B[新輸入到來]
  B --> C[計算 OOD 分數]
  C --> D{分數高於門檻？}
  D -- 是 --> E[預測類別]
  D -- 否 --> F[標記、拒絕或延後處理]
```

最簡單的分數是最大 softmax 機率。對於 logit $f_k(x)$，分數為

$$
s(x) = \max_k \frac{\exp f_k(x)}{\sum_j \exp f_j(x)},
$$

當 $s(x) < \tau$ 時，輸入會被標記。偵測器在一個 ID 集合與一個 OOD 集合上評估。兩組分數以 AUROC 比較，而 95% TPR 時的 FPR 則是在接受 95% ID 輸入的門檻上讀取。各種方法主要的差別在於它們計算的分數。

在協變量偏移下，可以對訓練資料重新加權，以估計測試分布上的表現。若 $p$ 為訓練輸入密度、$q$ 為測試密度，則測試風險為

$$
R_q(f) = \mathbb{E}_{x \sim p}\!\left[\frac{q(x)}{p(x)}\, L\big(f(x), y\big)\right].
$$

基準測試是這個領域比較偵測器的方式。它們把熟悉的資料集與另一個資料集配對，從差異很大的配對（例如 CIFAR-10 與街景門牌號碼）到較困難的配對（外觀相似、但類別是新的）都有。ImageNet-C（Hendrycks 與 Dietterich，2019）施加雜訊、模糊等損壞。WILDS（Koh 等人，2020）收集了十個資料集，包含來自不同醫院的腫瘤影像與來自不同地點的相機陷阱影像。在這些資料集上，標準訓練得到的分布外表現明顯低於分布內表現。

## 主要方法

這裡比較三個具代表性的分數，每個都有自己的頁面。

| 方法 | 分數 | 想法 | 頁面 |
|---|---|---|---|
| 最大 softmax 機率 | 最大的 softmax 輸出 | 低信心代表輸入不熟悉。是其他方法用來比較的基準 | [最大 softmax 機率](max-softmax-probability/index.md) |
| 馬氏距離 | 在特徵空間中到最近類別的距離 | 每個類別的特徵都擬合一個高斯分布；不熟悉的輸入遠離所有類別 | [馬氏距離](mahalanobis-distance/index.md) |
| 能量分數 | logit 的 log-sum-exp | 保留 softmax 正規化會消去的整體 logit 大小 | [能量分數](energy-score/index.md) |

其他方法包括 ODIN，它在 softmax 分數上加入溫度縮放與小幅的輸入擾動（Liang 等人，2017），以及 Generalized ODIN，它不需要在 OOD 資料上調參（Hsu 等人，2020）。Outlier Exposure 則用另一組離群值來訓練偵測器（Hendrycks 等人，2018）。

## 與其他主題的連結

[領域適應](../../paradigms/transfer/domain-adaptation/index.md)與 OOD 偵測共享一套偏移的詞彙。領域適應在訓練時通常有未標註的目標資料；OOD 偵測通常只在部署時才遇到新輸入。[泛化理論](../../paradigms/supervised/generalization-theory/index.md)假設訓練與測試資料來自同一分布，而偏移正好打破了這個假設。

過度自信把本頁與[不確定性量化與校準](../uncertainty-and-calibration/index.md)連在一起。Ovadia 等人（2019）發現，在分布內資料上擬合的校準方法，在資料集偏移下表現不足。

對抗輸入是另一種不熟悉的輸入。Lee 等人（2018）用同一個偵測器測試 OOD 樣本與對抗攻擊。參見[對抗樣本與穩健性](../adversarial-robustness/index.md)。

捷徑學習指的是網路答對了，但理由是錯的。Geirhos 等人（2019）指出，在 ImageNet 上訓練的 CNN 強烈依賴紋理而非形狀，這與人類的行為不同。[CNN 的形狀偏好](../../../brain-mind/visual-perception/geirhos-2019/index.md)頁面涵蓋了與人類的比較。

大腦也會自動偵測偏差。失配負波是聽覺皮層對打破規律序列之聲音的一種反應，而且聽者不需要注意這些聲音就會出現（Näätänen 等人，2007）。它是一種內建的新穎性訊號，正是 OOD 偵測試圖讓分類器具備的功能。[預測編碼](../../../brain-mind/predictive-coding/index.md)頁面描述了大腦把傳入訊號與預測相比較的觀點。網路能否使用類似的訊號，仍是一個開放的問題。

## 應用

- **醫學影像。** 在某家醫院訓練的模型，可能會遇到另一家醫院的掃描儀與病人。參見[醫療健康](../../../applications/healthcare/index.md)。
- **自動駕駛。** 車輛應該能辨識不尋常的物體或場景，並在無法安全決策時把控制權交還給人。參見[自動駕駛](../../../applications/autonomous-driving/index.md)。
- **詐欺與安全。** 不熟悉的交易或網路流量可能意味著新的攻擊，通常被視為[異常偵測](../../paradigms/unsupervised/anomaly-detection/index.md)。

## 開放問題

- **定義。** 這些重疊的領域使用不同的術語，而基準比較取決於在特定應用中什麼算是 OOD。
- **是否取得離群值。** 有些方法在離群值上訓練（Hendrycks 等人，2018），有些則避免這樣做（Hsu 等人，2020）。在部署時不會有的 OOD 樣本上調參，可能使結果看起來比實際更好。
- **封閉集準確率。** Vaze 等人（2021）回報，開放集表現與封閉集準確率高度相關，這使人不禁懷疑是否真的需要另外的偵測機制。
- **虛假特徵。** Nagarajan 等人（2020）指出，即使在容易學習的線性任務上，模型在偏移下仍可能失效；而偵測器可能不會察覺失效的原因是一個看起來正常的特徵。

## 參考文獻

### 開創性論文

- Shimodaira, H. (2000). *Improving predictive inference under covariate shift by weighting the log-likelihood function*. *Journal of Statistical Planning and Inference*. https://doi.org/10.1016/S0378-3758(00)00115-4 — 顯示依測試與訓練輸入密度之比對訓練資料加權，可以修正協變量偏移下的預測推論。
- Scheirer, W. J., de Rezende Rocha, A., Sapkota, A. & Boult, T. E. (2013). *Toward Open Set Recognition*. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. https://doi.org/10.1109/TPAMI.2012.256 — 將開放集辨識形式化：接受已知類別，拒絕未知類別。
- Hendrycks, D. & Gimpel, K. (2016). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. arXiv. https://arxiv.org/abs/1610.02136 — 提出最大 softmax 機率基準（ICLR 2017）。
- Liang, S., Li, Y. & Srikant, R. (2017). *Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks*. arXiv. https://arxiv.org/abs/1706.02690 — 提出 ODIN，使用溫度縮放與小幅輸入擾動（ICLR 2018）。
- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. arXiv. https://arxiv.org/abs/1807.03888 — 在特徵空間中使用對各類別高斯分布的馬氏距離，同時處理 OOD 與對抗輸入（NeurIPS 2018）。
- Liu, W., Wang, X., Owens, J. D. & Li, Y. (2020). *Energy-based Out-of-distribution Detection*. arXiv. https://arxiv.org/abs/2010.03759 — 以 logit 計算的能量分數取代 softmax 分數（NeurIPS 2020）。
- Geirhos, R. et al. (2020). *Shortcut Learning in Deep Neural Networks*. arXiv. https://arxiv.org/abs/2004.07780 — 把深度網路的許多失效視為捷徑學習（*Nature Machine Intelligence*）。

### 綜述與教科書

- Yang, J., Zhou, K., Li, Y. & Liu, Z. (2021). *Generalized Out-of-Distribution Detection: A Survey*. arXiv. https://arxiv.org/abs/2110.11334 — 綜述 OOD 偵測以及相關問題，並釐清它們的差異。
- Moreno-Torres, J. G. et al. (2012). *A unifying view on dataset shift in classification*. *Pattern Recognition*. https://doi.org/10.1016/j.patcog.2011.06.019 — 為分類問題的協變量、先驗與概念偏移提供共同的分類法。
- Näätänen, R., Paavilainen, P., Rinne, T. & Alho, K. (2007). The mismatch negativity (MMN) in basic research of central auditory processing: A review. *Clinical Neurophysiology*. https://doi.org/10.1016/j.clinph.2007.04.026 — 回顧失配負波，這是對偏差聲音的一種自動腦部反應。

### 文章與文件

- Koh, P. W. et al. (2020). *WILDS: A Benchmark of in-the-Wild Distribution Shifts*. arXiv. https://arxiv.org/abs/2012.07421 — 十個含自然偏移的資料集，涵蓋醫院與相機陷阱（ICML 2021）。
- Recht, B., Roelofs, R., Schmidt, L. & Shankar, V. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 新的 CIFAR-10 與 ImageNet 測試集，以及它們上的準確率下降。
- Hendrycks, D. & Dietterich, T. (2019). *Benchmarking Neural Network Robustness to Common Corruptions and Perturbations*. arXiv. https://arxiv.org/abs/1903.12261 — 介紹 ImageNet-C 與 ImageNet-P 等常見損壞基準。
- Hendrycks, D., Mazeika, M. & Dietterich, T. (2018). *Deep Anomaly Detection with Outlier Exposure*. arXiv. https://arxiv.org/abs/1812.04606 — 以輔助離群值訓練偵測器，改善對未見異常的偵測（ICLR 2019）。
- Hsu, Y.-C., Shen, Y., Jin, H. & Kira, Z. (2020). *Generalized ODIN: Detecting Out-of-distribution Image without Learning from Out-of-distribution Data*. arXiv. https://arxiv.org/abs/2002.11297 — 讓 ODIN 不再需要在離群值資料上調參。
- Vaze, S., Han, K., Vedaldi, A. & Zisserman, A. (2021). *Open-Set Recognition: a Good Closed-Set Classifier is All You Need?* arXiv. https://arxiv.org/abs/2110.06207 — 顯示開放集辨識能力與封閉集準確率相關，橫跨不同損失函數與架構。
- Nagarajan, V., Andreassen, A. & Neyshabur, B. (2020). *Understanding the Failure Modes of Out-of-Distribution Generalization*. arXiv. https://arxiv.org/abs/2010.15775 — 即使在容易的任務上，虛假相關也會導致偏移下的失效。
- Ovadia, Y. et al. (2019). *Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift*. arXiv. https://arxiv.org/abs/1906.02530 — 在資料集偏移下評估預測不確定性與校準的基準。
- Geirhos, R. et al. (2019). *ImageNet-trained CNNs are biased towards texture; increasing shape bias improves accuracy and robustness*. arXiv. https://arxiv.org/abs/1811.12231 — 顯示在 ImageNet 上訓練的 CNN 偏好紋理而非形狀，而風格化訓練能提高形狀偏好。

[^1]: 數字取自 Recht 等人（2019）摘要中，新測試集相對於原始測試集的結果。
