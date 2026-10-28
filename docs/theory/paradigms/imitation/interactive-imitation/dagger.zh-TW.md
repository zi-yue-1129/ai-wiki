---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation/behavioural-cloning
  - theory/paradigms/imitation/interactive-imitation/dart.md
  - theory/paradigms/imitation/interactive-imitation
  - theory/paradigms/reinforcement-learning
tags:
  - imitation learning
  - DAgger
  - covariate shift
aliases:
  - DAgger
  - Dataset Aggregation
  - 資料聚合
---

# DAgger（Dataset Aggregation）

DAgger 是一種互動式模仿學習演算法。學習者執行自己的策略，專家為學習者實際造訪的狀態提供正確動作，這些標註再加入訓練集。它透過在策略將面對的狀態上訓練，修正[行為克隆](../behavioural-cloning/index.md)的共變量偏移（covariate shift）問題。此方法出自 Ross、Gordon 與 Bagnell（2011），發表於 AISTATS 2011。

## 概述

行為克隆用專家示範擬合策略，但學習後的策略會在它自己到達的狀態上被評估，而這些狀態示範未必涵蓋。DAgger 以迭代來縮小這個差距：執行目前的策略、為造訪的狀態收集專家標註，再用至今收集的所有資料重新訓練。論文為此程序給出一個隨時程線性成長的效能界，而克隆的界則是二次方成長。

## 核心概念

- **共變量偏移**：測試時學習者的輸入來自與訓練時專家輸入不同的分布，因為學習者自己的動作改變了它所看到的狀態。
- **混合執行**：在早期幾輪，實際執行的策略可以是專家與學習者的混合，由隨迭代遞減的機率 \(\beta_i\) 控制。
- **合併資料集**：所有迭代中被標註狀態的聯集，而非只有最新一輪。保留所有較早的資料，才能讓策略學到每個先前策略所誘導的分布。
- **專家標註**：在學習者造訪的每個狀態上，專家給出的動作 \(\pi^*(s)\)。此方法假設專家可以對任何狀態給出這樣的標註。

## 運作方式

令 \(\pi^*\) 為專家，演算法如下：

1. 初始化 \(\hat\pi_1\)，並將 \(\mathcal D\) 設為空集合。
2. 對 \(i = 1, \dots, N\)：
    1. 形成實際執行的策略 \(\pi_i = \beta_i\,\pi^* + (1-\beta_i)\,\hat\pi_i\)。論文的簡單排程 \(\beta_i = \mathbb 1(i=1)\) 讓第一輪執行完全是專家，論文指出此設定在實務上通常最好。
    2. 執行 \(\pi_i\) 共 \(T\) 步，並記錄造訪的狀態。
    3. 以專家為每個造訪狀態標註，得到 \(\mathcal D_i = \{(s, \pi^*(s))\}\)。
    4. 合併 \(\mathcal D \leftarrow \mathcal D \cup \mathcal D_i\)，再於 \(\mathcal D\) 上訓練 \(\hat\pi_{i+1}\)。
3. 在 \(\hat\pi_1,\dots,\hat\pi_N\) 中，回傳在驗證執行上表現最好的策略。

混合排程只需要平均的 \(\beta\) 趨近於零。若每一輪都有 \(\beta_i = 1\)，學習者從不執行自己的策略，此程序就退化為以專家狀態進行的行為克隆。

## 關鍵方法

### A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning（Ross、Gordon 與 Bagnell，2011）

- **問題：** 在序列預測中，下一個輸入取決於先前的預測，因此常見的獨立同分布假設不再成立。行為克隆只在專家造訪的狀態上訓練，而學習策略的誤差會把它推向訓練資料沒有涵蓋的狀態。
- **核心想法：** 以迭代的執行、專家標註與重新訓練，把策略自己的狀態分布當成訓練分布。從線上學習的角度看，重新訓練出的策略序列是一個無悔（no-regret）的學習者，論文據此為代價給出界。
- **公式或演算法：** 即上方的演算法 3.1。令 \(J(\pi)\) 為 \(T\) 步的總代價，\(\ell\) 為替代損失。論文給出兩個界。對行為克隆，\(J(\hat\pi) \le J(\pi^*) + T^2\varepsilon\)，其中 \(\varepsilon\) 是專家狀態上的誤差，對 \(T\) 呈二次方。對 DAgger，\(J(\hat\pi) \le J(\pi^*) + uT\,\varepsilon_N + O(1)\)，其中 \(u\) 是專家單步 Q 值差距的上界，\(\varepsilon_N\) 是在學習者自身狀態上的最佳逐輪誤差。DAgger 的界對 \(T\) 呈線性。有限樣本版本的界在 \(N\) 隨 \(T^2\log(1/\delta)\) 成長時，以機率 \(1-\delta\) 成立。
- **結果：** 論文報告三個實驗。在 Super Tux Kart 賽車任務中，DAgger 策略在訓練 15 輪後「再也不會掉出賽道」。在 Super Mario Bros. 中，DAgger 明顯優於監督式基準，後者的分數停滯在低得多的水準。在手寫辨識（結構化預測）中，DAgger 的字元準確率達到 85.5%，高於監督式基準。
- **限制：** 界假設替代損失為強凸且有界，且學習者是無悔的（以 Follow-The-Leader 分析）。它也假設專家能為學習者到達的每個狀態給出標註，而這正是此方法在實務上成本高的原因。

## 關聯

DAgger 位於監督式學習與[強化學習](../../reinforcement-learning/index.md)之間。它的執行過程提供資料（如同 RL），專家提供標籤（如同行為克隆）。[DART](dart.md) 提供另一條不需線上專家的取得恢復資料的路徑。當額外觀測造成因果失誤時，而 DAgger 的資料覆蓋也無法解決這個問題，見[因果混淆](../behavioural-cloning/causal-confusion.md)。

## 應用

機器人操作中，由遙控操作員標註或修正學習者的執行過程；自駕中，由安全駕駛在學習者執行時接管。

## 開放問題

- 當學習者的狀態分布快速移動時，如何限制專家的標註工作量。
- 如何標註人類專家無法可靠判斷的狀態。
- 如何結合既有的離線示範，同時避免舊資料主導合併後的資料集。

## 參考文獻

### 奠基性論文

- Ross, S.、Gordon, G. J. 與 Bagnell, J. A.（2011）. A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. AISTATS 2011, PMLR 15. [arXiv:1011.0686](https://arxiv.org/abs/1011.0686) — 提出 DAgger，並證明隨時程線性成長的界，與行為克隆的二次方界相比。
- Ross, S. 與 Bagnell, J. A.（2010）. Efficient Reductions for Imitation Learning. AISTATS 2010, PMLR 9. https://proceedings.mlr.press/v9/ross10a.html — 同一作者較早在相同歸約設定下的工作，分析克隆策略的複合誤差。
- Laskey, M.、Lee, J.、Fox, R.、Dragan, A. 與 Goldberg, K.（2017）. DART: Noise Injection for Robust Imitation Learning. CoRL 2017. [arXiv:1703.09327](https://arxiv.org/abs/1703.09327) — 另一種方法，透過擾動專家來收集恢復資料，不需要線上查詢。論文在模擬中與 DAgger 比較。

### 綜述與教科書

- Osa, T. 等人（2018）. An Algorithmic Perspective on Imitation Learning. Foundations and Trends in Robotics. [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — 綜述，將 DAgger 放在其他模仿學習方法之中。

### 文章與預印本

- Kelly, M.、Sidrane, C.、Driggs-Campbell, K. 與 Kochenderfer, M. J.（2019）. HG-DAgger: Interactive Imitation Learning with Human Experts. ICRA 2019. [arXiv:1810.02890](https://arxiv.org/abs/1810.02890) — DAgger 的人類把關變體，用於與人類專家的互動式學習。
- de Haan, P.、Jayaraman, D. 與 Levine, S.（2019）. Causal Confusion in Imitation Learning. NeurIPS 2019. [arXiv:1905.11979](https://arxiv.org/abs/1905.11979) — 說明額外觀測可能傷害克隆策略，而 DAgger 的資料覆蓋並不能解決這個失誤。
