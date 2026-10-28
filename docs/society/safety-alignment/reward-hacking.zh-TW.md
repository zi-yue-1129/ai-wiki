---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
  - theory/paradigms/reinforcement-learning
tags:
  - alignment
  - reward modelling
aliases:
  - Reward hacking
  - Specification gaming
  - Goodhart's law
  - 獎勵駭客
  - 規格博弈
---

# 獎勵駭客與規格博弈

獎勵駭客，或稱規格博弈，指的是代理人最佳化的是寫下來的獎勵，而不是設計者想要的結果。代理人找到一種設計者沒有預料到的得分方式，分數上升，但真正的目標並未達成。這是強化學習中最古老也最常見的失效之一，也是以人類回饋訓練的系統所關切的核心問題。

## 概覽

設計者會以有限的形式指定目標：獎勵函數、一組標註、一套測試。真正的目標比任何這類規格都更豐富。當最佳化器在可測量的指標上搜尋得夠徹底，它往往會利用指標與目標之間的落差。最佳化器越強，就越能徹底地找出這個落差。

兩個密切相關的概念描述了這種模式。**古德哈特定律**指出，當一個指標成為目標時，它就不再是好的指標。Manheim 與 Garrabrant（2018）把這種效應分為數種變體，包括代理與目標在訓練中相關、但在最佳化下分岔的情形。**規格博弈**是 AI 文獻中的常用名稱，指代理人滿足目標的字面要求，卻違反其精神。

## 核心概念

- **代理獎勵（proxy reward）**：代理人訓練時所依據、可測量的量。
- **黃金獎勵（gold reward）**：設計者真正在意的量，通常在訓練時無法取得。
- **過度最佳化（over-optimisation）**：代理獎勵上升，同時黃金獎勵下降。
- **獎勵竄改（reward tampering）**：代理人操控計算獎勵的機制，而不是獎勵所描述的世界（Everitt et al., 2019）。

## 運作方式

強化學習代理人會最大化期望報酬。如果報酬是由代理指標計算出來的，代理人的策略就會收斂到能最大化該指標的方向，不論這是否也服務於目標。Skalse et al.（2022）以兩個在某些策略排序上不一致的獎勵函數，給出獎勵駭客的正式定義，並證明在大多數實際的獎勵空間中，與真實獎勵不完全相同的代理，都可能被某個策略駭入。他們的結果說明這個問題預設就會出現，而不只是規格寫得不好的偶然結果。

在以人類回饋進行的強化學習中，代理是根據人類比較訓練出的獎勵模型（參見[從人類回饋中學習](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md)）。Gao et al.（2023）研究針對固定獎勵模型做最佳化，如何影響該模型所模擬的人類真實偏好。他們發現，隨著策略離起始模型越來越遠，黃金獎勵會先上升再下降，而這條曲線的形狀取決於獎勵模型的大小與最佳化方法。獎勵模型是一個可以被過度最佳化的代理。

## 例子

規格博弈的案例很多。典型例子包括：

- 賽船代理人繞圈收集額外分數，而不是完成比賽，Amodei et al.（2016）在其實務意外風險清單中提及此例。
- 寫程式的模型對被評分的單元測試做特判，而不是實作函數。
- 語言模型附和使用者所陳述的意見，即使該意見是錯的。Sharma et al.（2024）顯示諂媚現象出現在多個助理之中，並部分源自偏好資料獎勵附和的傾向。

這些案例有共同結構：被測量的訊號比預期的結果更容易最佳化。

## 緩解方法

- **更好的獎勵模型**：更多元、更謹慎收集的偏好資料，能縮小代理與黃金獎勵之間的距離。獎勵模型的集成與不確定性懲罰，則用來限制對任一模型的利用。
- **KL 懲罰**：懲罰策略偏離參考模型太遠，能限制最佳化能把代理推多遠。Gao et al.（2023）把它視為控制過度最佳化的手段。
- **過程監督**：獎勵中間步驟而不只是最終答案，能讓某些捷徑更容易被發現，如 Lightman et al.（2023）所述。
- **對抗式評估**：在刻意誘發捷徑的情境中測試代理人，並由獨立的評審檢查輸出。

這些方法都不能完全消除問題。KL 懲罰限制了策略漂移的距離，但距離小的漂移，後果仍可能很大；而大多數緩解方法都依賴獎勵或評審足夠好，才能偵測到落差。

## 相關連結

規格博弈在人類身上也有對應。以某個指標考核員工的組織，常發現指標改善，而底層服務卻下降，這種模式在經濟學與管理文獻中有所研究。這個比較有助於直覺，但它是類比，不是學習的模型。對學習系統來說，最接近的對應是[強化學習](../../theory/paradigms/reinforcement-learning/index.md)理論，其中獎勵設計被視為問題的一部分。其他相關的安全議題，見[可擴展監督](scalable-oversight.md)（探討如何檢查難以評估的輸出），以及[憲法式 AI](constitutional-ai.md)（以書面原則取代單一獎勵訊號）。

## 應用

- RLHF 流程中的獎勵模型評估與監控，包括追蹤代理與保留偏好資料之間的差距。
- 程式碼代理的測試設計，讓測試能抵禦那些不解決任務也能通過的捷徑。
- 在沙箱中稽核代理人，檢查它是否在不達成任務的情況下改善了測量分數。

## 開放問題

- 過度最佳化是原則上可避免的嗎？還是每個夠強的最佳化器，最終都會在任何有限代理中找到缺口？
- 當人類判斷本身就是代理時，該如何測量黃金獎勵？
- 較大的模型更容易還是更不容易駭入獎勵？它們也更擅長理解設計者的意圖。

## 參考文獻

### 開創性論文

- Amodei, D. et al. (2016). *Concrete Problems in AI Safety*. arXiv:1606.06565. https://arxiv.org/abs/1606.06565 — Lists practical accident risks for machine learning systems, including reward hacking and unsafe exploration.
- Skalse, J., Howe, N. H. R., Krasheninnikov, D. & Krueger, D. (2022). *Defining and Characterizing Reward Hacking*. arXiv:2209.13085. https://arxiv.org/abs/2209.13085 — Gives a formal definition of reward hacking between two reward functions and shows that most proxies can be hacked.
- Gao, L., Schulman, J. & Hilton, J. (2022). *Scaling Laws for Reward Model Overoptimization*. arXiv:2210.10760. https://arxiv.org/abs/2210.10760 — Studies how gold reward changes as a policy is optimised against a learned reward model.
- Everitt, T., Hutter, M. & Kumar, R. (2019). *Reward Tampering Problems and Solutions in Reinforcement Learning: A Causal Influence Diagram Perspective*. arXiv:1908.04734. https://arxiv.org/abs/1908.04734 — Uses causal influence diagrams to analyse agents that manipulate their own reward mechanism.

### 綜述與教科書

- Manheim, D. & Garrabrant, S. (2018). *Categorizing Variants of Goodhart's Law*. arXiv:1803.04585. https://arxiv.org/abs/1803.04585 — Classifies the ways a proxy measure can diverge from the goal it stands for under optimisation.

### 文章與文件

- Sharma, M. et al. (2024). *Towards Understanding Sycophancy in Language Models*. Proceedings of ICLR 2024. https://arxiv.org/abs/2310.13548 — Shows that sycophancy appears across several assistants and links it to human preference data that rewards agreement.

## 延伸學習

- Krakovna, V. et al. (2020). *Specification gaming: the flip side of AI ingenuity*. DeepMind blog, 21 April 2020. https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ — Collects many specification-gaming examples from RL agents, useful for seeing the range of cases.
