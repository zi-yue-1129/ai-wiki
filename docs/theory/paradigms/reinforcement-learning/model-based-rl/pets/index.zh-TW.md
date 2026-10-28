---
translation_reviewed: 2026-10-28
---

# 機率式集成與軌跡取樣（Chua 等人，2018）

一種基於模型的方法，學習機率式神經網路動態模型的集成，並透過取樣軌跡進行規劃。集成表示對模型的不確定性，而取樣則把這份不確定性傳播到規劃中。

## 問題

基於模型的強化學習樣本效率高，但在使用高容量神經網路時，其漸近表現常低於最佳的無模型方法。Chua 等人探討如何縮小這個差距。他們研究能回報自身不確定性的模型，使規劃不會在資料稀少的地方過度信任模型。

## 核心想法

PETS 有兩個組成部分：

- **機率式集成。** 集成中的每個模型預測的是下一個狀態的分布，而不是單一點估計。集成同時捕捉兩種不確定性：每次預測中的偶然（aleatoric）雜訊，以及因資料有限而來的認知（epistemic）不確定性。
- **軌跡取樣。** 為了選擇動作，方法從集成中取樣若干粒子，讓每個粒子在規劃視野內通過模型向前傳播，並選擇平均分數最高的動作序列。取樣讓模型的不確定性保留在計畫中，而不是被壓縮成平均預測。

智能體在每一步都重新規劃（模型預測控制），只執行所選序列的第一個動作。

## 方程式或演算法

在每個規劃步驟中，智能體：

1. 以目前收集的資料擬合機率式集成。
2. 取樣動作序列；對每個序列，在視野 \(H\) 內以隨機選出的集成成員傳播粒子。
3. 以預測獎勵的總和為每個序列評分，並選擇分數最高者。
4. 執行第一個動作，觀察下一個狀態，加入資料，然後重複。

此方法不會在想像的資料上學習策略，而是在每一步直接用模型規劃。

## 結果

摘要報告，PETS 「在數個具挑戰性的基準任務上，達到無模型演算法的漸近表現，同時所需樣本數顯著減少」。在半獵豹（half-cheetah）任務上，作者報告 PETS 所需樣本數分別是軟演員–評論家的 8 分之一，以及近端策略最佳化的 125 分之一。

## 限制

- **規劃成本。** 每一步都要取樣軌跡，計算成本高於執行已學好的策略。
- **模型類別。** 結果取決於集成的架構，以及不確定性的表示方式。
- **基準範圍。** 實驗都在連續控制任務上進行，因此其他設定中的轉移並未被展示。

## 關聯

- 上層主題：[基於模型的強化學習](../index.md)。
- 規劃的概念與模型預測控制相關，上層頁面將其列為主要方法之一。
- [MBPO](../mbpo/index.md) 使用類似的集成，但以無模型學習器訓練策略，而不是在每一步規劃。
- 論文中的基準是[軟演員–評論家](../../policy-gradient-and-actor-critic/sac/index.md)與 [PPO](../../proximal-policy-optimisation/index.md)。

## 應用

- **機器人控制**，適用於真實試驗很少的情況。
- **連續控制**任務，動態模型平滑的情況。

## 未解問題

- 如何讓規劃在大型觀測空間中仍然足夠便宜。
- 如何把規劃與學到的策略結合，使運算量可以在執行時權衡。

## 參考文獻

### 奠基性論文

- Chua, Calandra, McAllister & Levine（2018），"Deep reinforcement learning in a handful of trials using probabilistic dynamics models"，[arXiv:1805.12114](https://arxiv.org/abs/1805.12114)——PETS 論文，包含機率式集成、軌跡取樣與樣本效率比較。
- Janner 等人（2019），"When to trust your model: Model-based policy optimization"，[arXiv:1906.08253](https://arxiv.org/abs/1906.08253)——MBPO，以短程模型展開訓練策略的基於模型方法。
- Kurutach 等人（2018），"Model-ensemble trust-region policy optimization"，[arXiv:1802.10592](https://arxiv.org/abs/1802.10592)——早期使用模型集成以減少策略最佳化中模型誤差的方法。
- Haarnoja 等人（2018），"Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor"，[arXiv:1801.01290](https://arxiv.org/abs/1801.01290)——PETS 用來比較樣本效率的無模型基準。
- Schulman 等人（2017），"Proximal policy optimization algorithms"，[arXiv:1707.06347](https://arxiv.org/abs/1707.06347)——PETS 用來比較樣本效率的無模型基準。
