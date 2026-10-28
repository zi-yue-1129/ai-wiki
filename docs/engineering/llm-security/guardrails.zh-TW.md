---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - security
  - safety
  - filtering
aliases:
  - Guardrails
  - Output Filtering
  - Content Moderation
  - 護欄
  - 輸出過濾
---

# 護欄與輸出過濾

護欄（guardrails）是放在語言模型周圍的檢查。它們篩選送入模型的內容與模型輸出的內容，依據政策對內容分類，或把對話限制在一組允許的路徑中。它們是系統層的控制，與模型內部的安全訓練相互補充。

本頁是[LLM 應用安全](index.zh-TW.md)的一部分。

## 概述

訓練模型拒絕有害請求會改變模型的行為，但這種行為並不保證。需要更強控制的應用程式，會在模型之外加上獨立的檢查。檢查可以放在輸入端、輸出端，或模型可以採取的行動上。由於護欄可能在兩個方向上出錯，它的設計是在阻擋危害與阻擋正當用途之間的取捨。

## 關鍵概念

- **輸入護欄：**對使用者或檢索內容送入模型之資料的檢查。
- **輸出過濾器：**在模型回傳給使用者或工具之前，對其輸出的檢查。
- **分類器護欄：**經訓練、依風險分類法為內容加上標籤的模型。
- **可程式化的護欄（rails）：**定義允許主題、對話路徑或回應風格的規則。
- **結構性控制：**不依賴判讀文字的限制，例如工具的允許清單或確認步驟。

## 運作方式

典型的流程會先篩選輸入，把通過的輸入交給模型，再篩選輸出，最後回傳安全的回覆或拒絕。分類器護欄本身也是語言模型。Inan 等人（2023）描述 Llama Guard，這是一個以 LLM 為基礎、同時針對提示與回應的安全防護模型，其核心是一套安全風險分類法。Rebedea 等人（2023）描述 NeMo Guardrails，這是一套工具組，開發者以可程式化的護欄控制對話系統的主題、對話路徑與輸出。

結構性控制可以補充分類器。一個在沒有確認步驟時無法寄送電子郵件的代理，即使分類器漏掉了寄信的指令，仍然受到保護。

## 限制

- **適應性攻擊者。**護欄是以已知攻擊測試的，新的措辭可能通過它們。見[越獄與紅隊測試](jailbreaks-and-red-teaming.zh-TW.md)。
- **兩個方向的錯誤。**嚴格的過濾器會擋下正當內容，寬鬆的過濾器則會漏掉危害。
- **間接內容。**只檢查使用者訊息的護欄，看不到藏在檢索文件中的指令。Greshake 等人（2023）描述了整合應用程式中的這種情況。
- **延遲與成本。**每次檢查都增加一次呼叫，而分類器護欄本身也是需要運行與維護的模型。
- **護欄不等於訓練。**護欄從模型之外過濾行為。模型自身的無害性訓練，見[Constitutional AI](../../society/safety-alignment/index.zh-TW.md)，是另一層。

## 關聯

- 護欄所針對的威脅模型，見[LLM 應用安全](index.zh-TW.md)。
- 拒絕行為及其失敗，見[越獄與紅隊測試](jailbreaks-and-red-teaming.zh-TW.md)。
- 以模型層訓練達成無害性，見[安全與對齊](../../society/safety-alignment/index.zh-TW.md)。

## 應用

- 必須保持在主題內、並避免不安全建議的客服聊天系統。
- 在使用語言模型的平台上，審查使用者產生的內容。
- 限制模型可存取資料與行動的企業助理。

## 開放問題

- 對特定應用，護欄的誤判率應如何設定？
- 分類器護欄能否在不必每次重新訓練的情況下，對適應性攻擊保持穩健？

## 參考文獻

### 開創性論文

- Inan, H. 等人（2023）。*Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations*。arXiv。https://arxiv.org/abs/2312.06674 — 針對提示與回應的分類器安全防護，其核心是一套安全風險分類法。
- Rebedea, T. 等人（2023）。*NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails*。arXiv。https://arxiv.org/abs/2310.10501 — 加入可程式化護欄的工具組，用以控制 LLM 應用程式的主題、對話路徑與輸出。
- Bai, Y. 等人（2022）。*Constitutional AI: Harmlessness from AI Feedback*。arXiv。https://arxiv.org/abs/2212.08073 — 依書面原則進行自我改進，以訓練無害的助理，是外部護欄之外的模型層替代方案。
- Greshake, K. 等人（2023）。*Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*。arXiv。https://arxiv.org/abs/2302.12173 — 顯示檢索內容中的指令如何繞過對使用者訊息的輸入檢查。
- Wei, A.、Haghtalab, N. 與 Steinhardt, J.（2023）。*Jailbroken: How Does LLM Safety Training Fail?*。arXiv。https://arxiv.org/abs/2307.02483 — 分析安全訓練為何可能失敗，這與外部護欄需要承擔多少工作有關。
