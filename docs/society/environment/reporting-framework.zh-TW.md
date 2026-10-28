---
translation_reviewed: 2026-10-28
---

# 能源與碳排的報告（Henderson 等人，2020）

!!! info "屬於「AI 的環境影響」"
    本方法頁隸屬於[AI 的環境影響](index.zh-TW.md)。它詳細說明一個框架；上層頁面則比較各個框架。

Henderson、Hu、Romoff、Brunskill、Jurafsky 與 Pineau（2020）提出一個框架，用來在機器學習實驗執行期間追蹤其能源使用與碳排放，並以標準格式發表結果。這個工具名為 Experiment Impact Tracker。作者利用收集到的結果，建立了節能強化學習的排行榜。

## 問題

準確報告能源與碳排放，對於理解機器學習的氣候影響十分必要，但這件事卻很少做。事後估算依賴的細節很容易遺失，而以不同方式報告的數字又無法相互比較。若沒有共同的格式，想報告能源使用的研究者就得從頭建立測量方法。

## 核心概念

在實驗進行期間測量能源並估算排放，而不是事後才算，並以標準形式發表。所有實驗採用相同格式，使結果可以比較；把結果集中在一處，則可以在能源與效能兩方面為方法排名。

## 框架的運作方式

1. **執行時追蹤。** 追蹤工具只需要稍微修改程式碼。它會記錄硬體、程序的開始與結束時間、CPU 與 GPU 的耗電，以及機器所在的電網區域。
2. **估算碳排。** 以各區域的平均碳強度把能量換算為排放。即時碳強度目前只支援加州。
3. **標準化輸出。** 以二氧化碳當量的形式，在標準的線上附錄與「碳影響聲明」中發表數字。
4. **收集並排名。** 深度強化學習能源排行榜，以每千瓦時的平均回報排名強化學習方法，涵蓋 Pong 與 Breakout 兩款遊戲，方法包括 PPO、A2C、帶 V-trace 的 A2C 與 DQN。

論文的主要例子是，一班 235 名學生各自執行五次 Pong。若改用 PPO 而非 DQN，可節省 888 kWh。作者也建議，雲端工作應盡可能使用低碳地區。

## 結果

框架本身就是結果。論文報告了追蹤工具、排行榜，以及提出降低能耗與排放方法的案例研究。排行榜顯示，沒有單一演算法在兩款遊戲都領先：A2C 搭配 V-trace 在 Pong 排名第一，PPO 則在 Breakout 排名第一。

## 限制

- **依賴驅動程式。** 功率讀數需要硬體與驅動程式的支援。並非所有晶片組都支援 Intel RAPL 介面，而在 Docker 容器內的每程序 GPU 讀數也不受支援。目前只涵蓋 macOS 與 Linux 上的 Intel RAPL 或 PowerGadget 系統。
- **區域平均值。** 碳排數字是區域供電的平均值。雲端供應商購買的潔淨能源，可能不會反映在這些數字中，而作者找不到此類情況下的即時能源結構資料。
- **封閉的資料來源。** 區域碳強度的備用數值來自一個封閉原始碼的系統，這限制了數字能被驗證的程度。
- **初始案例狹窄。** 排行榜只涵蓋兩款 Atari 遊戲的強化學習。其他領域可能需要不同的衡量標準與格式。
- **採用情況。** 標準附錄只有在研究者實際填寫時才有用。

## 與其他頁面的連結

- 只用三項輸入估算、不追蹤執行過程的較早計算器，見[機器學習排放計算器](emissions-calculator.zh-TW.md)。
- 把成本與準確度並列報告的論點，見[綠色 AI](green-ai.zh-TW.md)。
- 這類報告所揭露的能耗，可以如何降低，見[節能訓練](energy-efficient-training.zh-TW.md)。

## 開放問題

- 應如何在不同硬體與雲端供應商之間一致地測量能源與碳排？
- 誰應該查核研究者所報告的數字？
- 報告格式如何延伸到強化學習以外的領域？

## 參考文獻

### 開創性論文

- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248), 1–43。https://www.jmlr.org/papers/v21/20-312.html — 本頁所述的框架、Experiment Impact Tracker 與排行榜。預印本：https://arxiv.org/abs/2002.05651
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2020). Green AI. *Communications of the ACM*, 63(12), 54–63. doi:[10.1145/3381831](https://doi.org/10.1145/3381831) — 主張應報告研究成本，並將其列為評估標準，而此框架使這件事變得可行。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv 預印本。https://arxiv.org/abs/1910.09700 — 只用三項輸入估算排放，不在訓練期間追蹤執行過程。
- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — 事後才做的較早成本估算，說明了為何需要在執行中測量。
- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv 預印本。https://arxiv.org/abs/2104.10350 — 顯示此類報告所記錄的各項因素能使足跡改變多少。
