---
translation_reviewed: 2026-10-28
related:
  - society/ethics
  - society/governance
  - society/interpretability
aliases:
  - 政府與公共服務
  - Government
  - Public sector AI
---

# 政府與公共服務

政府用 AI 來做決策、規劃與提供公共服務，範圍從福利資格到稅務稽核。由於決策影響權利，而民眾往往無法選擇其他服務提供者，風險特別高。本頁說明**公共機構**使用 AI 的情形。規範 AI 的法律，請見[法律、政策與治理](../../society/governance/index.md)。

## 概況

| 領域 | 例子 |
|---|---|
| 福利與資格 | 標記個案待審，或篩選申請案的系統 |
| 風險評估 | 預測再犯、兒童保護風險或詐欺的工具 |
| 稅務與執法 | 稽核案件的選取，以及申報資料中的異常偵測 |
| 服務提供 | 提供公共資訊、翻譯與表格填寫的聊天機器人 |
| 規劃與基礎建設 | 交通、運輸與資源預測 |
| 文件處理 | 分類與摘要大量來函 |

## 風險集中之處

- **錯誤難以申訴。**錯誤的分數可能拒絕福利或引發調查，因此對決定提出異議的權利很重要。
- **偏見。**以歷史紀錄訓練的模型可能重現過去的歧視，而單一的準確率數字可能掩蓋各群體之間不平等的錯誤率。
- **不透明。**機關往往無法說明系統如何得出決定，大眾也無法檢視。

## 人類與機器決策的證據

機器學習能否改善公共決策，是尚待實證檢驗的問題。一項廣被引用的研究以保釋決定為案例探討這個問題，因此關於準確率的主張，應以真實的決定與結果來檢驗（見參考文獻）。

## 關鍵方法

有三種方法是多數公共機構工具的基礎。每個都連結到解釋它的頁面。

- [評估與驗證](../../theory/paradigms/supervised/evaluation-and-validation/index.md)：如何在模型將影響的人口上測試，而不只看平均準確率。
- [決策樹與集成方法](../../theory/paradigms/supervised/trees-and-ensembles/index.md)：風險評分與詐欺偵測中常見的表格資料模型。
- [大型語言模型](../../theory/models/llm/index.md)：起草與回覆公共來函，但需要人工審閱。

## 連結

- 公共工具中出現的公平性權衡，見[倫理與公平性](../../society/ethics/index.md)。
- 向受影響的人解釋決定，見[可解釋性](../../society/interpretability/index.md)。

## 未解問題

- 在部署會影響福利或人身自由的模型之前，公共機構應需要什麼樣的證據？
- 當理由不對當事人公開時，人們如何對自動化決定提出異議？
- 系統由廠商建置、由公共機構營運時，出了問題由誰負責？

## 參考文獻

### 開創性論文

- Veale, M. & Binns, R. (2017). Fairer machine learning in the real world: Mitigating discrimination without collecting sensitive data. *Big Data & Society* 4(2). https://doi.org/10.1177/2053951717743530 — 探討在不收集敏感屬性的情況下，如何減少機器學習的歧視，這是公共機構常見的處境。
- Kleinberg, J. et al. (2018). Human Decisions and Machine Predictions. *The Quarterly Journal of Economics* 133(1). https://doi.org/10.1093/qje/qjx032 — 以保釋決定為測試案例，探討機器學習能否改善人類的決策。
- Ananny, M. & Crawford, K. (2016). Seeing without knowing: Limitations of the transparency ideal and its application to algorithmic accountability. *New Media & Society* 20(3). https://doi.org/10.1177/1461444816676645 — 主張僅靠透明度，對演算法系統的問責來說是有限的途徑。

### 教科書與綜述

- OECD (2019). *Artificial Intelligence in Society*. OECD Publishing. https://www.oecd.org/en/publications/artificial-intelligence-in-society_eedfee77-en.html — 對 AI 的技術、經濟與政策版圖的綜述，涵蓋公平性、隱私、安全與問責等公共政策議題。

### 文章與文件

- European Union (2024). Regulation (EU) 2024/1689 (Artificial Intelligence Act). *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj — 2024 年 6 月 13 日通過的歐盟 AI 統一規則。
