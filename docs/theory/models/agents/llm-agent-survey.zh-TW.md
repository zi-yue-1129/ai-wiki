---
related:
  - engineering/agents
  - theory/models/llm
  - theory/models/reasoning
tags:
  - agents
  - large language models
  - survey
last_reviewed: 2026-11-01
translation_reviewed: 2026-11-01
aliases:
  - The Rise and Potential of Large Language Model Based Agents
  - LLM-based agents survey
  - 基於大型語言模型的智能體綜述
---

# 基於大型語言模型智能體的興起與潛力（Xi et al., 2023）

Xi、Chen、Guo 與同事（2023）綜述了以大型語言模型為基礎的 AI 智能體。他們提出一個通用的概念框架：LLM 扮演智能體的大腦，並由感知與行動模組輔助。他們以這個框架整理 LLM 智能體的應用、評估與未解問題（Xi et al., 2023）。

## 概觀

摘要把問題描述為一項長期追求：打造與人類能力相當或超越人類的 AI，而智能體被視為實現它的有希望途徑。過去的智能體研究多著重於特定任務的演算法或訓練策略。這份綜述認為，社群缺少一個通用而強大的模型，作為設計智能體的起點，並提出以大型語言模型作為這個起點（Xi et al., 2023）。

## 關鍵概念

- **智能體**：會感知環境、做出決策並採取行動的實體（Xi et al., 2023，摘要）。
- **大腦**：儲存知識與記憶，並負責推理、規劃與決策的控制器。論文稱之為 AI 智能體的核心（第 3 節）。
- **感知**：接收文字、影像與聲音等多模態輸入，並把它轉換成大腦可用形式的模組（第 3.2 節）。
- **行動**：透過文字輸出、工具使用與具身行動來執行決策的模組（第 3.3 節）。

## 概念框架

論文的框架有三個部分。大腦（第 3.1 節）涵蓋自然語言互動、知識、記憶、推理與規劃，以及可遷移性與泛化能力。感知（第 3.2 節）把多種模態的輸入轉換為大腦的表示。行動（第 3.3 節）涵蓋文字輸出、工具使用與具身行動（第 3.3.3 節）。綜述強調智能體以迴圈方式運作，重複感知、推理與行動，以便從環境中獲得回饋（第 3 節）。

這種拆解是綜述的主要組織工具。讀者可以藉此追問某個系統依賴哪個模組，以及哪個模組會成為限制。

## 應用

論文把應用分為三種情境（第 4 節）：

- **單一智能體**部署（第 4.1 節），綜述依任務導向、創新導向與生命週期導向來組織。
- **多智能體**互動（第 4.2 節），智能體可以為互補技能而合作，也可以為促進進展而對抗競爭（第 4.2.1 與 4.2.2 節）。綜述以軟體開發作為多智能體的例子（第 2.2 節）。
- **人機合作**（第 4.3 節），綜述以指令者—執行者與平等夥伴兩種模式加以描述。

## 評估

導論指出，綜述從四個面向回顧評估：效用、社交性、價值觀，以及持續演化的能力（第 1 節）。詳細協定請見第 6.2 節。綜述關於幻覺的討論也指出，智能體的大腦可能生成與來源或事實相衝突的內容，這限制了它在要求事實嚴謹的任務中的使用（第 3.1.2 節）。

## 挑戰

綜述列出數個未解問題（第 3.1.2 與第 6 節）：

- **幻覺。** 生成的內容可能與事實相衝突，這限制了它在事實要求高的任務中的使用（第 3.1.2 節）。
- **知識。** 已獲得的知識可能過時，或從一開始就不正確。重新訓練成本高，還可能造成災難性遺忘，因此綜述把知識編輯列為替代方案（第 3.1.2 節）。
- **安全與可信度。** 對抗性穩健性、可信度與其他風險（第 6.3 節）。綜述指出 LLM 容易受到對抗性攻擊（第 3.3.2 節）。
- **智能體數量的擴展。** 預先決定與動態擴展智能體數量（第 6.4 節）。
- **未解問題。** LLM 智能體是否能通往通用智能，以及從虛擬模擬環境走向實體環境的挑戰（第 6.5 節）。

## 相關連結

- [ReAct](../../../engineering/agents/react.md) 把推理與行動交錯進行，是實現大腦與行動模組的一種方式。
- [Toolformer](../../../engineering/agents/toolformer.md) 與 [Voyager](../../../engineering/agents/voyager.md) 是框架中行動與工具使用部分的具體系統。
- [Reflexion](../../../engineering/agents/reflexion.md) 把來自環境的回饋加入智能體迴圈。
- [思維鏈提示](../reasoning/chain-of-thought.md) 是許多 LLM 智能體所依賴的推理技術。
- [間接提示注入](../../../engineering/llm-security/indirect-prompt-injection.md) 描述智能體讀取不可信內容時出現的安全風險。

## 應用

綜述所列的應用包括軟體開發、科學研究，以及其他需要工具與多步驟規劃的任務（第 2.2 與 4 節）。它的框架適用於任何必須決策、使用工具並跨多個步驟行動的語言模型系統。

## 未解問題

- 如何同時評估智能體的效用與社交性，並衡量它們所依據的價值觀。
- 以 LLM 為大腦是否足以實現通用智能，還是需要其他組件。

## 參考文獻

### 開創性論文

- Xi, Z., Chen, W., Guo, X. et al. (2023). *The Rise and Potential of Large Language Model Based Agents: A Survey*. arXiv. https://arxiv.org/abs/2309.07864 — 提出 LLM 智能體的大腦、感知與行動框架的綜述，本頁討論的應用與未解問題即出自此文。
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — 在單一語言模型迴圈中，把推理軌跡與行動交錯進行。
- Schick, T. et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv. https://arxiv.org/abs/2302.04761 — 訓練語言模型自行決定何時、如何呼叫外部工具。
- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. arXiv. https://arxiv.org/abs/2303.11366 — 以語言式的強化學習，在多次嘗試之間改進智能體。
- Park, J. S. et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. arXiv. https://arxiv.org/abs/2304.03442 — 在互動情境中模擬人類行為的智能體，是大腦模組的一個例子。

### 綜述與相關工作

- Wang, G. et al. (2023). *Voyager: An Open-Ended Embodied Agent with Large Language Models*. arXiv. https://arxiv.org/abs/2305.16291 — 以大型語言模型進行開放式探索的具身智能體，是具身行動的例子。
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. arXiv. https://arxiv.org/abs/2302.12173 — 展示資料中隱藏的指令如何接管整合 LLM 的應用。
