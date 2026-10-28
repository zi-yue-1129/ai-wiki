---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai
  - start/history
tags:
  - history
  - symbolic AI
  - perceptron
aliases:
  - 符號時代
  - 達特茅斯會議
  - 符號 AI 時期
  - Symbolic era
---

# 歷史：達特茅斯與符號時代（1956–1974）

人工智慧領域在 1950 年代中期成形。研究者提出，推理可以寫成符號的操作，而機器也可以被設計來學習。最初的二十年產生了令人矚目的程式，也引來一陣樂觀情緒，同時出現了關於簡單學習機器能計算什麼、不能計算什麼的早期辯論。本頁涵蓋這段時期，它結束於[下一章](../expert-systems-and-winters/index.zh-TW.md)所討論的經費削減。

## 概述

「人工智慧」（artificial intelligence）這個名稱，出現在 1955 年為達特茅斯學院夏季研究計畫所寫的提案中。提案表示，研究的基礎是這樣一個猜想：學習的每個面向或智能的任何其他特徵，原則上都可以被精確描述，因而可以建造機器來模擬它 [(McCarthy et al., 1955)](http://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html)。研討會於 1956 年舉行，聚集了之後二十年塑造這個領域的研究者。

## 關鍵概念

- **符號 AI**：認為智能可以由符號、規則與狀態空間搜尋建構的觀點。見[符號 AI](../../../theory/paradigms/symbolic-ai/index.zh-TW.md)。
- **物理符號系統**：Newell 與 Simon 用來描述的系統，它操作符號以產生智能行為。
- **啟發式搜尋**：用經驗法則引導在大量可能性中的搜尋。
- **感知器**：一種單層學習機器，依據標記的範例調整權重。

## 早期程式與符號假說

Newell 與 Simon 的程式，包括 Logic Theorist 與 General Problem Solver，是最早展示機器執行人類所稱推理工作的例子之一。Newell 與 Simon 之後把他們的方法闡述為電腦科學的經驗研究，主張符號系統與啟發式搜尋是智能的基礎 [(Newell and Simon, 1976)](https://doi.org/10.1145/360018.360022)。這個觀點主導了二十年的研究，後來分類中「符號」一詞也由此而來。

## 感知器

Rosenblatt 把感知器介紹為資訊如何在大腦中儲存的機率模型。它的學習規則依據範例調整連結權重，並為「機器可以從資料而非人工撰寫的規則中學習分類」提供了早期證據 [(Rosenblatt, 1958)](https://doi.org/10.1037/h0042519)。感知器是[機器學習](../../../theory/machine-learning/index.zh-TW.md)中統計學習，與 1980 年代回歸的神經模型之間最早的交會點之一。

## 批評

1969 年，Minsky 與 Papert 分析了單層感知器的限制，指出它們無法計算某些函數，例如互斥或。這本書常被解讀為降低了人們對神經網路的興趣，但其分析適用的是單層網路，而非之後被證明可以訓練的多層網路 [(Minsky and Papert, 1969)](https://doi.org/10.7551/mitpress/4943.003.0015)。這次批評是一個範例：一項限制可以被正確陳述，卻仍被誤讀為對整個模型家族的判決。

## 最初的樂觀

早期的程式帶來了充滿信心的氛圍。研究者預期一代之內就能出現通用的機器智能。隨著程式在狹窄領域之外遇到困難，這個預期受到了考驗。玩具世界中的示範，與能在真實世界運作的系統之間的落差，是 AI 歷史中反覆出現的主題。

## 與其他頁面的關聯

符號計畫提出了許多問題，[符號 AI](../../../theory/paradigms/symbolic-ai/index.zh-TW.md)的相關頁面至今仍在回答。感知器與後續章節中的[深度學習](../../../theory/deep-learning/index.zh-TW.md)歷史相連。完整時間軸見 [AI 發展史](../index.zh-TW.md)總覽。

## 應用

這一時期的方法被應用於定理證明、遊戲、解謎與早期的語言任務。這些應用為後來的專家系統與規劃軟體打下基礎。

## 開放問題

- 為什麼對符號推理的早期樂觀，超出了當時方法所能達成的範圍？
- 感知器的批評，有多少是針對模型本身，又有多少是針對它被呈現的方式？
- 當前關於推理系統的研究，正在重新檢視哪些早期想法？

## 參考文獻

### 重要論文

- McCarthy、Minsky、Rochester 與 Shannon，*A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence*（1955）。http://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html — 提出「人工智慧」一詞並闡述其猜想的提案。
- Rosenblatt，*The perceptron: A probabilistic model for information storage and organization in the brain*，Psychological Review（1958）。https://doi.org/10.1037/h0042519 — 感知器學習機器的奠基論文。
- Newell 與 Simon，*Computer science as empirical inquiry: symbols and search*，Communications of the ACM（1976）。https://doi.org/10.1145/360018.360022 — 提出物理符號系統假說與啟發式搜尋的角色。
- Minsky 與 Papert，*Perceptrons: An Introduction to Computational Geometry*（1969；1988 年擴充版），MIT Press。https://doi.org/10.7551/mitpress/4943.003.0015 — 分析單層感知器的限制。連結指向 1988 年版的導論章節。

### 綜述與教科書

- Lighthill，*Artificial Intelligence: A General Survey*，Science Research Council（1972）。https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm — 對 AI 進展的批判性綜述，報告的日期為 1972 年，1973 年出版。詳見[下一章](../expert-systems-and-winters/index.zh-TW.md)。
