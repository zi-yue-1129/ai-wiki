---
status: complete
last_reviewed: 2026-11-02
related:
  - engineering/inference-optimization
  - engineering/hardware
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - Mooncake
  - KVCache-centric architecture
---

# Mooncake

!!! info "Part of Disaggregated Prefill and Decode"
    This method page belongs to [Disaggregated Prefill and Decode](disaggregated-serving.md). The parent page compares the systems; this page explains Mooncake's cache placement and overload policy.

Mooncake combines separate prefill and decoding pools with a distributed key-value (KV) cache. Its scheduler considers where reusable prefixes are stored, how long their transfer takes, and whether a request can finish within latency targets. The description below follows Qin et al.'s paper, including its October 2026 revision.[^mooncake]

## Problem

Prefill processes the prompt and builds the attention KV cache; decoding uses that state to generate further tokens. Long prompts can occupy resources needed for responsive decoding. Separating the phases reduces interference, but introduces another decision: where should the request run when its reusable state is on a different machine?

Two service-level objectives (SLOs) matter: **time to first token (TTFT)**, measured from arrival, and **time between tokens (TBT)** during generation. A cache hit can save computation while still missing TTFT because of transfer or queueing. Similarly, completing prefill is wasted work if the decoding pool subsequently rejects the request.[^workflow]

## Architecture and request path

Mooncake pools CPU, DRAM, SSD and network resources around the GPU cluster. **Conductor** is the global scheduler; **Messenger** moves cache blocks using remote direct memory access (RDMA). CPU memory holds paged KV blocks, with prefix-dependent hashes identifying reusable state. Hashing includes preceding blocks: an identical text fragment after a different prefix is not sufficient for a hit.[^workflow]

The conceptual request path is:

1. **Match a prefix and choose instances.** Compare cache availability, estimated prefill queues and transfer costs while selecting prefill and decoding resources.
2. **Load reusable state.** Fetch matching prefix blocks into the prefill instance. Skip this operation on a miss.
3. **Compute the uncached suffix.** A partial hit still needs incremental prefill. Newly computed state is stored for reuse.
4. **Stream state toward decoding.** Layer-wise loading and storing allow transfer to overlap computation; the path is not simply a sequence of fully blocking copies.
5. **Recheck decoding capacity and generate.** The local decoding scheduler checks its latency constraint again before admitting the request to continuous batching. Global placement does not reserve an infallible future slot.[^workflow]

### A partial hit is not a completed prompt

Consider an illustrative prompt of 4,096 tokens with a reusable prefix of 3,072 tokens:

| Quantity | Value |
|---|---|
| Total prompt length $N$ | 4,096 tokens |
| Reusable prefix length $H$ | 3,072 tokens |
| Uncached suffix $N-H$ | 1,024 tokens |
| Token coverage $H/N$ | 75% |

This is original arithmetic, not a paper benchmark. The suffix still attends to the preceding context. Thus 75% token coverage does not imply 75% less latency: queueing, data movement and suffix attention remain.

For intuition, compare two candidate placements with a simplified, non-overlapped cost:

$$
\widehat T_i = Q_i + X_i + F(N,H_i),
$$

where $Q_i$ is estimated queueing, $X_i$ is cache-loading time and $F$ is remaining prefill time at prefix coverage $H_i$. A node with a longer hit can lose to one with a shorter queue or faster transfer. This expression illustrates the scheduling tradeoff; it is not a latency guarantee or a model of Mooncake's layer-wise overlap. The paper's cache-aware scheduler combines estimated prefill, transfer and queueing costs, and also considers hot-block replication for load balancing.[^scheduling]

## Overload and early rejection

**Admission** decides whether to accept a request; it is separate from finding its cache blocks. Waiting until decoding to reject an unserviceable request wastes its prefill computation. Checking only the decoding pool's *current* load before prefill also causes trouble: a wave of accepted prefills can arrive after that check, alternately overloading and starving the two pools.

Mooncake instead predicts decoding load at the time those prefills will finish. The described implementation uses a **system-level estimate with a uniform decoding duration**, accounting for expected arrivals from prefill and departures from decoding. It does not claim to accurately predict every request's output length; request-level prediction is left for future work.[^overload]

To assess such a policy, report offered load, rejected requests, completed requests and latency attainment together. For example, in an illustrative cohort followed until completion, suppose 1,000 requests arrive, 700 are admitted and 650 finish within both latency targets. Then:

$$
\text{admission fraction}=700/1000=70\%,\qquad
\text{SLO completion fraction}=650/1000=65\%.
$$

The admitted-only success fraction is $650/700\approx92.9\%$. It answers a different question from success among all arrivals. For a rate, also state the measurement interval and treatment of unfinished requests. These example fractions are not Mooncake results; they explain why a high success percentage among accepted requests alone cannot establish greater serving capacity.

## Results and how to read them

The paper compares Mooncake with its experimental vLLM baseline. Its end-to-end evaluation uses a dummy model with the LLaMA2-70B architecture on nodes with eight A800 80-GB GPUs and high-bandwidth RDMA networking.[^evaluation]

| Reported comparison | Scope and interpretation |
|---|---|
| Up to 525% throughput increase | Certain simulated long-context cases under TTFT/TBT constraints; an increase of 525% means $1+5.25=6.25$ times the baseline. |
| Approximately 75% more SLO-compliant requests | Real request-trace replay using 10 prefill plus 10 decoding instances versus 20 vLLM instances; the comparison uses 30-second TTFT and 0.1-second TBT limits. |

The abstract describes the latter as allowing Kimi to handle more requests. Section 8.1.3 supplies the replay experiment: it should not be read as an independently measured, universal live-production speedup. Neither number isolates prefix reuse from phase separation, scheduling and the particular baseline. A separate overload experiment in section 8.2 compares admission strategies; it is not the experiment yielding the 525% headline.[^evaluation]

## Limitations and practical checks

- **Reuse is workload-dependent.** Measure prefix coverage, eviction and cold-start behaviour. Little sharing reduces the reuse opportunity, but does not remove every possible benefit of disaggregation.
- **Movement can dominate.** Profile cache-transfer bandwidth and contention alongside prefill time. More stored prefixes do not guarantee a lower TTFT.
- **Prediction can be wrong.** Changing output-length distributions can invalidate a uniform-duration estimate. Inspect late rejections and wasted prefill, not just pool utilisation.
- **Cache identity and isolation need care.** In deployment, scope reuse to compatible model state and execution settings, and enforce tenant permissions. Matching prefix hashes alone is not an access-control policy.

These are evaluation and deployment checks, rather than claims that the paper proves all such conditions safe.

## Connections

[Splitwise](splitwise.md) studies phase separation and hardware provisioning; [DistServe](distserve.md) optimises allocation, parallelism and placement for latency-constrained goodput.[^splitwise][^distserve] Mooncake adds distributed prefix-state management and overload admission to this design space.

[PagedAttention and vLLM](paged-attention.md) address KV-memory allocation and sharing; paging alone does not specify a distributed cache placement policy.[^paged] Orca's iteration-level scheduling explains how a batch can change between generation iterations, a separate concern from deciding whether to admit an entire request.[^orca]

[^mooncake]: Qin et al. (2024, revised 2026), *Mooncake*, abstract and sections 1–3; version 5 is linked below.
[^workflow]: Qin et al., *Mooncake*, sections 2–3 and 5.2: latency metrics, prefix-dependent block hashes, incremental prefill, layer-wise transfers and the decoding admission recheck.
[^scheduling]: Qin et al., *Mooncake*, section 6: cache-aware placement and hot-spot balancing.
[^overload]: Qin et al., *Mooncake*, sections 7.2–7.4: delayed load feedback and system-level prediction.
[^evaluation]: Qin et al., *Mooncake*, sections 8.1–8.2: testbed, simulated workloads, real-trace replay and separate admission-policy experiments.
[^splitwise]: Patel et al. (2023), *Splitwise*, abstract; linked below.
[^distserve]: Zhong et al. (2024), *DistServe*, abstract; linked below.
[^paged]: Kwon et al. (2023), *PagedAttention*, abstract; linked below.
[^orca]: Yu et al. (2022), *Orca*, abstract; linked below.

## References

### Seminal papers

- Qin, R. et al. (2024; revised 2026). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. arXiv:2407.00079v5. https://arxiv.org/html/2407.00079v5 — Primary architecture paper detailing distributed prefix reuse, scheduling, overload prediction and evaluation conditions.
- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. arXiv:2401.09670. https://arxiv.org/abs/2401.09670 — Explains phase-specific resource allocation and placement under latency constraints.
- Patel, P. et al. (2023). *Splitwise: Efficient generative LLM inference using phase splitting*. arXiv:2311.18677. https://arxiv.org/abs/2311.18677 — Studies separate prompt and generation machines with hardware provisioning tradeoffs.
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. https://arxiv.org/abs/2309.06180 — Explains paged KV allocation and sharing within and across requests.
- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — Introduces iteration-level scheduling and selective batching for autoregressive generation.
