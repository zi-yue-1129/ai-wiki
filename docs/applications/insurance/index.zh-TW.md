# 保險與精算科學

保險建立在風險定價之上。精算師已使用統計模型數百年，而機器學習以更豐富的資料（例如車聯網與理賠文字）擴展了這些模型。詐欺偵測與理賠處理則是較早、經過充分驗證的應用。能提升價格準確度的同一批模型，也可能產生新形式的不公平歧視，監管機構對此的審查日益嚴格。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 風險定價 | 廣義線性模型；梯度提升樹；神經網路 | 監管機構期待透明、可解釋的模型 |
| 理賠分流與準備金 | 理賠嚴重程度分類器；神經準備金模型 | 加速把理賠分派給適當的處理人員 |
| 詐欺偵測 | 監督式分類器；異常偵測；網路分析 | 嚴重的類別不平衡是核心困難 |
| 車聯網與依用量計價 | 從車輛感測器或手機資料建立的駕駛行為模型 | 資料同意與隱私問題 |
| 文件與理賠文字 | 用於閱讀醫療與維修報告的語言模型 | 新的錯誤與偏誤來源 |
| 核保與承保資格 | 關於保障範圍的自動化決定 | 受消費者保護規則規範 |

## 為什麼困難

- **罕見事件**：詐欺與大額理賠很少見，因此模型必須仔細校準，並以正確的指標評估。
- **長時間跨度**：保單的損失要數年後才會顯現，因此回饋很慢。
- **價格敏感**：預測風險的微小差異會改變誰會投保，進而改變風險池。
- **受保護特性的代理**：預測風險的特徵，也可能替代種族、性別或身心障礙等特性。

## 關鍵方法

- [決策樹與集成方法](../../theory/paradigms/supervised/trees-and-ensembles/index.md)：梯度提升樹是定價與詐欺模型的主力。
- [異常偵測](../../theory/paradigms/unsupervised/anomaly-detection/index.md)：標記與正常模式不同的理賠，與監督式詐欺模型並用。
- [機率與貝氏方法](../../theory/paradigms/probabilistic/index.md)：提供經過校準的風險估計與不確定性，這是定價所必需的。
- [可解釋性](../../society/interpretability/index.md)：解釋價格或決定的方法，監管機構越來越要求這類能力。

## 相關連結

- 銀行的信用評分與詐欺偵測與保險共用許多方法，見[金融](../finance/index.md)。
- 定價上的公平性約束與其他自動化決策是同一個問題，見[倫理與公平](../../society/ethics/index.md)。
- 人們在不確定下的判斷，以及如何感知與接受風險，是[認知科學](../../brain-mind/cognitive-science/index.md)的研究範圍。

## 應用

- 車險、住宅險與健康險的定價
- 理賠分流與自動化的初次報案處理
- 詐欺篩檢
- 以車聯網資料進行的依用量計價
- 準備金估計與保險組合監測

## 風險與限制

- **歧視性定價**：模型可能透過相關特徵，對某一群體提高價格，即使從未使用受保護的特性。
- **解釋缺口**：客戶或監管者可能無法得知價格為何變動。
- **模型風險**：在某一市場或產品中有效的模型，可能在另一個市場或產品中失效。
- **策略性行為**：客戶一旦知道裝置在測量自己，就會調整所回報的資訊或駕駛方式。

## 開放問題

- 能否在定價中加入公平性約束，而不破壞保險所依賴的風險分散機制。
- 如何驗證那些主要結果要數年後才會顯現的模型。

## 參考文獻

### 開創性論文

- Dal Pozzolo, A. et al. (2015). Calibrating Probability with Undersampling for Unbalanced Classification. *2015 IEEE Symposium Series on Computational Intelligence*. https://doi.org/10.1109/SSCI.2015.33 — 說明對稀有事件資料進行欠採樣會如何扭曲預測機率，以及如何修正，這是詐欺模型的核心問題。
- Bhattacharyya, S. et al. (2011). Data mining for credit card fraud: A comparative study. *Decision Support Systems*. https://doi.org/10.1016/j.dss.2010.08.008 — 在高度不平衡的資料上，比較偵測信用卡詐欺交易的學習方法。
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS*. https://arxiv.org/abs/1705.07874 — 提出 SHAP 值，把模型的預測歸因到各輸入特徵。

### 綜述與教科書

- Wüthrich, M. V. & Merz, M. (2023). *Statistical Foundations of Actuarial Learning and its Applications*. Springer. https://doi.org/10.1007/978-3-031-12409-9 — 把精算統計與現代機器學習連結起來的教科書，涵蓋定價與準備金。
- European Union. Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (AI Act). *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj — 具約束力的法條原文；其前言列出用於健康險與人壽險風險評估與定價的 AI 屬於高風險用途。
