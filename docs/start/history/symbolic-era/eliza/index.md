---
status: draft
last_reviewed: 2026-10-28
related:
  - brain-mind/psychology
tags:
  - natural language processing
  - chatbots
aliases:
  - ELIZA
  - 伊麗莎
  - 聊天機器人
  - 模式匹配
  - Pattern matching
  - ELIZA effect
  - ELIZA 效應
---

# ELIZA

ELIZA, written by Joseph Weizenbaum at MIT and described in 1966, was a conversation program that matched keywords in a user's sentence against decomposition patterns and produced replies from reassembly templates. It had no model of meaning, yet its reception showed how readily people attribute understanding to a machine that reflects their own words. It is the period's best-known natural language system and a landmark of the [symbolic era](../index.md).

## Overview

Natural language was one of the hardest problems the early AI programmers set themselves, because sentences depend on syntax, meaning and context. ELIZA took a different route. Rather than parse and understand a sentence, it looked for trigger words, rewrote the sentence into a fixed form, and returned a reply built from that form. The most famous script imitated a non-directive psychotherapist, which gave the program an easy excuse for asking questions and reflecting statements back to the user.

The program showed how little a conversation needs in order to feel meaningful to the person in it. Weizenbaum, who designed ELIZA to show the limits of such methods, was disturbed by how seriously some users took it. His 1966 paper describes the mechanism and discusses these psychological issues.

## Key concepts

- **Keyword**: a word in the input that triggers a particular set of rules. Each keyword can carry a rank that decides which one is used when several appear.
- **Decomposition rule**: a pattern that splits the input sentence into fragments, for example the words before and after a keyword.
- **Reassembly rule**: a template that puts the fragments into a reply. Pronouns are usually swapped (for example "my" becomes "your") so that the reply addresses the user.
- **Script**: the complete set of keywords and rules for one conversational role. Changing the script changes the program's behaviour without changing the matching engine.
- **ELIZA effect**: the tendency of people to attribute understanding, feelings or intent to a program that merely reflects their input.

## How it works

ELIZA's processing is a short cycle of pattern matching:

1. Scan the input for keywords and select the one with the highest rank.
2. Apply the decomposition rule attached to that keyword to split the input into parts.
3. Choose a reassembly rule for that decomposition, rotating through alternatives so that replies do not repeat exactly.
4. Fill the template with the parts, swapping pronouns, and return the reply.
5. If no keyword is present, fall back to a generic reply such as a request to continue.

The sequence below is an illustrative example of the method, not a transcript from the paper. Given an input "I am sad about my job", a rule for the phrase "I am" might decompose the sentence into "sad about my job" and reassemble it as "How long have you been sad about your job?" No part of the sentence is understood. The program has only a pattern and a template.

The engine is therefore a small set of rules over text, with no internal representation of the world, no memory of earlier meaning and no learning. Its output depends on the script it is given.

## Results

Weizenbaum's 1966 paper describes ELIZA's design and the scripts used in its demonstrations, and it discusses the psychological issues that the approach raises. The evidence is of a qualitative kind: the program is shown working on example conversations, and its effect on users is reported and discussed. The paper does not present a benchmark score, and the results should be read as a demonstration of an approach rather than a measured performance level.

## Limitations

- **No understanding.** Replies can be fluent and still be wrong about what the user said, because the program never represents the meaning of a sentence.
- **Brittleness.** Sentences that match no keyword, or that match a keyword in the wrong sense, produce replies that ignore the content.
- **Hand-written scripts.** Every new conversational domain needs a new script written by a person, and the rules do not transfer.
- **Misleading impressions.** The ELIZA effect means that user satisfaction is not evidence that the system understands. This became a central concern in later work on conversational systems.

## Open questions

- Where does fluent conversation end and understanding begin? The same question returns with [large language models](../../../../theory/models/llm/index.md), which produce far more capable replies by a very different route.
- How should designers present conversational systems so that users are not misled about what they understand? This is a question for [human-AI interaction](../../../../society/human-ai-interaction/index.md).
- Do people attribute mental states to machines in the same way they do to people? The [psychology](../../../../brain-mind/psychology/index.md) pages discuss the evidence on attributing minds to artificial systems.

## References

### Seminal papers

- Weizenbaum, J. (1966). ELIZA: A computer program for the study of natural language communication between man and machine. *Communications of the ACM*. https://doi.org/10.1145/365153.365168 — Describes ELIZA's keyword, decomposition and reassembly rules and discusses the psychological issues they raise.
- Chomsky, N. (1956). Three models for the description of language. *IRE Transactions on Information Theory*. https://doi.org/10.1109/TIT.1956.1056813 — Compares finite-state, phrase-structure and transformational models of grammar, the formal background of early work on natural language.
- Winograd, T. (1972). Understanding natural language. *Cognitive Psychology*. https://doi.org/10.1016/0010-0285(72)90002-3 — Describes a language-understanding system for a blocks microworld, the contrast case to ELIZA's pattern-based approach.

### Surveys and textbooks

- Nilsson, N. J. (2009). *The Quest for Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/CBO9780511819346 — A history of AI that places the early work on language and conversation within the wider development of the field.

### Articles and documentation

- Haenlein, M. & Kaplan, A. (2019). A brief history of artificial intelligence: On the past, present, and future of artificial intelligence. *California Management Review*. https://doi.org/10.1177/0008125619864925 — A short history of AI and its main perspectives, written as the introduction to a special issue on the field.
