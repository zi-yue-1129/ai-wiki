---
related:
- brain-mind/memory-learning
- theory/paradigms/continual
aliases:
  - Experience Replay
  - Replay Buffer
  - 經驗回放
  - 回放緩衝區
tags:
  - reinforcement learning
  - experience replay
  - off-policy learning
translation_reviewed: 2026-10-28
---

# 經驗回放

經驗回放會把代理人蒐集到的轉移（transition）存進緩衝區，之後反覆用來更新。它讓離策略（off-policy）的價值學習變得可行：從緩衝區抽出的 mini-batch 包含過去的經驗，因此更新不只依賴最新的一步。它也打破了相鄰轉移之間的強相關，讓神經網路的訓練更穩定。回放是[價值導向方法](../value-based-methods/index.md)與多數離策略 actor–critic 方法的組件，純同策略（on-policy）的策略梯度方法通常不用它。

## 概觀

回放緩衝區存的是行為策略產生的 \((s_t, a_t, r_t, s_{t+1})\) 元組。每次更新時，學習者抽出一個批次，對取樣到的轉移計算損失，然後繼續。任何變體都由三個決定定義：

- **保留哪些轉移**：全部最近的（先進先出的緩衝區），或經過挑選的。
- **怎麼取樣**：均勻取樣、依優先度取樣，或以整段序列取樣。
- **怎麼修正資料**：因為被存下的轉移來自較舊的策略，取樣可能引入偏差，需要補償。

## 做法

| 變體 | 想法 | 關鍵論文 |
|---|---|---|
| 均勻回放 | 從固定大小的先進先出緩衝區均勻取樣 | Mnih et al. (2015) |
| 優先回放 | 取樣機率隨 TD 誤差增加，並以重要性權重修正偏差 | Schaul et al. (2015), [arXiv:1511.05952](https://arxiv.org/abs/1511.05952) |
| 後見經驗回放（HER） | 在目標導向任務中，把失敗的轉移重新標記為實際達到的目標 | Andrychowicz et al. (2017), [arXiv:1707.01495](https://arxiv.org/abs/1707.01495) |
| 序列回放 | 存下固定長度的序列與序列起點的循環狀態，並用 burn-in 前綴重建該狀態 | Kapturowski et al. (2019), ICLR |
| 分散式回放 | 多個 actor 把經驗寫入同一個有優先度的緩衝區，由單一 learner 取樣 | Horgan et al. (2018), [arXiv:1803.00933](https://arxiv.org/abs/1803.00933) |
| 容量與比例研究 | 量測緩衝區大小與每筆新資料的更新次數如何影響學習 | Fedus et al. (2020), [arXiv:2007.06700](https://arxiv.org/abs/2007.06700) |

### 均勻回放

最初的深度 Q 網路使用從近期轉移緩衝區中均勻取樣。均勻取樣簡單，相對於存下的資料沒有偏差，但它會把同樣多的更新分給模型已經預測得很準的轉移，以及少見、令人意外的轉移。

### 優先回放

優先回放給每個轉移一個優先度，通常是 TD 誤差的大小，並依優先度的某次冪取樣。誤差大的轉移被重播得更頻繁，學習因此加快。由於取樣分布不再是資料分布，每次更新都要用重要性取樣權重加權。網路改變後，優先度會過時；對大型緩衝區計算優先度，也需要像 sum tree 這樣有效率的資料結構。

### 後見回放

在目標導向任務中，多數回合都以失敗結束，因此學習訊號很少。後見回放把代理人實際到達的狀態當作原本的目標，並以這個重新標記的目標與成功獎勵存下轉移。這讓失敗變成對「實際達成目標」有用的範例。

### 序列與分散式回放

循環網路需要序列而不是單一轉移。循環回放會存下固定長度的片段與其儲存的隱藏狀態，並使用 burn-in 前綴，讓訓練開始時的狀態不致過時。分散式回放進一步擴大規模：許多 actor 平行產生經驗，緩衝區保存由 actor 計算的優先度。

## 取捨

- **偏差與速度。** 優先回放學得更快，但會改變訓練分布。重要性權重能修正期望值，但變異可能很大。
- **資料過時。** 舊的轉移來自較舊的策略。大型緩衝區有助於樣本效率，但資料會較不能代表當前策略。
- **記憶體。** 原始觀測（尤其是影像）組成的緩衝區可能主導記憶體用量。
- **超參數。** 容量、每筆新資料的更新比例與優先度指數彼此影響，一個設定下的結果往往無法直接移植。

## 相關連結

回放與[探索](../exploration/index.md)密切相關，因為較大的緩衝區讓代理人能重新檢視罕見的成功。在[持續學習](../../continual/replay-and-memory/index.md)中，同樣的問題也會出現：為了避免遺忘，需要保留舊資料並重播。

大腦的類比是計算神經科學中最有名的例子之一。在睡眠與安靜休息時，海馬迴的位置細胞會重播近期經驗的序列，有時是反向的。Foster 與 Wilson（2006）在清醒的老鼠身上觀察到反向重播，這很像對與獎勵相關序列的優先取樣。這個類比是啟發性的，並非已證實的機制；見[記憶與學習](../../../../brain-mind/memory-learning/index.md)。

## 未解問題與更多變體

- **資料要保留多久。** 先進先出的緩衝區會遺忘，而蓄水池（reservoir）式的保留方式會留下舊轉移。在環境會變動時，哪種保留規則最好尚無定論。
- **過時的優先度。** 優先度是在轉移存入時計算的，會落後於網路。重新計算要花時間，而近似方法是以精度換速度。
- **學習式取樣。** 選擇要重播哪些轉移本身也可以學習，例如用元層級的策略來決定。這比人工設計的優先度還不成熟。
- **離策略修正。** 對於距離很遠的策略，重要性權重可能爆炸。其他修正方法（例如截斷軌跡或裁剪比率）存在，但會和回放設計互相影響。
- **不存原始資料的回放。** 生成模型可以在不儲存資料的情況下重播過去的經驗，這對隱私與記憶體限制很重要，但生成的樣本可能偏移。
- **大型模型的離策略資料。** 類似回放的重複使用，例如示範資料與模型輸出，在大型模型訓練中越來越常見，但這些情境的理論仍不完整。

## 參考文獻

### 開創性論文

- Mnih, V., et al. (2015). "Human-level control through deep reinforcement learning". *Nature* 518. https://doi.org/10.1038/nature14236 — 深度 Q 網路，推廣了均勻回放與目標網路。
- Schaul, T., et al. (2015). "Prioritized Experience Replay". [arXiv:1511.05952](https://arxiv.org/abs/1511.05952) — 依 TD 誤差取樣轉移，並以重要性權重修正偏差。
- Andrychowicz, M., et al. (2017). "Hindsight Experience Replay". [arXiv:1707.01495](https://arxiv.org/abs/1707.01495) — 把失敗的目標導向回合，以實際達到的目標重新標記。
- Horgan, D., et al. (2018). "Distributed Prioritized Experience Replay". [arXiv:1803.00933](https://arxiv.org/abs/1803.00933) — 多個 actor 共用一個有優先度的緩衝區，把回放擴大到大量環境。
- Kapturowski, S., et al. (2019). "Recurrent Experience Replay in Distributed Reinforcement Learning". ICLR. https://iclr.cc/virtual/2019/poster/648 — 以循環隱藏狀態與 burn-in 儲存序列。

### 綜述與教科書

- Fedus, W., et al. (2020). "Revisiting Fundamentals of Experience Replay". [arXiv:2007.06700](https://arxiv.org/abs/2007.06700) — 研究緩衝區容量與回放比例如何改變價值導向代理人的結果。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Foster, D. J. & Wilson, M. A. (2006). "Reverse replay of behavioural sequences in hippocampal place cells during the awake state". *Nature* 440. https://doi.org/10.1038/nature04587 — 海馬迴序列的反向重播，是此類比的神經科學基礎。
