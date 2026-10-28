---
translation_reviewed: 2026-10-28
---

# 基於種群的訓練（Jaderberg 等人，2017）

一種非同步的最佳化方法，訓練一組模型並在訓練過程中調整它們的超參數。落後的成員會複製表現較好成員的權重與超參數，然後探索新的超參數值。

## 問題

學習率、探索設定與損失權重等超參數，會強烈影響神經網路的訓練。在整個訓練過程中使用單一固定設定，通常只是一種折衷。分別訓練許多組態的搜尋方法，會把大部分預算花在不好的設定上，而且最後仍只回傳一組固定設定。Jaderberg 等人探討：單次訓練搭配一個模型種群，能否同時找到超參數時程並選出模型。

## 核心想法

PBT 保留一組工作者，每個工作者平行訓練自己的模型。每個工作者交替進行兩個階段：

- **步驟（step）。** 工作者以梯度下降訓練若干步，並記錄自己的表現（評估分數）。
- **複製與探索（exploit 與 explore）。** 工作者準備好後，可以利用種群中的其他成員。exploit 選擇另一個成員，複製其權重與超參數；explore 則對複製來的超參數進行擾動，或從原始先驗分布重新取樣，作為接下來訓練的新超參數。

因為複製與擾動都發生在訓練過程中，種群產生的是超參數值的時程，而不是一組固定設定。這個方法只需要對標準的分散式訓練框架做少量修改。

## 方程式或演算法

每個工作者重複以下循環：

1. 以目前的權重 \(\theta\) 與超參數 \(h\) 訓練 \(T\) 個梯度步。
2. 以效能指標 \(p\)（例如平均回合回報或驗證分數）評估模型。
3. 若該工作者的表現落後於種群其他成員，複製表現較佳成員的權重與超參數：\(h, \theta \leftarrow \text{exploit}(h, \theta, p, P)\)。
4. 對複製來的超參數進行擾動或重新抽樣：\(h \leftarrow \text{explore}(h)\)，然後繼續訓練。

論文以 \(\text{exploit}\) 選擇記錄效能較高的成員，並以 \(\text{explore}\) 擾動超參數或從先驗中重新抽樣。在實驗中，截斷選擇會把底部 20% 的工作者替換為前 20% 中的某位成員；強化學習的執行則對近期的回報做 t 檢定。多數實驗中，每個超參數以 1.2 或 0.8 的倍數擾動，GAN 實驗則使用 2.0 或 0.5。

## 結果

論文把 PBT 應用於深度強化學習、以機器翻譯為例的監督式學習，以及生成對抗網路。在強化學習方面，它調整了 DeepMind Lab 關卡上的 UNREAL、Atari 遊戲上的 Feudal Networks，以及星海爭霸 II 上的 A3C 智能體。引言指出 PBT「可以匹敵甚至超越經過大量調校的超參數排程」。摘要報告了更快的牆鐘收斂與更高的最終效能。強化學習的比較是在相同步數下進行的，因此論文並未測量其牆鐘速度。在翻譯上，論文報告 BLEU 在驗證集上由 23.71 提高到 24.23，在測試集上由 22.30 提高到 22.65。

## 限制

- **種群成本。** 此方法同時使用許多模型，因此需要足夠的並行運算資源。
- **貪婪複製。** 論文稱 PBT 為貪婪演算法，並且「可能陷入局部最優」。十個或更少的種群可能不足以維持探索所需的多樣性。
- **規則的選擇。** 選擇與探索規則及其設定取決於應用。

## 關聯

- PBT 是一種基於種群的[超參數最佳化](../../../../../../theory/optimization/index.md)，其時程可替代固定的學習率排程。
- 與演化方法一樣，它會挑選並突變種群中的成員，但內部迴圈是基於梯度的訓練。
- 它是 [FTW](../ftw/index.md) 所用種群的訓練方法，並屬於[基於種群的訓練](../index.md)總覽。

## 應用

- **強化學習。** 調整深度智能體的探索與學習率設定。
- **監督式學習。** 直接最大化翻譯的 BLEU 等指標。
- **生成模型。** 依照評估分數調整 GAN 的訓練。

## 未解問題

- 當評估分數有雜訊時，如何選擇 exploit 與 explore 的規則。
- 當複製偏好少數成員時，如何維持種群的多樣性。

## 參考文獻

### 奠基性論文

- Jaderberg et al. (2017), "Population based training of neural networks", [arXiv:1711.09846](https://arxiv.org/abs/1711.09846) — PBT 論文，包含 exploit 與 explore 步驟，以及在強化學習、翻譯與 GAN 上的實驗。
- Snoek, Larochelle & Adams (2012), "Practical Bayesian optimization of machine learning algorithms", [arXiv:1206.2944](https://arxiv.org/abs/1206.2944) — 超參數的貝氏最佳化，是 PBT 排程的搜尋式基線。
- Jaderberg et al. (2016), "Reinforcement learning with unsupervised auxiliary tasks", [arXiv:1611.05397](https://arxiv.org/abs/1611.05397) — UNREAL，論文中 PBT 所調整的智能體之一。
- Jaderberg et al. (2019), "Human-level performance in 3D multiplayer games with population-based reinforcement learning", *Science* 364, 859–865. https://discovery.ucl.ac.uk/id/eprint/10076318 — 把基於種群的訓練應用於奪旗遊戲。連結為作者機構的典藏紀錄。
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — 超參數是 PBT 所調整種類的深度強化學習方法。
