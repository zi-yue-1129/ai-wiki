---
tags:
  - supervised learning
  - evaluation
  - metrics
---

# 評估與驗證

衡量監督式模型在新資料上會表現得多好，並避免自欺。

## 切分資料

- **訓練／驗證／測試**：在驗證集上調校，在測試集上只報告一次。
- **k 折交叉驗證**在 $k$ 種切分上取平均，適用於小資料。類別不平衡時使用**分層**摺。
- **依群組與依時間切分**：把同一位病人、使用者或工作階段的所有樣本放在同一摺；預測任務則一律在比訓練資料更晚的時間上驗證。在這些情況下隨機切分會洩漏資訊。
- **巢狀交叉驗證**把超參數選擇與效能估計分開。

## 指標

| 任務 | 指標 | 注意事項 |
|---|---|---|
| 分類 | 準確率 | 類別不平衡時會誤導 |
| 分類 | 精確率、召回率、F1 | 取決於門檻 |
| 分類 | ROC-AUC、PR-AUC | 對稀有正例而言，PR-AUC 較有資訊量 |
| 機率 | 對數損失、Brier 分數、校準誤差 | 獎勵誠實的機率 |
| 迴歸 | RMSE、MAE、$R^2$ | RMSE 會重罰大誤差 |
| 排序 | NDCG、MAP | 依位置加權 |
| 分割 | IoU、Dice | |

**校準**問的是：預測為 80% 的事件，是否真的有 80% 的機率發生；溫度縮放（Guo et al., 2017）是修正深度網路的簡單方法。依任務分類的完整指標，以及使用這些指標的協定，見[評估](../../../evaluation/index.md)。

## 常見失誤

- **資料洩漏**：在全部資料上擬合的前處理、切分之間的重複樣本、編碼了標籤的特徵。
- **重複使用測試集**：反覆依測試分數挑選模型，會使模型對測試集過擬合；基準排行榜就深受其害。
- **捷徑學習**：因為錯誤的理由而得到高準確率；應在分布外與反事實資料集上測試。
- **子群體差距**：應報告各群體的指標，而不只是平均值（見[倫理與公平](../../../../society/ethics/index.md)）。
- **統計雜訊**：應報告信賴區間或多個隨機種子的結果，而不是單次執行的結果。

## 與其他概念的連結

LLM 的評估會加入基準污染與評審模型偏誤的問題；見[大型語言模型](../../../models/llm/index.md)。相關資源：[里程碑論文](../../../../reference/papers/index.md)。

## 參考文獻

### 開創性論文

- Saito & Rehmsmeier (2015), "The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets", *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — 說明為什麼在稀有正例上，精確率—召回率曲線比 ROC 曲線更有資訊量。
- Niculescu-Mizil & Caruana (2005), "Predicting good probabilities with supervised learning", ICML. https://doi.org/10.1145/1102351.1102430 — 比較常見分類器的機率校準，以及校準方法的效果。
- Guo et al. (2017), "On calibration of modern neural networks", ICML, [arXiv:1706.04599](https://arxiv.org/abs/1706.04599) — 顯示現代網路過度自信，並說明溫度縮放可以修正這一點。
- Zhang, C. et al. (2017). Understanding deep learning requires rethinking generalization. ICLR. arXiv:1611.03530. https://arxiv.org/abs/1611.03530 — 顯示網路可以記住隨機標籤，因此保留測試集不可或缺。

### 綜述與教科書

（本頁未查核任何綜述或教科書。）

### 講座與影片

- Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters*, 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010 — 說明 ROC 曲線與 AUC 的建構、解讀與常見誤用。

### 文章與文件

- Grinsztajn, Oyallon & Varoquaux (2022), "Why do tree-based models still outperform deep learning on tabular data?", [arXiv:2207.08815](https://arxiv.org/abs/2207.08815) — 嚴謹的基準設計，可作為公平比較方法的範本。

## 延伸學習

- StatQuest with Josh Starmer，關於 ROC 曲線與 AUC 的單元，YouTube。https://www.youtube.com/@statquest — 以視覺化的方式說明 ROC 曲線與 AUC 如何建構，以及它們衡量的是什麼。
