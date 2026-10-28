---
status: draft
last_reviewed: 2026-10-28
related:
- applications/software
- theory/paradigms/supervised
tags:
- engineering
- tools
- retrieval
aliases:
- Gorilla
- API 呼叫微調
- 檢索感知微調
- Patil et al. 2023
---

# Gorilla: Large Language Model Connected with Massive APIs

Gorilla (Patil et al., 2023) is a LLaMA-based model of 7 billion parameters, finetuned to write calls to machine learning APIs and trained to read API documentation that a retriever places in its prompt. It is one of three method pages on the [Tool Calling and the Model Context Protocol](../index.md) page.

## Overview

Asked to call an API, a language model often writes a call that looks plausible but uses the wrong arguments, or names an API that does not exist. The paper calls the second case hallucination. Documentation also changes over time, so anything learned from a fixed snapshot goes stale. Gorilla addresses both problems with one design choice: the model is trained to use documentation supplied at inference, so that its answers follow the documentation rather than memory.

The authors focus on machine learning model hubs, where many APIs do similar things and the differences matter.

## Key concepts

- **APIBench**: the authors' dataset of API calls from three model hubs, TorchHub, HuggingFace and TensorFlow Hub. Each entry is a model card converted to a structured record with fields such as domain, framework, API name, call and arguments. The paper reports 1,645 such calls.
- **Self-instruct generation**: GPT-4 writes user requests that need a given API, from a few example pairs and the API's documentation, without naming the API. The only hand-written data were six example pairs per hub.
- **Retriever-aware training**: during training, the prompt includes retrieved documentation, so the model learns to read it and to answer from it.
- **AST sub-tree matching**: the generated call is parsed into an abstract syntax tree and checked to be a sub-tree of the reference call. The check identifies which API was used.
- **Hallucination**: in the paper's definition, a call that is not a sub-tree of any API in the database, which is to say an API that does not exist.

## How it works

1. **Collect documentation.** Convert each model card into a structured API record.
2. **Generate instructions.** Ask GPT-4 for user requests that need each API, and generate ten instruction and API pairs per API.
3. **Finetune.** Train a LLaMA-7B base model on these pairs as user and agent conversations, using standard instruction finetuning. The retriever-aware version appends "Use this API documentation for reference" and the retrieved record to the user prompt during training.
4. **Retrieve and answer.** At inference, a retriever (BM25, a GPT-based index, or an oracle that always returns the right document) supplies the current documentation, and the model writes the call.
5. **Score.** Check each output with AST matching, and count three outcomes: correct, hallucinated, or a real API chosen wrongly.

## Results

The main comparison in the paper is on APIBench for TorchHub, without a retriever (zero-shot). Gorilla reaches an overall accuracy of 59.13 percent with a hallucination rate of 6.98 percent. GPT-4 reaches 38.70 percent with a hallucination rate of 36.55 percent (Table 1).[^1] The abstract states that the finetuned model surpasses GPT-4 at writing API calls.

Two further findings matter. The authors observe that GPT-3.5 hallucinated less than GPT-4 across their settings, which they suggest reflects the role of reinforcement learning from human feedback in making models truthful. They also find that adding a retriever at test time does not always help. A poorly matched retriever can mislead the model and increase errors. Finally, because the model was trained to read documentation, it adapts when a model's documentation changes, which the paper illustrates with a changed model registry.

## Limitations

- **Narrow domain.** The authors chose ML hubs for their functional similarity, which makes the task hard, but these APIs are not a sample of APIs in general. The paper also notes that ML APIs can produce biased predictions when trained on skewed data.
- **One call at a time.** The paper considers only one API call per output.
- **What the metric measures.** AST matching checks that a call matches a reference API. It does not check that the call runs or that its result answers the user.
- **Retriever dependence.** The gains depend on the retriever, and a mismatched retriever can reduce accuracy, as the paper reports.

## Open questions

- Does retriever-aware training carry over to general REST APIs, where documentation is less uniform? [ToolLLM](../toolllm/index.md) addresses this with a much larger set of APIs.
- How should a model combine several retrieved documents when a task needs more than one API?
- Can training adapt to documentation it has never seen, or does it need the retriever to supply the change?

## References

### Seminal papers

- Patil, S. G. et al. (2023). *Gorilla: Large Language Model Connected with Massive APIs*. arXiv. https://arxiv.org/abs/2305.15334 — The paper described here, introducing APIBench, retriever-aware finetuning and AST-based evaluation.
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. arXiv. https://arxiv.org/abs/2005.11401 — Introduces combining a retriever with a generator, the general pattern that Gorilla applies to API documentation.
- Wang, Y. et al. (2022). *Self-Instruct: Aligning Language Models with Self-Generated Instructions*. arXiv. https://arxiv.org/abs/2212.10560 — Describes generating instruction data from a model's own outputs, the method the authors adapt to create API requests.
- Touvron, H. et al. (2023). *LLaMA: Open and Efficient Foundation Language Models*. arXiv. https://arxiv.org/abs/2302.13971 — Introduces the open base models that Gorilla finetunes.
- Schick, T. et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv. https://arxiv.org/abs/2302.04761 — Alternative approach that trains a model on its own annotated tool calls rather than generated instructions.

[^1]: Patil et al. (2023), Table 1 of the Gorilla paper, https://arxiv.org/abs/2305.15334 — Source of the TorchHub zero-shot accuracy and hallucination figures for Gorilla and GPT-4.
