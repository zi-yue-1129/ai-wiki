# 元學習與少樣本學習

## 概念

**學會學習**：在「任務的分布」上訓練，使新任務只需極少範例就能學會。最常見的目標是少樣本學習：看 1–5 個例子就認得新類別（N-way K-shot）。

## 家族

| 家族 | 想法 | 例子 |
|---|---|---|
| 度量式 | 學一個嵌入空間，讓最近鄰或原型規則有效 | Siamese 網路、Matching Networks、Prototypical Networks |
| 最佳化式 | 學一組初始值（或最佳化器），幾步梯度就能適應 | MAML、Reptile、學習的最佳化器 |
| 模型式／黑盒 | 序列模型讀入範例並輸出預測 | 記憶增強網路、SNAIL、RL² |
| 貝氏／階層式 | 學習跨任務共享的先驗 | Neural processes、階層貝氏 |
| 上下文學習 | 大型預訓練 Transformer 從提示中的範例學習 | GPT-3 之後的 LLM |

**MAML**（Finn et al., 2017）尋找參數 \(\theta\)，使其在新任務的小資料集上做一兩步梯度更新後就表現良好：

\[
\min_\theta \sum_{\mathcal{T}} L_{\mathcal{T}}\big(\theta - \alpha \nabla_\theta L_{\mathcal{T}}(\theta)\big)
\]

## 上下文學習：湧現的元學習

只以下一個 token 預測訓練的 LLM，能從提示中的幾個例子學會任務。研究顯示 Transformer 可以在前向傳播中實作學習演算法（例如對線性迴歸做類似梯度下降的更新；Garg et al., 2022；von Oswald et al., 2023），而具有「爆發性」、Zipf 分布結構的資料會促進上下文學習（Chan et al., 2022）。用整個網路預訓練，實際上就是在數百萬個隱含任務上做元訓練。

## 相關概念

- **超參數最佳化與 AutoML**：學習學習的設定
- **神經架構搜尋**
- **學習的最佳化器**（VeLO）
- **元強化學習**：在一個回合內就能適應新環境的代理人

## 大腦與認知

- **Harlow 的學習定勢（1949）**：猴子解過許多「二選一辨別」問題後，解新問題越來越快——「學會學習」的原始證明
- **前額葉作為元強化學習系統**（Wang et al., 2018, *Nature Neuroscience*）：緩慢的多巴胺驅動學習，訓練出一個遞迴的前額葉網路，再由它在活動動態中執行自己的快速學習演算法
- **人類一次學習**：人看一個例子就能學會新的手寫字元；貝氏程式學習（Lake, Salakhutdinov & Tenenbaum, 2015）與 Omniglot 基準就是為此設計
- **演化提供的歸納偏誤**：演化是外迴圈、終生學習是內迴圈——以元學習觀點看先天結構
- **海馬迴**支援快速的一次性情節學習；見 [記憶與學習](../../../brain-mind/memory-learning/index.md)

## 延伸閱讀

- Hospedales et al. (2021)，《Meta-Learning in Neural Networks: A Survey》。https://arxiv.org/abs/2004.05439
- Finn et al. (2017) MAML。https://arxiv.org/abs/1703.03400
- Snell et al. (2017) Prototypical Networks。https://arxiv.org/abs/1703.05175
- Lake et al. (2017)，《Building machines that learn and think like people》，*Behavioral and Brain Sciences*。https://arxiv.org/abs/1604.00289
- Stanford CS330《Deep Multi-Task and Meta Learning》。https://cs330.stanford.edu
