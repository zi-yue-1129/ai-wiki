---
translation_reviewed: 2026-10-28
---

# 馬氏距離偵測器

馬氏距離偵測器把分布內訓練資料的特徵，建模為共享共變異數的類別條件高斯分布，並以測試輸入到最近類別均值的距離來打分。與所有類別都相距很遠的輸入被標記為分布外。本頁是[分布外偵測與分布偏移](index.md)的一部分。

## 概述

像 softmax 信心這類輸出分數依賴最後一層，可能過度自信。倒數第二層或中間層的特徵，攜帶了更多關於輸入典型程度的資訊。Lee 等人（2018）對這些特徵擬合一個簡單的高斯模型，並以馬氏距離作為 OOD 分數。馬氏距離會考慮特徵維度之間的相關性。

## 關鍵概念

- **類別條件高斯**：每個類別 \(c\) 在訓練資料中的特徵有一個均值 \(\mu_c\)。
- **共享共變異數**：由所有類別中心化後的特徵估計出一個共變異數 \(\Sigma\)，在樣本少時使模型保持穩定。
- **馬氏距離**：\(M(x)=\min_c (f(x)-\mu_c)^\top\Sigma^{-1}(f(x)-\mu_c)\)，其中 \(f(x)\) 為特徵向量。
- **特徵層**：特徵可以來自網路的多個層，它們的分數可以結合。

## 運作方式

對每個訓練樣本計算特徵，並估計各類別的均值與共享共變異數。對測試輸入，計算它到各類別的最小馬氏距離。距離很大，代表此輸入與任何訓練類別都不像，當距離超過門檻時即標記為 OOD。Lee 等人（2018）還加入一個使分數上升的小輸入擾動，這與[ODIN](odin.md)的想法相似，並以在一小組 OOD 輸入上訓練的邏輯斯迴歸，結合多個層的分數。

## 變體

- **單層分數**只使用最後的特徵層，較簡單、成本較低。
- **多層分數**結合多個層的距離，同時捕捉低階與高階的差異。
- **與類別無關的密度**對所有特徵擬合單一高斯，因此不需要類別標籤。

## 結果與限制

- 此偵測器可直接用於預訓練的網路，只需要訓練資料的特徵統計量（Lee 等人，2018）。
- 高斯假設只是近似。真實網路的特徵並非高斯分布，分數好壞取決於高斯擬合的程度。
- 此偵測器可同時用於對抗輸入與 OOD 輸入，但知道偵測器的攻擊者可能騙過它。
- 結合多個層可能需要一小組 OOD 範例，實務上未必有。

## 應用

- **以預訓練骨幹網路的影像分類器**：特徵統計量容易計算。
- **對抗與 OOD 篩檢**：同一個分數可以標記兩類輸入。
- **監控**：隨時間追蹤距離，以偵測輸入分布的漂移。

## 開放問題

- 共享共變異數的假設對某些架構並不成立，改進特徵的密度模型是開放的領域。
- 要保證分數能抵抗針對偵測器本身的適應性攻擊，很困難。

## 參考文獻

### 奠基性論文

- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). A simple unified framework for detecting out-of-distribution samples and adversarial attacks. In *Advances in Neural Information Processing Systems* 31. arXiv:1807.03888. https://arxiv.org/abs/1807.03888 — 提出馬氏距離偵測器及其多層結合方式。
- Liang, S., Li, Y. & Srikant, R. (2018). Enhancing the reliability of out-of-distribution image detection in neural networks. In *International Conference on Learning Representations*. arXiv:1706.02690. https://arxiv.org/abs/1706.02690 — 顯示輸入擾動與溫度有助於以輸出為基礎的偵測，與此處使用的輸入擾動步驟相關。
- Hendrycks, D. & Gimpel, K. (2017). A baseline for detecting misclassified and out-of-distribution examples in neural networks. In *International Conference on Learning Representations*. arXiv:1610.02136. https://arxiv.org/abs/1610.02136 — 特徵為基礎的偵測器希望改進的輸出分數基準。

### 綜述與教科書

- Koh, P. W. et al. (2021). WILDS: a benchmark of in-the-wild distribution shifts. In *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139. https://proceedings.mlr.press/v139/koh21a.html — 在自然偏移下測試偵測器的基準。
- Ben-David, S., Blitzer, J., Crammer, K., Kulesza, A., Pereira, F. & Vaughan, J. W. (2010). A theory of learning from different domains. *Machine Learning* 79(1–2), 151–175. https://doi.org/10.1007/s10994-009-5152-4 — 說明領域改變如何影響誤差，與何時應觸發基於距離的偵測器相關。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋高斯模型與基於密度的偵測背景。
