# 金融

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 詐欺偵測 | 梯度提升樹、交易網路上的圖神經網路、異常偵測 | 最古老、也最成功的機器學習應用之一 |
| 信用評分與核保 | 邏輯迴歸、提升法；替代資料 | 受法規規範；不利決定必須附上理由 |
| 反洗錢（AML）／KYC | 網路分析、實體解析、文件 AI | 誤報率高是主要成本 |
| 演算法與量化交易 | 統計套利、機器學習訊號、用於下單執行的強化學習 | 訊噪比低；過度擬合與市場狀態改變是主要問題 |
| 造市與交易執行 | 最佳執行、強化學習、市場微結構模型 | |
| 風險管理 | 壓力測試、VaR 模型、情境生成 | 模型風險管理（美國的 SR 11-7） |
| 客戶服務與理財建議 | 聊天機器人、機器人理財（robo-advisor）、供理專使用的 LLM 副駕駛 | 適合性與揭露規則仍然適用 |
| 文件處理 | 財報電話會議、申報文件、合約、保險理賠 | LLM 已廣泛採用 |
| 保險 | 定價、理賠分流、車聯網駕駛資料 | 公平性與歧視疑慮 |

## 為什麼金融對機器學習特別困難

- **非平穩性**：市場會適應，關係隨之改變——包括適應模型本身
- **訊噪比低**：可預測的成分微小
- **回測過度擬合**：測試大量策略，必然會有一些因為運氣而看起來很好（Bailey & López de Prado, 2014）
- **對抗者**：詐欺者會適應偵測器
- **可解釋性要求**：例如美國《平等信用機會法》要求對不利決定發出通知；歐盟 AI 法把信用評估列為高風險

## 金融領域的 LLM

- BloombergGPT（Wu et al., 2023）是專為金融設計的 LLM。
- 用途：摘要申報文件與電話會議、研究助理、量化分析師的程式碼、法遵審查、客服
- 風險：數字幻覺、資料洩漏，以及許多機構使用相似模型時產生的羊群效應

## 系統性風險

大量使用相似的模型與供應商，可能提高相關性、順循環性與集中風險，而自動化策略在閃崩情境中可能相互作用。

## 關鍵方法

下列三種方法與本頁最相關。每一項都連結到解釋該方法的頁面。

- [圖神經網路](../../theory/models/gnn/message-passing/index.md)：在交易網路上做訊息傳遞，用於標記可疑帳戶（Weber et al., 2019）。
- [異常偵測](../../theory/paradigms/unsupervised/anomaly-detection/index.md)：學習正常活動並標出偏離的模型，用於詐欺偵測。
- [線上學習](../../theory/paradigms/online/index.md)：隨資料到來而更新的模型，因應市場的非平穩性。

## 參考文獻

### 開創性論文

- Weber et al. (2019). Anti-Money Laundering in Bitcoin: Experimenting with Graph Convolutional Networks for Financial Forensics. arXiv. https://arxiv.org/abs/1908.02591 — 以圖卷積網路偵測比特幣中的非法交易。
- Chen & Guestrin (2016). XGBoost: A Scalable Tree Boosting System. arXiv. https://arxiv.org/abs/1603.02754 — 梯度提升樹，是詐欺與信用模型常用的方法。
- Wu et al. (2023). BloombergGPT: A Large Language Model for Finance. arXiv. https://arxiv.org/abs/2303.17564 — 專為金融設計的大型語言模型，在金融與一般資料上訓練。
- Bailey & López de Prado (2014). The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality. *The Journal of Portfolio Management*. https://doi.org/10.3905/jpm.2014.40.5.094 — 依測試過的策略數量調整夏普比率。

### 綜述與教科書

- Dixon, Halperin & Bilokon (2020). *Machine Learning in Finance*. Springer. https://doi.org/10.1007/978-3-030-41068-1 — 金融中機器學習方法的教科書。
