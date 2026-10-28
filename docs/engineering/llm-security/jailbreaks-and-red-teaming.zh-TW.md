---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - security
  - safety
  - red teaming
aliases:
  - Jailbreaks
  - Red Teaming
  - 越獄
  - 紅隊測試
---

# 越獄與紅隊測試

越獄（jailbreak）是一種輸入，會讓語言模型產生其安全訓練原本要阻止的輸出。紅隊測試（red-teaming）則是在系統發布前，由人或其他模型系統性地尋找這類失敗。兩者關係密切：紅隊測試找出越獄，而每個越獄又會啟發新的測試。

本頁是[LLM 應用安全](index.zh-TW.md)的一部分。同一問題的對齊面向，見[安全與對齊](../../society/safety-alignment/index.zh-TW.md)。

## 概述

安全訓練教導模型拒絕某些請求。越獄則找到繞過拒絕的方法，例如把請求包裝成故事、以不尋常的格式下指令，或加入一段讓模型視為允許回應之提示的文字。與劫持應用程式的提示注入不同，越獄通常是要讓模型本身產生有害的輸出。

## 關鍵概念

- **越獄：**經過設計、用以繞過模型拒絕行為的輸入。
- **紅隊測試：**有系統地嘗試讓系統失敗，以便在使用者之前找出危害。
- **攻擊成功率：**產生被禁止之輸出的嘗試比例。
- **遷移性：**對某一模型有效的攻擊，是否也對另一模型有效。
- **自動化紅隊測試：**由模型產生測試輸入，再由分類器或人員判斷輸出。

## 運作方式

文獻中反覆出現三類方法。人工越獄由人撰寫並以非正式方式分享，隨著模型更新而迅速改變。最佳化攻擊會搜尋一段文字後綴，使目標模型服從；Zou 等人（2023）顯示，在開放模型上找到的後綴可以遷移到其他模型，見[通用對抗後綴](universal-adversarial-suffixes.zh-TW.md)。模型驅動的攻擊由一個攻擊模型提出提示，並依據目標的回應加以改寫；Chao 等人（2023）報告能在二十次查詢內越獄黑箱模型。

紅隊測試採用相同的構想。Perez 等人（2022）以語言模型大規模產生測試問題，並衡量它們引出的有害回覆。Ganguli 等人（2022）描述了大規模的人工紅隊測試、危害的衡量方式，以及從中得出的經驗。

## 限制

- **證據不完整。**攻擊失敗並不表示模型安全，只表示該次攻擊未能成功。
- **攻擊會適應。**針對已知越獄調校的防禦，可能被新的措辭繞過。
- **衡量困難。**判斷輸出是否有害需要評分準則，而評審之間的分歧相當常見。
- **安全訓練並非完整解釋。**Wei 等人（2023）分析安全訓練如何可能失敗。

## 防禦

沒有單一防禦能涵蓋所有越獄。實務系統會結合更強的模型訓練、對輸入與輸出的系統層檢查（見[護欄與輸出過濾](guardrails.zh-TW.md)）、對模型輸出能產生之作用的限制，以及隨模型與攻擊演變而定期進行的紅隊測試。注入指令的應用層風險，見[間接提示注入](indirect-prompt-injection.zh-TW.md)。

## 關聯

- 以模型層訓練達成無害性，見[安全與對齊](../../society/safety-alignment/index.zh-TW.md)。
- 對應用程式最重要的威脅，見[LLM 應用安全](index.zh-TW.md)。
- 安全基準的評估實務，見[評估與基準](../evaluation/index.zh-TW.md)。

## 應用

- 聊天與代理系統發布前的安全測試。
- 每次模型更新後，以已知越獄進行的回歸測試。

## 開放問題

- 紅隊測試能否給出剩餘風險的上界，而不只是找到的失敗數量？
- 新越獄的揭露應如何處理？

## 參考文獻

### 開創性論文

- Zou, A. 等人（2023）。*Universal and Transferable Adversarial Attacks on Aligned Language Models*。arXiv。https://arxiv.org/abs/2307.15043 — 顯示自動找到的後綴能使對齊模型服從有害請求，且能跨模型遷移。
- Chao, P. 等人（2023）。*Jailbreaking Black Box Large Language Models in Twenty Queries*。arXiv。https://arxiv.org/abs/2310.08419 — 以攻擊模型在少量查詢內改進針對黑箱目標的越獄提示。
- Perez, E. 等人（2022）。*Red Teaming Language Models with Language Models*。arXiv。https://arxiv.org/abs/2202.03286 — 以語言模型產生紅隊測試案例，並衡量它們引出的有害回覆。
- Ganguli, D. 等人（2022）。*Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned*。arXiv。https://arxiv.org/abs/2209.07858 — 描述大規模的人工紅隊測試、危害衡量與減少危害的經驗。
- Wei, A.、Haghtalab, N. 與 Steinhardt, J.（2023）。*Jailbroken: How Does LLM Safety Training Fail?*。arXiv。https://arxiv.org/abs/2307.02483 — 分析安全訓練在面對越獄攻擊時如何失敗。
