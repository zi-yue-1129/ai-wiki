---
translation_reviewed: 2026-10-28
---

# 超參數最佳化

超參數是學習演算法中不由梯度下降擬合的設定，例如學習率、批次大小、正則化強度與網路寬度。超參數最佳化在訓練次數的預算內，搜尋能帶來最佳驗證表現的設定。本頁是[最佳化](../index.md)的一部分。

## 概述

調校超參數常常是建立模型最大的成本。Bergstra 與 Bengio（2012）指出，當只有少數超參數重要時，隨機取樣設定比規則的格點搜尋更好，因為格點會把大部分執行次數花在不重要的維度上。Snoek、Larochelle 與 Adams（2012）隨後顯示，依據先前執行結果擬合的驗證分數模型，能比隨機搜尋更有效率地選出下一個設定。後來的方法以不同方式降低成本：提早停止較差的執行、複製表現好的執行狀態，或在小模型上擬合設定，再遷移到大模型。

## 關鍵概念

- **搜尋空間**：每個超參數的範圍與型別，例如對數均勻的學習率，或優化器的選擇。
- **目標**：搜尋試圖最佳化的驗證分數，通常是損失或錯誤率。
- **預算**：搜尋可以花費的總運算量，以訓練次數、週期數或 GPU 小時衡量。
- **代理模型**：目標函數的廉價模型，依先前執行結果擬合，用來提出下一個設定。
- **多保真度**：使用完整訓練的廉價近似（如較少的週期或較少的資料）來及早為設定排序。

## 問題

給定搜尋空間與固定預算，應該訓練哪些設定？執行應如何停止或繼續，才能以最少的執行次數找到最佳設定？

## 運作方式

多數方法重複同一個迴圈：提出一個設定，以某個預算訓練它，記錄驗證分數，並用新分數決定下一次的提案。方法之間的差別，在於如何產生提案，以及保留每次執行的多少部分。

- **無模型取樣**隨機或在格點上抽取設定。隨機搜尋是標準基準。
- **以模型為基礎的搜尋**把代理模型擬合到觀察到的分數，並提出預期增益最佳的設定。[貝氏最佳化](bayesian-optimisation.md)頁面涵蓋此類方法。
- **多臂老虎機與提早停止方法**把預算視為資源。先啟動許多設定，及早捨棄表現差的。[Hyperband](hyperband.md)頁面涵蓋此類方法。
- **基於族群的訓練**並行執行多組設定，並在訓練中把表現好的執行的權重與設定複製到較弱的執行中。見[基於族群的訓練](../../paradigms/reinforcement-learning/multi-agent-rl/population-based-training/index.md)。
- **設定遷移**在小模型上擬合最佳設定，再重複用於大模型。Yang 等人（2022）顯示，在最大更新參數化（μP）下，許多最佳設定隨網路寬度增加而保持穩定，使這種遷移成為可能。見[μP](../../deep-learning/initialisation/mup.md)。

## 主要方法

本節提供比較並連結至下層頁面。每種方法都有自己的頁面。

- [貝氏最佳化](bayesian-optimisation.md)：高斯過程代理模型與獲取函數選出每個下一個設定。適用於執行成本高、搜尋空間小的情況。
- [Hyperband](hyperband.md)：跨多種預算的連續減半，先啟動許多設定，只把更多預算給表現最好的。適用於早期分數能預測最終分數的情況。
- [基於族群的訓練](../../paradigms/reinforcement-learning/multi-agent-rl/population-based-training/index.md)：族群在單次訓練中調整設定。
- [μP](../../deep-learning/initialisation/mup.md)：在小模型上調校，再把設定遷移到大模型。

## 變體

- **混合方法**把老虎機排程與提出設定的模型結合，既保留提早停止，也改善設定的選擇（Falkner 等人，2018）。
- **多目標調校**同時最佳化準確率與成本，例如延遲或記憶體。
- **條件式搜尋空間**，其中某些超參數只有在其他超參數取特定值時才存在，需要能處理結構的搜尋方法。

## 結果與限制

- 當只有少數超參數重要時，隨機搜尋優於格點搜尋（Bergstra 與 Bengio，2012）。
- 在 Snoek 等人（2012）的實驗中，貝氏最佳化在數個學習演算法上達到或超過專家水準的調校，包括卷積網路與潛在狄利克雷分配。其選擇高度取決於代理模型的先驗，而先驗的不同可能大幅改變結果。
- 高斯過程的擬合成本隨觀察次數快速增長，因此此方法較適合小預算。
- 隨著維度增加，以及存在大量類別或條件式選擇時，代理模型的可靠性會下降。
- Li 等人（2017）的實驗中，Hyperband 相較於所比較的方法（包括貝氏最佳化）獲得超過一個數量級的加速。
- μP 使我們能在一個有 1,300 萬參數的模型上調校，並把設定遷移到 BERT-large，總調校成本等於 BERT-large 一次預訓練的成本（Yang 等人，2022）。
- 代理模型在執行次數多與高維空間中擴展性差；提早停止方法則假設早期分數能正確排序設定。

## 應用

- **訓練深度網路**，其中學習率與排程主導結果。
- **預訓練大型模型**，從小模型遷移設定可省下大部分的調校成本。
- **AutoML 流程**，把超參數搜尋與[架構搜尋](../../deep-learning/nas-automl/index.md)結合。

## 開放問題

- 何時早期分數足以預測最終分數，使提早停止可靠？何時會誤導？
- 當預算小到只能完成一兩次完整訓練時，應如何進行搜尋？
- 當資料或架構改變（不只是寬度改變）時，遷移的設定是否仍正確？

## 與其他頁面的連結

- 上層主題：[最佳化](../index.md)
- 架構選擇：[神經架構搜尋與 AutoML](../../deep-learning/nas-automl/index.md)
- 常被調校的學習率排程：[學習率排程](../learning-rate-schedules.md)

## 參考文獻

### 奠基性論文

- Bergstra, J. & Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research* 13, 281–305. https://jmlr.org/papers/v13/bergstra12a.html — 顯示當只有少數超參數重要時，隨機取樣設定比格點更快找到好的配置。
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). Practical Bayesian Optimization of Machine Learning Algorithms. In *NeurIPS 2012*. arXiv:1206.2944. https://arxiv.org/abs/1206.2944 — 以高斯過程代理模型與期望改進來調校學習演算法。
- Jamieson, K. & Talwalkar, A. (2016). Non-stochastic Best Arm Identification and Hyperparameter Optimization. In *AISTATS 2016*, PMLR 51. https://proceedings.mlr.press/v51/jamieson16.html — 為超參數搜尋提出連續減半，並給出理論保證。
- Li, L. et al. (2017). Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization. *Journal of Machine Learning Research* 18(185). arXiv:1603.06560. https://arxiv.org/abs/1603.06560 — 提出 Hyperband，跨多個分支執行連續減半，並與貝氏最佳化比較。
- Jaderberg, M. et al. (2017). Population Based Training of Neural Networks. arXiv:1711.09846. https://arxiv.org/abs/1711.09846 — 在單次訓練中，透過複製族群中表現最好的成員，調整設定與權重。

### 綜述與教科書

- Shahriari, B. et al. (2016). Taking the Human Out of the Loop: A Review of Bayesian Optimization. *Proceedings of the IEEE* 104(1), 148–175. https://doi.org/10.1109/JPROC.2015.2494218 — 貝氏最佳化、其代理模型與獲取函數的綜述。
- Feurer, M. & Hutter, F. (2019). Hyperparameter Optimization. In *Automated Machine Learning*, Springer, 3–33. https://doi.org/10.1007/978-3-030-05318-5_1 — 綜述上述方法及其權衡的章節。
- Yang, G. et al. (2022). Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. arXiv:2203.03466. https://arxiv.org/abs/2203.03466 — 顯示在 μP 下，最佳設定可以從小網路遷移到大網路。
- Falkner, S., Klein, A. & Hutter, F. (2018). BOHB: Robust and Efficient Hyperparameter Optimization at Scale. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/falkner18a.html — 把老虎機排程與以模型為基礎的設定選擇結合。

## 延伸學習

- Hutter, F., Kotthoff, L. & Vanschoren, J. (eds.) (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer. https://doi.org/10.1007/978-3-030-05318-5 — 含超參數最佳化與架構搜尋章節的書籍。
