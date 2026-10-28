---
translation_reviewed: 2026-10-28
related:
- applications/robotics
- theory/paradigms/reinforcement-learning
- theory/models/world-models
tags:
- neuroscience
- motor control
- cerebellum
- control theory
aliases:
  - 運動控制與小腦
  - Motor Control and the Cerebellum
  - Motor control
  - Cerebellum
  - 小腦
  - 運動控制
---

# 運動控制與小腦

讓身體動起來，必須把意圖轉換成肌肉指令，而身體本身反應慢、帶有雜訊，而且會隨時間改變。神經系統的因應方式包括：預測自身指令的結果、用回饋修正誤差，以及從錯誤中學習。小腦與運動皮質是這項工作的核心結構。對 AI 而言，運動控制提供了一批具體問題：在不確定性下行動、從誤差中學習，以及從資料建立系統動態的模型。

本章概述運動控制的理解方式。每種方法各有一頁，連結列於下方。

## 概述

伸手拿一個杯子看似簡單，但大腦面對一連串困難的問題。感覺訊號會有數十毫秒的延遲，因此大腦不能只靠回饋來引導快速的動作。肌肉會因疲勞與負荷而改變表現，手臂的力學也取決於姿勢。運動控制理論要問的是：控制器如何應付這些情況，仍能產生精確的動作，以及大腦各部位分別負責什麼。

這些答案是數十年間逐步形成的。工程師與生理學家逐漸匯聚到幾個共通的想法：大腦保有一個身體的內部模型，它以依任務而定的方式使用回饋，並從誤差中學習。這些想法解釋了小腦在調整動作中的角色，也連結到在運動皮質中觀察到的群體層級動態。

## 核心概念

- **內部模型（internal model）**：大腦內部習得的映射，表示身體與外在世界如何回應指令。前向模型（forward model）預測指令的結果；反向模型（inverse model）則為期望的結果提出一個指令。
- **傳出複本（efference copy）**：送往感覺區的運動指令副本，使人能把自身動作的預期感覺結果，與真實的感覺結果相比較。
- **攀爬纖維與平行纖維（climbing fibre and parallel fibre）**：小腦浦肯野細胞（Purkinje cell）的兩種輸入。攀爬纖維攜帶類似誤差的教導訊號，平行纖維則攜帶情境訊號。
- **回饋控制（feedback control）**：在動作進行中，依據感測到的誤差加以修正。
- **最優控制（optimal control）**：在給定誤差與努力的成本，以及系統中存在雜訊的條件下，選出最能達成目標的指令。
- **神經群體動力學（neural population dynamics）**：一種觀點，認為許多神經元的聯合活動依一定規則隨時間演化，而不是每個神經元各自編碼某個固定的量。

## 關鍵方法

- [最優回饋控制（Todorov & Jordan 2002）](optimal-feedback-control/index.md)：把動作視為帶有雜訊下的最優控制，回饋只修正對任務有影響的偏差，其餘變異則不加修正。
- [小腦監督式學習（Marr、Albus 與 Ito）](marr-albus-ito/index.md)：一套說明小腦如何學習運動技能的理論，攀爬纖維充當教導訊號，改變浦肯野細胞突觸的強度。
- [內部前向模型（Kawato 1987；Wolpert、Ghahramani 與 Jordan 1995）](internal-forward-models/index.md)：主張大腦會預測自身指令的感覺結果，使它能在延遲的回饋抵達前修正動作。

前兩種方法說明大腦如何決定與修正動作，第三種則是這些決策所依賴的預測機制。實務上三者相互重疊：小腦被認為會學習前向模型，而最優回饋控制需要對身體狀態的估計，這正是前向模型所提供的。

## 連結

- **腦與心智。** 小腦也參與程序性學習與制約學習；見[記憶與學習的神經機制](../memory-learning/index.md)。把知覺與動作視為降低預測誤差的預測處理觀點，見[預測編碼與自由能原理](../predictive-coding/index.md)。神經系統的基本結構見[神經科學基礎](../neuroscience/index.md)，建模工具見[計算神經科學](../computational-neuroscience/index.md)。
- **運動皮質與腦機介面。** 對運動皮質的群體分析，是[腦機介面與神經解碼](../bci/index.md)所用解碼器的基礎，包括[以神經控制的手臂進行伸手與抓取（Hochberg 等人，2012）](../bci/neural-reach-and-grasp/index.md)的研究。
- **強化學習與基於模型的控制。** 前向模型正是基於模型的控制器用來規劃的東西。用習得模型規劃，與直接學習價值之間的對比，見[有模型與無模型控制](../decision-reward/model-based-vs-model-free/index.md)；獎勵導向的學習見[決策、多巴胺與獎勵](../decision-reward/index.md)。整體框架見[強化學習](../../theory/paradigms/reinforcement-learning/index.md)。
- **NeuroAI。** 運動控制一直是學習模型與世界模型的試驗場，見[NeuroAI：大腦與 AI 的雙向啟發](../neuroai/index.md)與[世界模型與具身智慧](../../theory/models/world-models/index.md)。

## 應用

- **機器人。** Albus 後來提出的小腦模型關節控制器（CMAC）是一種以查表為基礎的控制器，為機器人操作器而設計，把小腦的概念帶入工程。見[機器人](../../applications/robotics/index.md)。
- **腦機介面。** 從運動皮質讀取意圖動作的解碼器，依賴群體活動攜帶動作狀態與動態這一觀點。見[腦機介面概述](../bci/index.md)。
- **基於模型的強化學習。** 會學習環境模型並以之規劃的代理人，借用了運動控制中的前向模型概念。見[強化學習](../../theory/paradigms/reinforcement-learning/index.md)。
- **臨床神經科學。** 小腦受損與動作協調及適應能力的下降相關，這也是小腦被當作學習系統來研究的原因之一（見小腦方法頁所引的 Ito 2006 綜述）。

## 開放問題

- **小腦是否只學習動作？** 小腦回路也與認知和計時相關，運動理論的適用範圍仍有爭議。
- **運動皮質動態從何而來？** 觀察到的動態有多少來自迴路本身的特性、來自身體的回饋，或來自習得的內部模型，目前並不清楚。
- **最優控制能否擴展到習得的模型？** 當身體動力學已知時，最優回饋控制運作良好。從帶雜訊的資料中學習這些動力學，並以之規劃，仍然困難。
- **三種方法如何結合？** 最優回饋控制、小腦學習與前向模型，常被視為各自獨立的理論。是否有單一框架能涵蓋三者，仍是活躍的問題。

## 參考文獻

### 開創性論文

- Marr, D. (1969). A theory of cerebellar cortex. *Journal of Physiology*. https://doi.org/10.1113/jphysiol.1969.sp008820 — 提出小腦皮質學習運動技能，下橄欖核傳來的攀爬纖維輸入是教導訊號。
- Albus, J. S. (1971). A theory of cerebellar function. *Mathematical Biosciences*. https://doi.org/10.1016/0025-5564(71)90051-4 — 發展小腦學習模型，其中攀爬纖維訊號引導浦肯野細胞輸出的變化。
- Albus, J. S. (1975). A new approach to manipulator control: the cerebellar model articulation controller (CMAC). *Journal of Dynamic Systems, Measurement, and Control*. https://doi.org/10.1115/1.3426922 — 把小腦模型應用於機器人操作器控制。
- Todorov, E. & Jordan, M. I. (2002). Optimal feedback control as a theory of motor coordination. *Nature Neuroscience*. https://doi.org/10.1038/nn963 — 提出以隨機最優回饋控制作為運動協調的理論，協同與受控參數都由同一原理導出。
- Wolpert, D. M., Ghahramani, Z. & Jordan, M. I. (1995). An internal model for sensorimotor integration. *Science*. https://doi.org/10.1126/science.7569931 — 分析手部位置估計中的誤差如何隨時間傳播，並主張此結果支持運動系統的內部模型。
- Churchland, M. M., Cunningham, J. P., Kaufman, M. T., Foster, J. D., Nuyujukian, P., Ryu, S. I. & Shenoy, K. V. (2012). Neural population dynamics during reaching. *Nature*. https://doi.org/10.1038/nature11129 — 在伸手過程中，把運動皮質的活動分析為一個群體動力系統。

### 綜述與回顧

- Wolpert, D. M., Miall, R. C. & Kawato, M. (1998). Internal models in the cerebellum. *Trends in Cognitive Sciences*. https://doi.org/10.1016/S1364-6613(98)01221-2 — 回顧小腦同時持有前向與反向內部模型的證據。
- Ito, M. (2008). Control of mental activities by internal models in the cerebellum. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2332 — 回顧小腦內部模型的概念，包括非運動功能。
- Shadmehr, R., Smith, M. A. & Krakauer, J. W. (2010). Error correction, sensory prediction, and adaptation in motor control. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-060909-153135 — 回顧誤差修正與感覺預測如何支撐適應。
- Shenoy, K. V., Sahani, M. & Churchland, M. M. (2013). Cortical control of arm movements: a dynamical systems perspective. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev-neuro-062111-150509 — 回顧運動皮質的動力系統觀點，及其與動作的關係。
- Doya, K. (1999). What are the computations of the cerebellum, the basal ganglia and the cerebral cortex? *Neural Networks*. https://doi.org/10.1016/S0893-6080(99)00046-5 — 提出小腦、基底核與皮質的分工：分別為監督式、強化式與非監督式學習者。
