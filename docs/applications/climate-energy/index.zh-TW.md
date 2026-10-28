# 氣候與能源

## AI 用於氣候

| 領域 | 例子 |
|---|---|
| 天氣與氣候模擬 | AI 天氣模型（GraphCast、GenCast、Pangu-Weather、ECMWF 的 AIFS）；氣候模式中的機器學習參數化；GraphCast 之外的混合模型，例如 NeuralGCM |
| 極端事件 | 洪水預報（Google Flood Hub）、野火偵測、颱風路徑追蹤、熱浪預測 |
| 排放監測 | 以衛星偵測甲烷羽流、從影像估算發電廠排放（Climate TRACE）、森林砍伐警示 |
| 電網 | 負載與再生能源發電量預測、電網平衡、故障偵測、需量反應 |
| 建築與工業 | 空調控制（例如資料中心）、製程效率 |
| 能源材料 | 電池電解質、觸媒、太陽能材料、碳捕捉吸附劑（見[科學發現](../science/index.md)） |
| 核融合 | 以強化學習控制託卡馬克電漿；電漿破裂預測 |
| 運輸 | 路線最佳化、電動車充電排程 |
| 調適 | 作物韌性、早期預警系統、保險 |

Rolnick et al. (2022), "Tackling Climate Change with Machine Learning", *ACM Computing Surveys*，全面梳理了這個領域。

## AI 自身的足跡

| 議題 | 說明 |
|---|---|
| 用電 | 資料中心的需求快速成長；AI 所占的比例，各方預估差異很大 |
| 碳排放 | 取決於電網組成與時間點；訓練前沿模型的排放很可觀，但在大規模的情況下，推論往往佔了許多估算的大宗 |
| 用水 | 冷卻需要用水；當地的水資源壓力很重要 |
| 硬體 | 晶片與伺服器的內含排放，以及電子廢棄物 |
| 透明度 | 很少供應商揭露每個模型的能耗，各種估算差距很大 |

減緩方向：更有效率的模型（蒸餾、量化、MoE、稀疏化）、更節能的硬體、把運算排程到潔淨能源時段、選址靠近再生能源，以及建立回報標準。神經形態運算有望在某些工作負載上大幅節能（見[脈衝神經網路](../../brain-mind/snn-neuromorphic/index.md)）。

## 關鍵方法

下列三種方法與本頁最相關。每一項都連結到解釋該方法的頁面。

- [圖神經網路](../../theory/models/gnn/message-passing/index.md)：在大氣網格圖上做訊息傳遞，如 GraphCast（Lam et al., 2023）。
- [去噪擴散](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)：生成一組預報的擴散模型，如 GenCast（Price et al., 2024）。
- [策略梯度與 actor-critic](../../theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/index.md)：用於控制物理系統的強化學習，例如托卡馬克電漿形狀（Degrave et al., 2022）。

## 參考文獻

### 開創性論文

- Lam et al. (2023). Learning skillful medium-range global weather forecasting. *Science*. https://doi.org/10.1126/science.adi2336 — GraphCast，以圖神經網路預測全球天氣。
- Price et al. (2024). Probabilistic weather forecasting with machine learning. *Nature*. https://doi.org/10.1038/s41586-024-08252-9 — GenCast，以擴散模型做機率式預報。
- Bi et al. (2023). Accurate medium-range global weather forecasting with 3D neural networks. *Nature*. https://doi.org/10.1038/s41586-023-06185-3 — Pangu-Weather，用於全球預報的三維神經網路。
- Degrave et al. (2022). Magnetic control of tokamak plasmas through deep reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-021-04301-9 — 強化學習控制托卡馬克中的電漿形狀。

### 綜述與教科書

- Rolnick et al. (2022). Tackling Climate Change with Machine Learning. *ACM Computing Surveys*. https://doi.org/10.1145/3485128 — 全面回顧機器學習在氣候減緩與調適上的應用。
