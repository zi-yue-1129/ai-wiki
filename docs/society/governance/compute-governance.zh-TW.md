---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/governance
  - society/safety-alignment
  - theory/evaluation
tags:
  - compute
  - export controls
  - AI governance
aliases:
  - 算力治理
  - 運算治理
  - 出口管制
  - Export controls
---

# 算力治理與出口管制

算力治理把用於訓練與執行 AI 系統的運算能力，視為政策可以介入的環節。由於晶片、資料中心與訓練任務都是實體的、高度集中而且可以計量的，各國政府已開始把它們當作槓桿。本頁說明算力作為槓桿的理由、出口管制與法規門檻如何運用它，以及批評者的主要論點。

## 概述

訓練前沿模型需要大量運算能力，而這些能力由少數晶片設計商、晶圓代工廠與設備製造商提供。Sastry 等人主張，算力是 AI 治理的重要介入點，因為它具有三項特性。它是**可偵測的**，大型運算叢集很顯眼；它是**可排除的**，可以限制某些行為者取得而其他人不受限制；它也是**可量化的**，因此法規可以直接引用一個數字 [(Sastry et al., 2024)](https://arxiv.org/abs/2402.08797)。

## 關鍵概念

- **運算量（compute）**：電腦執行的算術運算次數，通常以浮點運算次數（FLOP）計算。訓練運算量是訓練一個模型所用的總量。
- **出口管制**：政府限制向特定國家或實體出售或轉讓先進晶片、晶片製造設備或模型權重。
- **運算門檻**：超過某個 FLOP 數值後會產生法律義務的界線，例如安全評估或通報義務。
- **運算的客戶審查（KYC）**：檢查誰正在租用大量運算能力，例如向雲端服務商租用。

## 運作方式

政府在供應鏈的數個環節對運算施加影響。出口管制限制誰能購買先進晶片與製造它們的設備。法規設定門檻，讓最大規模的訓練任務承擔更多義務。有些提案要求雲端服務商驗證租用大型叢集的客戶身分。

使用門檻的理由是，最有能力的模型訓練成本很高，因此以運算量為界線，可以只針對少數開發者，而不必管制每一個系統。Sastry 等人也提醒，範圍設定不當的運算規則可能影響隱私、經濟活動與權力集中，因此門檻的設計與門檻本身同樣重要 [(Sastry et al., 2024)](https://arxiv.org/abs/2402.08797)。

## 法規門檻

歐盟 AI 法規為通用 AI 模型設定義務。當模型的累積訓練運算量超過 10^25 次浮點運算時，會被推定具有系統性風險，此類模型須承擔額外義務，例如評估與事件通報 [(Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)。這個門檻只是代理指標：它計算的是運算量，並不直接衡量能力或風險。

政策文獻中的前沿 AI 提案採用類似的邏輯。Anderljung 等人描述了一種前沿 AI 法規，要求最有能力模型的開發者管理新興風險，並可採用註冊、評估與安全標準等工具 [(Anderljung et al., 2023)](https://arxiv.org/abs/2307.03718)。Shevlane 等人主張，危險能力評估應在部署前進行，這是任何以門檻為基礎的制度能發揮作用的前提 [(Shevlane et al., 2023)](https://arxiv.org/abs/2305.15324)。

## 出口管制

自 2022 年起，美國限制向部分國家出口先進運算晶片與晶片製造工具，並且多次調整這些限制的範圍。其宣示的目標結合了國家安全，以及減緩最強大系統擴散的考量。運算趨勢的數據顯示，機器學習所用的運算量成長得多快，這也是許多政策制定者把前沿視為移動目標的原因 [(Sevilla et al., 2022)](https://arxiv.org/abs/2202.05924)。

## 批評

批評者指出幾項問題。隨著效率提升，運算門檻可能過時，同樣的能力未來可能只需要更少的運算量。出口管制可能把開發推向其他供應商，或推向規模更小、較不顯眼的叢集。運算規則也較少觸及資料、演算法或系統的部署方式，因此無法取代安全評估。最後，以運算為治理的核心，可能使影響力集中在掌握晶片與雲端容量的少數企業手中。

## 與其他頁面的關聯

算力治理與[AI 安全與對齊](../safety-alignment/index.md)的安全討論相連，與[評估](../../theory/evaluation/index.md)中的評估方法相連，也與[環境影響](../environment/index.md)中的能源議題相連。其法律背景見[法律、政策與治理](index.md)。

## 應用

出口管制由貿易主管機關執行；門檻則由監管機構套用到模型開發者身上。雲端服務商在銷售大量運算容量時進行客戶檢查。研究團體也用同樣的計數邏輯估算訓練任務的規模，讓外部觀察者得以比較各系統。

## 開放問題

- 隨著演算法效率提升，運算門檻還能不能作為有效的信號？
- 能否在不進行侵入式監控的前提下，可靠地驗證運算的使用？
- 管制應如何在安全目標與其他國家的研究者和企業的取用權之間取得平衡？
- 治理是否應從「用了多少運算」轉向「模型能做什麼」的評估？

## 參考文獻

### 重要論文

- Sastry、Heim、Belfield、Anderljung、Brundage、Hazell、O'Keefe、Hadfield、Ngo、Pilz、Gor、Bluemke、Shoker、Egan、Trager、Avin、Weller、Bengio 與 Coyle，*Computing Power and the Governance of Artificial Intelligence*（2024）。https://arxiv.org/abs/2402.08797 — 主張算力是 AI 治理的重要槓桿，並討論其風險。
- Shevlane、Farquhar、Garfinkel、Phuong、Whittlestone、Leung、Kokotajlo、Marchal、Anderljung、Kolt、Ho、Siddarth、Avin、Hawkins、Kim、Gabriel、Bolina、Clark、Bengio、Christiano 與 Dafoe，*Model evaluation for extreme risks*（2023）。https://arxiv.org/abs/2305.15324 — 提出以危險能力評估作為監督基礎。
- Anderljung、Barnhart、Korinek、Leung、O'Keefe、Whittlestone、Avin、Brundage 等人，*Frontier AI Regulation: Managing Emerging Risks to Public Safety*（2023）。https://arxiv.org/abs/2307.03718 — 提出前沿模型的法規架構。
- Sevilla、Heim、Ho、Besiroglu、Hobbhahn 與 Villalobos，*Compute Trends Across Three Eras of Machine Learning*（2022）。https://arxiv.org/abs/2202.05924 — 量測機器學習歷史上訓練運算量的成長。

### 文章與文件

- 歐盟，*Regulation (EU) 2024/1689 (Artificial Intelligence Act)*，歐盟官方公報（2024）。https://eur-lex.europa.eu/eli/reg/2024/1689/oj — 為通用 AI 模型設定以運算量為基礎的系統性風險推定。
