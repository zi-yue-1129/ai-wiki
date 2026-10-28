---
related:
  - theory/models/agents
  - engineering/rag
  - society/safety-alignment
aliases:
  - 客服
  - 客戶服務
  - 對話系統
---

# Customer Service and Conversational Systems

Customer service was one of the first business uses of conversational AI and one of the largest in volume. The field moved from phone menus and intent classifiers to language-model agents that answer, act on accounts and hand over to people. Evidence on whether these systems help customers, and on how they change agent jobs, is still thin and mixed.

## Landscape

| Stage | Methods | Notes |
|---|---|---|
| Interactive voice menus | Touch-tone and keyword menus | Still common; cheap but frustrating for complex needs |
| Intent classification and slot filling | Classifiers over a fixed set of intents, with frame-based dialogue | Frameworks such as Rasa (Bocklisch et al., 2017) |
| Retrieval-based answers | Search over a knowledge base, with ranked answer suggestions for agents | Quality depends on the knowledge base |
| Generative assistants | Fine-tuned language models that draft or send replies | Requires guardrails against invented policies |
| Tool-using agents | Language models that call account, booking and refund tools, following a policy | ReAct (Yao et al., 2022); Toolformer (Schick et al., 2023) |
| Agent assist | Real-time suggestions, summaries and after-call notes for human agents | Often the first deployment, with a person kept in the loop |

## How a deployed system is structured

Most production systems combine a language model with deterministic checks. The model interprets the message and drafts a response. A policy layer decides what the model may do, such as refund limits, identity verification and escalation rules. Logs feed evaluation sets, and conversations that fail are routed to a person.

## Why it is hard

- **Policy compliance**: an agent that is helpful but ignores refund rules or disclosure obligations creates real liability.
- **Tool reliability**: a conversation that looks fluent can still have failed to change the account.
- **Measurement**: deflection rates and handle times are easy to measure, while customer satisfaction and resolution quality are harder.
- **Escalation**: knowing when to hand over, and handing over with context, is a design problem as much as a model problem.

## Key methods

- [LLM-based agents](../../theory/models/agents/index.md): a language model that plans, calls tools and observes results in a loop.
- [Retrieval-Augmented Generation](../../engineering/rag/index.md): grounds answers in policy documents and product manuals.
- [Instruction tuning and RLHF](../../theory/models/llm/instructgpt-rlhf/index.md): the training recipe that makes assistants follow instructions and stay on task.
- [Evaluation & benchmarks](../../engineering/evaluation/index.md): task-based tests of agents, such as τ-bench (Yao et al., 2024), which simulate customers following a policy.

## Connections

- Language interfaces for experts and the general case for LLM assistants are discussed in [Large Language Models](../../theory/models/llm/index.md).
- Financial advice and customer service in banks overlap; see [Finance](../finance/index.md).
- How people judge a conversational partner's helpfulness and trustworthiness is a [Psychology & AI](../../brain-mind/psychology/index.md) question, including how people respond to a machine that sounds human.

## Applications

- Account, billing and order-status support
- Agent assist for human contact centres
- Post-call summaries and quality review
- Proactive outreach for returns, renewals and reminders

## Risks and limits

- **Invented policy**: a model may promise a refund or a service that does not exist.
- **Unequal service**: automated front doors can make it harder to reach a person, which disadvantages customers who need one most.
- **Labour effects**: research on generative assistants in a large customer support team found productivity gains concentrated among less experienced agents (Brynjolfsson et al., 2023), but workforce outcomes depend on how firms use the tools.
- **Disclosure**: many jurisdictions require telling users when they are talking to a machine.

## Open questions

- Which metrics best capture whether a customer's problem was solved, rather than whether the conversation ended.
- How to set escalation thresholds that balance cost and fairness across customer groups.

## References

### Seminal papers

- Budzianowski, P. & Vulić, I. (2019). Hello, It's GPT-2 — How Can I Help You? Towards the Use of Pretrained Language Models for Task-Oriented Dialogue Systems. arXiv. https://arxiv.org/abs/1907.05774 — Shows how a pretrained language model can be fine-tuned for task-oriented customer dialogue with little data.
- Bocklisch, T. et al. (2017). Rasa: Open Source Language Understanding and Dialogue Management. arXiv. https://arxiv.org/abs/1712.05181 — Describes an open-source framework for intent classification and dialogue management used in production assistants.
- Yao, S. et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. arXiv. https://arxiv.org/abs/2210.03629 — Interleaves reasoning steps with tool actions, the pattern most customer-service agents build on.
- Schick, T. et al. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. arXiv. https://arxiv.org/abs/2302.04761 — Shows language models can learn when and how to call external APIs.

### Surveys and textbooks

- Yao, S. et al. (2024). τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains. arXiv. https://arxiv.org/abs/2406.12045 — Benchmark in which simulated customers and agents interact under domain policies, measuring whether the agent reaches the right outcome.
- Brynjolfsson, E., Li, D. & Raymond, L. (2023). Generative AI at Work. *NBER Working Paper 31161*. https://doi.org/10.3386/w31161 — Field study of a generative assistant for customer-support agents, with heterogeneous gains across experience levels.
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. arXiv. https://arxiv.org/abs/2203.02155 — Instruction tuning with human feedback, the training approach behind most deployed assistants.
