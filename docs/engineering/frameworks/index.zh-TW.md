# 框架與工具

## 深度學習框架

| 框架 | 優點 | 說明 |
|---|---|---|
| [PyTorch](https://pytorch.org/) | 在研究領域居主導地位，且在正式環境中日益普及；即時執行（eager execution）；生態系龐大；`torch.compile` | 由 Linux Foundation 治理 |
| [JAX](https://docs.jax.dev/) | 函數式轉換（`grad`、`jit`、`vmap`、`pmap`）、XLA 編譯，在 TPU 上表現極佳 | 相關套件：Flax、Optax、Equinox |
| [TensorFlow／Keras](https://www.tensorflow.org/) | 成熟的正式環境工具（TF Serving、TFLite） | Keras 3 可在 JAX、TF 或 PyTorch 上執行 |
| [MLX](https://github.com/ml-explore/mlx) | 適用於 Apple 晶片 | 裝置端實驗 |
| [scikit-learn](https://scikit-learn.org/) | 傳統機器學習 | 表格資料基準方法的預設選擇 |
| XGBoost、LightGBM、CatBoost | 梯度提升 | 表格資料 |

## Hugging Face 生態系

- **Hub**：數十萬個模型與資料集
- **transformers**、**diffusers**、**datasets**、**tokenizers**、**accelerate**、**peft**、**trl**（RLHF／DPO）、**evaluate**、**smolagents**、**LeRobot**
- 以 `safetensors` 作為安全的權重格式

## 大規模訓練

| 工具 | 用途 |
|---|---|
| PyTorch FSDP、DeepSpeed（ZeRO） | 分片參數、梯度與優化器狀態 |
| Megatron-LM／Megatron-Core | 超大模型的張量與管線平行 |
| torchtitan、NeMo | LLM 訓練的參考技術堆疊 |
| Ray | 分散式運算與超參數調校 |
| Weights & Biases、MLflow、TensorBoard | 實驗追蹤 |
| Axolotl、Unsloth、LLaMA-Factory、torchtune | 微調配方 |

## 推論與服務化

| 工具 | 說明 |
|---|---|
| [vLLM](https://github.com/vllm-project/vllm) | PagedAttention、連續批次處理；廣泛使用的開源服務引擎 |
| SGLang | 快速服務，支援結構化生成與前綴快取 |
| TensorRT-LLM、Triton Inference Server | 針對 NVIDIA 最佳化 |
| llama.cpp／GGUF、Ollama、LM Studio | 在 CPU、Mac 與消費級 GPU 上進行本地推論 |
| ONNX Runtime、OpenVINO、Core ML、LiteRT（TFLite）、ExecuTorch | 邊緣與跨平台部署 |

## LLM 應用與代理人框架

- **編排**：LangChain／LangGraph、LlamaIndex、Haystack、DSPy（程式化的提示最佳化）
- **代理人**：OpenAI Agents SDK、Claude Agent SDK、AutoGen、CrewAI、smolagents
- **協定**：用於工具與資料的 Model Context Protocol（MCP）；用於代理人之間通訊的 A2A
- **結構化輸出**：JSON schema／函式呼叫、Outlines、Instructor
- **向量資料庫**：FAISS、pgvector、Qdrant、Weaviate、Milvus、Chroma、LanceDB（見 [RAG](../rag/index.md)）
- **可觀測性與評估**：Langfuse、Arize Phoenix、Braintrust、promptfoo、Inspect（英國 AISI）

## 領域函式庫

- 視覺：timm、Ultralytics、Detectron2、MMDetection、OpenCV、Kornia
- 音訊：torchaudio、SpeechBrain、ESPnet、NeMo
- 圖：PyTorch Geometric、DGL
- 強化學習：Gymnasium、Stable-Baselines3、CleanRL、RLlib、TorchRL
- 機率：PyMC、NumPyro、Stan
- 科學：DeepChem、RDKit、e3nn、MONAI
- 神經科學：MNE、Nilearn、Brian2、snnTorch、NEST

## 如何選擇

- 學習與研究 → PyTorch（加上 Hugging Face）
- TPU 規模或偏好函數式風格 → JAX
- 表格資料 → scikit-learn 加梯度提升
- 本地 LLM → Ollama／llama.cpp；正式環境服務 → vLLM 或 SGLang
