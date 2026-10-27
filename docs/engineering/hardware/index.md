---
related:
- brain-mind/snn-neuromorphic
- engineering/training
- applications/climate-energy
- society/governance
---

# AI Hardware

## Why hardware matters

Deep learning's rise was enabled by GPUs; today compute is a strategic resource subject to export controls, multi-billion-dollar data centres and power constraints.

## Accelerator families

| Type | Examples | Character |
|---|---|---|
| GPUs | NVIDIA (Hopper H100/H200, Blackwell B200/GB200 and successors), AMD Instinct (MI300/MI350 series) | General-purpose parallel compute; CUDA ecosystem dominance |
| TPUs | Google TPU generations (v5e/v5p, Trillium, Ironwood) | Systolic arrays for matrix multiplication; pods with fast interconnect |
| Other datacentre ASICs | AWS Trainium/Inferentia, Microsoft Maia, Meta MTIA, Huawei Ascend, Cerebras wafer-scale engine, Groq LPU, SambaNova | Specialised for training or low-latency inference |
| Mobile / edge NPUs | Apple Neural Engine, Qualcomm Hexagon, MediaTek APU, Google Tensor | On-device inference at low power |
| FPGAs | AMD/Xilinx, Intel/Altera | Reconfigurable; low-latency niches |
| Neuromorphic | Intel Loihi 2, IBM TrueNorth/NorthPole, SpiNNaker 2 | Event-driven, brain-inspired (see [Spiking Networks](../../brain-mind/snn-neuromorphic/index.md)) |
| Analogue / in-memory | Memristor and phase-change crossbars | Compute where weights are stored; research and early products |
| Photonic | Optical matrix multiplication | Research and startups |

## Key concepts

- **FLOPs and precision**: throughput depends on number format — FP32, TF32, BF16, FP8, FP4/MXFP4 and INT8; lower precision = more throughput, with accuracy care
- **Memory bandwidth** (HBM) is often the bottleneck, especially for LLM inference ("memory wall")
- **Arithmetic intensity** and the roofline model decide whether a kernel is compute- or memory-bound
- **Interconnect**: NVLink/NVSwitch, InfiniBand, Ethernet (Ultra Ethernet), TPU ICI — scaling to tens of thousands of chips
- **Systolic arrays** and tensor cores accelerate matrix multiplication
- **Kernel software**: CUDA, cuDNN, Triton (OpenAI), ROCm, XLA, custom kernels such as FlashAttention
- **Hardware-aware model design**: e.g. Softmax and attention approximations designed for NPUs, MoE routing for memory, quantisation-friendly architectures

## Supply chain and policy

- Leading-edge chips are fabricated mostly by TSMC; advanced packaging (CoWoS) and HBM supply are bottlenecks
- Lithography relies on ASML's EUV machines
- US export controls on advanced AI chips and tools (2022 onward) shape global access; compute thresholds appear in AI regulation (see [Governance](../../society/governance/index.md))

## Energy

Data-centre power and cooling are binding constraints for scaling; see [Climate & Energy](../../applications/climate-energy/index.md). Efficiency gains come from lower precision, sparsity, better kernels, specialised chips and — in the long run — possibly neuromorphic and analogue computing.

## Resources

- Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* (domain-specific architectures chapter)
- Sze et al., *Efficient Processing of Deep Neural Networks*
- [Epoch AI](https://epoch.ai/) data on compute trends and hardware
- SemiAnalysis and Chips and Cheese for industry analysis
