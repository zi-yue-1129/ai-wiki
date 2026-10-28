---
translation_reviewed: 2026-10-28
---

# 運算治理與出口管制

運算治理嘗試透過訓練與執行模型所需的硬體與基礎設施來管理 AI。其主要工具包括：對先進晶片的出口管制、以訓練運算量為基礎的門檻，以及對出租運算能力的雲端供應商進行的身分查核。

!!! info "屬於法律、政策與治理"
    本頁隸屬於[法律、政策與治理](index.md)。它詳細說明一種政策取徑；上層頁面則涵蓋更廣的法律情勢。

## 概述

多數 AI 政策針對的是模型、資料或使用方式。運算治理則更往前一步，著眼於建構高能力模型所需的實體資源。其論點是：運算量比資料或演算法更容易觀察、衡量與控制。它可以被偵測、被限制、被計數，而且其生產仰賴少數幾家企業與國家。Sastry 等人（2024）詳細提出了這個論點，也列出了以運算作為政策槓桿的風險。

## 關鍵概念

- **出口管制**：對特定國家或使用者寄送指定商品、軟體或技術的法律限制。套用到 AI 上，它涵蓋先進的加速晶片與晶片製造設備，在部分提案中也涵蓋雲端運算的存取。
- **訓練運算量**：訓練一個模型所用的算術運算總數，通常以浮點運算次數（FLOP）計量。Heim 與 Koessler（2024）將它描述為監管機關用來決定哪些模型需要監督的指標。
- **運算門檻**：訓練運算量的一個數值，超過此值的模型便會觸發通報、回報或推定具較高風險等義務。
- **認識你的客戶（KYC）**：服務供應商用來核實客戶身分並保存紀錄的程序。Egan 與 Heim（2023）提議將銀行業的這套做法套用到運算供應商身上。

## 運作方式

運算治理透過三種槓桿發揮作用。

1. **限制供給。** 出口管制限制某國可以購買哪些晶片，以及可以購買哪些製造晶片的工具。Gupta 等人（2024）將美國的策略描述為：試圖讓先進加速晶片無法流向中國的 AI 開發者。[AI 硬體](../../engineering/hardware/index.md)頁面說明了使這一手段成為瓶頸的供應鏈：少數設計商、少數代工廠與少數設備商。
2. **設定門檻。** 法律定出一個訓練運算量的水準，超過即觸發額外義務。Heim 與 Koessler（2024）主張，訓練運算量目前是最適合作為此種篩選條件的指標，因為它與能力相關、可在模型生命週期早期衡量，並可由外部人士查核。它只是風險的不完美代理指標，因此應用來啟動審查，而非取代審查。
3. **監測與識別使用者。** Shavit（2023）提議，晶片韌體可以為檢查人員保存模型權重的快照，並可監控晶片供應鏈，使任何行為者都無法在未被追蹤的情況下累積大量晶片，同時不限制消費性裝置。知情客戶機制則增加了另一步驟：供應商在授予存取權之前，先確認客戶的身分。

這些槓桿之所以一再被提出，是因為運算量成長迅速。Sevilla 等人（2022）發現，深度學習興起後，訓練運算量大約每六個月倍增一次。[^1] 一個固定在某一水準的門檻，會隨時間變得愈來愈不具選擇性，這也是運算門檻備受爭議的原因之一。

## 關鍵方法

以下四種手段做了簡要比較。多數實際政策會結合數種手段。

| 手段 | 針對對象 | 主要優點 | 主要弱點 |
|---|---|---|---|
| 晶片出口管制（Gupta 等人，2024） | 晶片供應商與境外買家 | 作用於集中的供應鏈 | 流出受管制市場的晶片與效率提升會削弱其效果 |
| 運算門檻（Heim 與 Koessler，2024） | 訓練大型模型的開發者 | 可在模型部署前衡量 | 是能力與風險的代理指標；節省運算的技術可能規避它 |
| 硬體支持的驗證（Shavit，2023；Brundage 等人，2020） | 晶片、韌體及其持有者 | 讓外部人士得以查核關於訓練的主張 | 多數仍處於設計階段；引發隱私與成本的疑慮 |
| 運算供應商的知情客戶機制（Egan 與 Heim，2023） | 雲端運算的客戶 | 可顯示誰在使用運算，並可暫停存取 | 需要動態門檻、紀錄保存與政府能力 |

## 與其他主題的連結

- 使出口管制成為可能的硬體供應鏈，見 [AI 硬體](../../engineering/hardware/index.md)。
- 門檻依賴「訓練運算量與能力相關」這個想法。其經驗面見[縮放定律與湧現能力](../../theory/models/llm/scaling-laws/index.md)。
- 開放權重一旦下載便難以控制，這也是政策制定者轉而關注運算的原因之一。見[開源與封閉模型](../open-vs-closed/index.md)。
- 神經形態與類比硬體計算的是事件或物理量，而非密集算術。目前尚不清楚以 FLOP 為基礎的門檻如何適用於這類系統；見[脈衝神經網路與神經形態運算](../../brain-mind/snn-neuromorphic/index.md)。

## 應用

- **出口許可。** 向受限目的地銷售晶片需要政府核發許可。Gupta 等人（2024）檢視了這套制度在一個案例中的成效：一款為符合規定而設計的晶片之銷售情況。
- **大型訓練的回報制度。** Pistillo 與 Villalobos（2025）描述了，一項 2023 年的美國行政命令如何指示商務部，要求超過某訓練運算量門檻之模型的開發者進行回報，以及歐盟 AI 法如何推定此類模型具有系統性風險。[^2] 該行政命令之後已遭撤銷，因此目前的美國情勢應查閱[上層頁面](index.md)。

## 開放問題

- 隨著演算法效率提升，以及模型在推論時使用更多運算，運算門檻能否維持其意義？
- 驗證能否在不揭露開發者的資料、權重或超參數的前提下進行？
- 雲端運算的遠端使用，是否應與晶片銷售一樣納入存取管制？

### 批評

- **門檻目光短淺。** Hooker（2024）主張，依現有方式實施的運算門檻不太可能降低風險，因為運算與風險之間的關係不確定且持續變動。
- **門檻有漏洞。** Pistillo 與 Villalobos（2025）指出，微調、模型重用、模型擴展與額外的推論運算，都可能在使用較少訓練運算量的同時提升模型能力，使開發者得以維持在門檻以下。
- **出口管制容易被繞過。** Gupta 等人（2024）提出證據，指出中國的實驗室已取得受管制的晶片，並運用軟體與建模技術，從較弱的硬體中榨取更多效能。其論點集中於一家公司的一個模型，因此應視為一個有力的主張，而非定論。
- **範圍過廣的代價。** Sastry 等人（2024）警告，範圍設計不當的運算治理，會對隱私、經濟活動，以及權力集中於少數行為者等方面帶來風險。

## 參考資料

### 開創性論文

- Sastry, G. et al. (2024). *Computing Power and the Governance of Artificial Intelligence*. arXiv preprint. https://arxiv.org/abs/2402.08797 — 主張運算是 AI 治理中切實可行的介入點，並列出其用途與風險。
- Shavit, Y. (2023). *What does it take to catch a Chinchilla? Verifying Rules on Large-Scale Neural Network Training via Compute Monitoring*. arXiv preprint. https://arxiv.org/abs/2303.11341 — 提出硬體層級的監測，使政府能查核大型訓練運行的規則。
- Brundage, M. et al. (2020). *Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims*. arXiv preprint. https://arxiv.org/abs/2004.07213 — 分析十種機制（包括以硬體為基礎者），使關於 AI 系統的主張可以被查核。
- Heim, L. & Koessler, L. (2024). *Training Compute Thresholds: Features and Functions in AI Regulation*. arXiv preprint. https://arxiv.org/abs/2405.10799 — 主張訓練運算量適合作為監管監督的篩選條件，且不應單獨使用。
- Egan, J. & Heim, L. (2023). *Oversight for Frontier AI through a Know-Your-Customer Scheme for Compute Providers*. arXiv preprint. https://arxiv.org/abs/2310.13625 — 提議由運算供應商執行客戶身分核實，並討論由此產生的設計問題。
- Sevilla, J. et al. (2022). *Compute Trends Across Three Eras of Machine Learning*. arXiv preprint. https://arxiv.org/abs/2202.05924 — 衡量機器學習歷史上訓練運算量的成長，是以運算為基礎之政策背後的趨勢資料。

### 文章與官方文件

- Hooker, S. (2024). *On the Limitations of Compute Thresholds as a Governance Strategy*. arXiv preprint. https://arxiv.org/abs/2407.05694 — 質疑訓練運算量能否預測風險的隨筆，並提出更好的做法。
- Pistillo, M. & Villalobos, P. (2025). *Defending Compute Thresholds Against Legal Loopholes*. arXiv preprint. https://arxiv.org/abs/2502.00003 — 檢視可讓開發者規避美國與歐盟法律中門檻的節省運算技術。
- Gupta, R., Walker, L. & Reddie, A. W. (2024). *Whack-a-Chip: The Futility of Hardware-Centric Export Controls*. arXiv preprint. https://arxiv.org/abs/2411.14425 — 以中國開發者規避晶片出口管制為案例研究，並評估此策略。

[^1]: Sevilla 等人（2022）分別報告了各時期的倍增時間；此處引用的是深度學習時代的數字，確切估計值取決於所用的模型樣本。
[^2]: 歐盟的推定與美國的回報義務，皆以訓練運算量作為參照。確切數值見法律條文本身；應對照各法律的現行版本核對。
