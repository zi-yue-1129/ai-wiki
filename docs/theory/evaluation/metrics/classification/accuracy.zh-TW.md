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

## Top-k 成員判斷：排名視窗如何擴大

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="可使用鍵盤水平捲動的 top-k 準確率動畫">
<div style="width:640px">
<img data-source-asset-urls style="width:640px;min-width:640px;max-width:none;height:auto;display:block" src="../../../../assets/concept-animations/accuracy-topk-window-still.svg" data-still-src="../../../../assets/concept-animations/accuracy-topk-window-still.svg" data-motion-src="../../../../assets/concept-animations/accuracy-topk-window-motion.svg" alt="三筆人工四類別預測的真實類別分別排第 1、2、4 名。top-1 命中三分之一，top-2 命中三分之二，top-4 全數命中。青綠色選取框在離散狀態中擴大，金色圓點標出不變的真實類別。" width="640" height="360">
</div>
</div>

*原創 12 秒 SVG 教學動畫，搭配獨立的 GitHub 靜態回退圖（CC BY-SA 4.0）。* 三筆固定的**人工四類別排名**中，真實類別分別位於第 $1$、$2$、$4$ 名。允許的排名視窗從 $k=1$ 擴大到 $2$、$4$，top-k 準確率便從 $1/3$、$2/3$ 變成 $3/3$。改變的只有**評分規則**，模型、分數與輸入均未更新。四類別的 top-4 必然全對，不代表模型學得更好。Top-1 等於一般 argmax 準確率；此處 top-k 是**單標籤多類別**評估，不是多標籤完整集合準確率。

MkDocs 可播放／暫停；手機可聚焦圖形，再使用方向鍵水平捲動。減少動態效果模式固定顯示 top-2。[GitHub 靜態圖](../../../../assets/concept-animations/accuracy-topk-window-still.svg) · [完整 SVG 動畫](../../../../assets/concept-animations/accuracy-topk-window-motion.svg)。

## Top-k 邊界同分：分數相同仍可能改變命中結果

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="可使用鍵盤水平捲動的 top-k 同分動畫">
<div style="width:640px">
<img data-source-asset-urls style="width:640px;min-width:640px;max-width:none;height:auto;display:block" src="../../../../assets/concept-animations/accuracy-topk-tie-policy-still.svg" data-still-src="../../../../assets/concept-animations/accuracy-topk-tie-policy-still.svg" data-motion-src="../../../../assets/concept-animations/accuracy-topk-tie-policy-motion.svg" alt="四個人工分數 A 0.90、B 0.70、C 0.70、D 0.20，真實類別是 C。當 k 等於 2，依較低索引優先會漏掉 C（零分之一），依較高索引優先則納入 C（一分之一）。靜態圖並列兩種同分規則。" width="640" height="360">
</div>
</div>

*原創 8 秒 SVG 教學動畫與 GitHub 雙欄靜態回退（CC BY-SA 4.0）。* 設 $k=2$、真實類別 **C**，固定人工分數為 **A=0.90、B=0.70、C=0.70、D=0.20**。B 與 C 在第二名的邊界同分。若同分時優先**較低的類別索引**，取出 $\{A,B\}$，此筆得 **0/1**；若優先**較高的索引**，取出 $\{A,C\}$，則得 **1/1**。離散動畫只切換同分規則，不代表模型分數發生變動。單筆示意不能視為模型效能估計。

scikit-learn 的 `top_k_accuracy_score` 明確採用**較高類別索引優先**的同分規則。[^topk-api] 比較不同實作時，必須說明類別索引順序及同分規則。這不同於 ROC-AUC 對正負配對同分給半分；top-k 最後仍進行離散的集合成員判斷。

MkDocs 沿用播放／暫停和減少動態效果回退（較高索引情境）；GitHub 靜態圖則**並排保留兩種結果**。[GitHub 靜態圖](../../../../assets/concept-animations/accuracy-topk-tie-policy-still.svg) · [完整 SVG 動畫](../../../../assets/concept-animations/accuracy-topk-tie-policy-motion.svg)。

## 多標籤完整符合率與逐標籤正確比例

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="可使用方向鍵水平捲動的多標籤錯誤分布動畫">
<div style="width:640px">
<img data-source-asset-urls style="width:640px;min-width:640px;max-width:none;height:auto;display:block" src="../../../../assets/concept-animations/accuracy-multilabel-error-placement-still.svg" data-still-src="../../../../assets/concept-animations/accuracy-multilabel-error-placement-still.svg" data-motion-src="../../../../assets/concept-animations/accuracy-multilabel-error-placement-motion.svg" alt="四筆人工樣本各有三個二元標籤。三個錯誤若分散在三筆樣本，完整符合率為四分之一；若集中在一筆樣本，則提高到四分之三，但逐標籤正確比例始終為十二分之九。" width="640" height="360">
</div>
</div>

*原創八秒 SVG 教學動畫（CC BY-SA 4.0）。* 這些是**人為構造的比較結果，不是模型實測指標**。綠色勾號表示該二元標籤預測正確，橘色叉號表示錯誤；計算此示例只需比較結果，不必指定每格的原始 0/1 值。兩種分布都正確預測 **12 格中的 9 格**，逐標籤正確比例為 **0.75**、Hamming loss 為 **0.25**。但多標籤的 subset accuracy 要求**同一筆樣本的三個標籤全部正確**。將三個錯誤分散至三筆樣本時為 **1/4 = 0.25**；集中到一筆樣本時則為 **3/4 = 0.75**。因此，完整符合率也取決於**不同標籤的錯誤如何共同出現在各筆樣本**，不能只由逐標籤平均正確率推算。參見 [scikit-learn Accuracy 定義](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)及 [Hamming loss 文件](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.hamming_loss.html)。

MkDocs 可以播放／暫停；手機可聚焦圖像區域後以方向鍵水平捲動。減少動態效果模式固定為錯誤集中狀態。GitHub 的[雙情境靜態圖](../../../../assets/concept-animations/accuracy-multilabel-error-placement-still.svg)會同時顯示兩種結果；另可查看[完整 SVG 動畫](../../../../assets/concept-animations/accuracy-multilabel-error-placement-motion.svg)。

## 樣本權重可以反轉準確率排名

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="可使用方向鍵水平捲動的加權準確率動畫">
<div style="width:640px">
<img data-source-asset-urls style="width:640px;min-width:640px;max-width:none;height:auto;display:block" src="../../../../assets/concept-animations/accuracy-sample-weight-ranking-still.svg" data-still-src="../../../../assets/concept-animations/accuracy-sample-weight-ranking-still.svg" data-motion-src="../../../../assets/concept-animations/accuracy-sample-weight-ranking-motion.svg" alt="兩個模型對五筆人工樣本的預測都不變。等權重時 A 與 B 的準確率分別為 0.800 和 0.600；將第五筆樣本的權重由一改為五後，加權準確率變為九分之四與九分之七，排名反轉。" width="640" height="360">
</div>
</div>

*原創八秒 SVG 教學動畫（CC BY-SA 4.0）。* 模型 A 在第 1–4 筆預測正確，模型 B 在第 1、2、5 筆正確。兩者預測結果完全固定。五筆全部等權重時，A 為 **4/5 = 0.800**、B 為 **3/5 = 0.600**。如果只將第 5 筆的權重改成 **5**，其他仍為 1，結果就反轉為 **A = 4/9 ≈ 0.444**、**B = 7/9 ≈ 0.778**。

$
\mathrm{WeightedAccuracy}=\frac{\sum_i w_i\,\mathbf{1}(\hat y_i=y_i)}{\sum_i w_i}, \qquad w_i\ge 0,\ \sum_i w_i>0.
$

權重為**人為設定的重要性係數**，不是實際抽樣頻率、部署母體盛行率估計或推薦的類別平衡權重，也不代表 B 學習得更好。權重必須對應事先定義的評估目的（例如抽樣設計或部署損失），比較不同模型時也應使用同一套權重。scikit-learn 的 [`accuracy_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html) 提供 `sample_weight` 參數。

MkDocs 沿用播放／暫停與手機鍵盤水平捲動；減少動態效果模式固定顯示加權結果。GitHub 使用[兩種權重設定的靜態預覽](../../../../assets/concept-animations/accuracy-sample-weight-ranking-still.svg)；另可查看[完整 SVG 動畫](../../../../assets/concept-animations/accuracy-sample-weight-ranking-motion.svg)。

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

[^topk-api]: scikit-learn contributors. *top_k_accuracy_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.top_k_accuracy_score.html — 定義 top-k 準確率與較高索引優先的同分政策。
