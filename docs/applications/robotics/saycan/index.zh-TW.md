---
translation_reviewed: 2026-10-28
related:
  - theory/models/llm
  - theory/paradigms/reinforcement-learning
aliases:
  - SayCan
  - Do As I Can, Not As I Say
  - 語言模型規劃
---

# SayCan（Ahn 等人，2022）

Ahn 等人想知道：一個對世界知識豐富、卻沒有身體經驗的語言模型，如何引導機器人完成任務。他們的系統 SayCan 讓語言模型提出步驟，而由學習得來的價值函數檢查機器人實際上能執行哪些步驟。本頁說明這篇論文；上層主題是[機器人](../index.md)。

## 問題

語言模型能為「幫我拿杯飲料」這類任務提出合理的步驟，但它不知道機器人在當前場景中能否執行這些步驟。缺少這種與實體環境的連結，它的計畫可能流暢卻不可行。

## 核心想法

機器人擁有一組預訓練的技能。每個技能都有一個價值函數，論文將其視為可供性函數（affordance function），即技能從當前狀態出發成功的機率。SayCan 把語言模型對某技能的分數乘上該技能的可供性。語言模型提供任務層級的計畫，而技能與其價值函數則把這個計畫落實到實體場景中。

## 方程式

令 *i* 為指令，*s* 為當前狀態，ℓπ 為技能 π 的語言描述。語言模型給出 p(ℓπ | i)，可供性函數給出 p(cπ | s, ℓπ)，即技能 π 從 s 出發成功完成的機率。SayCan 選擇

π* = argmax（對所有 π）p(cπ | s, ℓπ) · p(ℓπ | i)。

論文的演算法 1 將此計算為可供性與語言模型分數的乘積，再取 argmax。在無折扣、稀疏獎勵的情況下，價值函數即對應於可供性函數（第 2 節）。

## 程序

1. 給定指令與當前狀態，以語言模型機率乘上可供性，為每個候選技能評分。
2. 執行分數最高的技能，並以更新後的歷史重複。
3. 選到終止動作時停止。

## 結果

評估使用 101 條指令，論文稱之為「101 個真實世界的機器人任務」，分為七個家族，每家族分別有 15、15、15、15、11、15、15 條指令（表 1）。機器人是 Everyday Robots 移動式操作機器人，手臂具有 7 個自由度（第 5 節）。表 2 的總計列顯示：

| 系統 | 規劃成功率 | 執行成功率 |
|---|---|---|
| PaLM-SayCan，模擬廚房 | 84% | 74% |
| PaLM-SayCan，真實廚房 | 81% | 60% |
| 無價值函數落地 | 67% | 總計列未報告 |
| 生成式基線 | 74% | 總計列未報告 |
| BC NL | 總計列未報告 | 0% |
| BC USE | 總計列未報告 | 9% |

從模擬廚房換到真實廚房，規劃成功率下降 3 個百分點，執行成功率下降 14 個百分點（第 5.1 節）。FLAN-SayCan 的規劃與執行成功率分別為 70% 與 61%，PaLM-SayCan 則為 84% 與 74%（表 3）。作者將 65% 的錯誤歸因於語言模型，35% 歸因於可供性失敗（第 5.1 節）。論文引言稱落地「幾乎讓效能加倍」，但表 2 中規劃成功率的差距（84% 對 67% 與 74%）小於這個說法，因此應引用表中數字。

## 限制

- **技能庫**：論文提出 551 個技能，但只使用其中「最適合組合」的一部分。技能的範圍與能力是主要瓶頸（第 4 節、第 8 節）。
- **資料成本**：行為克隆使用 68,000 筆遙操作示範；作者另收集了 276,000 次自主嘗試，其中約 12,000 次成功。強化學習則在模擬中使用 MT-Opt，以 16 顆 TPUv3 晶片運行約 100 小時（附錄 C.2）。
- **語言模型錯誤**：系統難以處理否定與模糊的指代。長期任務的失敗多半是語言模型過早終止（第 5.1 節）。作者預期它會繼承訓練資料的偏見與限制（第 8 節）。
- **回饋有限**：回饋只能透過當前步驟的價值函數回到規劃器。技能失敗但價值很高時，系統不容易反應，因此部分失敗可能未被察覺（第 5.2 節、第 8 節）。
- **評估範圍**：實驗只在作者的機器人與技能組合上進行。

## 後續工作

- **Inner Monologue（Huang 等人，2022）** 把來自環境的自然語言回饋，例如成功偵測、場景描述與人類互動，加入 LLM 規劃中。它不需要額外訓練，並針對上述回饋有限的問題。
- **與學習的連結**：技能與其可供性是透過行為克隆與強化學習學得的，這與[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)相關。

## 連結

- 本方法中的語言模型部分，見 [LLM](../../../theory/models/llm/index.md)。
- 技能學習的部分，見[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)。

## 參考文獻

### 開創性論文

- Ahn, M. et al. (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv. https://arxiv.org/abs/2204.01691 — 把語言模型與預訓練機器人技能的學習可供性函數結合，並在 101 條真實世界指令上評估。
- Huang, W. et al. (2022). Inner Monologue: Embodied Reasoning through Planning with Language Models. arXiv. https://arxiv.org/abs/2207.05608 — 在不需額外訓練的情況下，把來自環境的自然語言回饋回授到機器人的 LLM 規劃中。
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — 在大型真實機器人資料集上訓練、用於真實世界控制的 transformer 策略。

### 教科書與綜述

- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — 強化學習應用於機器人的綜述。
- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — 關於基礎模型能力、技術原理與風險的報告，機器人是其中的應用領域之一。
