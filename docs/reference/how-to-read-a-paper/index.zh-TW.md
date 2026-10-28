---
translation_reviewed: 2026-10-28
---

# 如何閱讀 AI 論文

一篇研究論文會提出主張，讀者的工作是看清證據支持其中哪些部分。本頁說明機器學習論文通常如何編排、一個能讓主要主張清楚浮現的閱讀順序，以及如何檢查基線、測試資料、隨機種子與程式碼，判斷一個亮眼的結果是否可能站得住腳。

## 概述

大多數 AI 研究首先以論文的形式送到讀者面前，常見的情況是先張貼在 arXiv，之後再於會議或期刊正式發表（見[會議與期刊](../venues/index.zh-TW.md)）。論文是一種論證。它主張某個方法在效能、速度或清晰度上勝過以往的方法，並以表格、圖表，以及越來越常見的程式碼來支持這項主張。讀者要決定接受這份論證多少，以及為了什麼目的而接受。

閱讀論文的能力很少被正式教授。Keshav（2007）提出一套實用的三遍閱讀法，本頁的建議即建立在其上，並補充機器學習論文常需要的檢查項目。目的不在於挑出每篇論文的毛病，而在於知道哪些主張有充分支持，哪些只是被暗示。

## 核心概念

- **主張（Claim）**：論文希望讀者接受的陳述，例如「我們的方法在基準 X 上勝過先前最好的方法」。
- **基線（Baseline）**：新方法所比較的對象。若基線較弱或調校不足，即使只有小幅進步，看起來也會很大。
- **消融實驗（Ablation）**：移除或改動某個組件後進行的實驗，用來說明哪一部分的設計產生了進步。
- **隨機種子與變異（Seed and variance）**：類神經網路的結果取決於隨機初始化、資料順序與硬體雜訊。單次實驗只是可能結果分布中的一個樣本。
- **資料污染（Contamination）**：測試題目，或其近似的複本，出現在模型的訓練資料中（見[基準測試污染](../../engineering/evaluation/contamination.zh-TW.md)）。
- **可重現性（Reproducibility）**：另一個團隊能否借助論文以及其程式碼與資料，得到相近的結果。

## 運作方式

### ML 論文的結構

大多數機器學習論文遵循相近的版面。**標題與摘要**說明問題、方法與最主要的結果。**引言**通常以貢獻列表作結，它是主張最有用的單一摘要。**相關工作**把論文放進先前方法的脈絡中。**方法**一節定義模型或演算法，常附上方程式或偽代碼。**實驗**一節列出資料集、基線、指標與訓練設定，並報告結果，通常還包括消融實驗。接著可能有**侷限**或**討論**一節，然後是結論、參考文獻與**附錄**。以 NeurIPS 為例，每份投稿都需要填寫可重現性檢核表。[^pineau]

### 閱讀順序

實用的順序是：先讀摘要與引言，再看圖表，接著讀方法，最後才讀實驗。把貢獻列表當成一組主張，並找出檢驗每項主張的表格。附錄可以留到最後。

Keshav 的方法符合這個順序。第一遍涵蓋標題、摘要、引言、章節標題與結論，並以一個判斷作結：這篇論文值不值得多花時間。第二遍仔細閱讀，記下圖表與不清楚之處，同時略過對主要論證無關緊要的細節。第三遍要求讀者在心中重建這項工作，使其假設與缺漏之處浮現出來。[^keshav]

### 判斷主張與基線

對每一項主要主張，都要問：要怎樣才會使它為假？具體來說，要檢查：

- **基線是否新穎、夠強，且調校的投入與新方法相當。** Dacrema 等人嘗試重現主要會議中 18 個神經推薦方法。只有 7 個能在合理的努力下重現，其中六個常被簡單的啟發式方法（例如最近鄰規則）超越。[^dacrema]
- **進步是否大於各次實驗之間的變異。** Henderson 等人指出，深度強化學習的結果會因隨機種子與實作細節而有相當大的差異，使得小幅的差距難以解讀。他們呼籲採用顯著性指標，並更標準化地報告實驗。
- **消融實驗是否移除了論文所歸功的那個組件。** Lipton 與 Steinhardt 把「未能辨識經驗進步的來源」列為機器學習論文中反覆出現的問題之一。他們舉的一個例子是：進步其實來自超參數調校，卻被歸功於架構上的改動。[^lipton]
- **搜尋的投入是否相當。** 在一項針對生成對抗網路的大規模比較中，Lucic 等人發現，只要有足夠的超參數搜尋與隨機重啟，多數模型都能達到相近的分數。因此，報告出來的差異可能反映的是搜尋的投入，而不只是演算法本身。

### 資料污染與選擇性報告

有兩個問題會讓一個醒目的數字看起來比實際更好。**資料污染**指測試題目，或其近似複本，出現在訓練資料中，因此分數有一部分量測的其實是回憶。Brown 等人為 GPT-3 報告了基準與訓練資料之間的重疊分析，並在移除重疊題目後重新評分一個子集。Sainz 等人則主張，應針對每個基準測量資料污染，而不是假設它不存在。[^brown] 去污染過濾器若找不到共享的詞序列，並不能證明測試集是乾淨的，因為經過改寫或翻譯的題目可以通過過濾（Yang et al., 2023）。[^yang] Jain 等人以隨時間發布的競賽題目建構 LiveCodeBench，讓模型能在訓練截止日之後發布的題目上接受測試。[^jain] 閱讀論文時，應比較模型的訓練截止日與基準的發表日期，並尋找關於去污染的說明，或是否使用私有或動態測試集。

**選擇性報告（cherry-picking）**指有選擇地呈現結果。它包括只展示眾多隨機種子中最好的一次、在看到結果之後才選擇資料集、子集或指標，或是對新方法在測試集上調校，而基線維持預設值。其跡象包括：隨機種子數量很少、沒有誤差線、沒有失敗案例，以及使用的指標並非該任務慣用的指標。像 GPT-3 作者那樣，在完整基準旁同時報告乾淨子集，是揭露的表現，但不能證明結果可靠。[基準測試套件](../../engineering/evaluation/benchmark-suites.zh-TW.md)說明了飽和的套件如何放大細微且經過選擇的差異。

### 程式碼與可重現性訊號

公開程式碼是強的訊號，但光有程式碼並不足夠。應查看：論文連結的程式碼是否與所描述的方法一致；是否有設定檔或腳本，載明超參數、隨機種子與資料切分；是否說明所用的運算量；以及是否有 README 說明如何重現主要表格。較弱的訊號包括「程式碼可應要求提供」，以及沒有訓練或評估腳本的儲存庫。

關於文件化的證據令人憂心。Gundersen 與 Kjensmo 調查了兩個主要 AI 會議的 400 篇論文，發現沒有一篇記錄了他們歸為重現所必需的全部變數；各類變數中，只有 20% 到 30% 有被記錄。[^gundersen] Kapoor 與 Narayanan 發現，在 17 個使用機器學習的領域中，有資料洩漏的問題，影響 329 篇論文。他們提議以模型資訊表（model info sheets）報告科學主張，使洩漏能在發表前被發現。[^kapoor] NeurIPS 2019 可重現性計畫結合了程式碼提交政策、社群可重現性挑戰，以及投稿流程中的檢核表，其報告也記錄了主辦者從中學到的經驗。[^pineau]

## 關鍵方法

各種閱讀策略的差異在於從哪裡開始，以及目的為何。下表比較四種常見的做法。它們並不互斥，仔細的讀者常會把快速的第一遍與聚焦於主張的檢查結合起來。

| 策略 | 起點 | 最適合 | 主要風險 |
|---|---|---|---|
| 三遍閱讀法（Keshav） | 標題、摘要與圖表，接著仔細閱讀，然後在心中重建方法 | 判斷論文是否重要，再理解它 | 第三遍很耗時，常被跳過 |
| 主張優先檢查 | 貢獻列表，以及檢驗每項主張的表格 | 判斷證據是否支持標題結論 | 缺少重新實作所需的方法細節 |
| 程式碼優先檢查 | 儲存庫、設定檔，以及產生主要表格的腳本 | 檢查可重現性與隱藏的調校 | 程式碼可能缺失、不完整，或與論文所述版本不同 |
| 引用追蹤 | 參考文獻，接著是引用該工作的後續論文 | 把結果放進脈絡中，並找出競爭的研究 | 被引用不等於認可，熱門也不是證據 |

## 關聯

[會議與期刊](../venues/index.zh-TW.md)說明審查模式與預印本，[里程碑論文](../papers/index.zh-TW.md)列出塑造多個領域的論文，而[詞彙表](../glossary/index.zh-TW.md)提供常見術語的繁體中文對照。

在評估方面，[評估與基準](../../engineering/evaluation/index.zh-TW.md)列出常見陷阱，並提供設計測試的協定；[評估與驗證](../../theory/paradigms/supervised/evaluation-and-validation/index.zh-TW.md)涵蓋監督式模型的資料切分、指標與不確定性。[基準測試套件](../../engineering/evaluation/benchmark-suites.zh-TW.md)說明飽和如何改變分數的意義，而[基準測試污染](../../engineering/evaluation/contamination.zh-TW.md)則更深入地介紹偵測與預防。

腦與心智的角度以一種特殊的形式提出同樣的問題。若一篇論文宣稱網路的活動與腦部記錄相似，在把這種相似視為證據之前，需要控制組，例如未經訓練的網路或其他替代模型。[NeuroAI](../../brain-mind/neuroai/index.zh-TW.md)涵蓋這個領域。[打造像人一樣學習與思考的機器](../../brain-mind/cognitive-science/building-machines-like-people/index.zh-TW.md)是一篇附有公開同儕評論的目標文章，讓讀者能看見爭議，而不只是主張。

## 應用

- **文獻回顧。** 三遍閱讀法讓研究者能快速篩選大量論文，並把仔細閱讀留給真正重要的少數幾篇。
- **審稿。** 主張優先檢查，以及關於基線與隨機種子的問題，構成審查的核心。
- **在既有結果上繼續研究。** 程式碼優先檢查能在重現方法之前，指出哪些設定很重要。
- **摘要。** 由生成式工具產出的摘要，可能漏掉最關鍵的基線細節與種子數量。應對照其所引用的表格來檢查主張。

## 開放問題

- 大多數領域並不要求提供重現結果所需的全部輸入。讀者要如何大規模地檢查主張？Kapoor 與 Narayanan 的模型資訊表是其中一項提議。
- 對於不公開訓練資料的封閉模型，能否偵測資料污染？Duan 等人發現，在 Pile 上訓練的大型語言模型中，成員推論幾乎不比隨機猜測好，而且許多方法都依賴對語料的存取（見[基準測試污染](../../engineering/evaluation/contamination.zh-TW.md)）。
- 發表場域是否應獎勵重現性的工作？當一個結果很少被其他團隊重現時，讀者應如何衡量它？

[^pineau]: Pineau et al.（2020），見參考資料。報告描述 NeurIPS 2019 計畫的三個組成部分：程式碼提交政策、可重現性挑戰，以及檢核表。
[^keshav]: Keshav（2007），見參考資料。該文描述三遍閱讀法，以及如何用於文獻調查。
[^dacrema]: Dacrema et al.（2019），見參考資料。18 個演算法中，7 個能在合理努力下重現，其中 6 個常被簡單的啟發式方法超越。
[^lipton]: Lipton 與 Steinhardt（2018），見參考資料。該文列出四種模式，包括未能辨識經驗進步的來源。
[^brown]: Brown et al.（2020），見參考資料。GPT-3 論文報告了其基準與訓練資料之間重疊的分析。
[^yang]: Yang et al.（2023），見參考資料。該文顯示，經改寫與翻譯的測試樣本可以躲過 n-gram 去污染。
[^jain]: Jain et al.（2024），見參考資料。該基準使用隨時間發布的題目，使結果能與各模型的截止日相比。
[^gundersen]: Gundersen 與 Kjensmo（2018），見參考資料。該調查涵蓋 IJCAI 與 AAAI 的 400 篇論文，發現各類變數中只有 20% 至 30% 有被記錄。
[^kapoor]: Kapoor 與 Narayanan（2022），見參考資料。該調查涵蓋 17 個領域、329 篇有資料洩漏錯誤的論文，並提議模型資訊表。

## 參考資料

### 開創性論文

- Keshav, S.（2007）。*How to read a paper*。ACM SIGCOMM Computer Communication Review。https://doi.org/10.1145/1273445.1273458 — 描述閱讀研究論文的三遍閱讀法，以及在調查文獻時如何運用。
- Lipton, Z. C. & Steinhardt, J.（2018）。*Troubling Trends in Machine Learning Scholarship*。arXiv。https://arxiv.org/abs/1807.03341 — 列出機器學習論文中四種反覆出現的問題，包括誤歸因的經驗進步，以及對數學與語言的誤用。
- Henderson, P. et al.（2018）。*Deep Reinforcement Learning that Matters*。arXiv。https://arxiv.org/abs/1709.06560 — 說明非確定性與變異如何使深度強化學習的結果難以解讀，並建議更好的報告方式。
- Lucic, M. et al.（2018）。*Are GANs Created Equal? A Large-Scale Study*。arXiv。https://arxiv.org/abs/1711.10337 — 對 GAN 模型的大規模實證比較，發現只要超參數與重啟得到足夠調校，多數模型都能達到相近的分數。
- Dacrema, M. F., Cremonesi, P. & Jannach, D.（2019）。*Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches*。arXiv。https://arxiv.org/abs/1907.06902 — 嘗試重現 18 個神經推薦方法，並與較簡單、經過良好調校的基線比較。
- Brown, T. B. et al.（2020）。*Language Models are Few-Shot Learners*。arXiv。https://arxiv.org/abs/2005.14165 — GPT-3 論文，其評估一節分析基準與訓練資料之間的重疊，並重新評分乾淨子集。

### 調查與教科書

- Gundersen, O. E. & Kjensmo, S.（2018）。*State of the Art: Reproducibility in Artificial Intelligence*。Proceedings of the AAAI Conference on Artificial Intelligence。https://doi.org/10.1609/aaai.v32i1.11503 — 調查 400 篇 AI 論文中用於重現的變數，並發現文件記錄並不完整。
- Kapoor, S. & Narayanan, A.（2022）。*Leakage and the Reproducibility Crisis in ML-based Science*。arXiv。https://arxiv.org/abs/2207.07048 — 調查使用機器學習的各領域中的資料洩漏，提出洩漏類型的分類，並建議以模型資訊表進行報告。

### 文章與文件

- Pineau, J. et al.（2020）。*Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)*。arXiv。https://arxiv.org/abs/2003.12206 — NeurIPS 2019 可重現性計畫的報告，涵蓋其程式碼政策、挑戰與檢核表。
- Sainz, O. et al.（2023）。*NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark*。arXiv。https://arxiv.org/abs/2310.18018 — 主張必須針對每個基準測量資料污染，因為它可能使報告的分數膨脹。
- Yang, S. et al.（2023）。*Rethinking Benchmark and Contamination for Language Models with Rephrased Samples*。arXiv。https://arxiv.org/abs/2311.04850 — 顯示經改寫與翻譯的測試樣本可以繞過 n-gram 去污染。
- Duan, M. et al.（2024）。*Do Membership Inference Attacks Work on Large Language Models?*。arXiv。https://arxiv.org/abs/2402.07841 — 發現在 Pile 上訓練的語言模型中，成員推論攻擊僅略勝隨機猜測，這限制了偵測資料污染的方式。
- Jain, N. et al.（2024）。*LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code*。arXiv。https://arxiv.org/abs/2403.07974 — 以隨時間發布的競賽題目建構程式碼基準，以限制資料污染。
