---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/trees-and-ensembles
  - theory/paradigms/supervised/loss-functions-and-optimization
  - theory/paradigms/supervised/evaluation-and-validation
  - theory/paradigms/supervised/kernel-methods-svm
---

# 梯度提升

梯度提升以分階段的方式建立加法模型。在每個階段，一棵小樹會擬合目前預測處損失函數的負梯度，並以步長加入模型。Friedman（2001）把這種方法描述為函數空間中的最速下降。XGBoost（Chen 與 Guestrin，2016）是同一想法的可擴展系統，LightGBM 與 CatBoost 則是後來建立在其上的系統。家族層級的全貌見[決策樹與集成方法](index.md)頁。

## 概述

提升法依序建立模型，每一個都修正目前集成的錯誤。梯度提升把這個想法推廣。它不是為某個特定損失而重新加權樣本，而是把目前的預測視為函數空間中的一點，並沿著下坡方向移動。每一步的方向由損失在每個訓練點上的梯度給出，而一棵迴歸樹用來逼近這個方向。

這種觀點讓人能使用各種損失函數，從迴歸的平方誤差到分類的多類別邏輯損失。每棵樹都保持淺層，使每一步都簡單；步長與樹的數量則控制集成向訓練資料移動的程度。

## 核心概念

- **加法模型**：預測值是許多棵樹的和，\(F_M(x) = \sum_m \nu\, h_m(x)\)，每棵樹都建立在前面各棵樹留下的殘餘訊號之上。
- **偽殘差**：損失對目前預測值的負梯度，\(r_{im} = -\partial L(y_i, F(x_i))/\partial F(x_i)\)，取值點為 \(F = F_{m-1}\)。對平方損失而言，它就是一般的殘差 \(y_i - F_{m-1}(x_i)\)。
- **弱學習器**：擬合偽殘差的淺層迴歸樹。
- **學習率或收縮**（shrinkage） \(\nu\)：介於 0 與 1 之間的係數，用來縮放每棵樹的貢獻。數值越小，需要的樹越多。
- **次抽樣**：讓每棵樹只擬合隨機抽取的一部分資料列，是為了加速與正則化而常用的變體。

## 運作方式

1. 從對該損失最適合的常數預測 \(F_0\) 開始。
2. 對於 \(m = 1, \dots, M\)：
   - 在目前的預測 \(F_{m-1}\) 處計算偽殘差 \(r_{im}\)；
   - 以成對的 \((x_i, r_{im})\) 擬合一棵迴歸樹 \(h_m\)；
   - 更新 \(F_m = F_{m-1} + \nu\, h_m\)。

對平方損失而言，偽殘差就是一般的殘差，因此每棵樹擬合的是集成仍然預測錯誤的部分。對其他損失，只要知道梯度，同樣的步驟也適用。樹的數量 \(M\) 與學習率通常以驗證集選定，因為樹太多會擬合雜訊。

## 關鍵方法

### Greedy function approximation: A gradient boosting machine（Friedman, 2001）

- **問題：** 提升法與特定損失及特定的重新加權規則綁在一起。需要一個通用方法，能處理任何可微分的損失，並以單一框架同時處理迴歸與分類。
- **核心想法：** 把加法展開視為函數空間而非參數空間中的數值最佳化。每個階段都是一次最速下降步，而這一步以弱學習器擬合負梯度來近似，使方法具有一般性。
- **公式或演算法：** 上節的分階段程序，包括偽殘差的定義與更新式 \(F_m = F_{m-1} + \nu h_m\)。
- **結果：** 摘要提出了針對最小平方、最小絕對偏差與 Huber-M 迴歸，以及分類中多類別邏輯概似的具體演算法。摘要未報告基準測試的數字，因此此處不列出數值。
- **限制：** 此程序是貪婪的。若沒有收縮因子或依據保留資料選定的停止規則，集成可能過擬合。樹是一棵接著一棵建立的，因此提升法不像森林那樣能在樹之間平行化。

### XGBoost: A Scalable Tree Boosting System（Chen & Guestrin, 2016）

- **問題：** 梯度提升樹在非常大的資料上訓練緩慢，而處理稀疏輸入需要特別小心。方法需要在不損失準確度的前提下擴展。
- **核心想法：** 一個完整的樹提升系統，包含處理稀疏資料的分裂搜尋演算法，以及用於近似分裂搜尋的加權分位數草圖（weighted quantile sketch）。摘要還提到對快取存取模式、資料壓縮與分片（sharding）的注意，這些都是加速的工程選擇。
- **公式或演算法：** 與 Friedman 方法相同的分階段更新 \(F_m = F_{m-1} + \nu h_m\)。系統所用的正則化目標與分裂增益公式不在此處重現。
- **結果：** 摘要指出，XGBoost「能以遠少於既有系統的資源，擴展到數十億筆範例以上」。除此說法外，本頁不列出加速倍數或準確度的數值。
- **限制：** 系統有許多超參數，包括深度、學習率、正則化與次抽樣設定，且彼此互相影響。它繼承了提升法依序建立的性質。摘要所做的是規模上的主張，並非與所有替代方法相比的準確度主張。

### LightGBM（Ke et al., 2017）

- **問題：** 在大型資料上，為每個特徵、在每個範例上找出最佳分裂，是梯度提升的主要成本。
- **核心想法：** 梯度單側抽樣（GOSS）會排除大量梯度很小的樣本，使分裂搜尋只在較少的範例上進行。互斥特徵捆綁（EFB）則把很少同時取非零值的特徵捆綁在一起，減少需要掃描的特徵數。
- **公式或演算法：** 此處不給出封閉形式。方法即上述的梯度提升程序，並在每次分裂搜尋中套用 GOSS 抽樣與 EFB 捆綁。
- **結果：** 摘要指出 LightGBM 將傳統 GBDT 的訓練過程「加速至多達 20 倍以上，同時達到幾乎相同的準確度」。「至多」一詞表示這是最佳情況的數字，本頁不重現論文中的實驗。
- **限制：** 加速幅度取決於資料集，摘要以上限（「至多」）的方式給出。本頁不重現論文的實驗。

### CatBoost（Prokhorenkova et al., 2017）

- **問題：** 摘要把此問題描述為一種特殊的目標洩漏所造成的預測偏移（prediction shift），在存在類別特徵時會影響提升法。
- **核心想法：** 有序提升（ordered boosting）是一種以排列驅動、取代經典提升演算法的方法。論文也提出一種處理類別特徵的創新演算法。兩者都在處理同一種預測偏移。
- **公式或演算法：** 演算法細節見論文，此處不再重述。
- **結果：** 摘要未報告數值結果，因此此處不列出數值。
- **限制：** 其好處主要是針對類別特徵與預測偏移而提出。摘要沒有說明在純數值表格上的增益幅度。

## 關聯

- 隨機森林透過平均彼此獨立的樹來降低變異；梯度提升則依序擬合樹來降低偏差。見[隨機森林](random-forests.md)。
- 偽殘差就是損失的負梯度，因此損失函數的選擇是方法的一部分。見[損失函數與最佳化](../loss-functions-and-optimization/index.md)。
- 樹的數量與學習率通常以驗證與提前停止來選定。見[評估與驗證](../evaluation-and-validation/index.md)。
- 在表格資料上，提升樹會與[支援向量機](../kernel-methods-svm/svm.md)等間隔方法相比較。

## 開放問題

- 新系統之間的差距，有多少來自演算法本身，又有多少來自為速度所做的工程？
- 哪一種學習率、樹深度與樹數量的組合，能以最少的調參得到最佳的準確度？

## 參考文獻

### 開創性論文

- Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *Annals of Statistics*, 29(5), 1189–1232. https://doi.org/10.1214/aos/1013203451 — 把提升法視為函數空間中的最速下降，因而能適用於多種損失。
- Chen, T. & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16)*, pp. 785–794. https://doi.org/10.1145/2939672.2939785 — XGBoost 系統，包含處理稀疏資料的分裂演算法與用於可擴展訓練的加權分位數草圖。
- Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q. & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems 30 (NIPS 2017)*. https://papers.nips.cc/paper/6907-lightgbm-a-highly-efficient-gradient-boosting-decision-tree — 提出 GOSS 與 EFB，加速大型資料上的梯度提升。
- Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V. & Gulin, A. (2017). CatBoost: Unbiased boosting with categorical features. arXiv:1706.09516. https://arxiv.org/abs/1706.09516 — 提出有序提升，以及針對預測偏移的有序目標統計量方案。

### 綜述與教科書

- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning*（第 2 版）。Springer。https://doi.org/10.1007/978-0-387-84858-7 — 涵蓋提升與樹集成的章節；作者提供免費 PDF。
