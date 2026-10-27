---
related:
- engineering/training
- engineering/mlops
---

# Frameworks & Tools

## Deep learning frameworks

| Framework | Strengths | Notes |
|---|---|---|
| [PyTorch](https://pytorch.org/) | Dominant in research and increasingly production; eager execution; huge ecosystem; `torch.compile` | Linux Foundation governance |
| [JAX](https://docs.jax.dev/) | Functional transforms (`grad`, `jit`, `vmap`, `pmap`), XLA compilation, excellent on TPUs | Flax, Optax, Equinox |
| [TensorFlow / Keras](https://www.tensorflow.org/) | Mature production tooling (TF Serving, TFLite) | Keras 3 runs on JAX, TF or PyTorch |
| [MLX](https://github.com/ml-explore/mlx) | Apple silicon | On-device experimentation |
| [scikit-learn](https://scikit-learn.org/) | Classical ML | The default for tabular baselines |
| XGBoost, LightGBM, CatBoost | Gradient boosting | Tabular data |

## The Hugging Face ecosystem

- **Hub**: hundreds of thousands of models and datasets
- **transformers**, **diffusers**, **datasets**, **tokenizers**, **accelerate**, **peft**, **trl** (RLHF/DPO), **evaluate**, **smolagents**, **LeRobot**
- `safetensors` as a safe weight format

## Training at scale

| Tool | Purpose |
|---|---|
| PyTorch FSDP, DeepSpeed (ZeRO) | Shard parameters, gradients and optimiser states |
| Megatron-LM / Megatron-Core | Tensor and pipeline parallelism for very large models |
| torchtitan, NeMo | Reference LLM training stacks |
| Ray | Distributed compute and hyperparameter tuning |
| Weights & Biases, MLflow, TensorBoard | Experiment tracking |
| Axolotl, Unsloth, LLaMA-Factory, torchtune | Fine-tuning recipes |

## Inference and serving

| Tool | Notes |
|---|---|
| [vLLM](https://github.com/vllm-project/vllm) | PagedAttention, continuous batching; widely used open serving engine |
| SGLang | Fast serving with structured generation and prefix caching |
| TensorRT-LLM, Triton Inference Server | NVIDIA-optimised |
| llama.cpp / GGUF, Ollama, LM Studio | Local inference on CPUs, Macs, consumer GPUs |
| ONNX Runtime, OpenVINO, Core ML, LiteRT (TFLite), ExecuTorch | Edge and cross-platform deployment |

## LLM application and agent frameworks

- **Orchestration**: LangChain/LangGraph, LlamaIndex, Haystack, DSPy (programmatic prompt optimisation)
- **Agents**: OpenAI Agents SDK, Claude Agent SDK, AutoGen, CrewAI, smolagents
- **Protocols**: Model Context Protocol (MCP) for tools and data; A2A for agent-to-agent communication
- **Structured output**: JSON schema / function calling, Outlines, Instructor
- **Vector databases**: FAISS, pgvector, Qdrant, Weaviate, Milvus, Chroma, LanceDB (see [RAG](../rag/index.md))
- **Observability and evals**: Langfuse, Arize Phoenix, Braintrust, promptfoo, Inspect (UK AISI)

## Domain libraries

- Vision: timm, Ultralytics, Detectron2, MMDetection, OpenCV, Kornia
- Audio: torchaudio, SpeechBrain, ESPnet, NeMo
- Graphs: PyTorch Geometric, DGL
- RL: Gymnasium, Stable-Baselines3, CleanRL, RLlib, TorchRL
- Probabilistic: PyMC, NumPyro, Stan
- Science: DeepChem, RDKit, e3nn, MONAI
- Neuroscience: MNE, Nilearn, Brian2, snnTorch, NEST

## Choosing

- Learning and research → PyTorch (+ Hugging Face)
- TPU-scale or functional style → JAX
- Tabular → scikit-learn + gradient boosting
- Local LLMs → Ollama / llama.cpp; production serving → vLLM or SGLang
