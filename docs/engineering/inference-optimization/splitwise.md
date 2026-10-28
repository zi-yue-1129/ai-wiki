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
  - Splitwise
  - Phase splitting
---

# Splitwise

!!! info "Part of Disaggregated Prefill and Decode"
    This method page belongs to [Disaggregated Prefill and Decode](disaggregated-serving.md). It explains Splitwise in detail; the parent page compares it with the other systems.

Splitwise is a cluster-level design that splits the two phases of an LLM request, prompt computation and token generation, onto separate machines. The authors' argument is that the phases need different hardware, so a cluster that provisions one machine type for both wastes resources. Splitwise provisions each phase separately and moves the state between machines over fast links. The paper reports higher throughput at lower cost, or more throughput at the same cost and power budget.

## Problem

The prompt phase processes many tokens in parallel and is compute-heavy. The token phase generates one token per step and is limited by memory. A machine that suits one phase is often a poor fit for the other, and a cluster built from a single machine type must over-provision for the phase it does not need. The problem is to match each phase to suitable hardware without the cost of dedicating a machine to each request.

## Core idea

Splitwise runs the prompt phase of a request on one machine and the token phase on another, so each can use the hardware that suits it. The cluster is provisioned per phase, so the number of prompt machines and token machines can be set to match the workload. The state needed by the token phase, mainly the KV cache, is transferred between the machines over the interconnect, and the transfer is designed to overlap with the work on each side.

## Procedure

1. Receive a request and route its prompt to a machine in the prompt pool.
2. Compute the prompt's KV cache on that machine.
3. Transfer the cache to a machine in the token pool over the cluster's fast interconnect.
4. Generate tokens on the token machine, one step at a time, with batching inside the pool.
5. Size the two pools for the workload, and adjust the split as the load changes.

## Results

The paper reports that the design achieves 1.4 times higher throughput at 20 percent lower cost than the current designs it compares against. It also reports that, at the same cost and power budget, the design can achieve 2.35 times more throughput. These are cluster-level results on the workloads and hardware in the paper, and the baselines are the designs of the time, so the figures should be read with that setup.

## Limitations

- **Transfer over the interconnect.** The benefit depends on a fast link between the machines. Without one, the cost of moving the cache can cancel the gain.
- **Hardware assumptions.** The design assumes that different hardware suits each phase, which depends on the accelerators available.
- **Provisioning.** The split between the pools must match the workload's mix of prompt and output lengths, and the mix changes over time.
- **Operational complexity.** Routing, failure handling and cache state now span several machines.

## Connections

- The approach that separates phases by GPU rather than by machine, with a placement search, is [DistServe](distserve.md).
- The cache-centred architecture that separates clusters under overload is [Mooncake](mooncake.md).
- The iteration-level batching inside each pool follows [Orca](orca.md).

## Open questions

- Can the pools be resized automatically in response to changes in the prompt and output mix?
- Does the phase-specific hardware advantage hold when accelerators are designed to serve both phases well?

## References

### Seminal papers

- Patel, P. et al. (2023). *Splitwise: Efficient generative LLM inference using phase splitting*. arXiv:2311.18677. https://arxiv.org/abs/2311.18677 — The primary paper: phase splitting onto separate machines, provisioned per phase, with throughput and cost results.
- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. arXiv:2401.09670. https://arxiv.org/abs/2401.09670 — A GPU-level separation with a placement search, for comparison.
- Qin, R. et al. (2024). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. arXiv:2407.00079. https://arxiv.org/abs/2407.00079 — A cache-centred disaggregated architecture, for comparison under overload.
- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — The iteration-level scheduling used inside each pool.
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — The paged cache layout that moved state is stored in.
