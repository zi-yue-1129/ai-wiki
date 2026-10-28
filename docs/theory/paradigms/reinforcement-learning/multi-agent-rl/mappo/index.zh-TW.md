---
translation_reviewed: 2026-10-28
---

# 多智能體 PPO（Yu 等人，2022）

顯示以共享策略與集中式價值函數的 PPO，是合作式多智能體遊戲中很強的基線，在數個基準上與 QMIX 和 MADDPG 相當。

## 問題

QMIX 與 MADDPG 等離策略及價值分解方法，主導了合作式多智能體基準。PPO 簡單且廣泛使用，但一般認為它在多智能體設定中較弱。Yu 等人探討：PPO 經過幾項有依據的調整後，能否在這些任務上表現良好。

## 核心想法

論文比較兩種做法：獨立 PPO（IPPO），每個智能體在局部觀測上有自己的評論家；以及 MAPPO，智能體共享一個策略網路，並由集中式價值函數以全域狀態為輸入。在智能體同質的設定中使用參數共享，論文附錄指出，有參數共享的 MAPPO「以明顯差距勝過沒有參數共享的 MAPPO」。價值函數可以同時接受智能體專屬特徵與全域特徵作為輸入。

## 方程式或演算法

MAPPO 即[近端策略最佳化](../../proximal-policy-optimisation/index.md)的 PPO 演算法，但有三項改變：智能體共享的演員、以全域狀態為輸入的集中式價值函數 \(V(s)\)，以及由該價值計算的優勢估計。論文建議以下做法：

- **價值正規化**，以穩定價值學習。
- **價值輸入**同時包含局部的智能體專屬特徵與全域特徵（若可取得）。
- **有限的迭代次數。**困難環境最多 10 次訓練迭代，簡單環境最多 15 次。
- **裁剪**，比率低於 0.2 時效果最好。
- **大批次**，以取得最佳的任務表現。

論文也發現，在多智能體領域中，若樣本重複使用過於頻繁，表現會下降。

## 結果

- **SMAC。**IPPO 與 MAPPO 在絕大多數地圖上都表現強勁。在相同的樣本數下，MAPPO 在多數地圖上至少與 QMIX 相當。在 6h_vs_8z 上，搭配特徵修剪的 MAPPO 中位勝率為 88.3%，QMIX 為 9.4%。
- **MPE。**MAPPO 與離策略基線表現相當，在所有任務上都與 QMIX 非常接近。
- **Google Research Football。**MAPPO 在每個情境中都明顯優於 QMIX。在 3v1 上，MAPPO 為 88.03，QMIX 為 8.12。
- **Hanabi。**MAPPO 的結果與該基準報告的最佳與平均回報相當或更好。

## 限制

- **樣本重用。**訓練資料重複使用過多時表現會下降，這限制了同策略方法的樣本效率。
- **同質智能體。**參數共享最適合同質智能體，論文最強的主張也多針對這類設定。
- **超參數敏感。**多項建議的因素彼此相互影響，結果需要仔細調整。

## 連結

- 母頁：[多智能體強化學習](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 它所調整的單智能體演算法是[近端策略最佳化](../../proximal-policy-optimisation/index.md)。
- 主要替代方案是 [QMIX](../qmix/index.md)（價值分解）與 [MADDPG](../maddpg/index.md)（集中式評論家的演員–評論家方法）。

## 應用

- **合作基準。**論文使用的星際爭霸多智能體挑戰（StarCraft Multi-Agent Challenge）、Google Research Football 與 Hanabi。
- **模擬中的團隊協調。**具有共享獎勵的多智能體導航與通訊任務。

## 未解問題

- 這些建議做法如何推廣到異質團隊與更多智能體。
- 如何結合同策略方法的穩定性與回放方法的樣本效率。

## 參考文獻

### 開創性論文

- Yu et al. (2022), "The surprising effectiveness of PPO in cooperative multi-agent games", NeurIPS 2022 Datasets and Benchmarks Track, [arXiv:2103.01955](https://arxiv.org/abs/2103.01955) — The MAPPO paper, with the benchmark results and recommended practices above.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — The single-agent PPO algorithm that MAPPO adapts.
- Rashid et al. (2018), "QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning", *Proceedings of ICML 2018*, PMLR 80, [arXiv:1803.11485](https://arxiv.org/abs/1803.11485) — The value-factorisation baseline that MAPPO is compared against.
- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — MADDPG, the centralised-critic baseline in the paper's comparisons.
- Engstrom et al. (2020), "Implementation matters in deep policy gradients: a case study on PPO and TRPO", [arXiv:2005.12729](https://arxiv.org/abs/2005.12729) — Shows that implementation details, which the MAPPO recommendations also depend on, can change PPO's results.
