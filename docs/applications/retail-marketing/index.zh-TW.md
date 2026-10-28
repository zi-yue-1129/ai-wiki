---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/online/contextual-bandits
  - theory/paradigms/supervised/trees-and-ensembles
  - society/ethics
aliases:
  - 零售、行銷與電子商務
  - Retail
  - E-commerce
---

# 零售、行銷與電子商務

零售是最早以大規模機器學習分析顧客資料的產業之一。推薦、需求預測、定價與廣告，如今塑造了大多數線上購物，而生成式工具也開始撰寫商品描述與行銷內容。本頁說明 AI 在銷售與行銷產品及服務中的應用。

## 概況

| 領域 | 例子 |
|---|---|
| 推薦 | 依瀏覽與購買紀錄推薦商品 |
| 需求預測 | 預測銷量，用以規劃庫存與物流 |
| 定價與促銷 | 設定價格與折扣，有時採動態調整 |
| 顧客留存 | 預測哪些顧客可能流失 |
| 廣告 | 決定把哪支廣告展示給哪位使用者 |
| 內容生成 | 起草商品描述、電子郵件與行銷文案 |

## 推薦與需求

以項目為基礎的協同過濾是早期且廣泛使用的方法。它從使用者評分矩陣中找出項目之間的關係，再推薦與顧客已喜歡的項目相關的商品（Sarwar 等人，2001）。亞馬遜的項目對項目系統是知名的產業案例（Linden 等人，2003）。Ferreira 等人（2016）分析了某線上零售商的需求預測與價格最佳化。

## 顧客流失

預測哪些顧客會離開，是標準的監督式學習問題。裝袋與提升分類樹是其中一組用於此問題的方法（Lemmens & Croux，2006）。留存優惠接著需要鎖定對象，這使預測與「誰能拿到折扣」的決策相連。

## 服務與生成式 AI

Huang & Rust（2018）討論 AI 如何改變服務工作。生成式工具現在產出許多行銷文案，這引發了品牌語氣、揭露與品質控管的問題。

## 關鍵方法

有三種方法最為相關。每個都連結到解釋它的頁面。

- [決策樹與集成方法](../../theory/paradigms/supervised/trees-and-ensembles/index.md)：顧客流失預測與許多預測系統背後的模型。
- [情境式強盜](../../theory/paradigms/online/contextual-bandits/index.md)：選擇要展示哪個優惠或廣告，並隨結果即時學習。
- [評估與驗證](../../theory/paradigms/supervised/evaluation-and-validation/index.md)：透過對照實驗，檢驗推薦或價格調整是否真的提高銷量。

## 風險

- **操弄。**個人化定價與推力設計可能利用顧客，各國對揭露的規定也不同。
- **隱私。**行為資料是這些系統的核心，因此同意與保存政策很重要。
- **回饋循環。**推薦可能縮小顧客看到的內容範圍，減少探索。

公平性與消費者保護的議題見[倫理與公平性](../../society/ethics/index.md)。

## 未解問題

- 推薦帶來的銷量成長，有多少是系統造成的，而不是原本就會購買的顧客？
- 個人化定價應如何揭露與限制？
- 無力建置同等資料系統的小型零售商會怎樣？

## 參考文獻

### 開創性論文

- Sarwar, B. et al. (2001). Item-based Collaborative Filtering Recommendation Algorithms. *WWW10*. https://archives.iw3c2.org/www10/cdrom/papers/519/sdm2.html — 以項目對項目的方法，從使用者評分矩陣找出項目之間的關係，進而產生推薦。
- Linden, G., Smith, B. & York, J. (2003). Amazon.com recommendations: item-to-item collaborative filtering. *IEEE Internet Computing*. https://doi.org/10.1109/MIC.2003.1167344 — 描述亞馬遜網站所用的項目對項目推薦方法。
- Ferreira, K. J., Lee, B. H. A. & Simchi-Levi, D. (2016). Analytics for an Online Retailer: Demand Forecasting and Price Optimization. *Manufacturing & Service Operations Management* 18(1). https://doi.org/10.1287/msom.2015.0561 — 線上零售商的需求預測與價格最佳化。
- Lemmens, A. & Croux, C. (2006). Bagging and Boosting Classification Trees to Predict Churn. *Journal of Marketing Research* 43(2). https://doi.org/10.1509/jmkr.43.2.276 — 以裝袋與提升分類樹預測顧客流失。

### 教科書與綜述

- Huang, M.-H. & Rust, R. T. (2018). Artificial Intelligence in Service. *Journal of Service Research* 21(2). https://doi.org/10.1177/1094670517752459 — 討論 AI 如何改變服務工作與服務業。
