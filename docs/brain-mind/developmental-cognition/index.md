---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/cognitive-science
- brain-mind/psychology
- brain-mind/neuroai
tags:
- psychology
- development
aliases:
  - 發展認知
  - 嬰幼兒如何學習
  - Developmental Cognition
  - How Children Learn
---

# Developmental Cognition and How Children Learn

Infants arrive with some knowledge and learn a great deal in their first years. Developmental cognition asks which abilities are built in, which are learned from experience, and how the two interact. Its methods are unusual, because infants cannot answer questions, so researchers measure what infants look at, how long they look, and what surprises them. These measures have produced some of the clearest evidence on how learning begins.

## Overview

Children learn language, objects, numbers and other people with little explicit instruction. Two broad positions compete. Nativists argue that a set of core knowledge is present early, which makes learning faster. Empiricists and learning theorists argue that general mechanisms, such as statistical learning, can extract structure from experience. Many current accounts combine the two. [Cognitive Science](../cognitive-science/index.md) covers the adult side of cognition; this page covers how it develops, and what that tells us about learning in general.

## Key concepts

- **Core knowledge**: a small set of systems present early in life, for objects, agents, number, space and social partners. Spelke and Kinzler (2007) set out this view.
- **Looking-time measures**: infants look longer at events that surprise them, so looking time serves as an index of expectation.
- **Statistical learning**: the ability to detect patterns, such as which sounds tend to follow one another, from the frequencies in a stream of input.
- **Goldilocks effect**: infants attend most to sequences that are neither too simple nor too complex, which shapes what they learn next.
- **Developmental change**: how abilities change with age and experience, and how early knowledge is revised.

## How it works

Infant research runs on a few paradigms. In a habituation study, an infant is shown an event until its looking time falls, and then a new event is shown. A longer look at the new event indicates that the infant detects a difference. Violation-of-expectation studies extend this by showing events that are physically possible or impossible.

```mermaid
flowchart LR
  E[Familiarisation<br/>or event] --> H[Habituation<br/>looking time falls]
  H --> T[Test event<br/>possible or impossible]
  T --> L[Longer look<br/>indicates surprise]
  L --> I[Inference about<br/>what the infant expects]
```

Two findings have shaped the field. Infants show expectations about objects and agents well before they can report them. They also extract statistical regularities from brief exposure, which suggests a general learning mechanism working alongside core knowledge.

## Key methods

Each method has its own page. This table is only a comparison.

| Method | What it measures | Page |
|---|---|---|
| Violation of expectation (Baillargeon, Spelke & Wasserman, 1985) | Whether infants look longer at physically impossible events, as a sign of expectation about objects | [Baillargeon et al. 1985](violation-of-expectation/index.md) |
| Statistical learning (Saffran, Aslin & Newport, 1996) | Whether infants pick up word-like units from the transition probabilities in continuous speech | [Saffran et al. 1996](statistical-learning/index.md) |

## Connections

- **Cognitive science**: the adult psychology of concepts and reasoning that development leads to is on [Cognitive Science](../cognitive-science/index.md).
- **Psychology**: how biases and reasoning change across life is discussed on [Psychology & AI](../psychology/index.md).
- **Language**: the speech-segmentation problem that statistical learning addresses is on [Language in the Brain](../language-in-brain/index.md).
- **Machine learning**: whether machines can learn core knowledge the way children do is discussed on [NeuroAI](../neuroai/index.md) and by Lake et al. (2017) in the references below.

## Applications

- **Early education**: research on learning in infancy informs how curricula are sequenced, including the idea that moderately complex material is most engaging.
- **Machine learning design**: the core-knowledge and statistical-learning debate shapes proposals for training AI systems with less data.

## Open questions

- **Which core knowledge is innate?** Evidence from infants is strong for some domains and contested for others, and the boundary is still under study.
- **How much structure can statistical learning explain?** Brief exposure yields real regularities, but it is unclear how far this extends to grammar and meaning.
- **Do looking-time measures mean what they seem to?** A longer look could reflect surprise, interest or something else, and the interpretation is debated.

## References

### Seminal papers

- Baillargeon, R., Spelke, E. S. & Wasserman, S. (1985). Object permanence in five-month-old infants. *Cognition*. https://doi.org/10.1016/0010-0277(85)90024-9 — Uses looking time to show that young infants expect objects to continue to exist when hidden.
- Saffran, J. R., Aslin, R. N. & Newport, E. L. (1996). Statistical learning by 8-month-old infants. *Science*. https://pubmed.ncbi.nlm.nih.gov/8943209/ — Shows that infants pick up word-like units from transition probabilities in a continuous stream of syllables.

### Surveys and reviews

- Spelke, E. S. & Kinzler, K. D. (2007). Core knowledge. *Developmental Science*. https://pmc.ncbi.nlm.nih.gov/articles/PMC2746564 — Sets out the core-knowledge systems that infants share across domains.
- Lake, B. M., Ullman, T. D., Tenenbaum, J. B. & Gershman, S. J. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — Argues that machines should build in core knowledge and learn as children do.
- Kidd, C., Piantadosi, S. T. & Aslin, R. N. (2012). The Goldilocks effect: human infants allocate attention to visual sequences that are neither too simple nor too complex. *PLoS ONE*. https://pmc.ncbi.nlm.nih.gov/articles/PMC3359326 — Shows that infants attend most to sequences of intermediate complexity.
