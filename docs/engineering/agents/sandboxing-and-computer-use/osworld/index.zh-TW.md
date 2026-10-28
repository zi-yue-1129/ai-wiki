---
translation_reviewed: 2026-10-28
---

# OSWorld：在真實環境中評測電腦操作代理人

OSWorld（Xie et al., 2024）是一個以執行結果為依據的環境與基準，用於評測操作真實電腦的代理人。每項任務都在可還原至已儲存狀態的虛擬機中執行，代理人看見螢幕，並以滑鼠與鍵盤行動。它是 [沙箱與電腦操作代理人](../index.md)頁面中三個里程碑方法之一，也是該頁中以螢幕截圖為基礎的代理人的參考點。

## 概述

作者認為，既有的基準要不是缺乏互動環境，就是侷限於特定應用程式或領域。真實的電腦工作會在不同應用程式與檔案之間移動，因此只針對單一應用程式的測試會漏掉很多內容。

OSWorld 提供一個真實的作業系統（主要基準使用 Ubuntu），並把每項任務定義為起始設定、指令與評估腳本三部分。評估腳本會檢查最終狀態（例如檔案或 cookie）來判定成功，因此只在文字上看起來正確的答案不算數。

## 關鍵概念

- **虛擬機快照（virtual machine snapshot）**：作業系統的已儲存狀態，可在每次執行前還原。論文指出，虛擬機能防止代理人的行動對真實主機造成不可逆的損害。
- **觀察（observation）**：代理人接收到的內容。OSWorld 允許使用螢幕截圖、無障礙（a11y）樹狀結構，或兩者並用。
- **行動空間（action space）**：可執行的 `pyautogui` 程式碼，使代理人能點擊、輸入、拖曳與按下組合鍵，另外加上三個特殊行動：WAIT、FAIL 與 DONE。
- **執行結果評估（execution-based evaluation）**：依每項任務撰寫的腳本，檢查機器的最終狀態，而不是把文字與參考答案比對。
- **GUI 定位（GUI grounding）**：把視覺上的目標轉換為螢幕上的精確座標。論文指出這是主要的失敗來源。

## 運作方式

互動迴圈如下：

1. 從快照還原虛擬機，並套用任務設定，例如下載檔案或開啟應用程式。
2. 把指令與第 $t$ 步的觀察交給代理人，即螢幕截圖 $o_t$、無障礙樹狀結構，或兩者。
3. 代理人輸出一段 `pyautogui` 程式碼，或 WAIT、FAIL、DONE 其中之一。
4. 模擬器在虛擬機中執行程式碼，並回傳新的狀態與觀察 $o_{t+1}$。
5. 重複第 2 至 4 步，直到代理人輸出 DONE 或 FAIL，或達到步數上限。論文實驗中的上限為 15 步。
6. 任務的評估腳本檢查機器狀態，並給予 0 到 1 之間的分數。

基準包含 Ubuntu 上的 369 項任務，涵蓋網頁與桌面應用程式、檔案輸入與輸出，以及跨多個應用程式的工作流程。另外提供 43 項 Windows 任務作為分析用途。

## 結果

- **整體。** 人類完成超過 72% 的任務。所測試的最佳模型達到 12.24%。以上數字取自論文摘要。
- **跨應用程式工作流程。** 依論文引言，這類任務中基線代理人的最高分數為 6.57%。
- **觀察設定。** 以 GPT-4V 為例，只用螢幕截圖的設定整體結果最低，為 5.26%。加入無障礙樹狀結構或 Set-of-Mark 標註，對某些模型有幫助，對另一些則有害。
- **輸入大小與歷史。** 較高的螢幕截圖解析度與較長的軌跡歷史，都能改善結果；論文指出，在某些設定下這些因素可使成功率大約加倍。
- **失敗分析。** 模型難以從螢幕截圖預測精確座標，會重複行動，容易被意外出現的視窗干擾，並且缺乏基本介面慣例的知識。

數字取自論文摘要與表格，描述的是 2024 年的模型，之後的系統已有所改進。

## 限制

- **桌面輸入限定。** 行動空間只包含滑鼠與鍵盤事件，因此行動裝置上的觸控手勢不在此基準範圍內。
- **步數上限。** 15 步的上限可能會中斷某些人類能夠完成的任務，不過作者表示，這個步數對大多數任務已經足夠。
- **平台偏向。** 主要基準在 Ubuntu 上執行，Windows 的任務集較小，且僅用於分析。

## 開放問題

- **定位。** 人與模型之間的差距在於找出元素的部分最大。更高解析度的視覺、更好的訓練，或與結構化介面資料的結合，能否縮小這個差距，尚未解決。
- **安全性。** 在虛擬機中執行的基準可以在沒有真實損害的情況下測試危險行動，但部署在個人電腦上的代理人沒有這層保護。
- **泛化。** 在固定的 369 項任務上的成功，未必代表在未見過的應用程式上的表現。作者的未來工作清單主要集中在 GUI 定位、互動知識與更高解析度的輸入。

## 參考文獻

### 奠基性論文

- Xie, T. et al. (2024). *OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments*. arXiv. https://arxiv.org/abs/2404.07972 — 提出以執行結果為依據的環境與基準，包含跨作業系統的 369 項電腦任務，並附有逐項評估腳本。
- Zhou, S. et al. (2023). *WebArena: A Realistic Web Environment for Building Autonomous Agents*. arXiv. https://arxiv.org/abs/2307.13854 — 為網頁代理人提供可自行架設、可重現的網站，是 OSWorld 沙箱化做法在瀏覽器上的前身。
- Koh, J. Y. et al. (2024). *VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks*. arXiv. https://arxiv.org/abs/2401.13649 — 面向需要螢幕截圖之網頁代理人的視覺基準，OSWorld 的標註截圖設定沿用其做法。
- Hong, W. et al. (2023). *CogAgent: A Visual Language Model for GUI Agents*. arXiv. https://arxiv.org/abs/2312.08914 — 視覺語言模型，僅依螢幕截圖即可在 PC 與 Android 介面中導覽。

### 綜述與教科書

- Wang, L. et al. (2023). *A Survey on Large Language Model based Autonomous Agents*. arXiv. https://arxiv.org/abs/2308.11432 — LLM 代理人綜述，將電腦操作代理人置於感知、記憶與行動模組的更廣脈絡中。

### 文章與文件

- Anthropic (2024). *Computer use, Claude 3.5 Sonnet, and Claude 3.5 Haiku*. Anthropic News. https://www.anthropic.com/news/3-5-models-and-computer-use — 宣布測試版，模型讀取螢幕截圖並回傳滑鼠與鍵盤行動，由開發者的軟體執行。
- Anthropic (n.d.). *Computer use tool*. Claude Platform documentation. https://docs.claude.com/en/docs/agents-and-tools/tool-use/computer-use-tool — 說明螢幕截圖與行動的迴圈，並建議在隔離環境中執行。
