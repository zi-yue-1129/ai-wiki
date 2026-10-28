---
translation_reviewed: 2026-10-28
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

DAgger 是一種互動式模仿學習演算法。學習者執行自己的策略，專家為學習者實際造訪的狀態提供正確動作，這些標註再加入訓練集。它透過在策略將面對的狀態上訓練，修正[行為克隆](../behavioural-cloning/index.md)的共變量偏移（covariate shift）問題。

## 問題

行為克隆只在專家造訪過的狀態上訓練。測試時，學習者會漂移到專家從未產生過的狀態，那裡的預測沒有監督，誤差會逐步累積。Ross 與 Bagnell（2010）分析了這種累積，指出單純克隆的代價可能隨時程長度以平方成長。

## 核心想法

從學習者自己的分布學習。每一輪都執行目前的策略，請專家標註造訪過的每個狀態的正確動作，把新標註的資料與之前所有資料合併，再重新訓練。因此，累積的資料集涵蓋了至今所有策略會遇到的狀態分布。

## 演算法

1. 以專家示範 $\mathcal{D}$ 訓練初始策略 $\pi_1$。
2. 對 $i = 1, \dots, N$：
    1. 執行 $\pi_i$，記錄它造訪的狀態 $s$。
    2. 向專家查詢每個造訪狀態的動作 $\pi^*(s)$。
    3. 合併資料：$\mathcal{D} \leftarrow \mathcal{D} \cup \{(s, \pi^*(s))\}$。
    4. 在 $\mathcal{D}$ 上訓練 $\pi_{i+1}$。
3. 以驗證時的執行結果，回傳表現最好的策略。

實務上，早期幾輪專家有時會接管執行，接管機率隨時間遞減，讓最初合併進來的狀態更接近專家的行為。

## 結果與保證

Ross、Gordon 與 Bagnell（2011）證明，對於無悔（no-regret）的線上學習者，所得策略的期望代價隨時程線性成長，而行為克隆的上界則是二次方。論文也在模仿學習與結構化預測任務上報告了優於先前方法的實驗結果。此保證假設專家能夠標註學習者到達的任何狀態。

## 限制

- **專家可得性。** 此方法需要專家能隨時標註任意狀態。人類標註者可能覺得成本高或不安全。
- **標註品質。** 人類修正可能有雜訊，而且當策略已開始偏離時，接管的人類標註品質可能下降（Kelly 等人，2018）。
- **資料成長。** 每一輪都會讓合併後的資料集變大，若不修剪，重訓成本會逐步增加。

## 與其他主題的連結

DAgger 位於監督式學習與[強化學習](../../reinforcement-learning/index.md)之間。它的執行過程提供資料（如同 RL），專家提供標籤（如同行為克隆）。[DART](dart.md) 提供另一條不需線上專家的取得恢復資料的路徑。當額外觀測造成因果失誤時，見[因果混淆](../behavioural-cloning/causal-confusion.md)。

## 應用

機器人操作中，由遙控操作員標註或修正學習者的執行過程；自駕中，由安全駕駛在學習者執行時接管。

## 開放問題

當學習者的狀態分布快速移動時，如何限制專家的標註工作量。如何標註人類專家也無法判斷的狀態，以及如何把 DAgger 與既有的離線資料結合。

## 參考文獻

### 奠基性論文

- Ross, S.、Gordon, G. J. 與 Bagnell, J. A.（2011）. *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS 2011, PMLR 15:627–635. https://proceedings.mlr.press/v15/ross11a.html — 提出 DAgger，並證明所學策略的期望代價界。arXiv 版本為 arXiv:1011.0686。
- Ross, S. 與 Bagnell, J. A.（2010）. *Efficient Reductions for Imitation Learning*. AISTATS 2010, PMLR 9:661–668. https://proceedings.mlr.press/v9/ross10a.html — 分析克隆策略的誤差如何沿時程累積，這正是 DAgger 要解決的問題。

### 文章與預印本

- Laskey, M. 等人（2017）. *DART: Noise Injection for Robust Imitation Learning*. arXiv:1703.09327. https://arxiv.org/abs/1703.09327 — 另一種方法，透過擾動專家來收集恢復資料，不需要線上查詢。
- Kelly, M. 等人（2018）. *HG-DAgger: Interactive Imitation Learning with Human Experts*. arXiv:1810.02890. https://arxiv.org/abs/1810.02890 — 人類把關的 DAgger 變體，並討論人類專家的標註品質問題。
- de Haan, P.、Jayaraman, D. 與 Levine, S.（2019）. *Causal Confusion in Imitation Learning*. arXiv:1905.11979. https://arxiv.org/abs/1905.11979 — 說明額外觀測可能傷害克隆策略，並提出以定向查詢的專家來解決。
