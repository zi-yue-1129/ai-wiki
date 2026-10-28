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

每個工作者重複以下迴圈：

1. 以目前的權重 \(\theta\) 與超參數 \(h\) 進行 \(T\) 步梯度訓練。
2. 以效能指標 \(p\) 評估模型，例如平均回合回報或驗證分數。
3. 若該工作者的表現落後於種群中的其他成員，複製表現較好成員的權重與超參數，\(h, \theta \leftarrow \text{exploit}(h, \theta, p, P)\)。
4. 對複製來的超參數進行擾動或重新取樣，\(h \leftarrow \text{explore}(h)\)，然後繼續訓練。

論文中，\(\text{exploit}\) 會選擇紀錄表現較高的成員，\(\text{explore}\) 則擾動超參數或從先驗分布重新取樣。

## 結果

論文將 PBT 應用於深度強化學習、機器翻譯的監督式學習，以及生成對抗網路。在強化學習方面，它調整 UNREAL 在 DeepMind Lab 關卡上的設定、Feudal Networks 在 Atari 遊戲上的設定，以及 A3C 智能體在星海爭霸上的設定。作者報告，PBT「能夠與經過精心調整的超參數時程相當，甚至更好」，並且能讓智能體以更快的實際時間收斂，最終表現也更高。

## 限制

- **種群成本。** 此方法同時使用許多模型，需要足夠的平行運算資源。
- **貪婪地複製。** exploit 會複製表現最好的成員，可能降低種群的多樣性。
- **規則的選擇。** exploit 與 explore 的規則及其設定取決於應用。

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

- Jaderberg 等人（2017），"Population based training of neural networks"，[arXiv:1711.09846](https://arxiv.org/abs/1711.09846)——PBT 論文，包含 exploit 與 explore 步驟，以及在強化學習、翻譯與 GAN 上的實驗。
- Snoek, Larochelle & Adams（2012），"Practical Bayesian optimization of machine learning algorithms"，[arXiv:1206.2944](https://arxiv.org/abs/1206.2944)——超參數的貝氏最佳化，是 PBT 時程的搜尋式基準。
- Jaderberg 等人（2016），"Reinforcement learning with unsupervised auxiliary tasks"，[arXiv:1611.05397](https://arxiv.org/abs/1611.05397)——UNREAL，論文中 PBT 所調整的智能體之一。
- Jaderberg 等人（2019），"Human-level performance in 3D multiplayer games with population-based reinforcement learning"，*Science* 364, 859–865。https://doi.org/10.1126/science.aau6249——將 PBT 應用於奪旗遊戲。
- Mnih 等人（2015），"Human-level control through deep reinforcement learning"，*Nature* 518, 529–533。https://doi.org/10.1038/nature14236——深度強化學習方法之一，其超參數正是 PBT 所調整的類型。
