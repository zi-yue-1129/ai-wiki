---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# 準確率

準確率是預測與正確標籤相符的比例。它是最簡單的分類指標，也是最常被誤讀的一個。

## 定義

對於二元問題，設真正例為 $TP$、真負例為 $TN$、偽正例為 $FP$、偽負例為 $FN$：

$$\text{準確率} = \frac{TP + TN}{TP + TN + FP + FN}$$

多類別問題中，它是預測類別與真實類別相同的樣本所占的比例。


## 動態教學：類別比例與平衡準確率

<div style="max-width:100%;overflow-x:auto" role="group" tabindex="0" aria-label="教學動畫（聚焦後可使用方向鍵水平捲動）">
<div style="width:640px">
<img data-source-asset-urls src="../../../../assets/concept-animations/accuracy-prevalence-still.svg" data-motion-src="../../../../assets/concept-animations/accuracy-prevalence-motion.svg" data-still-src="../../../../assets/concept-animations/accuracy-prevalence-still.svg" alt="正例比例由百分之十增加到百分之九十，真正率與真負率保持固定。普通準確率從 0.89 降至 0.81，平衡準確率維持 0.85。" width="640" height="360">
</div>
</div>

*原創教學動畫, CC BY-SA 4.0.* MkDocs 網站可播放／暫停，窄螢幕可聚焦後以方向鍵水平捲動；減少動態效果模式顯示靜態影格。 [GitHub 靜態預覽](../../../../assets/concept-animations/accuracy-prevalence-still.svg) · [完整 SVG 動畫](../../../../assets/concept-animations/accuracy-prevalence-motion.svg).

這是**假設母體比例的解析示例，並非模型實測或有限樣本結果**。若正例比例為 $p$，固定敏感度（TPR）$0.80$ 與特異度（TNR）$0.90$：

$$
\begin{gathered}
\operatorname{Accuracy}(p) \\
= p(0.80)+(1-p)(0.90) \\
= 0.90-0.10p.
\end{gathered}
$$

平衡準確率為**兩類別召回率的不加權平均**，$(0.80+0.90)/2=0.85$。當 $p$ 從 $0.10$ 變為 $0.90$，一般準確率便從 **0.89 降至 0.81**，但平衡準確率保持 **0.85**。[^balanced-demo] 此結論以兩個條件辨識率固定為前提；實際分布偏移也可能使它們改變。

## 解讀

準確率在預測標籤已固定時容易解釋；若模型輸出分數，轉換成標籤的規則（二元分類門檻或多類別 argmax 等）可能改變準確率。它的弱點是取決於類別比例。若 99% 的案例是負例，一個從不預測正例的模型，準確率就有 99%，但完全找不到任何正例。

## 何時使用

當類別大致平衡，且每種錯誤代價相同時，使用準確率。否則應同時報告精確率與召回率，或改用如 [PR-AUC](pr-auc.md) 之類的排序指標。

## 範例

以[共用的人工 100 筆混淆矩陣範例](index.md)為例，準確率為 $(40 + 30) / 100 = 0.70$。同一分類器的精確率為 0.80、召回率為 0.67（見[精確率](precision.md)與[召回率](recall.md)），準確率本身並不能顯示哪一類錯誤較多。

## 性質與變體

- **基準線。** 永遠預測多數類別的分類器，準確率等於該類別的比例。在 90% 為負例的資料上，0.90 的準確率並沒有進步。
- **平衡準確率。** 各類別召回率的平均。二元情況下為 $\tfrac{1}{2}(\mathrm{TPR} + \mathrm{TNR})$，不受類別大小影響。
- **Top-k 準確率。** 多類別問題中，只要真實類別在分數最高的 $k$ 個之中，該案例即算正確。
- **限制。** 準確率對所有錯誤一視同仁，無法表達誤報與漏報成本不同的情況。

## 常見陷阱

- **類別不平衡。** 高準確率可能只是因為模型預測多數類別。應以多數類別的比例作為基準比較。
- **多標籤資料。** 在 scikit-learn 中，多標籤輸入的準確率是子集準確率：只有整組標籤完全相符，樣本才算正確。這比逐標籤平均的準確率更嚴格（見參考文獻）。

## 相關指標

[精確率](precision.md)、[召回率](recall.md)與 [F1 分數](f1.md)分別拆解了準確率所合併的兩種錯誤。家族概述見[分類指標](index.md)。

## 參考文獻

### 文章與文件

- scikit-learn contributors. *accuracy_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html — API 參考，說明定義、正規化選項與多標籤的行為。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類評分器的概述，以及各自的適用時機。

### 補充來源

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — 說明為什麼在稀有正例上，精確率—召回率曲線比 ROC 曲線更有資訊量。
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — 統計學習的標準教科書，涵蓋其評估方法。

[^balanced-demo]: scikit-learn contributors. *balanced_accuracy_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html — 定義本示意採用的逐類別召回率平均。
