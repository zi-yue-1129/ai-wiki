---
status: draft
last_reviewed: 2026-10-28
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
    This method page belongs to [Disaggregated Prefill and Decode](disaggregated-serving.md). It explains Mooncake in detail; the parent page compares it with the other systems.

Mooncake is a serving architecture built around the KV cache. It separates the prefill and decoding clusters, and it treats the cache of prompts as a shared resource that can be stored, moved and reused across requests. The paper describes it as designed for highly overloaded scenarios, and it reports throughput gains in simulated cases and a higher number of requests handled in a production deployment.

## Problem

Serving at scale faces two pressures at once. Requests with long prompts need large amounts of compute in prefill, and many requests share prefixes, so their KV caches are repeated work. When the system is overloaded, a scheduler that treats each request in isolation cannot reuse this work, and it cannot keep latency low for the requests that arrive during a peak. The problem is to serve more requests under overload by making the cache a first-class resource.

## Core idea

Mooncake separates the prefill and decoding clusters and organises the system around the KV cache. Caches of prompts are kept in a distributed store, so that a request that shares a prefix with an earlier one can reuse the stored cache instead of recomputing it. The scheduler places prefill and decoding work with the cache in mind, and it can move cache blocks between machines when that is cheaper than recomputation.

## Procedure

1. Receive a request and check the distributed cache store for a stored prefix that matches its prompt.
2. If a match exists, load the cached blocks; otherwise run prefill on a prefill node.
3. Store the new cache blocks, so that later requests can reuse them.
4. Send the cache to a decoding node and generate tokens there.
5. Under overload, let the scheduler reject, delay or re-route requests to keep the rest within their objectives.

## Results

The paper reports that Mooncake can achieve up to a 525 percent increase in throughput in certain simulated scenarios. It also reports that under real workloads, the architecture enables the deployed service to handle 75 percent more requests. The simulated and deployed results come from different setups, and the gain in the deployed case depends on how much prefix sharing the workload contains.

## Limitations

- **Dependence on prefix sharing.** The reuse of cached prefixes gives much of the gain. A workload with little sharing benefits far less.
- **Store capacity and placement.** The distributed cache store has its own memory limits, and the placement policy decides which blocks survive.
- **Simulated results.** The largest throughput figure comes from simulation, so it is an estimate for the modelled scenarios.
- **Engineering scope.** The architecture spans storage, scheduling and transfer, and it is a large system to build and operate.

## Connections

- The GPU-level separation with a placement search, which is an alternative design, is [DistServe](distserve.md).
- The phase split across machines, which Mooncake also uses, is described in [Splitwise](splitwise.md).
- The paged memory layout that makes block-level reuse practical is [PagedAttention and vLLM](paged-attention.md).

## Open questions

- How should the cache store be sized and placed when prefix sharing varies across users and time?
- Can the reuse policy be made safe for prompts that contain private data, which must not leak through a shared cache?

## References

### Seminal papers

- Qin, R. et al. (2024). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. arXiv:2407.00079. https://arxiv.org/abs/2407.00079 — The primary paper: a cache-centred architecture that separates prefill and decoding clusters, with simulated and deployed results.
- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. arXiv:2401.09670. https://arxiv.org/abs/2401.09670 — A GPU-level separation with goodput-based placement, for comparison.
- Patel, P. et al. (2023). *Splitwise: Efficient generative LLM inference using phase splitting*. arXiv:2311.18677. https://arxiv.org/abs/2311.18677 — A machine-level phase split, for comparison.
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — The paged cache layout that makes block-level reuse practical.
- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — The iteration-level scheduling that serving systems of this kind build on.
