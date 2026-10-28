---
translation_reviewed: 2026-10-28
---

# 超參數最佳化

超參數最佳化是在訓練開始前就固定的設定中，尋找能取得最佳結果者的過程，例如學習率、批次大小、權重衰減與網路寬度。各種方法的差異在於如何選擇下一個要嘗試的設定，以及如何分配每次試驗的運算資源。

## 概述

訓練會擬合模型的參數 \(\theta\)，但還有許多其他選擇需事先決定。這些就是超參數 \(\lambda\)。例子包括學習率及其[排程](learning-rate-schedules.md)、Adam 的係數、權重衰減的強度、批次大小，以及網路的深度與寬度。

每個 \(\lambda\) 的選擇都定義了一次不同的訓練，並以保留的資料評分。外層問題因此是 \(\lambda^\* = \arg\max_\lambda S(\lambda)\)，其中 \(S(\lambda)\) 是用 \(\lambda\) 訓練後的驗證分數。單次評估可能要花費數小時或數天的運算，因此相對於搜尋空間的大小，只能負擔少數幾次試驗。超參數最佳化（HPO）就是在固定預算內搜尋這個空間的一組策略。

Snoek 等人（2012）把調參描述為常常是需要專家判斷或暴力搜尋的「黑魔法」。此問題之所以困難，有三個原因：搜尋空間混合了連續、離散與類別型的設定；分數帶有雜訊，因為不同的隨機種子會給出略有不同的結果；而且每次評估都很昂貴。

## 核心概念

- **超參數**：訓練前選定的設定，與訓練所學的參數相對。見[詞彙表](../../reference/glossary/index.md)。
- **搜尋空間**：每個超參數的範圍與尺度，例如學習率在 \(10^{-5}\) 到 \(10^{-1}\) 之間依對數尺度取樣。
- **試驗**：以一組設定進行的一次訓練評估。
- **預算（保真度）**：完整訓練的較便宜版本，例如較少的 epoch、資料子集或較小的模型。
- **代理模型與獲取函數**：在貝氏最佳化中，代理模型是分數隨 \(\lambda\) 變化的統計模型，獲取函數則決定下一個要評估的點。
- **遷移**：把在小型或便宜模型上找到的設定，套用到大型模型。只有當最佳設定在不同規模間保持穩定時，這樣做才合理。

## 運作方式

每種方法都遵循同一個循環：提出一組設定、以某個預算訓練、記錄驗證分數，再用這些紀錄提出下一組。各方法的差異在於提案規則，以及如何分配預算。

連續減半是核心的預算分配演算法。給定 \(n\) 組設定、最小預算 \(r\) 與縮減因子 \(\eta > 1\)（通常為 3 或 4）：

1. 以預算 \(r\) 訓練全部 \(n\) 組設定。
2. 保留其中最好的 \(\lfloor n/\eta \rfloor\) 組，並把預算乘以 \(\eta\)。
3. 重複此步驟，直到剩下一組，再將其完整訓練。

每一輪大約保留 \(1/\eta\) 的設定，並給予存活者更多預算，因此大部分運算會集中在有希望的試驗上。Hyperband 會多次執行這個程序，每次對設定數量與起始預算做不同的權衡。因此它不必事先決定要多積極地停止表現差的試驗。[^1]

## 關鍵方法

有五類方法涵蓋了大多數實務。下表比較它們，其後各段說明每種方法的依據。

| 方法 | 如何提出試驗 | 每次試驗的預算 | 典型用途 |
|---|---|---|---|
| 網格搜尋 | 在搜尋空間上的固定格點 | 完整 | 超參數少、訓練便宜 |
| 隨機搜尋 | 獨立的隨機抽樣 | 完整 | 簡單的基準，超參數多 |
| 貝氏最佳化 | 代理模型加獲取函數 | 完整 | 連續超參數少、訓練昂貴 |
| 連續減半與 Hyperband | 隨機抽樣，並提早停止表現差的試驗 | 自適應 | 設定數多、學習曲線可靠 |
| 基於族群的訓練 | 複製並擾動一個執行中的族群 | 完整，隨時間共享 | 排程、強化學習、平行叢集 |
| muTransfer（muP） | 在小模型上調參，把設定套用到大模型 | 僅限小模型 | 預訓練超大型網路 |

**網格搜尋與隨機搜尋。** 網格搜尋會評估格點上的每一點，其成本隨超參數數量呈指數成長。隨機搜尋則獨立抽取每組設定，因此每次試驗都會探索每個超參數的新值。Bergstra 等人（2011）指出，隨機搜尋在數個神經網路任務上效果良好，但在深度信念網路上並不可靠。它是強的基準，但並非完整的答案。

**貝氏最佳化。** 此方法以代理模型（通常是高斯過程）擬合已見過的設定與分數。獲取函數（例如期望改進）會在「看起來好的設定」與「模型不確定的設定」之間取得平衡（Frazier，2018；Shahriari 等人，2016）。Snoek 等人（2012）將此方法應用於卷積網路與其他學習演算法，並報告其結果達到或超越專家調參。由於每一步通常要等待前一步的結果，平行版本需要額外設計；此方法最適合連續維度少於約二十個的情形。Bergstra 等人（2011）中的序列方法之一，樹狀結構 Parzen 估計器，改為對好與壞設定的密度建模，而非直接對分數建模。

**連續減半與 Hyperband。** Jamieson 與 Talwalkar（2015）把超參數搜尋視為非隨機的最佳臂辨識問題，並分析其中的連續減半。Li 等人（2016）提出 Hyperband，它以數個分組（bracket）執行連續減半，並報告在深度學習與核方法問題上，相對於貝氏競爭者有超過一個數量級的加速。[^2] BOHB（Falkner 等人，2018）保留 Hyperband 的預算分配，但以模型提出設定，作者報告其表現優於兩個母方法。ASHA（Li 等人，2018）使連續減半變為非同步：試驗一旦排進前一部分，就立即晉升。這適合大型叢集，論文報告其隨工作節點數量近乎線性擴展。[^3]

**基於族群的訓練。** 基於族群的訓練（PBT）會平行訓練一群模型。每隔一段時間，表現較差的成員會複製表現較好者的權重與超參數，然後擾動被複製的超參數。由於設定在訓練中會改變，PBT 找到的是一條排程，而非單一固定值（Jaderberg 等人，2017）。論文報告在深度強化學習中收斂較快、最終表現較高，並將此方法應用於機器翻譯（直接最大化 BLEU）與生成對抗網路（最大化 Inception score）。整個族群必須同時訓練，因此需要平行叢集；而它所找到的排程，只適用於產生該排程的那次執行。

**muTransfer。** 在最大更新參數化下，隨著模型變大，許多最佳超參數會保持穩定。因此，Yang 等人（2022）在小模型上調參，再把最佳設定套用到大模型，而不直接調大模型。其結果與限制見 [muP 頁面](../deep-learning/initialisation/mup/index.md)，該頁也說明了此參數化（Yang 與 Hu，2020）。此方法與寬度有關，因此並不能單獨解決如何跨深度或資料集大小遷移設定的問題。

## 關聯

- **縮放與規劃。** 大型訓練的成本過高，無法直接調參，因此團隊會在小規模實驗上擬合趨勢再外推，如[縮放定律](../models/llm/scaling-laws/index.md)所述。[運算最佳化訓練](../models/llm/compute-optimal-training/index.md)則以類似的推理，在固定預算下決定模型大小與資料量。
- **多臂賭博機。** 連續減半屬於賭博機方法，必須在探索新選項與利用已知的好選項之間取得平衡。[隨機賭博機](../paradigms/online/stochastic-bandits/index.md)頁面涵蓋隨機設定，它與 Hyperband 分析所用的非隨機設定不同。
- **演化。** PBT 類似演化搜尋，都有族群與選擇。見[演化計算與群體智慧](../../evolutionary/index.md)。
- **腦與心智。** 基於賭博機的 HPO 所形式化的探索與利用權衡，在人與動物的[決策與獎勵](../../brain-mind/decision-reward/index.md)研究中同樣是核心。兩者的相似之處在於結構。沒有證據顯示大腦會對自身的設定運行高斯過程，因此這只是類比，而非機制。

## 應用

- **調整深度網路。** Snoek 等人（2012）展示了貝氏最佳化調整卷積網路，Hyperband 也在深度學習問題上接受評估（Li 等人，2016）。
- **強化學習。** PBT 是為深度強化學習而發展的，這類訓練既長又有雜訊（Jaderberg 等人，2017）。
- **軟體。** Optuna（Akiba 等人，2019）允許搜尋空間依賴先前的選擇，並在訓練期間修剪表現差的試驗。
- **大型模型的預訓練。** Yang 等人（2022）報告，從 1,300 萬參數模型遷移來的設定，勝過已發表的 BERT-large 結果；從 4,000 萬參數模型遷移來的設定，則勝過已發表、參數為 67 億的 GPT-3 結果。

## 開放問題

- 提早停止假設，試驗在小預算下的排名能預測其在完整預算下的排名。這在何時、多常會失效？
- muTransfer 涵蓋寬度。是否有同樣可靠的方法，能跨深度、資料大小與批次大小遷移超參數？
- 在共用的驗證集上反覆調參，可能會對該驗證集過度擬合。調參成本與選擇效應應如何公平地報告？
- 當單次試驗的成本與一次完整訓練相當時，哪些方法仍然可行？

## 參考文獻

### 開創性論文

- Bergstra, J., Bardenet, R., Bengio, Y. & Kégl, B. (2011). *Algorithms for Hyper-Parameter Optimization*. NIPS 24. https://proceedings.neurips.cc/paper/2011/hash/86e8f7ab32cfd12577bc2619bc635690-Abstract.html — 在神經網路與深度信念網路上，比較隨機搜尋與兩種序列式期望改進方法，包括樹狀結構 Parzen 估計器。
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). *Practical Bayesian Optimization of Machine Learning Algorithms*. arXiv. https://arxiv.org/abs/1206.2944 — 以高斯過程的貝氏最佳化調整學習演算法（包括卷積網路），並報告其結果達到或超越專家調參。
- Jamieson, K. & Talwalkar, A. (2015). *Non-stochastic Best Arm Identification and Hyperparameter Optimization*. arXiv. https://arxiv.org/abs/1502.07943 — 將超參數搜尋視為最佳臂辨識問題，並分析其中的連續減半。
- Li, L., Jamieson, K., DeSalvo, G., Rostamizadeh, A. & Talwalkar, A. (2016). *Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization*. arXiv. https://arxiv.org/abs/1603.06560 — 提出 Hyperband，透過自適應的資源分配與提早停止，加速隨機搜尋。
- Falkner, S., Klein, A. & Hutter, F. (2018). *BOHB: Robust and Efficient Hyperparameter Optimization at Scale*. arXiv. https://arxiv.org/abs/1807.01774 — 結合模型式的提案與 Hyperband 的預算分配，並將結果與兩個母方法比較。
- Li, L., Jamieson, K., Rostamizadeh, A., Gonina, E., Hardt, M., Recht, B. 等人（2018）。*A System for Massively Parallel Hyperparameter Tuning*. arXiv. https://arxiv.org/abs/1810.05934 — 提出 ASHA，即連續減半的非同步版本，並說明其在一項生產級調參服務中的應用。
- Jaderberg, M., Dalibard, V., Osindero, S., Czarnecki, W. M., Donahue, J., Razavi, A. 等人（2017）。*Population Based Training of Neural Networks*. arXiv. https://arxiv.org/abs/1711.09846 — 聯合最佳化一群模型及其超參數，產生超參數排程而非固定值。
- Yang, G. & Hu, E. J. (2020). *Feature Learning in Infinite-Width Neural Networks*. arXiv. https://arxiv.org/abs/2011.14522 — 提出最大更新參數化，使網路寬度趨於無限時仍能進行特徵學習。
- Yang, G., Hu, E. J., Babuschkin, I., Sidor, S., Liu, X., Farhi, D. 等人（2022）。*Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*. arXiv. https://arxiv.org/abs/2203.03466 — 提出 muTransfer，在小模型上調參，並將設定遷移到較大的 Transformer 與 ResNet。

### 綜述與教科書

- Bischl, B., Binder, M., Lang, M., Pielok, T., Richter, J., Coors, S. 等人（2021）。*Hyperparameter Optimization: Foundations, Algorithms, Best Practices and Open Challenges*. arXiv. https://arxiv.org/abs/2107.05847 — 回顧網格與隨機搜尋、演化方法、貝氏最佳化、Hyperband 與 racing，並提出實務建議。
- Frazier, P. I. (2018). *A Tutorial on Bayesian Optimization*. arXiv. https://arxiv.org/abs/1807.02811 — 介紹高斯過程代理模型與獲取函數的教學，包括期望改進，以及平行與多保真度的延伸。
- Shahriari, B., Swersky, K., Wang, Z., Adams, R. P. & de Freitas, N. (2016). *Taking the Human Out of the Loop: A Review of Bayesian Optimization*. Proceedings of the IEEE. https://doi.org/10.1109/JPROC.2015.2494218 — 回顧以貝氏最佳化處理昂貴黑箱函數的方法，超參數調整是其中一個應用。

### 文章與文件

- Akiba, T., Sano, S., Yanase, T., Ohta, T. & Koyama, M. (2019). *Optuna: A Next-generation Hyperparameter Optimization Framework*. arXiv. https://arxiv.org/abs/1907.10902 — 說明 Optuna 軟體的設計，包括定義即執行（define-by-run）的搜尋空間，以及對無望試驗的修剪。

[^1]: Li 等人（2016）將 Hyperband 描述為一種賭博機式方法，會把預先定義的資源（例如迭代次數、資料樣本或特徵）分配給隨機抽樣的設定。分組結構見於論文中，此處不另述。
[^2]: Li 等人（2016）的摘要中，以「超過一個數量級」的字句，描述其相對於各種深度學習與核方法問題上競爭方法組的加速。
[^3]: Li 等人（2018）的摘要報告 ASHA 隨工作節點數量線性擴展，並在一項使用 500 個工作節點的任務上得到驗證。
