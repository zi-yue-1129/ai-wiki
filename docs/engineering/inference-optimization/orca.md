---
tags:
- engineering
- systems
---

# Orca: Iteration-Level Scheduling

Orca is a serving system that schedules generation one model iteration at a time. Finished requests leave the batch and waiting requests join between iterations, which removes the idle time that request-level batching wastes on short requests. The idea, known as continuous batching, is now standard in LLM serving engines.

## Overview

Generation is sequential: each request produces one token per iteration until it finishes. Request-level batching groups requests, then waits until the whole batch is done, so a short request sits idle while a long request in the same batch keeps going. Orca moves the scheduling decision to the iteration level, so the GPU always runs on whichever requests are still active.

## Key concepts

- **Iteration**: one forward pass of the model that produces one new token for every active request.
- **Iteration-level scheduling**: deciding the batch again before each iteration, rather than before each request.
- **Selective batching**: batching the parts of the computation that can be shared across requests, while handling attention for each request separately, because sequences have different lengths.

## How it works

Before each iteration, the scheduler removes finished requests, adds waiting requests whose prompts fit in memory, and runs one iteration on the resulting batch. Linear layers run as one batched matrix multiplication. Attention runs per request, because each request has its own cached keys and values.

```mermaid
flowchart LR
  Q[Waiting queue] --> S[Scheduler: remove finished, add new]
  S --> B[Batch of active requests]
  B --> I[One model iteration]
  I --> O[One new token per request]
  O --> S
```

## Key methods

Orca's method is the iteration-level scheduler and selective batching, described above. The paper's evidence compares throughput against request-level batching for GPT-style generation at comparable latency.

## Results

The paper reports large throughput gains over request-level batching for generative models, with comparable latency. Exact figures depend on the model size and workload, so readers should check the paper's evaluation section.

## Limitations

- **Memory fragmentation**: requests of different lengths still need contiguous memory in this design, which the later paged KV cache work addresses.
- **Scheduling policy**: the choice of which waiting request to admit affects fairness and latency, and the paper's policy is a simple one.
- **Workload dependence**: gains are largest when requests have very different output lengths.

## Open questions

- How should a scheduler balance long prompts, which occupy many iterations of prefill, against short requests waiting for a slot?
- Chunked prefill mixes prompt processing with decoding steps, but its effect on latency targets depends on the service objective.

## References

### Seminal papers

- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — Introduces iteration-level scheduling and selective batching for generative model serving.

### Related work

- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. https://arxiv.org/abs/2309.06180 — Adds paged KV-cache memory management on top of iteration-level scheduling in vLLM.
- Pope, R. et al. (2023). *Efficiently Scaling Transformer Inference*. MLSys 2023. https://arxiv.org/abs/2211.05102 — Analyses how inference workloads and partitioning interact with batch size and latency.
- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM. https://escholarship.org/content/qt78h8v7mr/qt78h8v7mr.pdf — Gives the performance model that explains why small batches leave the GPU underused.
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. NeurIPS 2022. https://arxiv.org/abs/2205.14135 — Speeds up the attention kernel that runs per request in each iteration.
