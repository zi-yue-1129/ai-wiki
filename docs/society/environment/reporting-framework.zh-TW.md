---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - 能源與排放的報告
  - Experiment Impact Tracker
  - 機器學習足跡的系統性報告
---

# 能源與排放的報告（Henderson 等人，2020）

!!! info "屬於 AI 的環境影響"
    本方法頁隸屬於 [AI 的環境影響](index.zh-TW.md)。它詳細說明一個框架；上層頁面則將它與其他做法並列比較。

Henderson、Hu、Romoff、Brunskill、Jurafsky 與 Pineau（2020）提出一個框架，用來在機器學習實驗執行期間追蹤其能源用量與碳排放，並以標準格式發布結果。他們用這個框架為節能強化學習建立了排行榜，並把它當作其他領域可以仿效的範例。

## 問題

要理解機器學習對氣候的影響，就需要準確報告能源與碳排放，但這種報告很少做。事後的估算依賴容易遺失的細節，而以不同方式報告的數字又無法互相比較。若沒有共同格式，想報告能源用量的研究者就得從頭建立量測方式。

## 核心想法

在實驗期間測量能源並估算排放，而不是事後才算，並把結果發布在標準化的線上附錄中。每份實驗都採用相同格式，使結果可以比較；把它們彙整在一處，也就能建立排行榜。

## 框架如何運作

1. **執行時追蹤。** 在實驗進行時記錄能源用量，並估算排放的碳量。
2. **標準化輸出。** 把數字發布在標準的線上附錄中，使各篇論文的報告格式一致。
3. **彙整結果。** 把報告收集成排行榜，讓讀者能同時比較方法的能源效率與表現。
4. **從案例研究中學習。** 透過案例研究，提出降低能源用量與排放的做法。

摘要描述了追蹤、標準化附錄與排行榜。能源如何量測並換算為排放的細節，則在論文中。

## 結果

摘要報告了這個框架、以它建立的節能強化學習排行榜，以及提出降低方法的案例研究。這是一個報告框架，因此它的成果是它所建立的做法，而不是一個可以與其他頁面估算相比較的單一數字。

## 限制

- **取決於量測。** 能源讀數取決於可用的硬體與工具，碳排放數字則取決於當地電網碳強度的估算。
- **第一個案例範圍狹窄。** 排行榜是為強化學習建立的。其他領域可能需要不同的指標與格式。
- **採用率。** 標準附錄只有在研究者實際填寫時才有用，而數字的可查核程度，也受限於報告內容本身。

## 與其他主題的連結

- 較早的計算工具只以三個輸入估算、不追蹤執行過程，見[排放計算器](emissions-calculator.zh-TW.md)頁面。
- 要求把成本與準確度並列報告的主張，見[綠色 AI](green-ai.zh-TW.md)頁面。
- 降低這類報告所揭露的能源用量的做法，見[節能訓練](energy-efficient-training.zh-TW.md)。

## 開放問題

- 能源與碳排放應如何在不同硬體與雲端供應商之間一致地量測？
- 誰應該查核研究者所報告的數字？
- 這種報告格式如何延伸到強化學習以外的領域？

## 參考資料

### 開創性論文

- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — 本頁所述的框架，用於追蹤並以標準格式報告能源與碳排放。
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2019). Green AI. arXiv:1907.10597. https://arxiv.org/abs/1907.10597 — 主張應報告研究成本並將其列為評估標準，而這個框架使這項主張得以實行。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — 以三個輸入估算排放，不在訓練期間追蹤執行過程。
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — 事後才做的早期成本估算，說明為何在執行期間量測很重要。
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — 顯示這類報告所記錄的各項因素，能使碳足跡改變多少。
