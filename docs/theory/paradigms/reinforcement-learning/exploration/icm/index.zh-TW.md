---
translation_reviewed: 2026-10-28
---

# 內在好奇心模組（Pathak 等人，2017）

一種探索方法，給智能體的好奇心獎勵等於其自身前向模型在學到的特徵空間中的誤差。特徵以自監督的逆動態模型訓練，因此獎勵會忽略智能體無法影響的環境部分。

## 問題

外在獎勵常常極為稀疏，甚至完全沒有，因此智能體需要內在獎勵來探索，並學習日後可能有用的技能。把原始像素當作好奇心訊號的預測效果很差，因為智能體無法控制的視覺細節（例如擺動的樹葉）會產生很大的誤差，卻沒有有用的資訊。Pathak 等人探討如何定義好奇心，使它對智能體自身動作的後果有所反應。

## 核心想法

ICM 有三個網路：

- **編碼器**把觀測 \(s_t\) 映射為特徵向量 \(\phi(s_t)\)。
- **逆動態模型**從 \(\phi(s_t)\) 與 \(\phi(s_{t+1})\) 預測動作 \(a_t\)。訓練這個模型會迫使特徵保留智能體動作能影響的資訊，並捨棄其餘部分。
- **前向模型**從 \(\phi(s_t)\) 與 \(a_t\) 預測 \(\phi(s_{t+1})\)。

內在獎勵是前向模型在特徵空間中的平方誤差。環境中智能體無法影響的部分不會被 \(\phi\) 表示，因此不會產生好奇心。智能體會因造訪那些「自己的動作會產生它尚未能預測之後果」的狀態而獲得獎勵。

## 方程式或演算法

以前向模型 \(\hat\phi\)，內在獎勵為

\[
r^{\text{int}}_t = \tfrac{\eta}{2}\,\lVert \hat\phi(\phi(s_t), a_t) - \phi(s_{t+1}) \rVert_2^2 ,
\]

其中 \(\eta\) 是縮放因子。編碼器、前向模型與逆模型聯合訓練，而策略最大化內在與外在獎勵的總和。

## 結果

論文在 VizDoom 與超級瑪利歐兄弟等視覺遊戲上評估 ICM，這些遊戲的外在獎勵稀疏或不存在。摘要指出，單靠好奇心就能讓智能體學會探索。論文的圖示報告，只以好奇心訓練的智能體能跨越超級瑪利歐兄弟第一關的很大一部分，而在 VizDoom 中，智能體學會沿著走廊行走，而不是撞牆或卡在角落。

## 限制

- **隨機動態。** 若智能體無法控制的狀態與轉移相關，前向模型仍可能無法預測。
- **新穎性。** 與其他好奇心獎勵一樣，它偏好智能體難以預測的狀態，而這些狀態未必是任務重要的狀態。
- **特徵學習。** 逆模型的特徵取決於智能體的動作，因此在智能體幾乎無法控制的環境中，探索可能較弱。

## 關聯

- 上層主題：[探索](../index.md)。
- 它與 [隨機網路蒸餾](../rnd/index.md)同屬預測誤差獎勵，但它在學到的特徵空間中預測，而 RND 則與隨機目標比較。
- 論文的主要智能體 ICM with A3C 結合好奇心獎勵與[非同步演員–評論家方法 A3C](../../policy-gradient-and-actor-critic/a3c/index.md)。

## 應用

- **稀疏獎勵的遊戲**，如論文使用的平台遊戲與第一人稱遊戲。
- **機器人學**，智能體必須學會哪些動作會改變場景。

## 未解問題

- 如何讓特徵空間捕捉智能體的控制能力，又不遺失與任務相關的細節。
- 如何把好奇心與目標導向的探索結合。

## 參考文獻

### 奠基性論文

- Pathak, Agrawal, Efros & Darrell（2017），"Curiosity-driven exploration by self-supervised prediction"，[arXiv:1705.05363](https://arxiv.org/abs/1705.05363)——ICM 論文，包含逆動態特徵空間、前向模型獎勵，以及 VizDoom 與超級瑪利歐兄弟實驗。
- Burda, Edwards, Storkey & Klimov（2018），"Exploration by random network distillation"，[arXiv:1810.12894](https://arxiv.org/abs/1810.12894)——RND，不需要特徵空間的預測誤差獎勵。
- Bellemare 等人（2016），"Unifying count-based exploration and intrinsic motivation"，[arXiv:1606.01868](https://arxiv.org/abs/1606.01868)——偽計數獎勵，是好奇心方法比較的計數方法。
- Stadie, Levine & Abbeel（2015），"Incentivizing exploration in reinforcement learning with deep predictive models"，[arXiv:1507.00814](https://arxiv.org/abs/1507.00814)——較早、以學到的預測模型為基礎的預測型探索獎勵。
- Houthooft 等人（2016），"VIME: Variational information maximizing exploration"，[arXiv:1605.09674](https://arxiv.org/abs/1605.09674)——資訊增益探索，是另一種好奇心訊號。
