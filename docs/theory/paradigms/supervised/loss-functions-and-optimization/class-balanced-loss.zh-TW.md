---
translation_reviewed: 2026-10-28
tags:
  - class imbalance
  - loss functions
  - long-tailed learning
aliases:
  - class-balanced loss
  - 類別平衡損失
  - 有效樣本數
---

# 類別平衡損失

類別平衡損失依每個類別的樣本數為其在訓練損失中的貢獻加權。Cui 等人（2019）讓權重依賴「有效樣本數」，而非原始樣本數，因為隨著某類別樣本增加，多出來的樣本帶來的新資訊會逐漸減少。

## 問題

在長尾資料集中，少數頭部類別有很多樣本，許多尾部類別只有少量樣本。使用一般交叉熵訓練的模型，可能偏向頭部類別而取得高準確率，但尾部類別的召回率很差。常見的修正是依逆頻率加權，但當尾部類別的樣本幾乎重複時，這種加權會過度放大它們。

## 核心想法

Cui 等人把每個類別的樣本視為來自一組小鄰域，因此同一類別的樣本會彼此重疊。於是預期的不重複樣本數為

$$E_n = \frac{1 - \beta^n}{1 - \beta},$$

其中 $n$ 是該類別的樣本數，$\beta \in [0, 1)$ 是超參數。類別權重與 $1/E_n$ 成正比，得到類別平衡損失。

## 運作方式

1. 統計每個類別 $c$ 的樣本數 $n_c$。
2. 以選定的 $\beta$ 計算有效樣本數 $E_{n_c}$。
3. 設定類別權重 $w_c \propto 1/E_{n_c}$，並正規化使權重總和等於類別數。
4. 以加權交叉熵訓練，或使用焦點損失的變體。

當 $\beta \to 1$ 時，有效樣本數趨近於原始樣本數，權重趨近逆頻率；$\beta$ 較小時，權重趨近均勻。

## 結果

Cui 等人在多個影像基準的長尾切分上評估此方法，並報告最佳的 $\beta$ 取決於資料集。確切數字見論文，重用前應先查證。

## 限制

- **超參數。** 效能取決於 $\beta$，而論文顯示過大的 $\beta$ 在某些資料上會傷害表現。
- **從一開始就加權。** 從第一個 epoch 就開始重新加權，可能讓尾部類別欠擬合。Cao 等人（2019）的做法是把重新加權延後到訓練的後期階段。
- **適用範圍。** 此方法針對分類。延伸到回歸目標需要不同的處理，若想要事後的替代方案，見[邏輯調整](logit-adjustment.md)。

## 與其他主題的連結

類別平衡損失是透過改變訓練目標來處理不平衡的方法之一。另一類則在訓練後改變決策規則，例如[邏輯調整](logit-adjustment.md)。不平衡問題在[模仿學習](../../imitation/index.md)中也很重要，稀有但關鍵的動作可能被常見動作淹沒。哪些指標能揭露不平衡，見[評估與驗證](../evaluation-and-validation/index.md)。

## 應用

長尾影像辨識、罕見病灶的醫學影像，以及任何常見類別主導資料的分類任務。

## 開放問題

如何在不以測試分布調參的情況下選擇有效樣本數參數；以及加權與表徵學習的交互作用，Kang 等人（2020）透過分離表徵與分類器來研究這個問題。

## 參考文獻

### 奠基性論文

- Cui, Y.、Jia, M.、Lin, T.-Y.、Song, Y. 與 Belongie, S.（2019）. *Class-Balanced Loss Based on Effective Number of Samples*. CVPR 2019. https://openaccess.thecvf.com/content_CVPR_2019/html/Cui_Class-Balanced_Loss_Based_on_Effective_Number_of_Samples_CVPR_2019_paper.html — 提出有效樣本數加權與類別平衡損失。arXiv 版本為 [arXiv:1901.05555](https://arxiv.org/abs/1901.05555)。
- Cao, K.、Wei, C.、Gaidon, A.、Arechiga, N. 與 Ma, T.（2019）. *Learning Imbalanced Datasets with Label-Distribution-Aware Margin Loss*. arXiv:1906.07413. https://arxiv.org/abs/1906.07413 — 說明從一開始就加權可能傷害尾部類別，並提出邊界方法與延後加權。

### 文章與預印本

- Menon, A. K. 等人（2021）. *Long-tail Learning via Logit Adjustment*. ICLR 2021. https://arxiv.org/abs/2007.07314 — 說明依類別先驗做 logit 偏移，可以是加權以外、一致的替代方案。
- Kang, B. 等人（2020）. *Decoupling Representation and Classifier for Long-Tailed Recognition*. arXiv:1910.09217. https://arxiv.org/abs/1910.09217 — 分離表徵學習與分類器學習，並說明只在分類器端重新平衡就很有效。
- Ren, J. 等人（2022）. *Balanced MSE for Imbalanced Visual Regression*. arXiv:2203.16427. https://arxiv.org/abs/2203.16427 — 把平衡的概念延伸到回歸，以似然為基礎修正 MSE 損失。
