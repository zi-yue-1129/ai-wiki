---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - security
  - model theft
  - APIs
aliases:
  - Model Extraction
  - Model Stealing
  - Model Theft
  - 模型萃取
  - 模型竊取
---

# 模型萃取與竊取

模型萃取（model extraction）是一種攻擊：只能查詢模型的人，從回答中重建出其行為的副本，或其內部的一部分。這個副本可能與原模型競爭、洩露機密的設計選擇，或成為其他攻擊的基礎。對於透過公開 API 部署的模型，風險最高。

本頁是[LLM 應用安全](index.zh-TW.md)的一部分。它關心的是模型本身。復原訓練資料的隱私風險，見[訓練資料萃取](../../society/privacy/training-data-extraction.zh-TW.md)。

## 概述

透過 API 提供的模型，每一次回答都會揭露其功能。攻擊者若送出足夠多的查詢並記錄輸出，就能訓練第二個模型來模仿第一個。此方法與知識蒸餾密切相關；知識蒸餾是壓縮模型的正當方法。兩者的差別在於，教師模型的擁有者是否同意。

## 關鍵概念

- **受害模型：**被複製行為的已部署模型。
- **查詢存取：**攻擊者能送入輸入並看到輸出，但看不到權重。
- **替代模型：**依據受害模型的回答所訓練出來的副本。
- **功能竊取：**複製模型的作用，而不複製其權重。
- **參數復原：**從輸出中復原模型內部結構的一部分。

## 運作方式

基本程序分三步。攻擊者選擇輸入，通常取自相關的公開資料集。攻擊者記錄受害模型的輸出，例如標籤或機率。攻擊者以輸入輸出配對訓練替代模型。之後，替代模型就能在新的輸入上近似受害模型。

Tramèr 等人（2016）描述了透過預測 API 萃取機器學習模型的方法。Orekondy 等人（2019）顯示，僅能以黑箱方式存取的攻擊者，可以用自己挑選的自然影像竊取影像分類器的功能。Krishna 等人（2020）研究對 BERT 系列 API 的萃取，攻擊者只靠查詢存取即可重建本地副本。Carlini 等人（2024）展示另一種攻擊：在典型的 API 存取下，他們復原了正式運作中語言模型的嵌入投影層（至對稱性為止），並報告攻擊成本低於二十美元。Hinton 等人（2015）提出了蒸餾，即以較大模型的輸出訓練較小模型，這正是許多同類機制的基礎。

## 限制

- **不完美的副本。**替代模型通常能近似受害模型在常見輸入上的行為，但在罕見輸入上會失敗。
- **防禦與效用相互取捨。**速率限制、輸出四捨五入與輸出擾動能降低萃取，但也會降低 API 的價值。
- **證據多來自較小的情境。**許多萃取結果來自分類器或特定的模型家族，而隨著前沿模型的規模與存取方式改變，其成本也會改變。

## 防禦

常見的措施包括速率限制與對查詢模式的異常偵測、降低輸出的細節、為輸出加上浮水印以便追蹤副本（見[模型輸出浮水印](watermarking.zh-TW.md)），以及禁止以輸出訓練模型的合約條款。沒有任何措施是完整的，選擇取決於輸出需要揭露多少。

## 關聯

- 模型輸出的隱私面向，包括復原訓練資料，見[訓練資料萃取](../../society/privacy/training-data-extraction.zh-TW.md)。
- 成員推論（判斷某筆紀錄是否在訓練資料中）見[成員推論](../../society/privacy/membership-inference.zh-TW.md)。
- 對建立在模型上之應用程式的威脅，見[LLM 應用安全](index.zh-TW.md)。

## 應用

- 在不同查詢預算下，稽核已部署 API 的行為外洩情況。
- 利用浮水印追蹤被複製的輸出。

## 開放問題

- 在給定的查詢預算下，前沿模型的行為有多少可以被複製？
- 哪些防禦能在保持 API 有用的同時，提高萃取的成本？

## 參考文獻

### 開創性論文

- Tramèr, F. 等人（2016）。*Stealing Machine Learning Models via Prediction APIs*。arXiv。https://arxiv.org/abs/1609.02943 — 顯示透過預測 API 提供的模型，可以從其回答中被萃取。
- Orekondy, T.、Schiele, B. 與 Fritz, M.（2019）。*Knockoff Nets: Stealing Functionality of Black-Box Models*。CVPR。https://arxiv.org/abs/1812.02766 — 以攻擊者挑選的自然影像，竊取黑箱影像分類器的功能。
- Krishna, K. 等人（2020）。*Thieves on Sesame Street! Model Extraction of BERT-based APIs*。ICLR。https://arxiv.org/abs/1910.12366 — 僅以查詢存取，重建基於 BERT 之 API 的本地副本。
- Carlini, N. 等人（2024）。*Stealing Part of a Production Language Model*。ICML。https://arxiv.org/abs/2403.06634 — 以少量成本復原正式運作中語言模型的嵌入投影層。
- Hinton, G.、Vinyals, O. 與 Dean, J.（2015）。*Distilling the Knowledge in a Neural Network*。arXiv。https://arxiv.org/abs/1503.02531 — 提出蒸餾，即以較大模型的輸出訓練較小模型。
