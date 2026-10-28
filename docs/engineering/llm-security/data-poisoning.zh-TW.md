---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - security
  - training data
  - backdoors
aliases:
  - Data Poisoning
  - Backdoor Attacks
  - 資料投毒
  - 後門攻擊
---

# 資料投毒與後門攻擊

資料投毒（data poisoning）是把惡意樣本放入模型的訓練資料，使模型在測試時表現出攻擊者所要的行為。後門（backdoor）則是一種投毒攻擊，其行為只在輸入中出現特定模式時才被觸發，因此模型在其他情況下看起來正常。由於網路爬取資料大規模使用，攻擊面很大，也難以稽核。

本頁是[LLM 應用安全](index.zh-TW.md)的一部分。

## 概述

現代模型的訓練資料來自許多來源，其中大部分不會逐筆檢查。因此，能發布會被爬取之內容的攻擊者，就能影響模型學到的東西。結果可能是一個對某個特定片語照單全收的分類器、一個提出不安全程式寫法的程式模型，或是一個平時正常、直到觸發條件出現才異常的模型。

## 關鍵概念

- **投毒：**新增或更改訓練樣本，以改變模型的行為。
- **後門：**由輸入中的觸發條件啟動的隱藏行為。
- **乾淨標籤攻擊：**被投毒的樣本，其標籤在人類審查者看來是正確的。
- **定向與非定向：**攻擊是針對單一輸入，還是針對整體效能。
- **網路規模投毒：**把內容放在資料集爬蟲會收集的位置上的攻擊。

## 運作方式

以觸發條件為基礎的後門，最先是在影像模型中被展示的。Gu 等人（2017）展示，在訓練資料中帶有觸發圖樣（例如一小塊貼片）的模型，可以被植入後門，並指出外包訓練的風險。Chen 等人（2017）把以資料投毒為基礎的定向後門攻擊，應用於臉部辨識這類安全關鍵的系統。Shafahi 等人（2018）提出乾淨標籤投毒，被投毒的樣本保持正確標籤，卻仍能改變模型對某一目標輸入的預測。

對語言模型而言，Wallace 等人（2021）研究隱蔽投毒：對訓練資料做少量改動，使攻擊者能在出現某個觸發片語時控制預測，而這些改動很難被察覺。Carlini 等人（2023）顯示，對網路規模的訓練資料集進行投毒是可行的，即把內容放在爬蟲會收集的地方；他們針對一組熱門資料集展示了這點。

## 限制

- **難以偵測。**被植入後門的模型可以通過一般測試，因為觸發條件在正常輸入中很少出現。
- **取決於資料佔比。**效果取決於攻擊者控制的資料比例，以及訓練的執行方式。
- **證據因情境而異。**許多結果來自影像或受控的文字任務，這些攻擊在大型語言模型上的遷移並不一致。

## 防禦

防禦包括控制資料來源、去除重複並過濾訓練語料、偵測離群樣本、以多樣的觸發條件測試模型，以及在訓練後稽核模型。這些防禦都不完整，因此資料來源與清楚的訓練來源紀錄，是第一道防線。訓練資料的隱私面向，見[訓練資料萃取](../../society/privacy/training-data-extraction.zh-TW.md)。

## 關聯

- 成員推論所涉及的風險，見[成員推論](../../society/privacy/membership-inference.zh-TW.md)。
- 版權與訓練資料（包括記憶化），見[版權與 AI](../../society/copyright/index.zh-TW.md)。
- 對模型應用程式的威脅，見[LLM 應用安全](index.zh-TW.md)。

## 應用

- 在部署前，為分類器或程式助理檢查是否有觸發條件。
- 以來源檢查來挑選訓練語料的來源。

## 開放問題

- 在不知道觸發條件的情況下，能否偵測已訓練模型中的投毒？
- 需要多少乾淨資料，才能稀釋被投毒的部分？

## 參考文獻

### 開創性論文

- Gu, T.、Dolan-Gavitt, B. 與 Garg, S.（2017）。*BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain*。arXiv。https://arxiv.org/abs/1708.06733 — 顯示以帶觸發圖樣的資料訓練的模型可被植入後門，並提出外包訓練的風險。
- Chen, X. 等人（2017）。*Targeted Backdoor Attacks on Deep Learning Systems Using Data Poisoning*。arXiv。https://arxiv.org/abs/1712.05526 — 把定向後門投毒應用於臉部辨識等安全關鍵系統。
- Shafahi, A. 等人（2018）。*Poison Frogs! Targeted Clean-Label Poisoning Attacks on Neural Networks*。arXiv。https://arxiv.org/abs/1804.00792 — 提出乾淨標籤投毒，被投毒樣本保持正確標籤。
- Wallace, E. 等人（2021）。*Concealed Data Poisoning Attacks on NLP Models*。NAACL。https://arxiv.org/abs/2010.12563 — 顯示對語言模型的隱蔽投毒，由觸發片語控制預測。
- Carlini, N. 等人（2023）。*Poisoning Web-Scale Training Datasets is Practical*。arXiv。https://arxiv.org/abs/2302.10149 — 顯示網路規模資料集可以在實務上被投毒，即把內容放在爬蟲會收集的地方。
