---
translation_reviewed: 2026-10-28
---

# 馬氏距離偵測器

馬氏距離偵測器依據輸入的內部特徵與各類別特徵的距離來評分。網路的特徵被建模為高斯群聚，每個類別一個；遠離所有群聚的輸入會被標記為分布外。Lee 等人（2018）為 OOD 與對抗輸入提出這個方法。它是[分布外偵測](../index.md)頁面所描述的分數之一。

## 概述

最大 softmax 機率只使用網路的最終輸出。Lee 等人（2018）則改看特徵空間，也就是分類器做決策所依據的中間表徵。在這個空間中，同一類的訓練樣本傾向聚在一起。作者為每個類別擬合一個高斯分布，並以輸入到最近類別的距離作為它典型程度的度量。此方法適用於任何預先訓練的 softmax 分類器，計算基本分數時不需要離群值資料。論文也描述了一些改進，例如使用多個層與小幅輸入擾動，但這裡不涵蓋。

## 關鍵概念

- **特徵空間。** 網路某一層的活化值，作為輸入的表徵。
- **類別條件高斯。** 擬合於某一類別特徵的高斯分布，其平均數位於類別中心。
- **馬氏距離。** 以共變異數重新縮放特徵空間的距離，因此變異較大的方向，其權重比變異較小的方向低。
- **共享共變異數。** 此方法對所有類別使用同一個共變異數矩陣，如高斯判別分析所做的那樣。

## 運作方式

令 $f(x)$ 為輸入 $x$ 的特徵。利用訓練資料，此方法估計每個類別 $c$ 的平均數 $\mu_c$，以及一個共享的共變異數 $\Sigma$：

$$
\mu_c = \frac{1}{N_c}\sum_{i:\,y_i=c} f(x_i), \qquad \Sigma = \frac{1}{N}\sum_{c}\sum_{i:\,y_i=c}\big(f(x_i)-\mu_c\big)\big(f(x_i)-\mu_c\big)^{\top}.
$$

分數是到最近類別之馬氏距離平方的負值：

$$
M(x) = \max_c \; -\big(f(x)-\mu_c\big)^{\top}\Sigma^{-1}\big(f(x)-\mu_c\big).
$$

當 $M(x)$ 低於在驗證資料上選定的門檻 $\tau$ 時，輸入會被標記。程序如下。

1. 訓練分類器並凍結它。
2. 抽取訓練資料的特徵，估計 $\mu_c$ 與 $\Sigma$。
3. 對保留的分布內輸入與 OOD 輸入計算 $M(x)$，並選定 $\tau$。
4. 回報 AUROC 與 95% 真陽性率時的偽陽性率。

## 結果

論文回報，此方法在其實驗中對分布外與對抗樣本的偵測都達到最先進的表現。先前多數方法只針對這兩個問題之一做評估。摘要也指出，在較困難的設定下（例如訓練資料含有雜訊標籤或樣本數很少），此方法更為穩健。確切數字見論文，本頁沒有重新執行。

## 限制

- **高斯假設。** 一個類別的特徵未必能由單一、共享共變異數的高斯分布很好地描述，這可能使分數對某些類別不合適。
- **共變異數估計。** 共變異數矩陣的每一列與每一行都對應一個特徵。當特徵維度相對於訓練樣本數很大時，估計會有雜訊，通常需要正規化。
- **標籤與層的選擇。** 此方法需要有標籤的訓練資料來形成類別平均數，而且表現取決於使用哪一層的特徵。
- **以離群值調參。** 論文中有些設定是用包含 OOD 樣本的驗證資料選定的。Hsu 等人（2020）指出，當這類資料事先無法取得時，以 OOD 資料調參很難站得住腳。

## 開放問題

- 哪些層包含最多關於不熟悉程度的有用資訊？能否在沒有離群值資料的情況下選定它們？
- 非參數的替代方案是否更好？Sun 等人（2022）以最近鄰距離取代高斯假設，並回報它不需要分布假設。

## 與其他主題的連結

此方法是把高斯密度模型套用在特徵上，因此與[異常偵測](../../../paradigms/unsupervised/anomaly-detection/index.md)頁面相連，那裡的密度式偵測器扮演類似的角色。由於它使用中間特徵而非輸出機率，它不直接依賴 [最大 softmax 機率](../max-softmax-probability/index.md)基準與[能量分數](../energy-score/index.md)所依據的 softmax 信心。

論文同時處理對抗輸入與 OOD 輸入，因此與[對抗樣本與穩健性](../../adversarial-robustness/index.md)並列。一個大腦上的類比，是知覺會把輸入與一個關於典型輸入的內部模型相比較，見[預測編碼](../../../../brain-mind/predictive-coding/index.md)。

## 參考文獻

### 開創性論文

- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. arXiv. https://arxiv.org/abs/1807.03888 — 提出針對 OOD 與對抗輸入的馬氏距離分數，在特徵空間中使用類別條件高斯（NeurIPS 2018）。
- Hendrycks, D. & Gimpel, K. (2016). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. arXiv. https://arxiv.org/abs/1610.02136 — 提出馬氏分數所比較的最大 softmax 機率基準（ICLR 2017）。
- Sun, Y., Ming, Y., Zhu, X. & Li, Y. (2022). *Out-of-Distribution Detection with Deep Nearest Neighbors*. arXiv. https://arxiv.org/abs/2204.06507 — 以特徵空間中的最近鄰距離取代高斯假設（ICML 2022）。

### 綜述與教科書

- Yang, J., Zhou, K., Li, Y. & Liu, Z. (2021). *Generalized Out-of-Distribution Detection: A Survey*. arXiv. https://arxiv.org/abs/2110.11334 — 綜述分類式、密度式與距離式的 OOD 偵測方法。

### 文章與文件

- Hsu, Y.-C., Shen, Y., Jin, H. & Kira, Z. (2020). *Generalized ODIN: Detecting Out-of-distribution Image without Learning from Out-of-distribution Data*. arXiv. https://arxiv.org/abs/2002.11297 — 討論以離群值資料調參為何會使評估產生偏誤，並提出替代方案。
