---
status: complete
last_reviewed: 2026-11-01
related:
  - engineering/inference-optimization
  - engineering/hardware
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - Splitwise
  - Phase splitting
---

# Splitwise

!!! info "Part of Disaggregated Prefill and Decode"
    This method belongs to [Disaggregated Prefill and Decode](disaggregated-serving.md), which compares the systems.

Splitwise assigns prompt processing and subsequent token generation to different machines, with independent provisioning for the two phases.[^splitwise] Separation can use homogeneous hardware; different accelerator types are an option, not a requirement. The paper's workloads show different compute and memory demands, motivating phase-specific allocation.

## Scheduling and handoff

The design has prompt, token and dynamically sized **mixed** pools. A cluster scheduler selects a prompt/token machine pair using queues measured in pending tokens; machine schedulers manage local queues and batching.[^splitwise]

The prompt machine produces the first token and KV cache. The token machine continues generation. Layer-wise asynchronous transfers can overlap later prompt computation; smaller prompts can use serialized transfer instead. Mixed-pool machines can serve both phases at high load.[^splitwise]

Thus a two-box diagram is a useful introduction, but does not fully describe the scheduler. Pool management also differs from assigning one dedicated machine to every request: each machine can serve multiple requests over time.

## Why cache transfer matters

The state contains cached attention keys and values for the processed context. PagedAttention addresses cache allocation and sharing; it does not make network transfer free.[^paged] The query-head count is not always the key/value-head count: grouped-query attention shares key/value heads across groups of queries.[^gqa]

For one hypothetical sequence with uniform layers, the **logical** uncompressed payload is

$$
B_{\mathrm{KV}}=2LSH_{\mathrm{KV}}d_hb.
$$

Here $L$ is layer count, $S$ cached sequence length, $H_{\mathrm{KV}}$ key/value heads, $d_h$ elements per head, and $b$ bytes per element. The factor two counts keys and values.

This counts tensor elements, not a particular implementation's allocation. It excludes metadata, padding, replication, compression and transport overhead. Distributed shards may divide the logical payload, while replicated heads can increase the physical total; do not assume that each GPU holds this entire amount.

### Worked payload example

Assume $L=32$, $S=4096$, $H_{\mathrm{KV}}=8$, $d_h=128$ and $b=2$. Then the logical cache is **536,870,912 bytes = 512 MiB**. At an effective payload bandwidth of **25 GB/s**, using decimal gigabytes, a fully serialized transfer takes at least

$$
t_{\mathrm{transfer}}\geq
\frac{B_{\mathrm{KV}}}{\beta_{\mathrm{effective}}}
=\frac{536{,}870{,}912}{25\times10^9}
\approx21.5\ \mathrm{ms}.
$$

These are illustrative parameters, not measurements of Splitwise or a named model. If $H_{\mathrm{KV}}$ were 32 instead, the payload would be four times larger. A link's advertised bit rate, effective byte throughput and a binary MiB count must not be substituted for one another.

The bound measures transfer work in this simple single-flow model. Overlap can hide part of that work from end-to-end latency; it does not eliminate bytes or synchronization. Shared network capacity and simultaneous transfers can make effective per-request bandwidth smaller.

## First token versus the handoff gap

Because the prompt worker can return the first token before a serialized transfer completes, measuring only **time to first token (TTFT)** can miss a subsequent pause.[^splitwise]

Consider this deliberately serial illustrative timeline, with transfer at that bandwidth limit, a 40 ms initial wait-and-prefill time and an 8 ms decode step:

| Event | Time from arrival, approximately |
|---|---|
| First token returned | 40.0 ms |
| Cache transfer completes | 61.5 ms |
| Second token returned | 69.5 ms |

TTFT is 40 ms, while the first-to-second token gap is about 29.5 ms. This is arithmetic for the assumed timeline, not a measured schedule. Queueing, overlapping transfer or a different point at which tokens are delivered changes it.

Report inter-token latency and its tail as well as TTFT. DistServe similarly treats prefill and decoding latency objectives separately when allocating resources and placement.[^distserve]

## What the evaluation establishes

The prototype extends vLLM for cache transfer; the larger cluster designs use a profiled, event-driven simulator.[^splitwise] It is important to distinguish those measurements from simulated provisioning results.

Two specific reported operating points are:

- **Figure 18(a), conversation trace:** Splitwise-AA achieves 2.15× the throughput of Baseline-A100 at the same cost and provisioned power.
- **Figure 18(b), iso-cost:** Splitwise-AA achieves 1.4× the throughput of Baseline-H100, using 25% more power and twice the space.[^splitwise]

These are different baselines and constraints, not simultaneous attributes of one deployment. Provisioned power is a capacity budget, not automatically the measured energy consumed per request.

## Related techniques

- [Orca](orca.md) introduces iteration-level scheduling; it is a scheduling reference, not evidence that the Splitwise prototype runs the Orca implementation.[^orca]
- [PagedAttention and vLLM](paged-attention.md) concern cache memory management, a separate issue from cross-machine routing.[^paged]
- [DistServe](distserve.md) optimizes phase-specific resources and parallelism under latency constraints.[^distserve]
- [Mooncake](mooncake.md) uses a KV-cache-centric architecture, including distributed cache resources and overload handling.[^mooncake]

## Reproduction and operational limits

A comparison should record:

1. Model and checkpoint, attention-head layout, cache precision and parallelism.
2. Accelerator types, machine counts, power caps and the cost accounting period.
3. Prompt/output length distributions, arrival process, batch policy and pool-sizing policy.
4. Effective network bandwidth, transfer strategy and the number of concurrent transfers.
5. Latency objectives and percentiles, accepted request rate, per-request gaps and resource utilisation.
6. What is measured on hardware and what is estimated with a model or simulator.

Keep the lossless handoff assumption explicit. Changing cache precision or representation introduces an additional approximation whose accuracy needs separate evaluation. A scheduling improvement does not itself establish that a lossy cache representation preserves outputs.

Failures and retries need an explicit state-ownership policy: which worker owns a request, when a transfer is complete and what the client has already received. These are deployment questions rather than guarantees inferred from throughput figures. Replaying a request after partial output also requires care to avoid duplicate streamed tokens.

A workload with long prompts stresses different resources from one with long outputs. Fixed pool ratios should therefore be evaluated against changing demand, not assumed optimal for every trace.

[^splitwise]: Patel et al., arXiv v2 (2024), Sections IV–VI and Figure 18; see References.
[^paged]: Kwon et al. (2023), abstract; see References.
[^gqa]: Ainslie et al. (2023), abstract; see References.
[^distserve]: Zhong et al. (2024), abstract; see References.
[^orca]: Yu et al. (2022), publisher abstract; see References.
[^mooncake]: Qin et al., arXiv v5 (2026), abstract; see References.

## References

- Patel, P. et al. (2023; revised 2024). *Splitwise: Efficient Generative LLM Inference Using Phase Splitting*. https://arxiv.org/abs/2311.18677 — Describes phase-specific pools, scheduling, cache transfer and hardware-profiled cluster design evaluation.
- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. https://arxiv.org/abs/2401.09670 — Optimizes phase allocation and placement under first-token and per-output-token latency requirements.
- Qin, R. et al. (2024; revised 2026). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. https://arxiv.org/abs/2407.00079 — Describes distributed cache resources, separated serving phases and scheduling under overload.
- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI. https://www.usenix.org/conference/osdi22/presentation/yu — Introduces iteration-level scheduling and selective batching for autoregressive generation.
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP. https://arxiv.org/abs/2309.06180 — Addresses KV-cache fragmentation and sharing to enable larger serving batches.
- Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. EMNLP. https://aclanthology.org/2023.emnlp-main.298/ — Explains why key/value-head count can differ from query-head count in grouped-query attention.
