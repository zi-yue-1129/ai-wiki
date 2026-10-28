# 持續學習

## 概念

從**一連串任務或非平穩的資料流**中學習，同時保留過去學到的東西。也稱終身學習或增量學習。標準神經網路會出現**災難性遺忘**（McCloskey & Cohen, 1989）：訓練任務 B 會覆寫解決任務 A 的權重。

## 穩定性—可塑性兩難

學習者必須夠**可塑**才能學新知識，又要夠**穩定**才不會失去舊知識。大腦處理得非常好；人工網路預設則不行。

## 情境

| 情境 | 測試時模型必須…… |
|---|---|
| 任務增量 | 在給定任務身份下解決每個任務 |
| 領域增量 | 在輸入分布改變下解決同一任務 |
| 類別增量 | 不知道任務身份，區分目前為止看過的所有類別（最難） |

（van de Ven, Tuytelaars & Tolias, 2022）

## 方法家族

| 家族 | 想法 | 例子 |
|---|---|---|
| 正規化 | 懲罰對舊任務重要的權重改變 | EWC（Kirkpatrick et al., 2017）、Synaptic Intelligence、MAS |
| 重播（複習） | 把儲存或生成的舊樣本混入新資料 | 經驗重播、iCaRL、生成式重播、dark experience replay |
| 參數隔離／架構式 | 不同任務用不同參數 | Progressive networks、PackNet、每任務一個 adapter/LoRA |
| 知識蒸餾 | 讓新模型輸出接近舊模型 | LwF（Learning without Forgetting） |
| 預訓練模型＋提示 | 凍結強大的骨幹，只學小提示或輸出頭 | L2P、CODA-Prompt |

**彈性權重鞏固（EWC）**加入以 Fisher 資訊 \(F_i\) 加權的二次懲罰：

\[
L(\theta) = L_B(\theta) + \sum_i \frac{\lambda}{2} F_i\,(\theta_i - \theta^*_{A,i})^2
\]

——明確受到大腦突觸鞏固的啟發。

## LLM 的持續學習

- 在新領域或較新資料上持續預訓練，並混入一般資料重播以避免遺忘
- 知識編輯（ROME、MEMIT）針對性更新事實——大規模時很脆弱
- 以檢索與外部記憶「學習」而不改權重
- 微調可能侵蝕安全行為或一般能力——一種實務上的遺忘

## 大腦如何避免災難性遺忘

- **互補學習系統**（McClelland, McNaughton & O'Reilly, 1995）：海馬迴快速、稀疏地學習；新皮質緩慢地學習，並透過海馬迴記憶的**交錯重播**（尤其在睡眠中）被訓練。這正是經驗重播的理論起源
- **突觸鞏固**：學習時形成的樹突棘可維持數月；被選擇性穩定的突觸就像 EWC 保護的權重
- **稀疏、依情境的編碼**減少干擾（類似參數隔離）；神經調節物質控制何時允許可塑性
- **後設可塑性**：突觸會依歷史改變自身的可塑程度（Benna & Fusi 的級聯模型）

見 [記憶與學習的神經機制](../../../brain-mind/memory-learning/index.md)。

## 延伸閱讀

- Parisi et al. (2019)，《Continual lifelong learning with neural networks: A review》。https://arxiv.org/abs/1802.07569
- Kudithipudi et al. (2022)，《Biological underpinnings for lifelong learning machines》，*Nature Machine Intelligence*。https://www.nature.com/articles/s42256-022-00452-0
- Wang et al. (2024)，《A Comprehensive Survey of Continual Learning》，*IEEE TPAMI*。https://arxiv.org/abs/2302.00487
- [Avalanche](https://avalanche.continualai.org/) 函式庫（ContinualAI）
