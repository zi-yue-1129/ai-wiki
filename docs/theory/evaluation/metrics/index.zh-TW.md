---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
---

# 指標

指標把模型的輸出與正確答案轉換成一個數字。合適的指標取決於這個數字要支持的決定，因此選擇指標本身就是設計的一部分。本頁依任務整理常見指標。監督式學習的經典情境，已在[評估與驗證](../../paradigms/supervised/evaluation-and-validation/index.md)中深入說明。

## 依任務分類的指標

| 任務 | 指標 | 獎勵的是什麼 | 注意事項 |
|---|---|---|---|
| 分類 | 準確率 | 整體正確性 | 類別不平衡時會誤導 |
| 分類 | 精確率、召回率、F1 | 在一個選定門檻下的正確正例 | 取決於門檻，因此要報告門檻 |
| 分類 | ROC-AUC | 在所有門檻下，正例排在負例之上的程度 | 對稀有正例可能過於樂觀 |
| 分類 | PR-AUC | 在各召回率水準下的精確率 | 基準線等於正例比例，因此會隨資料集而變 |
| 機率 | 對數損失、Brier 分數 | 誠實的機率 | 對數損失會嚴厲懲罰過度自信的錯誤 |
| 校準 | 校準誤差 | 預測的信心與觀察到的頻率一致 | 取決於預測如何分箱 |
| 迴歸 | RMSE、MAE、$R^2$ | 誤差的大小 | RMSE 對大誤差的懲罰比 MAE 重 |
| 排序 | NDCG、MAP | 排序，並依位置加權 | 需要分級或二元的相關性標籤 |
| 分割 | IoU、Dice | 預測區域與正確區域的重疊程度 | 小區域會放大邊界誤差 |

scikit-learn 指南列出每個類別的標準評分器（見參考文獻）。

## 讓指標對應到決定

- **挑選候選名單**時，應使用排序指標。在固定門檻下的準確率，可能掩蓋良好的排序。
- **稀有事件**（例如詐欺或疾病）應使用 PR-AUC，並報告實際會使用的門檻下的精確率。ROC-AUC 可能很高，但精確率很差。
- **直接使用機率**（例如作為風險分數）時，除了區分能力，也要檢查校準。Guo et al. (2017) 指出，現代神經網路常常過度自信。

## 校準

當模型對某些案例給出機率 $p$ 時，這些案例中大約有 $p$ 的比例為正例，此模型就是校準的。校準與準確率是不同的概念：模型可能排序得很好，卻給出尺度錯誤的機率。溫度縮放可以修正深度網路的過度自信（Guo et al., 2017）。Niculescu-Mizil 與 Caruana（2005）比較了常見分類器的校準。

## 語言模型的指標

語言模型常以保留文字上的對數似然，或在選擇題上的準確率來評分。自由格式的答案通常由程式或評審模型檢查。這些選擇及其周邊的協定，見[評估與基準](../../../engineering/evaluation/index.md)與[評估協定](../protocols/index.md)。生成式影像模型的指標，本頁尚未涵蓋。

## 開放問題

指標是一種代理。它是否符合使用者重視的價值，是應用層面的問題，無法靠公式解決。由於沒有單一指標能涵蓋所有取捨，比較審慎的做法是同時報告數個指標，並附上它們的定義與門檻。

## 與其他概念的連結

指標數值取決於資料的切分方式，因此同一個指標在不同協定下可能得到不同的數字。見[評估協定](../protocols/index.md)。

## 參考文獻

### 開創性論文

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — 說明為什麼在稀有正例上，精確率—召回率曲線比 ROC 曲線更有資訊量。
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — 比較常見分類器的機率校準，以及校準方法的效果。
- Guo, C. et al. (2017). On calibration of modern neural networks. ICML. https://arxiv.org/abs/1706.04599 — 顯示現代網路過度自信，並說明溫度縮放可以修正這一點。

### 綜述與教科書

- Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters* 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010 — 說明 ROC 曲線與 AUC 的建構、解讀與常見誤用。

### 文章與文件

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 標準分類、迴歸與排序評分器及其定義的參考。
