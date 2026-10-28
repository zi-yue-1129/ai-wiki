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
- **Hardware-aware model design**: e.g. Softmax and attention approximations designed for NPUs, [MoE](../../theory/models/mixture-of-experts/index.md) routing for memory, quantisation-friendly architectures

## Subchapters

- [AI accelerators](accelerators/index.md): GPU, TPU and ASIC design principles, with pages on the [TPU](accelerators/tpu/index.md) and [Eyeriss v2](accelerators/eyeriss-v2/index.md).
- [Memory Hierarchy and Bandwidth](memory-hierarchy/index.md): registers, on-chip SRAM and HBM, arithmetic intensity, the [roofline model](memory-hierarchy/roofline.md), and why LLM decoding is bandwidth-bound.
- [Interconnects and Scaling](interconnects/index.md): NVLink, InfiniBand and TPU inter-chip links, collective operations, and how parallelism strategies use them.
- [In-Memory and Analogue Computing](in-memory-computing/index.md): computing inside resistive crossbars, the noise and conversion costs it brings, and its training and LLM challenges.
- [Hardware-Aware Model and Software Co-Design](co-design/index.md): number formats, fused kernels and compilers, and architecture choices measured on the target chip.

## Supply chain and policy

- Leading-edge chips are fabricated mostly by TSMC; advanced packaging (CoWoS) and HBM supply are bottlenecks
- Lithography relies on ASML's EUV machines
- US export controls on advanced AI chips and tools (2022 onward) shape global access; compute thresholds appear in AI regulation (see [Governance](../../society/governance/index.md))

## Energy

Data-centre power and cooling are binding constraints for scaling; see [Climate & Energy](../../applications/climate-energy/index.md). Efficiency gains come from lower precision, sparsity, better kernels, specialised chips and — in the long run — possibly neuromorphic and analogue computing.

## Open issues

- **The memory wall.** Gholami et al. argue that memory bandwidth now limits AI serving more than compute. Whether future chips close that gap, or widen it, is open.
- **Sparse hardware.** Speed-ups from unstructured sparsity remain rare on accelerators, so the benefit of pruning depends on the chip.
- **Comparable measurements.** Vendor throughput and power figures use different precisions, memory systems and software, so they are hard to compare.

## References

### Seminal papers

- Jouppi, N. P., et al. (2017). *In-Datacenter Performance Analysis of a Tensor Processing Unit*. arXiv:1704.04760. https://arxiv.org/abs/1704.04760 — Reports the TPU at about 15 to 30 times the speed of contemporary CPUs and GPUs, with far better performance per watt.
- Chen, Y.-H., et al. (2018). *Eyeriss v2: A Flexible Accelerator for Emerging Deep Neural Networks on Mobile Devices*. arXiv:1807.07928. https://arxiv.org/abs/1807.07928 — A mobile accelerator that exploits sparsity, reported as 12.6 times faster than the original Eyeriss.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — A tutorial and survey of DNN hardware, architectures and evaluation metrics.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory bandwidth, not compute, is the main constraint on AI serving.
- Dao, T., et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — An IO-aware attention kernel that reduces memory traffic between GPU memory levels.
