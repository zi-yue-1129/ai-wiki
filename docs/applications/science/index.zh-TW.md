# 科學發現

AI 正在改變科學的做法：它可以作為**替代模擬器**、**模式發現者**、**假說生成者**、**實驗規劃者**，並且越來越常擔任**研究代理人**。

## 依領域

| 領域 | 例子 |
|---|---|
| 天氣與氣候 | GraphCast（GNN）、Pangu-Weather、FourCastNet、GenCast（擴散式、機率性）；ECMWF 已將 AI 預報（AIFS，2025）納入作業——以極低的運算成本，常比傳統數值模式更準確 |
| 材料科學 | GNoME 預測了數十萬種新的穩定晶體；MatterGen 生成具有目標性質的材料；機器學習原子間勢（MACE）加速模擬 |
| 化學 | 逆合成規劃、反應預測、自主化學實驗室（Coscientist、ChemCrow） |
| 物理 | 大型強子對撞機的噴注標記與異常偵測；以強化學習控制託卡馬克電漿（Degrave et al., 2022）；神經網路量子態；以符號迴歸重新發現定律 |
| 天文 | 系外行星偵測、星系形態、重力波偵測，以及利用學習到的先驗重建黑洞陰影影像 |
| 數學 | 引導結理論與表示論中的直覺（Davies et al., 2021）；用於組合數學的 FunSearch；用於奧林匹克題目的 AlphaProof 與 AlphaGeometry；LLM 加上 Lean 形式化 |
| 生物 | 見[生命科學](../life-science/index.md) |
| 地球觀測 | 洪水預報（Google Flood Hub）、森林砍伐監測、作物製圖 |
| 神經科學 | 連結體重建、尖峰分類、行為追蹤——見[神經科學基礎](../../brain-mind/neuroscience/index.md) |

## 典型方法

- **替代模型／仿真器**：訓練網路來逼近昂貴的模擬（流體力學、氣候、分子動力學）——速度快好幾個數量級
- **物理資訊機器學習**：把微分方程或對稱性嵌入模型（PINN、FNO 等神經算子、等變網路）
- **反問題**：利用學習到的先驗，從觀測（影像、斷層掃描）推斷成因
- **閉環發現**：貝氏最佳化加上機器人＝自主實驗室（例如用於材料合成的 A-Lab）
- **以文獻為基礎的發現**：LLM 探勘數百萬篇論文以找出關聯
- **AI 科學家**：能生成假說、執行計算實驗並撰寫論文的代理人（Sakana 的 AI Scientist、Google 的 AI co-scientist、FutureHouse 的代理人）；產出仍需要人類仔細審查

## 疑慮

- **可重現性**：以機器學習為基礎的科學中，資料洩漏十分普遍（Kapoor & Narayanan, 2023 在多個領域都發現了洩漏）
- **驗證**：AI 生成的假說與主張（例如「數百萬種新材料」）需要實驗證實；部分主張後來受到批評
- **理解與預測**：預測精準，卻沒有機制層面的洞見
- **單一文化**：過度依賴相同的工具與資料集，會使研究的視野變窄（Messeri & Crockett, 2024, *Nature*）

## 學習資源

- Wang et al. (2023), "Scientific discovery in the age of artificial intelligence", *Nature*
- [AI for Science](https://ai4sciencecommunity.github.io/) 社群、Microsoft Research AI for Science、DeepMind 科學部落格
- Karniadakis et al. (2021), "Physics-informed machine learning", *Nature Reviews Physics*
- [WeatherBench 2](https://sites.research.google/weatherbench/)
