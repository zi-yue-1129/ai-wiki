# 監督式學習

## 概念

從標註範例 \((x_i, y_i)\) 學習映射 \(f: X \to Y\)。標籤直接告訴學習者正確答案，因此可以直接計算並最小化誤差：

\[
\min_\theta \frac{1}{n}\sum_{i=1}^n L\big(f_\theta(x_i), y_i\big) + \lambda R(\theta)
\]

## 任務類型

| 任務 | 輸出 | 常用損失 |
|---|---|---|
| 二元分類 | {0, 1} | 二元交叉熵、hinge |
| 多類別分類 | K 類之一 | softmax 交叉熵 |
| 多標籤分類 | K 個標籤的任意子集 | 每個標籤的 sigmoid 交叉熵 |
| 迴歸 | 實數 | 均方誤差、MAE、Huber |
| 序數迴歸 | 有順序的類別（如疾病分級） | 累積連結損失 |
| 結構化預測 | 序列、樹、分割 | CRF 損失、序列交叉熵、Dice |
| 排序 | 項目的順序 | 成對／列表式損失 |
| 存活分析 | 有設限的事件發生時間 | Cox 部分概似 |

## 演算法

線性與邏輯迴歸、k 近鄰、決策樹、隨機森林、梯度提升樹（XGBoost、LightGBM、CatBoost）、支援向量機、單純貝氏、高斯過程，以及各種神經網路。詳見 [機器學習](../../machine-learning/index.md)。

## 標籤從哪裡來

- **人工標註**（群眾外包、領域專家）：昂貴、緩慢、有時不一致；要測量標註者間一致性（Cohen's κ）
- **自然標籤**：實際發生事情的紀錄（點擊、購買、診斷、價格）
- **程式化標籤**：啟發式規則（見 [弱監督](../semi-supervised/index.md)）
- **模型產生的標籤**：用 LLM 標註或從大模型蒸餾；需以人工標籤驗證

## 常見陷阱

| 問題 | 症狀 | 解法 |
|---|---|---|
| 過擬合 | 訓練表現遠高於測試 | 正規化、更多資料、早停、資料增強 |
| 標籤雜訊 | 準確率停滯、記住錯誤 | 抗雜訊損失、重新標註、confident learning |
| 類別不平衡 | 準確率高但少數類別召回率很差 | 重新加權、重抽樣、focal loss、看 PR-AUC |
| 資料洩漏 | 驗證分數好得可疑 | 前處理只在訓練集 fit；依病人／時間／使用者切分 |
| 捷徑學習 | 模型利用虛假線索（如 X 光片上的醫院浮水印） | 壓力測試、反事實資料、跨領域評估 |
| 分布偏移 | 部署後表現下降 | 監控、[領域適應](../transfer/index.md) |

## 現代 AI 中的監督式學習

即使是「自監督」的基礎模型也依賴監督步驟：LLM 的**監督式微調（SFT）**就是監督學習（也是一種[模仿學習](../imitation/index.md)）；RLHF 中的獎勵模型也是用偏好標籤以監督方式訓練。

## 大腦與行為

- **小腦**：來自下橄欖核的攀爬纖維攜帶誤差訊號，驅動浦金埃氏細胞突觸的可塑性——經典的 Marr–Albus–Ito 小腦監督學習理論
- **Delta 規則與 Rescorla–Wagner**：Widrow–Hoff delta 規則（1960）與古典制約的 Rescorla–Wagner 模型（1972）數學形式相同：學習量與預測誤差成正比
- **類別學習**：心理學中的原型模型與範例模型，分別對應類別中心分類器與 kNN

## 延伸閱讀

- Hastie, Tibshirani & Friedman,《The Elements of Statistical Learning》（免費 PDF）
- [scikit-learn 監督式學習指南](https://scikit-learn.org/stable/supervised_learning.html)
- Geirhos et al. (2020), "Shortcut learning in deep neural networks", *Nature Machine Intelligence*
