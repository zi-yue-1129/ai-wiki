---
translation_reviewed: 2026-10-30
---

# 馬氏距離偵測器

Lee 等人的偵測器對預訓練神經網路的特徵擬合類別均值與共享共變異數，再根據到最近類別的接近程度評分。[^lee] 本頁是[分布外偵測](index.md)的一部分。

## 擬合特徵統計量

令 $z_i=f(x_i)\in\mathbb R^d$ 為訓練特徵、$y_i$ 為其標籤、$C$ 為類別數、$N_c$ 為類別 $c$ 的樣本數。論文中的最大概似估計為[^lee]

$$
\hat\mu_c=\frac{1}{N_c}\sum_{i:y_i=c}z_i,\qquad
\hat\Sigma=\frac{1}{N}\sum_{c=1}^{C}\sum_{i:y_i=c}
(z_i-\hat\mu_c)(z_i-\hat\mu_c)^\top.
$$

每筆殘差都以**所屬類別的均值**中心化，而非整體均值。否則，類別中心之間的距離也會計入共變異數。此處分母 $1/N$ 指定了最大概似的慣例；改變分母會縮放平方距離，因此也會改變數值門檻。

高斯模型是對表徵的假設，並非特徵確實服從該分布的證明。神經分類器能擬合標籤，並不足以確立它也是良好的密度模型。

## 距離、平方距離與分數

必須區分三個量：

$$
D_c^2(x)=(f(x)-\hat\mu_c)^\top\hat\Sigma^{-1}
(f(x)-\hat\mu_c),\qquad
D_{\min}^2(x)=\min_c D_c^2(x),\qquad
M(x)=-D_{\min}^2(x).
$$

二次型是**平方**馬氏距離。SciPy 的距離函式回傳其平方根，第三個參數則須傳入共變異數的反矩陣。[^scipy] 若直接傳入共變異數矩陣，或將函式回傳值當作平方距離，就會實作出不同的計算。

當共變異數矩陣為正定時，$D_{\min}^2$ 非負，而 $M$ 非正。分數越接近零，表示越接近某個類別。以 $M>\tau$ 作為接受條件，等價於 $D_{\min}^2<-\tau$；拒絕規則不可混淆這兩種方向。

這也說明了為何分數不應被當成機率。其大小取決於表徵、共變異數估計器與計算慣例。$-2$ 不代表負機率，接近零的分數也無法證明輸入屬於訓練分布。

### 計算範例

取兩個類別均值 $\mu_1=(0,0)$、$\mu_2=(4,0)$，以及共變異數 $\Sigma=\operatorname{diag}(4,1)$。對特徵 $z=(a,b)$，

$$
D_1^2=\frac{a^2}{4}+b^2,\qquad
D_2^2=\frac{(a-4)^2}{4}+b^2.
$$

| 特徵 | $D_1^2$ | $D_2^2$ | $M$ | $\tau=-3$ 時的決策 |
|---|---|---|---|---|
| $(2,1)$ | 2 | 2 | -2 | 接受 |
| $(0,2)$ | 4 | 8 | -4 | 拒絕 |

門檻與數字僅供說明，並非模型測量結果。沿第一軸移動兩個單位，對平方距離的貢獻是 $1$；沿第二軸移動相同距離，貢獻則為 $4$。共變異數改變了幾何，而不只是測量一般歐幾里得長度。若最近類別出現平手，任選一個索引都會得到相同的未擾動分數。

## 輸入前處理與多層特徵

演算法 1 在每層選出最近類別，朝**降低平方距離**的方向進行輸入梯度步伐，再重新計算最大負距離。各層分數以在驗證樣本上擬合的邏輯斯迴歸權重結合。[^lee] 微分時固定選出的類別，步伐為

$$
\tilde x_\ell=x-\varepsilon\operatorname{sign}
\left(\nabla_xD_{\ell,\hat c}^2(x)\right).
$$

提高 $M$ 與提高 $D^2$ 是相反的操作。多層實作也必須區分「每層各自擾動一份輸入」與「所有層共用同一次擾動」。

骨幹網路的權重不必重新訓練，但擬合特徵統計量與擬合驗證偵測器，是兩個不同的操作。若將完整集成描述成只需要儲存訓練均值，就會漏掉驗證階段。應報告調參使用的是真實 OOD 樣本，還是替代的負類資料。

## 數值條件

共享共變異數並不保證反矩陣穩定。經驗共變異數可能病態或奇異；scikit-learn 說明了將其向縮放後的單位矩陣收縮，作為一種改善方法。[^covariance] 例如，

$$
\Sigma_\alpha=(1-\alpha)\hat\Sigma+
\alpha\frac{\operatorname{tr}(\hat\Sigma)}{d}I.
$$

其中 $0\leq\alpha\leq1$。這是一項可選的實作決策，並不表示 Lee 等人指定了這種正規化。應記錄 $\alpha$ 與估計器。當平均變異數為正，且 $\alpha>0$ 時，單位矩陣項會提高原本為零的特徵值；若所有殘差的變異數都為零，光靠這個式子就無法做到。

對可逆的共變異數矩陣，解 $\Sigma v=z-\mu_c$ 後計算 $(z-\mu_c)^\top v$，會得到與乘上反矩陣相同的二次型。廣義反矩陣會改變零空間方向的處理方式，因此重現時不應悄悄用它取代反矩陣。

## 論文結果與範圍

表 5 報告：CIFAR-10／DenseNet 對 SVHN，在使用 ID／OOD 驗證資料調參時，TPR 為 95% 的 **TNR 為 90.8%**；softmax 基準為 40.2%，ODIN 則為 86.2%。[^lee] TNR 衡量 OOD 輸入被拒絕的比例，不是類別準確度。

這些比較限定於所述資料、模型與調參流程，並不保證能處理每種分布偏移或適應性攻擊。

## 關聯與評估清單

最大 softmax 基準使用輸出機率，[^baseline]而 [ODIN](odin.md) 在該輸出分數上加入溫度縮放與輸入擾動。[^odin] 特徵偵測器則使用內部表徵的幾何。

為了讓比較可重現，應記錄：

1. 模型權重版本、特徵層、池化方式與輸入前處理。
2. 哪些有標籤資料用於擬合均值與共變異數，哪些資料用於調整偵測器。
3. 共變異數估計、正規化與數值求解器。
4. 分數方向、平方或平方根的慣例、門檻與正類定義。
5. 是否啟用前處理與多層結合，以及其推論成本。
6. 各種偏移下的結果、熟悉輸入的錯誤拒絕，以及拒絕後採取的行動。

這些是實務報告選項。有用的篩檢旗標仍需要獨立評估的備援機制，例如棄答或人工審查。改變表徵時應重新計算並驗證特徵統計量，而非假定舊的數值門檻可以直接沿用。

[^lee]: Lee et al.（2018），公式 1–2、演算法 1、第 2.2 節與表 5；詳見參考文獻。
[^scipy]: SciPy 的馬氏距離定義與參數文件；詳見參考文獻。
[^covariance]: scikit-learn 的經驗共變異數與收縮共變異數章節；詳見參考文獻。
[^baseline]: Hendrycks & Gimpel（2017），摘要；詳見參考文獻。
[^odin]: Liang et al.（2018），摘要；詳見參考文獻。

## 參考文獻

- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. NeurIPS. https://arxiv.org/abs/1807.03888 — 定義特徵統計量、負距離評分、輸入前處理及以驗證資料擬合的特徵集成。
- Hendrycks, D. & Gimpel, K. (2017). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. ICLR. https://arxiv.org/abs/1610.02136 — 提出以最大 softmax 機率偵測分類錯誤與陌生輸入的基準。
- Liang, S., Li, Y. & Srikant, R. (2018). *Enhancing the Reliability of Out-of-distribution Image Detection in Neural Networks*. ICLR. https://arxiv.org/abs/1706.02690 — 提出用於 softmax 分布外偵測的溫度縮放與輸入擾動。
- SciPy contributors. *scipy.spatial.distance.mahalanobis*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.mahalanobis.html — 指定平方根距離的慣例，以及 API 中反共變異數矩陣參數的意義。
- scikit-learn contributors. *Covariance estimation*. https://scikit-learn.org/stable/modules/covariance.html — 說明經驗共變異數、數值反矩陣問題與收縮共變異數估計器。
