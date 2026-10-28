---
translation_reviewed: 2026-10-28
tags:
  - class imbalance
  - loss functions
  - long-tailed learning
aliases:
  - logit adjustment
  - 邏輯調整
  - 長尾學習
---

# 邏輯調整（Logit Adjustment）

邏輯調整透過依類別先驗平移模型的輸出分數，來處理類別不平衡。它可以在訓練後套用（不改變已學到的模型），也可以直接放進訓練損失。Menon 等人（2021）指出，對平衡誤差而言，這是一致的修正，而重新加權損失則不是。

## 問題

在長尾資料上訓練的分類器，會學到偏向頭部類別的分數，因為這些類別主導訓練訊號。經典修正是依類別頻率為損失加權，但這會改變訓練目標。論文認為，當訓練資料可以被完美擬合時，重新加權的效果有限。因此需要的是針對決策規則的修正。

## 核心想法

Menon 等人在預測時把每個類別的 logit 平移 $-\tau \log \pi_y$，其中 $\pi_y$ 是類別先驗，$\tau > 0$ 為純量（見原論文第 4.1 節的式 9）。同一個偏移也可以直接放進訓練損失。在取最大分數之前減去對數先驗，決策規則的行為就像類別是平衡的。此方法改變的是稀有與主流標籤之間的邊界，而不是學到的特徵。

## 運作方式

1. 從訓練標籤估計類別先驗 $\pi_y$。
2. 事後套用：測試時預測 $\arg\max_y \left( f_y(x) - \tau \log \pi_y \right)$，其中 $\tau$ 是在驗證資料上調整的純量。
3. 訓練中套用：使用包含對數先驗偏移的損失，使學到的 logit 已包含此調整。

事後版本不需要重新訓練，先驗中每個類別只需一個純量。

## 結果

Menon 等人在長尾基準上評估此方法，衡量平衡誤差。數字取決於設定，請直接查閱論文。

## 限制

- **校準。** 此修正假設分數是校準過的對數機率。來自回歸或排序目標的分數不符合此假設，因此偏移不能直接套用。
- **純量調參。** 類似溫度的純量 $\tau$ 必須在反映目標平衡的保留資料上調整。
- **先驗需已知。** 先驗來自訓練集。若測試分布不同，偏移量就需要改變。

## 與其他主題的連結

邏輯調整是[類別平衡損失](class-balanced-loss.md)在訓練後的對應方法，後者改變訓練目標。兩者都處理長尾分類。它所平移的決策門檻，也是成本敏感分類的主題，其中不對稱的錯誤成本以相同方式處理。不平衡如何出現在指標中，見[評估與驗證](../evaluation-and-validation/index.md)。

## 應用

長尾影像辨識、相機陷阱的物種分類，以及任何漏掉稀有類別代價很高的任務。

## 開放問題

如何把此修正延伸到非校準機率的輸出；以及當不平衡在輸入空間中變化時，每個類別一個偏移是否仍然足夠。

## 參考文獻

### 奠基性論文

- Menon, A. K.、Jayasumana, S.、Rawat, A. S.、Jain, H.、Veit, A. 與 Kumar, S.（2021）. *Long-tail Learning via Logit Adjustment*. ICLR 2021. https://arxiv.org/abs/2007.07314 — 說明平衡誤差的一致修正是依類別先驗做 logit 偏移，可事後套用或放入損失。
- Cui, Y. 等人（2019）. *Class-Balanced Loss Based on Effective Number of Samples*. CVPR 2019. https://openaccess.thecvf.com/content_CVPR_2019/html/Cui_Class-Balanced_Loss_Based_on_Effective_Number_of_Samples_CVPR_2019_paper.html — 邏輯調整所比較的類別重新加權基準。

### 文章與預印本

- Cao, K. 等人（2019）. *Learning Imbalanced Datasets with Label-Distribution-Aware Margin Loss*. NeurIPS 2019. https://proceedings.neurips.cc/paper/2019/hash/621461af90cadfdaf0e8d4cc25129f91-Abstract.html — 使用依類別頻率而定的邊界，是另一種同樣改變決策邊界的方法。
- Kang, B. 等人（2020）. *Decoupling Representation and Classifier for Long-Tailed Recognition*. ICLR 2020. https://arxiv.org/abs/1910.09217 — 分離表徵學習與分類器學習，並說明在分類器端的重新平衡很有效。
- Ren, J. 等人（2022）. *Balanced MSE for Imbalanced Visual Regression*. CVPR 2022. https://openaccess.thecvf.com/content/CVPR2022/html/Ren_Balanced_MSE_for_Imbalanced_Visual_Regression_CVPR_2022_paper.html — 平衡概念在回歸上的對應，以修正 MSE 損失。
