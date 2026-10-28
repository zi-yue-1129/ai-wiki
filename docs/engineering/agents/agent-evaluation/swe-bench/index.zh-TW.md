---
translation_reviewed: 2026-10-28
---

# SWE-bench：解決真實 GitHub 議題

SWE-bench（Jimenez et al., 2023）測試語言模型代理人能否修改真實的軟體儲存庫，使某個被回報的 GitHub 議題得到解決，並以專案自身的測試作為裁判。它是[代理人評估](../index.md)頁面中的三個里程碑式方法之一。

## 概述

軟體工程很適合用來評估代理人。這項工作需要閱讀龐大的程式碼庫、找出相關程式碼、編輯它、執行測試，並對失敗做出反應。早期的程式基準，例如 HumanEval，要求依照文件字串寫出單一函式（Chen et al., 2021）。這種測試檢驗的是生成能力，卻不涉及跨越整個專案的導覽。

SWE-bench 從 12 個熱門的 Python 儲存庫中收集了 2,294 個議題及其拉取請求（Jimenez et al., 2023）。模型會拿到議題文字，以及修復前狀態的儲存庫副本，並必須產生一項能通過專案測試的修改。

## 關鍵概念

- **議題**（issue）：使用者撰寫的錯誤回報或功能請求，後來由原始專案中的一個拉取請求解決。
- **基準提交**（base commit）：該拉取請求之前的儲存庫狀態。代理人從這裡開始。
- **補丁**（patch）：代理人產生的差異檔（diff），會套用到基準提交上。
- **FAIL_TO_PASS 測試**：修復前失敗、修復後必須通過的測試。
- **PASS_TO_PASS 測試**：修復前後都通過、且必須持續通過的測試。
- **解決率**（resolve rate）：兩組測試都符合要求的實例所占比例，是最主要的指標。

## 運作方式

評分遵循固定的程序：

1. 在基準提交上檢出儲存庫，並在隔離環境中安裝其相依套件。
2. 把議題文字與程式碼庫交給模型。在原始設定中，模型會在單一提示中收到從儲存庫檢索出的部分內容，並回傳一個補丁。之後的代理人系統則讓模型透過工具在迴圈中瀏覽儲存庫。
3. 收集模型產生的補丁。
4. 把補丁套用到基準提交上，並執行 FAIL_TO_PASS 與 PASS_TO_PASS 測試。
5. 只有當所有 FAIL_TO_PASS 測試通過，且沒有任何 PASS_TO_PASS 測試失敗時，才算該實例已解決。

這項檢查是自動且可重複的，但評分標準完全取決於測試的品質。

## 結果

論文的主要結果並不高。摘要報告，表現最好的模型 Claude 2 只解決了 1.96% 的議題，經過微調的 SWE-Llama 則只能解決最簡單的議題（Jimenez et al., 2023）。

之後的代理人系統在同一基準上的分數高出許多。SWE-agent 加入了專為編輯檔案、瀏覽儲存庫與執行測試而設計的自訂介面，它在 SWE-bench 上報告的 pass@1 為 12.5%（Yang et al., 2024）。這類分數取決於模型、框架與基準版本，因此只應在同一種協定之下比較。

評分錯誤也會改變結論。Aleithan et al. (2024) 檢視了通過測試的補丁，發現其中不少含有洩漏的解答或薄弱的測試。移除有問題的實例後，某個 SWE-agent 配置的解決率從 12.47% 降至 3.97%。[^1]

## 限制

- **範圍狹窄。** 所有實例都來自 Python 專案，而那 12 個儲存庫都是熱門的開源專案，其程式碼與討論在網路上廣為流傳。
- **測試薄弱。** 補丁可能通過並未真正檢驗行為的測試。Aleithan et al. 報告，他們檢視的通過補丁中，有 31.08% 因此而可疑。
- **解答洩漏。** 有些議題或留言中包含修復本身，因此模型可能只是照抄而成功。同一分析發現，成功的補丁中有 32.67% 涉及此問題。
- **資料汙染。** 超過 94% 的議題早於 LLM 的知識截止日期，因此模型在訓練時可能已見過它們（Aleithan et al., 2024）。
- **通過測試不等於可以合併。** 通過測試的補丁，仍可能因風格、範圍或設計而被維護者拒絕。

## 開放問題

- **穩健的評分。** 經過篩選的子集，例如 SWE-bench Verified，目的是提升品質，但 Zhu et al. (2025) 仍指出該子集的測試案例不足。能否在規模化下讓測試式評分變得穩健，尚無定論。
- **能力還是介面。** Yang et al. (2024) 顯示介面設計會改變結果。分數究竟衡量的是模型的工程能力，還是其工具的品質，很難分開。
- **其他語言與任務。** 在 Python 議題上的結果，未必能遷移到其他語言、功能請求，或大規模的系統變更。

## 參考文獻

### 奠基性論文

- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv. https://arxiv.org/abs/2310.06770 — 來自 12 個 Python 儲存庫、共 2,294 個議題的基準，由各專案自身的測試評分。
- Yang, J. et al. (2024). *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. arXiv. https://arxiv.org/abs/2405.15793 — 顯示自訂的代理人與電腦介面如何改變代理人在 SWE-bench 上的表現。
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — 提出 HumanEval，這是單一函式的基準，而 SWE-bench 將其擴展到整個儲存庫。

### 綜述與教科書

- Yehudai, A. et al. (2025). *Survey on Evaluation of LLM-based Agents*. arXiv. https://arxiv.org/abs/2503.16416 — 代理人評估的綜述，在應用基準中涵蓋軟體工程代理人。

### 文章與文件

- Aleithan, R. et al. (2024). *SWE-Bench+: Enhanced Coding Benchmark for LLMs*. arXiv. https://arxiv.org/abs/2410.06992 — 對 SWE-bench 的人工分析，發現成功補丁中有解答洩漏與測試薄弱的問題。
- Zhu, Y. et al. (2025). *Establishing Best Practices for Building Rigorous Agentic Benchmarks*. arXiv. https://arxiv.org/abs/2507.02825 — 報告 SWE-bench Verified 的測試案例不足，並為基準建構者提出檢查清單。

[^1]: Aleithan et al. (2024)，摘要，https://arxiv.org/abs/2410.06992 — 報告在移除有問題的實例後，使用 GPT-4 的 SWE-Agent 解決率從 12.47% 降至 3.97%。
