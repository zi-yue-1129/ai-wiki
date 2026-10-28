# 氣候與能源

## AI 用於氣候

| 領域 | 例子 |
|---|---|
| 天氣與氣候模擬 | AI 天氣模型（GraphCast、GenCast、Pangu-Weather、ECMWF 的 AIFS）；氣候模式中的機器學習參數化；GraphCast 之外的混合模型，例如 NeuralGCM |
| 極端事件 | 在 80 多個國家的洪水預報（Google Flood Hub）、野火偵測、颱風路徑追蹤、熱浪預測 |
| 排放監測 | 以衛星偵測甲烷羽流、從影像估算發電廠排放（Climate TRACE）、森林砍伐警示 |
| 電網 | 負載與再生能源發電量預測、電網平衡、故障偵測、需量反應 |
| 建築與工業 | 空調控制（DeepMind 在 2016 年把資料中心冷卻能耗降低約 40%）、製程效率 |
| 能源材料 | 電池電解質、觸媒、太陽能材料、碳捕捉吸附劑（見[科學發現](../science/index.md)） |
| 核融合 | 以強化學習控制託卡馬克電漿；電漿破裂預測 |
| 運輸 | 路線最佳化、電動車充電排程 |
| 調適 | 作物韌性、早期預警系統、保險 |

Rolnick et al. (2022), "Tackling Climate Change with Machine Learning", *ACM Computing Surveys*，全面梳理了這個領域。

## AI 自身的足跡

| 議題 | 說明 |
|---|---|
| 用電 | 資料中心的需求快速成長；國際能源總署（IEA，2025）預估，全球資料中心用電量到 2030 年將約增加一倍，其中 AI 是主要推動力 |
| 碳排放 | 取決於電網組成與時間點；訓練前沿模型的排放很可觀，但在大規模的情況下，推論往往佔了許多估算的大宗 |
| 用水 | 冷卻需要用水；當地的水資源壓力很重要 |
| 硬體 | 晶片與伺服器的內含排放，以及電子廢棄物 |
| 透明度 | 很少供應商揭露每個模型的能耗，各種估算差距很大 |

減緩方向：更有效率的模型（蒸餾、量化、MoE、稀疏化）、更節能的硬體、把運算排程到潔淨能源時段、選址靠近再生能源，以及建立回報標準。神經形態運算有望在某些工作負載上大幅節能（見[脈衝神經網路](../../brain-mind/snn-neuromorphic/index.md)）。

## 學習資源

- [Climate Change AI](https://www.climatechange.ai/)：論文、暑期學校、教學資料
- IEA (2025)，*Energy and AI*
- Luccioni 等人關於量測 AI 碳足跡的研究；[CodeCarbon](https://codecarbon.io/)
- [WeatherBench 2](https://sites.research.google/weatherbench/)
