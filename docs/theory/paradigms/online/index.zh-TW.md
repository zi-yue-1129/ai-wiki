# 線上學習與多臂吃角子老虎

## 線上學習

資料**一次一筆**地到來；學習者先預測、看到結果、立即更新。不假設資料獨立同分布——在對抗式設定中，序列甚至可以由對手選擇。

**表現指標：遺憾（regret）**——比事後看來最好的固定決策差了多少。

\[
\text{Regret}_T = \sum_{t=1}^T \ell_t(w_t) - \min_w \sum_{t=1}^T \ell_t(w)
\]

好的演算法達到次線性遺憾（例如 \(O(\sqrt{T})\)），也就是平均遺憾趨近於零。

| 演算法 | 說明 |
|---|---|
| 線上梯度下降 | 把 SGD 看成線上演算法 |
| 感知器 | 經典線上分類器 |
| Hedge／乘法權重 | 結合專家建議；學習理論與賽局論的基礎 |
| Follow-the-regularised-leader | 統一許多線上方法 |
| Online Newton step、AdaGrad | 自適應步長（AdaGrad 源自線上學習） |

## 多臂吃角子老虎（Multi-armed bandits）

賭徒面對 K 台中獎率未知的吃角子老虎機，每次拉桿**只看到被拉那台**的獎勵。這是**探索—利用權衡**最純粹的形式。

| 演算法 | 想法 |
|---|---|
| ε-greedy | 大多數時候利用，以機率 ε 探索 |
| 信賴上界（UCB） | 「面對不確定時保持樂觀」：選看起來可能最好的那台 |
| Thompson 取樣 | 從後驗抽一個信念，依它貪婪行動 |
| EXP3 | 對抗式吃角子老虎 |
| 情境式吃角子老虎（LinUCB、神經網路版） | 依情境特徵選擇行動 |

應用：新聞與商品推薦、廣告投放、自動分流流量的 A/B 測試、適應性臨床試驗、動態定價、把查詢路由到不同的 LLM 或提示。

吃角子老虎是沒有狀態轉移的一步版[強化學習](../reinforcement-learning/index.md)。

## 串流資料與概念漂移

真實資料流會漂移。工具：漂移偵測（ADWIN、DDM、Page–Hinkley）、滑動視窗、增量樹（Hoeffding trees），以及 [River](https://riverml.xyz/) 等函式庫。另見 [持續學習](../continual/index.md) 與 [MLOps](../../../engineering/mlops/index.md)。

## 大腦與心智中的探索

- 人類混合使用**有方向的探索**（尋求資訊，類似 UCB）與**隨機探索**（決策雜訊，類似 Thompson／softmax）（Wilson et al., 2014；Gershman, 2018）
- **藍斑核—正腎上腺素**系統被認為在利用與探索之間切換（Aston-Jones & Cohen, 2005）
- 吃角子老虎任務中，**額極皮質**活動追蹤探索性選擇（Daw et al., 2006）
- 探索隨年齡下降，兒童比成人更愛探索——一種生命早期的「高溫」搜尋（Gopnik, 2020）
- 吃角子老虎任務是**計算精神醫學**的標準工具，用來測量焦慮、憂鬱、ADHD 中改變的探索行為

## 延伸閱讀

- Lattimore & Szepesvári，《Bandit Algorithms》，Cambridge University Press。https://cambridge.org/core/books/bandit-algorithms/introduction/022B0BDCFDC5B66E5EF2C2690467D928
- Shalev-Shwartz (2012)，《Online Learning and Online Convex Optimization》。https://doi.org/10.1561/2200000018
- Hazan，《Introduction to Online Convex Optimization》。預印本（免費）：https://arxiv.org/abs/1909.05207
- Russo et al.，《A Tutorial on Thompson Sampling》。https://arxiv.org/abs/1707.02038
