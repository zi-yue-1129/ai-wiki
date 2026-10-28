# AI 硬體

## 為什麼硬體重要

深度學習的崛起得益於 GPU；如今運算已成為戰略資源，受到出口管制、數十億美元的資料中心與電力限制的約束。

## 加速器類型

| 類型 | 例子 | 特性 |
|---|---|---|
| GPU | NVIDIA（Hopper H100／H200、Blackwell B200／GB200 及其後繼產品）、AMD Instinct（MI300／MI350 系列） | 通用的平行運算；CUDA 生態系佔主導地位 |
| TPU | Google 各世代 TPU（v5e／v5p、Trillium、Ironwood） | 用於矩陣乘法的脈動陣列；搭配高速互連的機架群 |
| 其他資料中心 ASIC | AWS Trainium／Inferentia、Microsoft Maia、Meta MTIA、華為昇騰（Ascend）、Cerebras 晶圓級引擎、Groq LPU、SambaNova | 專為訓練或低延遲推論設計 |
| 行動裝置／邊緣 NPU | Apple Neural Engine、Qualcomm Hexagon、MediaTek APU、Google Tensor | 低功耗的裝置端推論 |
| FPGA | AMD／Xilinx、Intel／Altera | 可重新配置；適合低延遲的利基市場 |
| 神經形態 | Intel Loihi 2、IBM TrueNorth／NorthPole、SpiNNaker 2 | 事件驅動、受大腦啟發（見[脈衝神經網路](../../brain-mind/snn-neuromorphic/index.md)） |
| 類比／記憶體內運算 | 憶阻器與相變交叉陣列 | 在儲存權重的地方進行運算；處於研究與早期產品階段 |
| 光子 | 光學矩陣乘法 | 研究與新創公司 |

## 關鍵概念

- **FLOPs 與精度**：吞吐量取決於數值格式——FP32、TF32、BF16、FP8、FP4／MXFP4 與 INT8；精度越低吞吐量越高，但需要留意準確度
- **記憶體頻寬**（HBM）常常是瓶頸，對 LLM 推論尤其明顯（「記憶體牆」）
- **運算強度**與屋脊線模型決定一個核心運算是受限於運算還是記憶體
- **互連**：NVLink／NVSwitch、InfiniBand、乙太網路（Ultra Ethernet）、TPU ICI——擴展到數萬個晶片
- **脈動陣列**與張量核心加速矩陣乘法
- **核心軟體**：CUDA、cuDNN、Triton（OpenAI）、ROCm、XLA，以及像 FlashAttention 這類自訂核心
- **考量硬體的模型設計**：例如為 NPU 設計的 Softmax 與注意力近似、為記憶體考量的 MoE 路由、適合量化的架構

## 供應鏈與政策

- 最先進的晶片主要由台積電製造；先進封裝（CoWoS）與 HBM 的供應是瓶頸
- 微影依賴 ASML 的 EUV 機台
- 美國自 2022 年起對先進 AI 晶片與工具實施出口管制，影響全球的取得途徑；運算門檻也出現在 AI 法規中（見[治理](../../society/governance/index.md)）

## 能源

資料中心的電力與冷卻，是規模化擴展的硬性限制；見[氣候與能源](../../applications/climate-energy/index.md)。效率的提升來自較低的精度、稀疏化、更好的核心、專用晶片，以及長期來看可能的神經形態與類比運算。

## 學習資源

- Hennessy 與 Patterson，*Computer Architecture: A Quantitative Approach*（特定領域架構的章節）
- Sze et al.，*Efficient Processing of Deep Neural Networks*
- [Epoch AI](https://epoch.ai/) 關於運算趨勢與硬體的資料
- SemiAnalysis 與 Chips and Cheese 的產業分析
