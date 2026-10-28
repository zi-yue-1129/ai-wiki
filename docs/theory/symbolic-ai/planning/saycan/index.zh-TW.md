---
translation_reviewed: 2026-10-28
---

# SayCan

SayCan 是讓大型語言模型為機器人規劃的一種方法。語言模型提出下一步應使用哪種技能，一組學得的價值函數則估計每項技能在機器人當前場景中是否可行。機器人選擇兩者分數都最高的技能，執行它，並重複這個過程，直到指令完成。它由 Google 的 Michael Ahn 及同事於 2022 年提出，是[自動規劃概述](../index.md)中以語言為基礎的代表性方法。

## 概述

語言模型知道任務通常如何完成。被問到如何清理灑出的液體時，它能寫出合理的步驟序列。但這些步驟對於特定房間中的特定機器人未必可行，因為機器人可能沒有海綿、搆不到灑出的液體，或是手上正拿著別的東西。

SayCan 結合了兩種資訊來源。語言模型判斷哪些步驟有助於完成指令，技能價值函數則根據當前觀測判斷哪些步驟實際上能夠完成。單靠任何一方都不夠。

## 關鍵概念

- **技能（Skill）**：一個簡短、預先訓練好的機器人行為，以自然語言命名，例如「拿起海綿」。
- **語言模型分數**：在給定指令與已完成步驟的情況下，模型賦予某技能作為下一步的機率。
- **可供性（Affordance，價值函數）**：從當前觀測出發，某技能成功的機率的學習估計。

## 運作方式

令 $i$ 為指令、$\ell$ 為已完成的步驟、$s$ 為當前觀測。對每個候選技能 $a$，機器人以該技能的語言模型機率與其價值函數組成一個分數。機器人接著選擇

$$
a^{*} = \arg\max_{a} \; p_{\text{LLM}}(a \mid i, \ell)\; \cdot\; V_a(s),
$$

其中 $V_a(s)$ 是從狀態 $s$ 出發，技能 $a$ 成功的估計機率。程序如下。

1. 讀入指令，並把已完成步驟的清單設為空。
2. 詢問語言模型，在給定指令與已完成步驟的情況下，技能庫中每項技能的機率。
3. 詢問每項技能的價值函數，依當前觀測估計其成功機率。
4. 把兩個分數相乘，選擇乘積最高的技能並執行。
5. 把剛執行的技能加入已完成步驟，然後回到第 2 步，直到模型表示任務完成。

只有當模型認為某技能有用，而機器人認為它可行時，才會選擇該技能。後續研究如 Inner Monologue 在同樣的迴圈中加入了來自環境的閉環回饋。[^3]

## 結果

論文在真實機器人任務上評估此方法，指令為抽象的自然語言長程任務，由行動機械手（mobile manipulator）執行。摘要指出，此方法能完成這些指令，並且需要真實世界的落地。這裡不引用成功率。[^2]

## 限制

- **技能庫固定。**機器人只能做技能所允許的事。計畫若需要缺少的技能，就無法完成，不論語言模型的文字多麼合理。
- **價值函數的成本。**每項技能都需要一個訓練好的價值函數，當機器人或環境改變時必須重新訓練。
- **依賴兩個部分。**語言模型分數不佳時，可能選到可行卻無益的技能；此外，這個迴圈比預先計算的計畫慢。

## 未解問題

- 閉環回饋能否讓計畫在技能未曾設計的情境中更可靠？後續研究對此有所探討。[^3]
- 單靠語言模型規劃效果很差，因此在一般情境中需要多少落地？[^4]

## 相關連結

SayCan 把技能視為計畫的基本行動，這種結構在 [SHOP2](../shop2/index.md) 中以較僵硬的形式出現。它依賴[大型語言模型](../../../models/llm/index.md)中的知識，其價值函數則如[強化學習](../../../paradigms/reinforcement-learning/index.md)般是學得的。可與 [STRIPS](../strips/index.md) 比較。

## 應用

- **行動機械手操作**，機器人執行類似家務的指令，例如清潔或取物。[^2]
- **混合式規劃器**，語言模型以形式化語言寫出計畫，再由古典規劃器求解，如 LLM+P 所示。[^5]

[^1]: Ahn et al. (2022)，見上方列表。
[^2]: Ahn et al. (2022)，見上方列表。內容與主張依論文摘要。這裡不引用成功率。
[^3]: Huang et al. (2022, Inner Monologue)，見上方列表。
[^4]: Valmeekam et al. (2023)，見上方列表。
[^5]: Liu et al. (2023)，見上方列表。

## 參考文獻

### 開創性論文

- Ahn, M. et al. (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv. https://arxiv.org/abs/2204.01691 — 提出 SayCan，在真實機器人上結合語言模型的技能分數與學得的可供性價值函數。
- Huang, W., Abbeel, P., Pathak, D. & Mordatch, I. (2022). Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents. arXiv. https://arxiv.org/abs/2201.07207 — 說明大型語言模型能把任務分解為計畫，而這些計畫必須轉譯為可執行的行動。

### 文章與文件

- Huang, W. et al. (2022). Inner Monologue: Embodied Reasoning through Planning with Language Models. arXiv. https://arxiv.org/abs/2207.05608 — 為機器人的語言模型規劃加入來自環境的閉環語言回饋。
- Liu, B. et al. (2023). LLM+P: Empowering Large Language Models with Optimal Planning Proficiency. arXiv. https://arxiv.org/abs/2304.11477 — 把語言問題轉為 PDDL，交由古典規劃器求解，再把計畫翻譯回語言。
- Valmeekam, K. et al. (2023). On the Planning Abilities of Large Language Models: A Critical Investigation. arXiv. https://arxiv.org/abs/2305.15771 — 測量語言模型自主規劃的能力，並顯示在引導外部規劃器時的進步。
- Kambhampati, S. et al. (2024). LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks. arXiv. https://arxiv.org/abs/2402.01817 — 立場論文，主張語言模型在與外部驗證器的迴圈中最能發揮作用。
