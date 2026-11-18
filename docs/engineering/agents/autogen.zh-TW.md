---
status: draft
last_reviewed: 2026-11-18
translation_reviewed: 2026-11-18
related:
  - theory/models/agents
tags:
  - agents
  - multi-agent
  - conversation
aliases:
  - AutoGen
  - Microsoft AutoGen
  - Conversable agents
  - 對話式代理
  - 多代理對話
---

# AutoGen（Wu 等人，2023）

AutoGen 是一個用來建構語言模型應用程式的框架，其基礎是*可對話代理*（conversable agents）：這些代理彼此傳送訊息，而其回覆可以來自語言模型、人類、工具，或這些來源的組合。Wu 等人（2023）描述了此框架，並報告其在數學、問答、文字版家務任務與程式撰寫上的實驗。

本頁是[多代理編排模式](multi-agent-orchestration.zh-TW.md)中對話群組模式背後的命名方法之一。本頁也是[代理工程](index.zh-TW.md)的一部分。

## 概述

在這類框架出現之前，想讓數個模型合作的開發者，必須為每個應用手動撰寫訊息傳遞、發言順序與停止規則。AutoGen 把這些部分整理成可重複使用的元件。開發者只需調整程式碼中的設定或系統訊息，就能改變互動模式，而不必重寫控制流程。論文中的範例，以同一組代理型別處理差異很大的任務。

## 問題

許多實用任務同時需要多種能力：推理、執行程式、查詢文件，以及在資訊不足時詢問人類。論文要處理的問題，是如何在同一個應用中結合這些能力，而不為每種能力撰寫獨立的控制程式。它的問題是：在適當的角色與停止規則下，代理之間的對話能否完成原本需要客製化流水線才能完成的工作。

## 核心想法

每個代理都有角色，會接收訊息、從中保留上下文，並透過共同介面產生回覆（send、receive 與 generate_reply）。能力可以來自語言模型、人類、工具，或它們的組合。論文中的內建型別包括：

- **ConversableAgent**：基礎類別，預設可使用語言模型、人類與工具。
- **AssistantAgent**：由語言模型支援的代理，以系統訊息設定為撰寫程式與修正錯誤。
- **UserProxyAgent**：向人類索取輸入、執行其他代理提出的程式碼，並進行函式呼叫的代理。
- **GroupChatManager**：選出下一位發言者，並把其回覆廣播給其他代理。

代理收到訊息後會呼叫 generate_reply，並把回覆送回，除非終止條件成立。論文把這稱為去中心化機制：交流由代理自身的回覆推動，因此不需要獨立的控制層。開發者可以註冊自訂回覆函式，例如讓一個代理在回覆發送者之前，先諮詢另一個代理。

## 方程式或演算法

此程序是一個訊息迴圈，而非一條方程式：

1. 建立具有角色與能力的代理：模型、人類、工具或其組合。
2. 把初始訊息送給某一個代理。
3. 接收訊息的代理呼叫 generate_reply。這可能包括查詢模型、詢問人類、執行程式或呼叫函式。
4. 把回覆送給下一個代理。在群組對話中，管理者挑選下一位發言者並廣播回覆。
5. 重複上述步驟，直到終止條件成立：自動回覆次數達上限、程式碼中寫定的條件，或回覆中出現停止詞。論文中預設的助理提示要求代理在完成時回覆「TERMINATE」。

控制可以用自然語言、程式碼，或兩者並用。在程式碼中，開發者可設定終止條件、人工輸入模式、自動回覆次數上限與自訂回覆函式。靜態流程以固定順序安排代理；動態流程則使用自訂回覆函式、由模型選擇的函式呼叫，或 GroupChatManager。

## 結果

在 ALFWorld（文字版家務任務基準）上，論文報告的是三次嘗試平均的成功率。三代理的 ALFChat 設定達到 69%，兩代理設定為 54%，ReAct 為 54%。三次嘗試中取最佳者，結果分別為 77%、63% 與 66%。在逐任務表格中，三代理設定在「Pick 2」任務類型上得到 41%，ReAct 的平均值為 24%。

在 MATH 基準上，論文報告 AutoGen 在完整的 5,000 題測試集上達到 69.48%，而單獨的 GPT-4 為 55.18%。論文還報告了 Natural Questions 上的檢索增強問答情境、仿照 OptiGuide 式任務的程式撰寫情境、動態群組對話的試驗，以及西洋棋情境。其中 ALFWorld 與 MATH 的比較最有系統性，其餘則是較非正式測量的示範。

## 限制

- **評估範圍窄。**結果來自少數情境，主要使用 GPT-3.5 與 GPT-4 模型。多個情境是示範而非量測。
- **成本。**每個代理都會增加模型呼叫，長對話也會增加 Token。ALFWorld 的比較是對嘗試次數取平均，因此無法說明在相同 Token 預算下，這項增益與單一代理相比如何。
- **終止需要設計。**開發者必須設定自動回覆次數上限或終止條件，否則對話可能比預期更長。
- **人類監督是一項選擇。**人類輸入可以設定，論文建議在開發期間讓人類始終留在迴圈中。這個選擇需要開發者自行決定。
- **目前狀態。**AutoGen 專案的穩定版文件表示，該專案「已封存，不再由 Microsoft 積極維護」（於 2026-11-18 查核）。論文描述的是設計本身，因此採用軟體前應先確認其目前狀態。

## 關聯

- 固定角色流水線的替代方案是 [MetaGPT](metagpt.zh-TW.md)，它把每個角色綁定到預先定義的文件。
- ReAct 是 ALFWorld 比較中的單一代理基準，見 [ReAct](react.zh-TW.md)。
- 這些系統的對話紀錄，是[代理可觀測性](agent-observability.zh-TW.md)中追蹤所需的原始資料。
- 代理的一般框架見 [AI 代理](../../theory/models/agents/index.zh-TW.md)。

## 應用

- **程式撰寫助理**：一個代理撰寫程式，使用者代理執行它，錯誤則回傳給代理修改。
- **文件問答**：代理在作答之前，先提出後續的檢索問題。
- **人類監督的工作流程**：工具執行前，由人類核准每一步。

## 開放問題

- 多代理的增益有多少來自角色分工，又有多少來自額外的嘗試與 Token？
- 在開放式群組對話中，哪些終止規則仍然可靠？
- 哪些對話模式能推廣到不同任務，哪些只是針對單一基準調校？

## 參考文獻

### 開創性論文

- Wu, Q. 等人（2023）。*AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*。arXiv。https://arxiv.org/abs/2308.08155 — 此框架、其代理型別與對話程式設計模型，以及本頁所述的實驗。
- Yao, S. 等人（2023）。*ReAct: Synergizing Reasoning and Acting in Language Models*。ICLR。https://arxiv.org/abs/2210.03629 — 單一代理的推理與行動方法，作為 ALFWorld 上的基準。
- Shridhar, M. 等人（2020）。*ALFWorld: Aligning Text and Embodied Environments for Interactive Learning*。arXiv。https://arxiv.org/abs/2010.03768 — 論文比較所用的家務任務文字基準。
- Hong, S. 等人（2023）。*MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*。arXiv；發表於 ICLR 2024。https://arxiv.org/abs/2308.00352 — 具有固定中間文件的角色式框架，是以對話為基礎之設計的主要替代方案。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 涵蓋單一代理、多代理與人機代理情境的 LLM 代理綜述。

### 文章與文件

- Microsoft。*AutoGen documentation (stable)*。https://microsoft.github.io/autogen/stable/ — 專案官方文件，其中表示該專案已封存，不再積極維護。
