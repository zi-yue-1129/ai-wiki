---
related:
- theory/models/llm
- engineering/rag
- theory/models/agents
- applications/cybersecurity
---

# Prompt Engineering

Prompting is how you specify a task to a foundation model. As models improved, the craft shifted from "magic phrases" toward **clear communication** and **context engineering** — supplying the right information, tools and examples.

## Core principles

1. **Be explicit about the goal, audience and format.** Say what success looks like.
2. **Give context**: why the task matters, constraints, background documents.
3. **Show examples** (few-shot) when format or style matters; vary them to avoid over-copying.
4. **Structure the prompt**: separate instructions, context and input (headings or XML-style tags).
5. **Ask for reasoning when the task needs it**, or use a reasoning model.
6. **Specify output structure** (JSON schema, sections) and use structured-output features when available.
7. **Iterate with an evaluation set**, not by eyeballing one example.

## Techniques

| Technique | Description | When |
|---|---|---|
| Zero-shot instruction | Just describe the task | Strong models, simple tasks |
| Few-shot | Include input–output examples | Format/style control, classification |
| Role / system prompt | Set persona, rules and context | Assistants and products |
| Chain-of-thought | "Think step by step" or show worked reasoning | Math, logic, multi-step problems with non-reasoning models |
| Self-consistency | Sample several reasoning paths, vote | Higher accuracy at higher cost |
| Decomposition / prompt chaining | Split into subtasks with separate calls | Complex workflows |
| ReAct / tool use | Interleave reasoning with tool calls | Agents |
| Retrieval augmentation | Insert relevant documents | Knowledge-heavy tasks ([RAG](../rag/index.md)) |
| Self-critique / reflection | Ask the model to review and revise | Writing, code |
| Prompt optimisation | Automatically search prompts (DSPy, APE) | Many examples and a metric available |

## Context engineering for agents

- Keep system prompts focused; put stable material first to benefit from **prompt caching**
- Provide tools with clear names, descriptions and examples
- Manage long contexts: summarise, retrieve on demand, put the most important information at the start or end ("lost in the middle")
- Persist notes and plans in files for long tasks

## Security: prompt injection

Any untrusted text in the context (web pages, emails, documents, tool outputs) can carry instructions. Treat it as data: separate it clearly, limit the agent's privileges, and require confirmation for consequential actions. See [Cybersecurity](../../applications/cybersecurity/index.md).

## Common mistakes

- Vague requests ("make it better")
- Contradictory instructions
- Examples that don't match the real input distribution
- Asking for things the model cannot know (private or very recent facts) without supplying them
- Over-long prompts full of irrelevant rules

## References

- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Introduces prompts whose worked examples include intermediate reasoning steps, the technique in the Techniques section.
- Wang, X. et al. (2023). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. ICLR 2023. https://arxiv.org/abs/2203.11171 — Samples several reasoning paths and takes a majority vote over the final answers, a common test-time method.
- Yao, S. et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. https://arxiv.org/abs/2210.03629 — Interleaves reasoning traces with tool actions, the basis of many agent prompting patterns on this page.
- Brown, T. et al. (2020). *Language Models are Few-Shot Learners*. NeurIPS 2020. https://arxiv.org/abs/2005.14165 — Shows that large language models can perform new tasks from a few examples placed in the prompt.
- Schulhoff, S. et al. (2024). *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques*. arXiv. https://arxiv.org/abs/2406.06608 — Broad taxonomy of prompting techniques with shared terminology, useful for checking the list of methods here.
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. arXiv. https://arxiv.org/abs/2302.12173 — Shows that instructions hidden in retrieved content can hijack an application, the threat model in the security section.

## Further learning

- [Prompt Engineering Guide](https://www.promptingguide.ai/) (DAIR.AI; MIT) — community guide with a worked example for each technique above.
