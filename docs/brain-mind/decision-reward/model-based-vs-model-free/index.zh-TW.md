---
translation_reviewed: 2026-10-28
related:
- theory/paradigms/reinforcement-learning
- brain-mind/neuroscience
tags:
- reinforcement learning
- decision making
aliases:
  - 有模型與無模型控制
  - 模型基礎與模型自由
  - Model-Based vs Model-Free
  - Model-Free Reinforcement Learning
---

# 有模型與無模型控制

有模型與無模型控制是代理人從經驗中選擇行動的兩種方式。無模型控制器直接從過去的獎勵中學習每個行動的好壞。有模型控制器則學習世界如何運作，並用這個模型進行規劃。這個區分來自強化學習，神經科學則借用它來探問大腦依賴哪一種、以及何時依賴哪一種。

本頁是[決策、多巴胺與獎勵](../index.md)的子頁。上層頁面提供概述，本頁說明這個區分，以及 Daw、Niv 與 Dayan（2005）的仲裁提案。

## 概述

以一個例子來說：道路封閉後選擇上班的路線。無模型的習慣說「上次走左邊沒問題，所以走左邊」。有模型的規劃說「左邊封閉，所以走右邊」，它用到了對路網的知識。習慣便宜又快；規劃能立即適應變化，但需要更多運算與時間。

## 核心概念

- **無模型價值（model-free value）**：從行動之後得到的獎勵學來的行動好壞估計。更新時使用獎勵預測誤差，即實際獲得的獎勵與預期獎勵之差。
- **有模型價值（model-based value）**：在學得的轉移模型（什麼導致什麼）與獎勵模型（每個結果值多少）上進行規劃所得的估計。
- **彈性**：有模型控制在環境改變時能立即更新，因為模型改變後，規劃隨之改變。無模型控制則必須透過經驗重新學習價值。
- **成本**：無模型控制在做決定時成本低；有模型控制則在每次選擇時都要花運算。
- **仲裁（arbitration）**：當兩個控制器意見不合時，決定採用哪一個控制器選擇的規則。

## 以不確定性仲裁

Daw、Niv 與 Dayan（2005）的出發點是：大腦似乎有不止一個選擇行為的控制器，包括一個與前額葉皮質相關、另一個與背外側紋狀體相關。他們的問題是，當兩者意見不合時，應該聽誰的。

他們的答案以強化學習理論為基礎。這兩個系統在計算上的簡單性，與彈性及統計效率之間做取捨。他們的提案是一個以不確定性為基礎的貝氏仲裁規則：在每一刻，估計較可靠的控制器接管。作者主張，這個規則能解釋一系列關於哪個系統在何種情境中佔主導的實驗發現。

仲裁的大致運作如下：

1. 維持一個從獎勵預測誤差學得的無模型行動價值估計。
2. 維持一個在學得模型上規劃所得的有模型估計。
3. 從各控制器近期的準確度估計其不確定性。
4. 由不確定性較低的控制器來控制選擇。

論文中的精確形式，對不確定性與仲裁的描述比這裡的大綱更為詳細；本頁所用的摘要沒有寫出其方程式。

## 結果

摘要指出，這個以不確定性為基礎的規則能解釋一系列關於兩個系統優勢地位的實驗發現，且是以定性方式報告。摘要沒有數值擬合，因此本頁不引用任何數字。

## 限制

- 這項提案是關於仲裁的理論，它所解釋的證據來自有限的實驗範式。
- 兩種控制器如何對應到特定腦區，仍是開放的問題；摘要並未解決。
- 兩個系統可能以簡單切換無法捕捉的方式互動，例如一方訓練另一方；仲裁觀點並不排除這種可能。

## 與其他主題的關聯

- **獎勵預測誤差**：無模型控制器由多巴胺神經元所發出的同一種預測誤差更新。見[多巴胺的獎勵預測誤差](../../neuroscience/dopamine-reward-prediction-error/index.zh-TW.md)。
- **擴散決策模型**：這是另一個問題，關於證據如何累積成選擇。見[擴散決策模型](../diffusion-model/index.md)。
- **強化學習**：同一個區分也是 AI 代理人的核心，它們結合學得的價值與規劃。見[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)。

## 應用

- **計算精神醫學**：把對有模型與無模型控制的權重擬合到行為上，用以研究成癮與強迫等狀況。這些是研究工具，並非臨床診斷。
- **AI 代理人**：許多系統結合學得的價值函數（無模型部分）與在學得模型上的搜尋或規劃（有模型部分），而如何結合兩者是實務上的設計問題。

## 開放問題

- **兩個系統是相互競爭還是相互合作？** 仲裁把它們視為競爭者，而一方訓練另一方的現象則暗示合作。
- **哪個訊號驅動仲裁？** 不確定性是一個候選；大腦也可能使用成本或時間壓力等其他訊號。
- **兩個系統如何對應到大腦？** 前額葉與紋狀體的對應是有用的起點，但仍需直接檢驗。

## 參考文獻

### 開創性論文

- Daw, N. D., Niv, Y. & Dayan, P.（2005）。Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control. *Nature Neuroscience*。https://doi.org/10.1038/NN1560 — 提出有模型與無模型控制器之間以不確定性為基礎的仲裁。
- Schultz, W., Dayan, P. & Montague, P. R.（1997）。A Neural Substrate of Prediction and Reward. *Science*。https://doi.org/10.1126/science.275.5306.1593 — 顯示多巴胺神經元發出獎勵預測誤差，這正是無模型控制所用的學習訊號。

### 綜述與回顧

- Gold, J. I. & Shadlen, M. N.（2007）。The neural basis of decision making. *Annual Review of Neuroscience*。https://doi.org/10.1146/annurev.neuro.29.051605.113038 — 回顧神經元如何把證據累積至決策，此處引用以說明選擇的神經框架。
- Dayan, P. & Daw, N. D.（2008）。Decision theory, reinforcement learning, and the brain. *Cognitive, Affective, & Behavioral Neuroscience*。https://doi.org/10.3758/CABN.8.4.429 — 回顧決策理論與強化學習模型如何與大腦中的選擇相關，包括兩種控制器。
- Sutton, R. S. & Barto, A. G.（2018）。*Reinforcement Learning: An Introduction*，第二版。MIT Press。http://incompleteideas.net/book/the-book-2nd.html — 關於無模型價值學習與以模型規劃的標準教科書。
