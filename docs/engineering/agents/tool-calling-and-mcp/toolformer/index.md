---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/self-supervised
- theory/models/llm
tags:
- engineering
- agents
- tools
aliases:
- Toolformer
- 語言模型自學使用工具
- 自監督工具使用
- Schick et al. 2023
---

# Toolformer: Language Models Can Teach Themselves to Use Tools

Toolformer (Schick et al., 2023) trains a language model to decide which tool to call, when, with which arguments, and how to use the result. It needs only a few demonstrations per tool, because the model annotates a text corpus with its own candidate calls. It is one of three method pages on the [Tool Calling and the Model Context Protocol](../index.md) page.

## Overview

Language models write fluent text but are unreliable at tasks that a simple program does exactly, such as arithmetic, or at facts that changed after training. One remedy is a fixed procedure that hands such questions to a tool. Toolformer asks whether the model can learn the procedure itself. The aim was to avoid large corpora of human-labelled tool use. The authors start from a plain text collection, let the model propose API calls inside it, and keep only those calls that help the model predict the text that follows.

The tools are a calculator, a question-answering system, two search engines, a translation system and a calendar (Schick et al., 2023).

## Key concepts

- **Inline API call**: a tool call written as text inside the training sequence, with the tool name, its arguments and, after the call, the result. Because calls are text, the same model that writes language can write them.
- **Self-supervision**: the model is prompted with a handful of examples per tool to annotate text, so the labels come from the model rather than from people.
- **Usefulness filter**: a candidate call is kept only if including it, with its result, lowers the model's loss on the tokens that follow.

## How it works

For a model $M$ and a text $x_1, \dots, x_n$, the paper defines the weighted loss from position $i$ onward, given a prefix $z$, as

$$
L_i(z) = -\sum_{j=i}^{n} w_{j-i} \log p_M(x_j \mid z, x_{1:j-1}).
$$

A call $c_i$ with result $r_i$ at position $i$ is compared in two ways: $L_i^+ = L_i(e(c_i, r_i))$, the loss when the call and its result are placed before the text, and $L_i^- = \min\big(L_i(\varepsilon), L_i(e(c_i, \varepsilon))\big)$, the better of no call at all and a call without its result. The call is kept when $L_i^- - L_i^+ \ge \tau_f$. Here $e(\cdot)$ formats a call and $\varepsilon$ is the empty sequence.

The procedure runs in four steps:

1. **Sampling.** For each text, compute the probability $p_i$ that the model starts a call at position $i$ after a few-shot prompt. Keep the positions with $p_i > \tau_s$, at most $k$ of them, and at each sample up to $m$ candidate calls that end at a closing token.
2. **Execution.** Run each candidate call and record its result $r_i$.
3. **Filtering.** Keep only the calls that pass the usefulness test above.
4. **Finetuning.** Interleave the surviving calls and results with the original text, and finetune the model on the augmented corpus with the ordinary language-modelling loss. The base model is GPT-J with 6.7 billion parameters.

At inference, when the model writes the opening token of a call, the surrounding software runs the tool, inserts the result and lets the model continue.

## Results

The paper evaluates zero-shot, with no examples in the prompt, and uses lenient matching rules suited to a model that writes free text.

- **Arithmetic.** On ASDiv, SVAMP and MAWPS, Toolformer scores 40.4, 29.4 and 44.0. GPT-3 (175B) scores 14.0, 10.0 and 19.8 (Table 4). The model calls the calculator in 97.9 percent of examples. With tools disabled, Toolformer scores 14.8, 6.3 and 15.0, still above its GPT-J baseline, which the authors attribute to finetuning on examples of calls.
- **Factual completion.** On three LAMA subsets, Toolformer improves on the best baseline of the same size by 11.7, 5.2 and 18.6 points, and is competitive with GPT-3 (175B). It uses the question-answering tool in 98.1 percent of examples (Table 3).
- **Question answering.** On Web Questions Toolformer scores 26.3, against 29.0 for GPT-3 (175B). It beats the same-size baselines but does not reach the larger model (Table 5).[^1]

## Limitations

- **No chained calls.** Calls are generated for each tool independently, so the training data contains no example in which one tool's output feeds another. The authors name this as a clear limitation.
- **No interactive use.** The model cannot browse a list of search results or refine its query.
- **Sensitivity to wording.** Whether a call is made depends on the exact wording of the input.
- **Sample inefficiency.** The authors report that more than a million documents yielded only a few thousand useful calculator examples.
- **Limit of one call.** Evaluation allows at most one call per input, to avoid loops in which the model calls tools without producing output.

## Open questions

- Can the sample-and-filter loop be repeated to learn chains of tools and interactive use? The authors suggest iterating it by analogy with bootstrapping methods.
- How should a model weigh the benefit of a call against its cost?
- The paper tests five kinds of tool on a 6.7-billion-parameter base model. How the approach behaves with many more tools and much larger models is not tested.

## References

### Seminal papers

- Schick, T. et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv. https://arxiv.org/abs/2302.04761 — The paper described here, introducing self-supervised tool use with a usefulness filter.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Introduces GPT-3 and few-shot prompting, the baseline model against which Toolformer's arithmetic and question-answering results are compared.
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — Prompting alternative in which a model interleaves reasoning with actions, instead of learning when to call a tool.
- Patil, S. G. et al. (2023). *Gorilla: Large Language Model Connected with Massive APIs*. arXiv. https://arxiv.org/abs/2305.15334 — Later finetuning approach for API calls that adds retrieved documentation to the prompt.

### Surveys and textbooks

- Qu, C. et al. (2024). *Tool Learning with Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2405.17935 — Survey of tool learning organised by planning, tool selection, tool calling and response generation.

[^1]: Schick et al. (2023), Table 5 of the Toolformer paper, https://arxiv.org/abs/2302.04761 — Source of the Web Questions scores for Toolformer and GPT-3 (175B).
