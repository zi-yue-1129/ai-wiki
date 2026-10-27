# 計算神經科學

用數學模型、模擬與資料分析理解神經系統**如何計算**。

## Marr 的三個分析層次

David Marr（1982）《Vision》提出理解任何資訊處理系統的三個層次，至今仍是 AI 與神經科學共同的思考框架：

| 層次 | 問題 | 例子（視覺邊緣偵測） | AI 對照 |
|---|---|---|---|
| 計算層次 | 要解決什麼問題？為什麼？ | 找出影像中強度劇烈變化的位置 | 損失函數、目標 |
| 演算法／表徵層次 | 用什麼表徵與演算法？ | 高斯拉普拉斯濾波、零交叉 | 模型架構、學習規則 |
| 實作層次 | 物理上如何實現？ | 視網膜神經節細胞、V1 簡單細胞 | GPU、神經形態晶片 |

Richards et al.（2019, *Nature Neuroscience*）〈A deep learning framework for neuroscience〉建議用「**目標函數、學習規則、架構**」三要素理解大腦，這直接借用了深度學習的觀點。

## 神經元模型

| 模型 | 複雜度 | 說明 |
|---|---|---|
| McCulloch-Pitts | 極簡 | 二值閾值單元 |
| 速率模型 | 簡單 | 輸出為放電頻率，類似人工神經元 |
| 整合放電（LIF） | 簡單 | 膜電位積分輸入、漏電、超過閾值就發脈衝並重置；SNN 的基礎 |
| Izhikevich 模型 | 中等 | 兩個變數即可重現多種放電型態 |
| Hodgkin-Huxley | 高 | 以離子通道動力學描述動作電位（1963 年諾貝爾獎） |
| 多室模型 | 很高 | 包含樹突結構的空間細節 |

LIF 方程：

\[
\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R\,I(t), \quad V \geq V_{th} \Rightarrow \text{發放脈衝}, V \leftarrow V_{reset}
\]

## 神經編碼與解碼

- **編碼**：刺激 → 神經反應。調諧曲線、感受野、線性—非線性—泊松（LNP）模型、廣義線性模型（GLM）
- **解碼**：神經反應 → 刺激或意圖。線性解碼器、貝氏解碼器、深度網路；BCI 的核心（見 [腦機介面](../bci/index.md)）
- **群體編碼**：資訊分布在許多神經元的共同活動中
- **有效編碼與稀疏編碼**：Olshausen & Field（1996）以稀疏編碼學習自然影像，得到類似 V1 簡單細胞的感受野——無監督學習解釋神經特性的經典例子

## 神經網路動力學

- **吸引子網路**：Hopfield 網路（記憶）、連續吸引子（頭部方向細胞、工作記憶）
- **興奮—抑制平衡**
- **儲備池計算**（Reservoir Computing / Echo State Networks）
- **神經流形與低維動力學**：高維神經活動常落在低維流形上；用 RNN 訓練認知任務再分析其動力學，可產生關於前額葉的假說（Mante et al., 2013；Sussillo & Barak, 2013）
- **臨界性假說**：大腦可能運作在有序與混沌的邊界

## 學習規則

| 規則 | 說明 |
|---|---|
| Hebb 規則 | 共同活化的突觸增強：\(\Delta w \propto x_{pre}\,x_{post}\) |
| Oja 規則 | 加入正規化的 Hebb，會學出主成分 |
| BCM 規則 | 具有滑動閾值的可塑性 |
| STDP | 突觸前比突觸後早放電 → 增強；晚放電 → 減弱 |
| 三因子規則 | Hebb ＋ 第三個調節訊號（如多巴胺），連結局部可塑性與獎勵學習 |

## 規範性模型（Normative Models）

從「最佳化某個目標」推導出大腦應該怎麼做，再與實驗比較：有效編碼、貝氏觀察者、最佳控制、強化學習、資源理性（resource rationality）。

## 工具

- 模擬：[NEURON](https://neuron.yale.edu/)、[NEST](https://www.nest-simulator.org/)、[Brian2](https://briansimulator.org/)
- 資料分析：[MNE-Python](https://mne.tools/)（EEG/MEG）、[Nilearn](https://nilearn.github.io/)（fMRI）、[SpikeInterface](https://spikeinterface.readthedocs.io/)
- 資料標準與平台：[NWB](https://www.nwb.org/)、[DANDI Archive](https://dandiarchive.org/)、[OpenNeuro](https://openneuro.org/)、Allen Brain Atlas

## 學習資源

- Dayan & Abbott《Theoretical Neuroscience》
- Gerstner 等《Neuronal Dynamics》（[線上全文](https://neuronaldynamics.epfl.ch/)）
- [Neuromatch Academy 計算神經科學課程](https://compneuro.neuromatch.io/)（CC BY 4.0，強烈推薦）
- Marr《Vision》
- 3Blue1Brown 風格的 Artem Kirsanov YouTube 頻道（計算神經科學視覺化）
