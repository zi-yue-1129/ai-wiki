---
translation_reviewed: 2026-10-28
---

# 脈衝神經網路與神經形態運算

## 為什麼要用脈衝？

生物神經元用短暫、離散的**脈衝**溝通。脈衝神經網路（SNN）——有時稱為「第三代」神經網路（Maass, 1997）——明確地模擬這一點。吸引力在於：

- **能源效率**：只在脈衝發生時運算（事件驅動），而且脈衝是二值的
- **時間編碼**：時序本身就能攜帶資訊
- **生物擬真**：連接神經科學模型與機器學習的橋樑
- **天然適合事件式感測器**（動態視覺感測器、矽耳蝸）

## SNN 常用的神經元模型

| 模型 | 說明 |
|---|---|
| 漏電整合放電（LIF） | 主力模型；見 [計算神經科學](../computational-neuroscience/index.md) |
| 適應性 LIF／ALIF | 加入放電頻率適應，改善時間任務（Bellec et al., 2018） |
| Izhikevich | 低成本產生豐富的放電型態 |
| 共振放電 | 振盪動態 |
| Hodgkin–Huxley | 對大型 SNN 太昂貴；用於細緻建模 |

## 脈衝編碼方式

| 方式 | 資訊由什麼攜帶 |
|---|---|
| 頻率編碼 | 一段時間內的脈衝數 |
| 首脈衝時間／延遲編碼 | 第一個脈衝何時到達 |
| 相位編碼 | 相對於振盪的脈衝時機 |
| 群體／順序編碼 | 哪些神經元、以什麼順序放電 |
| 差分／事件編碼 | 輸入的變化 |

## 訓練 SNN

脈衝是階梯函數，導數幾乎處處為零——反向傳播無法直接使用。

| 方法 | 想法 | 工具 |
|---|---|---|
| ANN 轉 SNN | 先訓練一般網路，再把啟動值映射成放電頻率 | 準確率好，但常需很多時間步 |
| 代理梯度 | 反向傳播時用平滑的替代導數；隨時間反向傳播（Neftci, Mostafa & Zenke, 2019） | snnTorch、SpikingJelly、Norse、Lava-DL |
| 局部／生物合理規則 | STDP、三因子規則、e-prop（Bellec et al., 2020） | 晶片上線上學習 |
| 精確脈衝時間梯度 | EventProp 等方法 | 事件式訓練 |
| 演化／儲備池方法 | 液態機 | 可訓練參數很少 |

### 脈衝時序依賴可塑性（STDP）

突觸前脈衝比突觸後脈衝早 Δt > 0 到達，突觸增強；晚到則減弱——通常是數十毫秒的指數視窗（Bi & Poo, 1998）。單靠 STDP 就能做非監督特徵學習；加上獎勵訊號（獎勵調節 STDP）則支援強化學習。

## 神經形態硬體

| 晶片／系統 | 機構 | 說明 |
|---|---|---|
| TrueNorth | IBM（2014） | 100 萬個神經元，約 70 mW |
| Loihi／Loihi 2 | Intel（2017／2021） | 晶片上學習；Hala Point 系統（2024）約 11.5 億個神經元 |
| SpiNNaker／SpiNNaker 2 | 曼徹斯特大學／德勒斯登工大 | 大量 ARM 核心即時模擬大腦 |
| BrainScaleS | 海德堡 | 類比、加速（比生物時間快） |
| Akida | BrainChip | 商用邊緣 AI |
| Speck／Xylo | SynSense | 超低功耗視覺與音訊 |
| 天機芯（Tianjic） | 清華大學 | ANN/SNN 混合晶片（Nature, 2019） |
| 達爾文系列 | 浙江大學 | 大規模神經形態系統 |

相關：以憶阻器、相變記憶體做的**記憶體內運算**，把權重存在運算發生的地方——就像突觸。

## SNN 擅長與不擅長的地方

**適合**：常駐感測（關鍵字喚醒、手勢辨識、異常偵測）、事件相機視覺、功耗受限的機器人、腦機介面與植入裝置、振動訊號的預測性維護、即時大腦模擬。

**挑戰**：在大型基準上與 ANN 的準確率差距已縮小但部分仍存在；訓練較慢；工具與硬體分散；能源效益高度依賴脈衝稀疏度與實際使用的硬體——要仔細評測。脈衝版 Transformer 與 LLM（如 Spikformer、SpikeGPT）是活躍研究方向。

## 事件式感測器

**動態視覺感測器**（事件相機）非同步地輸出每個像素的亮度變化，延遲達微秒級、動態範圍高——受視網膜啟發。是無人機、機器人與高速追蹤中 SNN 的天然搭檔。

## 關鍵方法

### 替代梯度（Neftci、Mostafa 與 Zenke，2019）

- **問題：** 脈衝是階躍函數，其導數幾乎處處為零，因此反向傳播無法直接訓練脈衝網路。
- **核心想法：** 前向傳遞時保留硬閾值；反向傳遞時，以平滑的替代函數取代閾值的導數，再進行時間反向傳播。
- **方程式：** 前向時，神經元在膜電位超過閾值時發放脈衝；反向時，其導數被以以閾值為中心的平滑替代函數 \(\sigma'\) 取代。
- **結果：** 論文將替代梯度呈現為訓練脈衝網路的一種靈活且有效的方法，而非單一基準的結果。
- **限制：** 替代函數的選擇是經驗性的。時間反向傳播需要儲存網路的歷史，記憶體成本隨序列長度增加。

### 具局部更新的線上學習：e-prop（Bellec 等人，2020）

- **問題：** 時間反向傳播需要完整的歷史，也很難與生物學調和。遞迴脈衝網路能否只用局部可取得的資訊進行線上學習？
- **核心想法：** 以每個突觸的資格跡（可隨時間向前計算）近似梯度，並與從外部傳到神經元的學習訊號結合。如此，更新可以在每個時間步進行。
- **方程式：** 權重更新是把學習訊號與資格跡相乘後，對時間加總：

\[
\Delta W_{ji} = \sum_t L_j(t)\, e_{ji}(t)
\]

- **結果：** 作者指出，在其測試的任務上，此線上規則的表現接近時間反向傳播。
- **限制：** 此規則省略了部分梯度項，因此只是近似。報告的結果僅涵蓋作者選擇的任務。

## 學習資源

- Eshraghian et al. (2023), "Training Spiking Neural Networks Using Lessons From Deep Learning", *Proceedings of the IEEE*，以及 [snnTorch](https://snntorch.readthedocs.io/) 教學
- Roy, Jaiswal & Panda (2019), *Nature*
- Schuman et al. (2022), *Nature Computational Science*
- Gerstner 等《Neuronal Dynamics》（免費線上）
- [Open Neuromorphic](https://open-neuromorphic.org/) 社群
- 框架：[snnTorch](https://github.com/jeshraghian/snntorch)、[SpikingJelly](https://github.com/fangwei123456/spikingjelly)、[Norse](https://github.com/norse/norse)、[Lava](https://github.com/lava-nc/lava)、[Brian2](https://briansimulator.org/)

## 參考文獻

### 開創性論文

- Neftci, E. O., Mostafa, H. & Zenke, F.（2019）。Surrogate Gradient Learning in Spiking Neural Networks. *IEEE Signal Processing Magazine*. https://doi.org/10.1109/MSP.2019.2931595 — 提出替代梯度，讓脈衝網路能以時間反向傳播訓練。
- Bellec, G., 等人（2020）。A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*. https://doi.org/10.1038/s41467-020-17236-y — e-prop 學習規則，是脈衝網路時間反向傳播的線上近似。

### 綜述與教科書

- Eshraghian, J. K., 等人（2023）。Training Spiking Neural Networks Using Lessons From Deep Learning. *Proceedings of the IEEE*. https://doi.org/10.1109/JPROC.2023.3308088 — 以深度學習工具訓練脈衝網路的教學，含 snnTorch 範例。
- Roy, K., Jaiswal, A. & Panda, P.（2019）。Towards spike-based machine intelligence with neuromorphic computing. *Nature*. https://doi.org/10.1038/s41586-019-1677-2 — 脈衝式運算與神經形態硬體的綜述。
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L.（2014）。*Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — 關於脈衝神經元模型與網路的免費線上教科書。
