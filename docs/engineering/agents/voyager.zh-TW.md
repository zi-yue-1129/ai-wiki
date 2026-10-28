---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - agents
  - lifelong learning
  - embodied AI
aliases:
  - Voyager
  - Minecraft Agent
  - 終身學習代理
  - 技能庫
---

# Voyager（Wang 等人，2023）

Voyager 是一個在 Minecraft 中遊玩的語言模型代理，它會自行探索世界，並保留所學到的技能。它為每項技能撰寫可執行的程式碼，把程式碼存入不斷成長的技能庫，並在遇到類似任務時取回。Wang 等人（2023）以 GPT-4 為模型提出此系統，且不做微調。

本頁是[代理工程](index.zh-TW.md)的一部分，也是本節的命名方法之一，並示範代理如何在不改變權重的情況下隨時間學習。

## 概述

Minecraft 之類的遊戲提供開放式的世界與眾多任務，持續學習的代理需要在已完成的工作之上繼續建構。在這類情境中，早期的代理不是遵循固定腳本，就是每次都從頭學習。Voyager 結合三個元件，使它能持續發現新事物，並記住所學。

## 問題

終身學習要求代理在獲得新能力的同時不遺忘舊能力，而且每學一項新技能都不必重新完整訓練。Voyager 處理的問題是：語言模型代理如何在開放世界中探索、選擇接下來要學什麼，並重用已學會的內容，而且全部只透過對模型的黑箱查詢完成。

## 核心想法

Voyager 有三個元件。第一，自動課程（curriculum）提出下一項任務，以最大化探索。第二，技能庫儲存成功技能的可執行程式碼，並在之後以任務計畫與環境回饋的嵌入向量取回相關技能，使複雜行為由較簡單的行為組成。第三，迭代提示機制利用環境回饋、執行錯誤與自我驗證來改進程式。作者認為，這些技能具有時間延展性與組合性，能使能力逐步疊加，並減少災難性遺忘。

## 方程式或演算法

每一次迭代：

1. 課程依據代理已探索的內容與已能做到的事，提出一項任務。
2. 模型為某項技能撰寫程式碼，並使用從技能庫取回的相關技能。
3. 程式在環境中執行。錯誤、環境回饋，以及另一個 GPT-4 批判者所做的自我驗證會被送回，程式持續修改，直到任務成功或達到嘗試上限。
4. 經驗證的技能加入技能庫，供之後的任務取回。

## 結果

摘要指出，在 Minecraft 中，Voyager 獲得的獨特物品多 3.3 倍、移動距離長 2.3 倍，科技樹的關鍵里程碑解鎖速度快達 15.3 倍，均優於先前最先進的方法。摘要也指出它展現出強的情境內終身學習能力。

## 限制

- **特定環境。**結果來自 Minecraft，那裡的行動與回饋都有結構。論文並未證明能遷移到結構較少的環境。
- **依賴強大的模型。**此方法透過黑箱查詢使用 GPT-4，因此效能取決於該模型。
- **以程式碼作為技能格式。**以程式碼表示的技能可以檢視與重用，但只能涵蓋環境介面所能表達的內容。
- **檢索錯誤。**從技能庫取回錯誤的技能，可能在不恰當的情境中被重用。

## 關聯

- 不遺忘地學習的問題，是[持續學習](../../theory/paradigms/continual/index.zh-TW.md)的主題。
- Voyager 所建立於其上的推理與行動迴圈是 [ReAct](react.zh-TW.md)。
- 以跨次嘗試的語言回饋與以權重為基礎的學習之比較，見 [Reflexion](reflexion.zh-TW.md)。
- 技能庫類似人們儲存程序的方式；相關記憶文獻見[大腦中的記憶與學習](../../brain-mind/memory-learning/index.zh-TW.md)。

## 應用

- 在長時間遊戲中逐步累積技能的遊戲代理。
- 為重複出現的子任務重用經驗證程式碼的模擬代理。

## 開放問題

- 如何讓技能庫不收錄那些僅偶然成功的技能？
- 課程機制能否推廣到沒有清楚進度衡量的環境？

## 參考文獻

### 開創性論文

- Wang, G. 等人（2023）。*Voyager: An Open-Ended Embodied Agent with Large Language Models*。arXiv。https://arxiv.org/abs/2305.16291 — 提出 Voyager，包括自動課程、可執行技能庫與 Minecraft 中的迭代提示。
- Yao, S. 等人（2023）。*ReAct: Synergizing Reasoning and Acting in Language Models*。ICLR。https://arxiv.org/abs/2210.03629 — Voyager 代理行動迴圈所依據的推理與行動方法。
- Shinn, N. 等人（2023）。*Reflexion: Language Agents with Verbal Reinforcement Learning*。NeurIPS。https://doi.org/10.52202/075280-0377 — 說明語言代理如何從語言回饋中跨次嘗試學習，與技能庫形成對照。
- Park, J. S. 等人（2023）。*Generative Agents: Interactive Simulacra of Human Behavior*。UIST。https://doi.org/10.1145/3586183.3606763 — 在共享環境中具有記憶的互動式代理，是對已儲存經驗的另一種運用。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，涵蓋記憶、規劃與工具使用。
