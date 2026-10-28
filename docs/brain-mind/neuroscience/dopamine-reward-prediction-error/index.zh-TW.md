---
translation_reviewed: 2026-10-28
related:
- brain-mind/decision-reward
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- reinforcement learning
- decision making
aliases:
  - 多巴胺的獎勵預測誤差
  - Dopamine Reward Prediction Error
  - RPE
---

# 多巴胺的獎勵預測誤差（Schultz, Dayan & Montague, 1997）

多巴胺神經元訊號的是預期獎勵與實得獎勵之間的差異。這正是時序差分強化學習中驅動學習的那個量，也因此這項發現是 AI 與神經科學之間最強的連結之一。

本頁屬於[神經科學基礎](../index.md)。它詳細說明一種方法；多巴胺如何支持決策的完整圖像，見[決策、多巴胺與獎勵](../../decision-reward/index.md)。

## 概述

當你得到一個意外的好事，大腦會學到帶來這件好事的線索是有價值的。當同樣的獎勵變成可預期時，那份驚喜就消失了。多巴胺似乎攜帶的是「驚喜」本身，而不是獎勵。這個單一訊號能解釋獎勵如何塑造行為，並為 AI 中的一條學習規則提供精確的生物學對應。

## 核心概念

- **獎勵預測誤差（reward prediction error）**：實得獎勵減去預測獎勵。正值代表比預期好，負值代表比預期差。
- **相位性多巴胺反應（phasic dopamine response）**：多巴胺神經元短暫的放電增加或下降，與較緩慢的基線變化相對。
- **制約刺激（conditioned stimulus）**：例如燈光或聲音等線索，可靠地預測獎勵。
- **時序差分誤差（temporal-difference error）**：預測誤差在 AI 中的版本，還會用到下一個狀態的預測值。

## 問題

在動物學習獎勵的過程中，中腦多巴胺神經元傳遞的是什麼？早期的看法主要把多巴胺與獎勵本身或動作連結起來。問題在於：它的活動是直接跟隨獎勵，還是跟隨預期與實際結果之間的變化？

## 核心想法

多巴胺神經元對未預期的獎勵有反應，隨著學習進行，反應會移到最早的可靠預測線索上。此型態符合時序差分誤差，即實得獎勵減去預測獎勵。當某個線索已能良好預測獎勵，獎勵本身引起的反應就很小；而預期獎勵缺席時，放電會在獎勵應該出現的時間點下降到基線以下。

作者把此發現呈現為強化學習理論與大腦之間的連結。他們的關鍵一步，是把記錄到的反應與學習演算法應產生的結果相比較，而不只是描述這些反應。

## 方程式或演算法

以現代符號，時序差分誤差為

\(\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)\)

其中 \(r_t\) 為時刻 t 的獎勵，\(V\) 為學得的狀態價值，\(\gamma\) 為折扣因子。學習便是把價值估計朝 \(\delta_t\) 的方向調整。比較連續狀態預測的時序差分形式，出自 Sutton（1988）；把它對應到多巴胺訊號的提議，則來自 Montague、Dayan 與 Sejnowski（1996）。

## 結果

這些記錄是在執行獎勵任務的猴子身上進行的。Schultz、Dayan 與 Montague（1997）報告的主要型態如下：

- 未預期獎勵出現時，多巴胺放電增加。
- 學習後，反應從獎勵移到最早的可靠預測線索上。
- 預期獎勵未出現時，放電在獎勵應該出現的時間點下降到基線以下。

這些型態與上式的預測誤差訊號相符。報告的發現來自數量有限的動物與任務。

## 限制

- **樣本與任務。**記錄來自數量有限的猴子與獎勵任務。推廣到其他物種、任務與腦區，需要後續研究。
- **預測誤差並非全部。**後續研究對多巴胺是否只編碼預測誤差、還是也包含顯著性、新奇性與獎勵資訊，仍有爭論。Schultz（2016）回顧了一種雙成分的看法：先出現一個早期、通用的反應，接著是一個較晚、對誤差具特異性的反應。

## 與其他主題的關聯

- **強化學習**：預測誤差是時序差分學習的核心更新，也是 AI 中許多代理研究的基礎。見[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)。
- **無模型控制**：[有模型與無模型控制](../../decision-reward/model-based-vs-model-free/index.md)中的無模型控制器，正是由這同一訊號更新。
- **決策**：多巴胺如何偏移選擇，以及它與證據累積的互動，見[決策、多巴胺與獎勵](../../decision-reward/index.md)。

## 應用

- **AI 中的強化學習**：時序差分更新被用於遊戲與控制代理，而它與多巴胺的吻合，是神經科學啟發演算法的常見例子。
- **計算精神醫學**：把預測誤差學習模型擬合到行為上，用於研究成癮等狀況。這些是研究工具，並非臨床診斷。

## 開放問題

- **多巴胺只編碼誤差嗎？**有關顯著性與新奇性訊號的報告，使這個問題仍然開放。
- **誤差如何計算？**計算預期價值的迴路，以及它如何傳到多巴胺神經元，仍在研究中。
- **這能推廣到人類學習嗎？**人類影像研究支持相似的角色，但所測得的訊號比單一神經元記錄來得間接。

## 參考文獻

### 開創性論文

- Schultz, W., Dayan, P. & Montague, P. R.（1997）。A Neural Substrate of Prediction and Reward. *Science*。https://doi.org/10.1126/science.275.5306.1593 — 顯示多巴胺神經元發出獎賞預測誤差訊號，將強化學習與大腦連結起來。
- Montague, P. R., Dayan, P. & Sejnowski, T. J.（1996）。A framework for mesencephalic dopamine systems based on predictive Hebbian learning. *Journal of Neuroscience*。https://doi.org/10.1523/JNEUROSCI.16-05-01936.1996 — 提出預測式 Hebb 學習框架，把時序差分學習對應到多巴胺訊號。
- Sutton, R. S.（1988）。Learning to predict by the methods of temporal differences. *Machine Learning*。https://doi.org/10.1007/BF00115009 — 提出時序差分學習，多巴胺訊號所比較的誤差即來自此演算法。

### 綜述與回顧

- Schultz, W.（2016）。Dopamine reward prediction-error signalling: a two-component response. *Nature Reviews Neuroscience*。https://doi.org/10.1038/nrn.2015.26 — 回顧多巴胺神經元中一個早期、通用反應與一個較晚、對誤差具特異性反應的證據。
- Dayan, P. & Daw, N. D.（2008）。Decision theory, reinforcement learning, and the brain. *Cognitive, Affective, & Behavioral Neuroscience*。https://doi.org/10.3758/CABN.8.4.429 — 回顧決策理論與強化學習模型如何與大腦中的選擇相關。
- Sutton, R. S. & Barto, A. G.（2018）。*Reinforcement Learning: An Introduction*, 2nd ed. MIT Press。http://incompleteideas.net/book/the-book-2nd.html — 時序差分學習的標準教科書，也是預測誤差模型背後的演算法。
