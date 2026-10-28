# 人力資源與招募

AI 現在出現在僱用流程的許多環節：撰寫職缺廣告、篩選履歷、安排並分析面試、把技能與職位配對，以及監測績效。這些用途都可能影響一個人的生計，因此就業是規範最明確的應用領域之一。

## 概況

| 階段 | 方法 | 說明 |
|---|---|---|
| 人才搜尋與職缺廣告 | 用於草擬與鎖定對象的語言模型 | 用字可能改變誰會來應徵 |
| 履歷篩選 | 關鍵字規則、排序模型、語言模型擷取 | 在數個司法管轄區是規範最嚴格的用途 |
| 技能配對 | 以嵌入向量把個人資料與職位配對 | 取決於技能如何表示 |
| 面試 | 結構化評分、語音與影片分析、逐字稿摘要 | 以影片評分有爭議，也受到廣泛批評 |
| 評估與人力規劃 | 離職模型、績效預測 | 風險在於使用反映過去偏誤的歷史結果 |
| 內部調動與監控 | 推薦培訓與職位；活動追蹤 | 有監控疑慮 |

## 為什麼困難

- **有偏誤的標籤**：以過去的錄用決定訓練的篩選模型，會學到那些決定，包括其中的偏誤。
- **代理變數**：郵遞區號、學校或就業空窗等特徵，可能與受保護的特性相關。
- **不透明**：求職者很少知道是否使用了模型，或為何被淘汰。
- **樣本小**：許多職位的錄用人數太少，無法可靠地衡量結果。

## 關鍵方法

- [監督式學習與評估](../../theory/paradigms/supervised/evaluation-and-validation/index.md)：篩選模型的基礎，並以子群體指標進行檢驗。
- [倫理與公平](../../society/ethics/index.md)：公平性的定義，以及各定義之間的取捨。
- [可解釋性](../../society/interpretability/index.md)：解釋哪些輸入驅動了分數的工具，求職者與監管者都需要這些資訊。
- [大型語言模型](../../theory/models/llm/index.md)：用於履歷解析、草擬與面試摘要，並帶來新的失敗模式，例如捏造資格。

## 相關連結

- 公平性的取捨（機會均等、校準等）見[倫理與公平](../../society/ethics/index.md)。本頁把它們應用到招募。
- 自動化決策工具的規則屬於[法律、政策與治理](../../society/governance/index.md)的範圍。
- 人們如何形成第一印象，以及結構化面試如何改變判斷，是[認知科學](../../brain-mind/cognitive-science/index.md)的研究對象。人類判斷中的捷思與偏誤，是演算法工具被拿來比較的人類基準。

## 應用

- 履歷篩選與排序
- 把應徵者與開放職位配對
- 結構化面試評分與逐字稿分析
- 人力規劃與內部調動

## 風險與限制

- **差別影響**：即使工具從不使用受保護的特性，仍可能使某一受保護群體的淘汰率較高。Raghavan et al.（2020）檢視了招募工具廠商關於偏誤緩解的主張，以及支撐這些主張的證據。
- **自動化偏誤**：即使被要求審查分數，招募人員仍可能傾向於依從分數。
- **法律義務**：在某些地方，雇主在使用前必須對自動化工具進行稽核。紐約市第 144 號地方法（Local Law 144）要求，在使用自動化僱用決策工具之前一年內完成偏誤稽核，執法自 2023 年 7 月 5 日開始（紐約市消費者與勞工保護局）。
- **高風險分類**：歐盟 AI 法把用於招募與篩選的 AI 系統列為高風險用途，須承擔風險管理、資料治理與人類監督等義務（Regulation (EU) 2024/1689）。

## 開放問題

- 對於招募應採用哪一種公平性指標，因為各指標彼此衝突（Kleinberg et al., 2016；Chouldechova, 2017）。
- 偏誤稽核能否偵測到實務上真正重要的問題，還是只能偵測它們所設計要測試的問題。

## 參考文獻

### 開創性論文

- Raghavan, M. et al. (2020). Mitigating bias in algorithmic hiring: Evaluating claims and practices. *FAT\* 2020*. https://doi.org/10.1145/3351095.3372828 — 檢視招募工具廠商關於偏誤緩解的主張，以及他們提出的證據。
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2016). Inherent Trade-Offs in the Fair Determination of Risk Scores. arXiv. https://arxiv.org/abs/1609.05807 — 證明當基礎比率不同時，數種自然的公平性標準無法同時成立。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. arXiv. https://arxiv.org/abs/1610.02413 — 定義以真陽性率相等為基礎的公平性標準，並說明如何以後處理來實現。
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*. https://doi.org/10.1089/big.2016.0047 — 證明當群體的基礎比率不同時，校準與錯誤率平衡無法同時成立。

### 綜述與教科書

- Mehrabi, N. et al. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*. https://doi.org/10.1145/3457607 — 綜述偏誤的來源，以及機器學習中使用的公平性定義與緩解方法。

### 文章與文件

- European Union. Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (AI Act). *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj — 具約束力的法條原文，把招募與篩選用 AI 列為高風險。
- New York City Department of Consumer and Worker Protection. Automated employment decision tools. https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page — 關於第 144 號地方法偏誤稽核要求的官方說明。
