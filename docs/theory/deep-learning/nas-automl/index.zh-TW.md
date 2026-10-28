---
translation_reviewed: 2026-10-28
---

# 神經架構搜尋與 AutoML

神經架構搜尋（NAS）把網路架構的設計自動化：搜尋程序提出候選架構，估計每個候選的表現，並傳回最佳者。它是自動化機器學習（AutoML）更大領域的一部分。本頁是[深度學習](../index.md)的一部分。

## 概述

手工設計網路依賴專家直覺與一長串的試驗。Zoph 與 Le（2017）顯示，以強化學習訓練的循環控制器，能設計出在 CIFAR-10 上可媲美人工設計架構的卷積網路。這種方法很昂貴，因為每個候選都必須從頭訓練。後來的大部分研究都致力於讓同樣的搜尋變便宜，例如在候選之間共享權重、在連續空間中搜尋，或使用較便宜的效能代理。

## 關鍵概念

- **搜尋空間**：搜尋可能產生的架構集合，例如運算的選擇與它們的連接方式。
- **搜尋策略**：提出候選的規則，例如強化學習、演化、梯度下降或隨機取樣。
- **效能估計**：衡量候選品質的方式，可以是完整訓練、短期訓練，或共享權重的捷徑。
- **權重共享**：在許多候選架構之間重複使用的一組參數，使每個候選不必從頭訓練。
- **硬體感知目標**：除了準確率之外，還包含目標裝置上實測成本（如延遲）的搜尋目標。

## 問題

如何在固定的運算預算內找到好的架構，而不必由人寫出每個候選？所得結果能否遷移到未搜尋過的任務與裝置？

## 運作方式

Elsken、Metzen 與 Hutter（2019）把 NAS 描述為三個部分：搜尋空間、搜尋策略與效能估計策略。搜尋策略從空間中提出一個架構，估計器為其評分，分數再更新搜尋策略。此循環重複直到預算用盡，最佳架構接著被完整訓練，並在保留資料上評估。

各種方法的差別主要在於如何讓這個循環更便宜。有些保留強化學習控制器，並在候選之間共享權重；有些把離散選擇放寬為連續選擇，以梯度下降最佳化；演化方法則對一群架構進行突變，並保留最優者。

## 主要方法

- [DARTS](darts.md)：搜尋空間的連續放寬，以梯度下降最佳化。
- [高效神經架構搜尋（ENAS）](efficient-neural-architecture-search.md)：由控制器在一個共享網路的子圖中取樣。
- [正則化演化](regularized-evolution.md)：每一步移除最老架構的老化演化，在相同運算下與強化學習搜尋相當或更好。
- [大規模演化](large-scale-evolution.md)：以新穎突變運算子、從簡單網路開始、在極大規模上執行的簡單演化。
- [MnasNet](mnasnet.md)：獎勵結合準確率與手機實測延遲的強化學習搜尋。

## 變體

- **強化學習搜尋**（Zoph 與 Le，2017）以每個取樣候選的驗證準確率訓練控制器。
- **演化搜尋**保留一群架構並對其突變。Real 等人（2019）顯示，移除族群中最老的成員，而非最差的成員，能使搜尋更有效。
- **硬體感知搜尋**把候選在目標手機上的實測延遲加入目標函數。Tan 等人（2019）以此想法設計行動端影像分類器。

## 結果與限制

- Zoph 與 Le（2017）報告，搜尋所得的網路在 CIFAR-10 上的測試錯誤率為 3.65%，他們形容其可與最好的人工設計架構相匹敵。
- ENAS 報告其成本約為標準 NAS 的千分之一，方法是權重共享（Pham 等人，2018）。
- DARTS 報告其搜尋比非可微分方法快好幾個數量級（Liu 等人，2019）。
- 以權重共享進行的評估，可能不可靠地排序候選。Yu 等人（2020）發現，數種權重共享方法在搜尋階段，並不能可靠地勝過隨機取樣的架構。
- 可微分搜尋可能會朝向無參數運算（如跳接）崩潰，而這在搜尋早期看起來很好。Zela 等人（2020）分析了這種崩潰，並提出可以避免它的正則化。

## 應用

- **行動端與邊緣視覺模型**，其中目標裝置上的延遲是目標的一部分。
- **序列模型**，例如 Zoph 與 Le（2017）為語言建模找到的循環單元。
- **AutoML 系統內可重複使用的搜尋流程**，把架構搜尋與[超參數最佳化](../../optimization/hyperparameter-optimisation/index.md)所述的超參數搜尋結合起來。

## 開放問題

- 當基準也以同等運算量調校時，搜尋出的架構能否勝過調校良好的人工基準？
- 廉價的效能估計有多可靠？它們錯誤排序架構的頻率如何？
- 在一個資料集上搜尋出的架構，能否遷移到其他任務，以及今日使用的大型模型？

## 與其他頁面的連結

- 上層主題：[深度學習](../index.md)
- 調整固定架構的超參數搜尋：[超參數最佳化](../../optimization/hyperparameter-optimisation/index.md)
- 被搜尋的架構類型：[Transformer](../../models/transformer/index.md)

## 參考文獻

### 奠基性論文

- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — 以循環控制器與強化學習設計卷積與循環單元。
- Real, E., Aggarwal, A., Huang, Y. & Le, Q. V. (2019). Regularized Evolution for Image Classifier Architecture Search. In *Proceedings of the AAAI Conference on Artificial Intelligence* 33, 4780–4789. https://doi.org/10.1609/aaai.v33i01.33014780 — 顯示移除最老成員的演化搜尋，在相同運算預算下能與強化學習搜尋相當或更好。
- Pham, H., Guan, M., Zoph, B., Le, Q. & Dean, J. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — 提出候選之間的權重共享，降低搜尋成本。
- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — 提出搜尋空間的連續放寬與雙層梯度搜尋。
- Tan, M. et al. (2019). MnasNet: Platform-Aware Neural Architecture Search for Mobile. In *CVPR 2019*. arXiv:1807.11626. https://arxiv.org/abs/1807.11626 — 把行動手機上的實測延遲加入搜尋目標。

### 綜述與教科書

- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — 把 NAS 組織為搜尋空間、搜尋策略與效能估計的綜述。
- Yu, K. et al. (2020). Evaluating the Search Phase of Neural Architecture Search. In *ICLR 2020*. arXiv:1902.08142. https://arxiv.org/abs/1902.08142 — 檢驗權重共享方法的搜尋階段，是否真能找到好的架構。
- Zela, A. et al. (2020). Understanding and Robustifying Differentiable Architecture Search. In *ICLR 2020*. arXiv:1909.09656. https://arxiv.org/abs/1909.09656 — 分析可微分搜尋的崩潰，並提出正則化方法。

## 延伸學習

- Hutter, F., Kotthoff, L. & Vanschoren, J. (eds.) (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer. https://doi.org/10.1007/978-3-030-05318-5 — 含 NAS 與超參數最佳化章節的書籍。
