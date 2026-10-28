---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/agents
tags:
  - agents
  - tool use
  - self-supervised learning
aliases:
  - Toolformer
  - 自學工具使用
  - 工具增強語言模型
---

# Toolformer (Schick et al., 2023)

Toolformer is a method for training a language model to call external tools by itself. The model learns from its own text, with calls to APIs inserted where they help predict the following words, so that it decides which API to call, when, with which arguments and how to use the result. Schick et al. (2023) introduced it with a calculator, a question-answering system, two search engines, a translation system and a calendar.

This page is part of [Agent Engineering](index.md) and is one of the named methods behind [Tool calling and the Model Context Protocol](tool-calling-and-mcp.md).

## Overview

Language models are strong at language but weak at some basic functions, such as arithmetic or looking up a fact, where small, specialised tools do better. A common fix is to prompt the model with examples of tool use. Toolformer instead teaches the model to use tools during training, so that tool use is part of the model's own decisions rather than a fixed prompt pattern.

## Problem

Training a model to use tools by hand requires large annotated datasets of tool use, which are costly to build for every API. The question is whether a model can generate its own training data for tool use from a few demonstrations per API, without losing its general language ability.

## Core idea

The method has three steps. First, the model samples candidate positions in a text where an API call might help and proposes a call there. Second, it executes the calls and keeps only those whose results make the following tokens easier to predict, which is the paper's measure of usefulness. Third, it fine-tunes on the text with the kept calls inserted. The result is a model that produces calls and their arguments in the same stream of text that it generates, and that uses the returned results to continue.

## Equation or algorithm

For each API, with a handful of demonstrations:

1. Sample candidate API calls at positions in a text, using the model.
2. Execute each call and insert its result after the call.
3. Keep a call only if inserting it, with its result, lowers the loss on the tokens that follow by at least a threshold: 1.0 by default, and 0.5 for the calculator and translation tools. The comparison is with the lower of two baselines, a text with no call and a text with the call but without its result.
4. Fine-tune the model on the filtered text, which keeps the language modelling objective.

At inference time the model writes a call token sequence when it decides a tool is needed, and the surrounding program executes it.

## Results

The paper fine-tunes GPT-J, a model with 6.7 billion parameters. The abstract reports that Toolformer achieves substantially improved zero-shot performance across a variety of downstream tasks, often competitive with much larger models, without sacrificing its core language modelling abilities. The tools cover arithmetic, factual lookup, search, translation and dates.

## Limitations

- **Fixed tool set at training time.** New tools need new training data and a new fine-tuning run.
- **Filter design.** The usefulness criterion depends on the loss, so calls that help in ways the loss does not measure can be discarded.
- **Tool errors.** A wrong result from a tool is inserted with the same authority as a right one.
- **Model-level training.** The approach changes weights, which limits its use with closed models unless the provider supports it.

## Connections

- Prompt-based tool use, the alternative that ReAct takes, is on [ReAct](react.md).
- Tool protocols that standardise how tools are offered to a model are on [Tool calling and the Model Context Protocol](tool-calling-and-mcp.md).
- The model family that Toolformer fine-tunes is covered in [Transformer](../../theory/models/transformer/index.md).
- Retrieval, one of the tools in the paper, is described on [Retrieval-Augmented Generation](../rag/index.md).

## Applications

- Models that call calculators or search engines during an answer.
- Assistants that check dates, units or translations through dedicated services.

## Open questions

- How many tools can one model learn to use before it confuses them?
- Can tool use be learned from feedback on final answers rather than from loss reduction?

## References

### Seminal papers

- Schick, T. et al. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. NeurIPS. https://doi.org/10.52202/075280-2997 — Introduces Toolformer, which learns to call APIs in a self-supervised way from a few demonstrations per tool.
- Yao, S. et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR. https://arxiv.org/abs/2210.03629 — The prompt-based alternative, in which tool use is interleaved with reasoning.
- Parisi, A., Zhao, Y. & Fiedel, N. (2022). TALM: Tool Augmented Language Models. arXiv. https://arxiv.org/abs/2205.12255 — An earlier approach that augments language models with tool calls.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering tool use among their components.

### Articles and documentation

- Model Context Protocol. *Specification, revision 2025-06-18*. https://modelcontextprotocol.io/specification/2025-06-18 — The later standard for connecting models to tools, which takes a different route from training tool use into the model.
