# 世界模型與具身智慧

## 世界模型是什麼？

**世界模型**＝代理人內部對環境如何運作的模型，能預測「如果我做 a，接下來會發生什麼」。有了世界模型，代理人可以在「想像」中規劃，而不必在真實世界中試誤。

這個概念源自心理學：Craik（1943）提出心智建構外部世界的「小型模型」；Tolman（1948）發現老鼠會建立迷宮的**認知地圖**。

## 技術路線

| 路線 | 代表 | 說明 |
|---|---|---|
| 潛在動力學模型 | World Models（Ha & Schmidhuber, 2018）、Dreamer 系列、MuZero | 在壓縮的潛在空間預測未來，用於 RL 規劃；DreamerV3 能在 Minecraft 中從零收集鑽石 |
| 影片生成作為世界模擬器 | Sora、Genie 系列、Cosmos 等 | 生成可互動或物理上合理的影片世界 |
| JEPA | I-JEPA、V-JEPA 系列 | LeCun 主張在表徵空間預測，而非像素 |
| 自駕車世界模型 | GAIA 等 | 生成駕駛場景供訓練與測試 |
| LLM 作為隱式世界模型 | Othello-GPT | 只看棋步文字訓練的模型，內部出現了棋盤狀態的表徵（Li et al., 2023） |

## 具身智慧（Embodied AI）

智慧不只在大腦中，而是在**身體與環境的互動**中產生。

### Moravec 悖論
對人類困難的事（下棋、算數）對電腦容易；對人類容易的事（走路、拿杯子）對電腦極難。因為感覺運動能力經過數億年演化最佳化。

### 機器人基礎模型

| 類型 | 代表 |
|---|---|
| 視覺—語言—行動模型 VLA | RT-2、OpenVLA、π0／π0.5（Physical Intelligence）、Gemini Robotics、GR00T（NVIDIA） |
| 大規模機器人資料 | Open X-Embodiment（數十家實驗室、多種機器人）、DROID |
| 模仿學習 | ALOHA、Diffusion Policy、Action Chunking Transformer |
| 模擬平台 | Isaac Sim/Lab、MuJoCo、Habitat、Genesis |

詳見 [機器人](../applications/robotics.md)。

## 神經科學與認知科學基礎

- **預測性大腦**：小腦被認為包含運動的**前向模型**，預測動作的感覺後果（Wolpert 等），讓我們搔自己不覺得癢
- **認知地圖**：海馬迴**位置細胞**（O'Keefe, 1971）與內嗅皮質**網格細胞**（Moser 夫婦, 2005），2014 年諾貝爾生理醫學獎；近年認為海馬迴—內嗅系統不只表徵空間，也表徵抽象概念空間（Behrens et al., 2018）
- **心智模擬與想像**：海馬迴受損者難以想像未來情境（Hassabis et al., 2007）
- **具身認知**：概念理解依賴感覺運動系統（Barsalou 的知覺符號系統、Lakoff 的概念隱喻）
- **主動推論**：代理人透過行動讓感官輸入符合預測（Friston），見 [認知科學](../brain-mind/cognitive-science.md)
- **發展心理學**：嬰兒透過操作物體建立直覺物理與物體恆存概念（Spelke 的核心知識）

## 開放問題

- 影片生成模型是否真的學到物理，還是只學到表面統計？
- 如何讓世界模型支援長時程、可組合的規劃？
- 機器人資料遠少於網路文字，如何擴展？
- 具身經驗對「理解」是否必要？

## 學習資源

- Ha & Schmidhuber〈World Models〉互動論文 [worldmodels.github.io](https://worldmodels.github.io/)
- LeCun〈A Path Towards Autonomous Machine Intelligence〉（2022）
- Hafner 等 DreamerV3 論文
- Pfeifer & Bongard《How the Body Shapes the Way We Think》
