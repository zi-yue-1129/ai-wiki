---
translation_reviewed: 2026-10-28
tags:
- motor control
- internal models
- prediction
- neuroscience
aliases:
  - 內部前向模型
  - 前向模型
  - Internal forward model
  - Forward model
  - Efference copy
---

# 內部前向模型（Kawato 1987；Wolpert、Ghahramani 與 Jordan 1995）

內部前向模型是神經系統內部習得的映射，從運動指令與身體當前的狀態，映射到預測的下一個狀態。大腦可以利用這樣的預測，在延遲的感覺回饋抵達之前就採取行動，也能分辨自身感覺與外在世界的變化。這是運動控制中長久存在的想法，也是基於模型的強化學習的基本組成部分。

本頁屬於[運動控制與小腦](../index.md)。它詳細說明一種方法。它與另外兩種方法的關係，見章節概述。

## 概述

假設你移動手，而世界碰撞了它。感覺訊號會在事件發生後的一小段時間才抵達，而到那時下一個指令已經必須發出。只對回饋作出反應的控制器總會慢半拍。前向模型的想法是：大腦持續保有一個對自身動作會產生什麼結果的預測，並在真實回饋抵達時修正這個預測。

## 問題

運動控制面臨延遲、雜訊與動力學的變化。來自眼睛與皮膚的回饋需要時間才能抵達大腦，因此只依賴回饋的控制器無法進行快速修正。在感測器有雜訊時，大腦還必須推斷手臂的當前狀態，例如位置與速度。問題在於，神經系統如何在這些限制下規劃並修正動作，以及它是否在內部表示自身指令的結果。

## 核心想法

核心主張是，神經系統包含兩種互補的習得映射。前向模型根據當前狀態與送出的指令，預測下一個感覺狀態。反向模型，也就是控制器，則產生一個能帶來期望狀態的指令。前向模型的預測能立即取得，因此可以與延遲的回饋結合，得到對當前狀態更好的估計。

Kawato、Furukawa 與 Suzuki（1987）提出一個用於隨意動作控制與學習的階層式網路，其中動力學與反向動力學模型經由練習習得；他們以搭配機器人手臂的電腦模擬加以檢驗。Wolpert、Ghahramani 與 Jordan（1995）在一項感覺運動任務中檢驗了此想法。他們探討人們對手部位置估計的誤差如何隨時間擴散，並以最優狀態估計來解讀結果。他們的結論是，此模式支持運動系統的內部模型。

## 方程式與演算法

前向模型根據當前狀態與指令預測下一個狀態：

\(\hat{x}_{t+1} = f(x_t, u_t)\)

預測的狀態在回饋抵達時會被修正。在線性情況下，這就是卡爾曼濾波器所用的更新式：

\(\hat{x}_{t+1} \leftarrow \hat{x}_{t+1} + K\,(y_{t+1} - \hat{y}_{t+1})\)

其中 \(y_{t+1}\) 是觀察到的感覺回饋，\(\hat{y}_{t+1}\) 是預測的回饋，\(K\) 是增益，決定誤差在多大程度上改變估計。前向模型提供預測；增益則決定控制器相對於預測，對回饋的信任程度。

學習通常以誤差驅動的方式描述。預測的感覺回饋與實際回饋之間的不一致，被用來調整前向模型。

## 結果

前向模型的實驗證據是間接的。前向模型不能直接觀察，它的存在是從行為推斷出來的。Wolpert、Ghahramani 與 Jordan（1995）在最優狀態估計的框架下，分析估計手部位置的誤差如何隨時間傳播，並把結果視為對內部模型的直接支持。Wolpert、Miall 與 Kawato（1998）則回顧小腦中的內部模型。

## 限制

- **證據是間接的。** 前向模型是從行為與誤差擴散的方式推斷出來的，而不是從單一神經元讀取的。對同樣的資料，也可能有其他解釋。
- **模型的形式不明確。** 大腦學習的是身體的精確模型，還是只在所訓練情境下有效的近似模型，目前尚未定論。
- **模型儲存的位置不確定。** 小腦是主要候選者。[小腦監督式學習](../marr-albus-ito/index.md)一頁說明了 Ito（2008）的假說，即小腦編碼此類模型。其他區域也可能分擔此角色。
- **預測與適應相互關聯。** Shadmehr、Smith 與 Krakauer（2010）回顧證據，顯示前向模型是經由由感覺預測誤差驅動的運動適應而保持校準的。

## 連結

- **最優控制。** 最優回饋控制需要對身體狀態的估計，而前向模型提供此估計。見[最優回饋控制](../optimal-feedback-control/index.md)。
- **小腦。** 小腦被認為學習內部模型，這把本頁連結到[小腦監督式學習](../marr-albus-ito/index.md)。
- **世界模型與基於模型的強化學習。** 預測行動結果的環境學習模型，是前向模型在 AI 中的對應物。見[世界模型與具身智慧](../../../theory/models/world-models/index.md)與[有模型與無模型控制](../../decision-reward/model-based-vs-model-free/index.md)。

## 應用

- **機器人。** 把動力學預測與延遲感測器結合的狀態估計，是機器人控制中的標準做法。見[機器人](../../../applications/robotics/index.md)。
- **基於模型的強化學習。** 學習環境前向模型並以之規劃的代理人，應用的是同一個概念；見[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)。

## 開放問題

- **前向模型在哪裡學習並儲存？** 小腦是候選者，但完整的網路尚未描繪清楚。
- **前向模型是精確的還是近似的？** 大腦的模型是通用的，還是綁定於特定任務，仍有爭議。
- **知覺與動作是否由同一模型服務？** 同一個預測可能同時支持兩者，但共享模型的證據仍在研究中。

## 參考文獻

### 開創性論文

- Kawato, M., Furukawa, K. & Suzuki, R. (1987). A hierarchical neural-network model for control and learning of voluntary movement. *Biological Cybernetics*. https://doi.org/10.1007/BF00364149 — 提出一個階層式網路，其中動力學與反向動力學模型經由練習習得，並以模擬加以檢驗。
- Wolpert, D. M., Ghahramani, Z. & Jordan, M. I. (1995). An internal model for sensorimotor integration. *Science*. https://doi.org/10.1126/science.7569931 — 分析手部位置估計中的誤差如何隨時間傳播，並以此作為運動系統內部模型的支持。

### 綜述與教科書

- Wolpert, D. M., Miall, R. C. & Kawato, M. (1998). Internal models in the cerebellum. *Trends in Cognitive Sciences*. https://doi.org/10.1016/S1364-6613(98)01221-2 — 回顧小腦中的內部模型。
- Kawato, M. (1999). Internal models for motor control and trajectory planning. *Current Opinion in Neurobiology*. https://doi.org/10.1016/S0959-4388(99)00028-8 — 討論運動控制與軌跡規劃中的內部模型。
- Shadmehr, R., Smith, M. A. & Krakauer, J. W. (2010). Error correction, sensory prediction, and adaptation in motor control. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-060909-153135 — 回顧前向模型如何經由感覺預測誤差驅動的運動適應而保持校準。
