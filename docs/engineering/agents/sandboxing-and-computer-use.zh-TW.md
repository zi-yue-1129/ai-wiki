---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - agents
  - security
  - computer use
aliases:
  - Sandboxing
  - Computer-Use Agents
  - Computer Use
  - 沙箱
  - 電腦操作代理
---

# 沙箱與電腦操作代理

電腦操作代理（computer-use agent）會像人一樣操作軟體：讀取畫面，並送出點擊、按鍵與捲動。沙箱（sandboxing）則限制這類代理能觸及的範圍，使一次錯誤或一次攻擊無法擴散到任務之外。

本頁是[代理工程](index.zh-TW.md)的一部分。

## 概述

許多任務沒有 API。電腦操作代理仍能處理這些任務，方法是觀察畫面，並透過人會使用的同一種輸入裝置行動。同樣的能力也意味著，代理可能讀取私人檔案、傳送訊息並更改設定。沙箱就是讓這些能力保持在任務範圍內的一組控制。

## 關鍵概念

- **電腦操作迴圈：**代理觀察截圖或無障礙樹狀結構，模型選擇一個行動，執行該行動，然後觀察新的狀態。
- **沙箱：**隔離的執行環境，通常是容器或虛擬機器，擁有自己的檔案系統與程序。
- **最小權限：**只授予任務所需的檔案、帳號與網路存取。
- **出站允許清單：**沙箱可以連線的網路目的地清單。
- **限定範圍的短期憑證：**只適用於單一任務、並在短時間內過期的存取權杖。
- **確認步驟：**在不可逆的行動（例如付款或刪除）之前，由人類核准。

## 運作方式

典型的部署會結合數個層次。代理在虛擬機器或容器中執行，使當機或惡意行動只影響該執行個體。它的檔案系統限於工作目錄，網路存取則經過允許清單。憑證為該次工作階段發出，之後撤銷。每個行動與截圖都會被記錄，讓審查者能重建發生的事，並有一個可以停止執行的緊急開關。

透過畫面控制也很慢，且容易出錯。版面的小變化、彈出視窗與意外的對話框，都可能使代理偏離方向，因此迴圈通常會在採取下一步之前檢查每個行動的結果。

## 評估電腦操作代理

OSWorld（Xie 等人，2024）提供真實的電腦環境，讓多模態代理嘗試開放式任務，而不是侷限於單一應用程式的任務。WebArena（Zhou 等人，2023）則為網頁代理提供四個領域中寫實且可重現的網站。兩者都用來衡量代理能否完成任務，也顯示目前的代理距離可靠使用還有多遠。見[代理評估](agent-evaluation.zh-TW.md)。

## 安全

畫面內容是不受信任的。代理所看到的網頁、電子郵件或文件，可能含有代理可能遵循的指令，這就是 Greshake 等人（2023）所描述的間接提示注入風險。模型上下文協定（MCP）規範對工具也提出相同原則：使用者必須理解並同意工具會做什麼，主機在呼叫工具前必須取得明確同意（見[工具呼叫與 MCP](tool-calling-and-mcp.zh-TW.md)）。

實務上的防禦包括限制代理的權限、在提示中把指令與被觀察的內容分開、對不可逆行動要求確認，以及監控執行過程（見[LLM 應用安全](../llm-security/index.zh-TW.md)）。

## 限制

- **基準只涵蓋部分的真實使用。**基準環境是它所模擬軟體的簡化副本。
- **沙箱可能不完善。**沙箱本身的缺陷，或權限授予過寬，都會使保護失效。
- **感知錯誤。**代理可能誤讀畫面，尤其是小字或密集文字。
- **成本與延遲。**每一步都需要一次模型呼叫與一張新的截圖。

## 關聯

- 代理的一般框架，見[AI 代理](../../theory/models/agents/index.zh-TW.md)。
- 建立在模型上的應用程式安全，見[LLM 應用安全](../llm-security/index.zh-TW.md)。
- 傳統安全實務，例如威脅建模與隔離，見[網路安全](../../applications/cybersecurity/index.zh-TW.md)。

## 應用

- **軟體測試**：透過使用者介面執行腳本化流程。
- **在沒有 API 的舊系統中填寫表單**。
- **無障礙輔助**：代理代表有動作或視覺障礙的使用者操作介面。OSWorld 的作者即以無障礙與生產力作為這類代理的動機。

## 開放問題

- 哪些權限可以安全地授予，又該如何向使用者呈現？
- 代理能否可靠地分辨畫面上的指令與資料？
- 大規模運行沙箱的成本，應如何納入評估？

## 參考文獻

### 開創性論文

- Xie, T. 等人（2024）。*OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments*。arXiv。https://arxiv.org/abs/2404.07972 — 用於評估多模態代理在開放式任務上表現的可擴展真實電腦環境。
- Zhou, S. 等人（2023）。*WebArena: A Realistic Web Environment for Building Autonomous Agents*。arXiv。https://arxiv.org/abs/2307.13854 — 用於建構與測試網頁代理的四個領域可重現網站。
- Greshake, K. 等人（2023）。*Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*。arXiv。https://arxiv.org/abs/2302.12173 — 顯示應用程式處理的內容可能夾帶模型會遵循的指令。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，涵蓋其建構方式、應用與待解挑戰。

### 文章與文件

- Model Context Protocol。*Specification, revision 2025-06-18*。https://modelcontextprotocol.io/specification/2025-06-18 — 說明代表使用者行動之代理所適用的同意與工具安全原則。
