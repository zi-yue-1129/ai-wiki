---
status: draft
last_reviewed: 2026-10-28
related:
  - society/governance
  - applications/creative
  - applications/cybersecurity
  - applications/social-science
tags:
  - misinformation
  - deepfakes
aliases:
  - 不實資訊
  - 假訊息
  - 深偽
  - Deepfake
  - Disinformation
---

# Misinformation and Deepfakes

Generative AI makes it cheap to produce convincing text, images, audio and video. This lowers the cost of false content, and it also changes how people judge what is real. This page covers how false information spreads, how AI changes that process, and what can be done about it.

## Overview

Misinformation is false or misleading information shared without intent to deceive. Disinformation is false information shared on purpose. A **deepfake** is synthetic media, usually video or audio, that shows a real person doing or saying something they did not. Before generative AI, fabricating convincing media took skill and time. Today a single person with a consumer tool can produce material that looks like a press photo, a news clip or a voice message from a family member.

Two effects matter most. First, false content becomes cheaper to make and to scale. Second, the mere existence of realistic fakes lets people dismiss authentic evidence as fake. The second effect is sometimes called the **liar's dividend**.

## Key concepts

- **Synthetic media**: text, images, audio or video generated or substantially altered by a model.
- **Provenance**: a record of where a piece of content came from and how it was edited, attached to the file.
- **Watermarking**: a signal embedded in generated content to mark its origin. It can be removed or weakened.
- **Detection**: classifying content as manipulated or generated. Detectors and generators are in an arms race.
- **Liar's dividend**: the ability of a person to deny real evidence by claiming it is fake.

## How it works

Three processes shape the harm.

1. **Spread.** Content spreads through social networks, often faster than corrections. Emotionally charged and novel claims travel furthest. People, rather than automated accounts, drive most of the spread (see [Key methods](#key-methods)).
2. **Production.** Generative models lower the skill needed to create a fake. Text can be produced at scale, personalised to readers, and posted from many accounts. Voice cloning and face-swap tools are used for fraud and impersonation (see [Cybersecurity](../../applications/cybersecurity/index.md)).
3. **Doubt.** When fakes are common, people trust less of what they see. This erodes shared evidence even when the content is genuine.

Detection is one line of defence. Detectors look for artefacts left by generators, such as inconsistent lighting, blinking or compression traces, but they tend to degrade on content from generators they were not trained on. Provenance systems take the opposite approach: they record authenticity at capture or creation, rather than guessing it afterwards.

## Key methods

Each method has its own page with the problem, method, results and limitations. The table compares them briefly.

| Method | Question | Main result (per abstract) | Read more |
|---|---|---|---|
| Spread of true and false news (Vosoughi et al., 2018) | Do true and false stories spread differently, and do bots explain the difference? | False news spread farther, faster, deeper and more broadly; humans, not robots, drive the difference | [How False News Spreads](spread-of-false-news.md) |
| Facial manipulation detection (Rössler et al., 2019) | Can manipulated faces be detected reliably at scale? | A benchmark of over 1.8 million manipulated images; no numeric accuracy in the abstract | [FaceForensics++](facial-manipulation-detection.md) |

## Responses

| Approach | What it does | Limits |
|---|---|---|
| Provenance (for example [C2PA Content Credentials](https://c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html)) | Records capture and edit history in signed metadata | Only useful if adopted along the whole chain; metadata can be stripped |
| Watermarking of generated output | Marks model output at creation | Can be removed or weakened; must be robust across platforms |
| Detection | Flags likely fakes after publication | Degrades on new generators; false positives harm real people |
| Platform rules and labelling | Downranks, labels or removes content | Trade-offs with free expression; hard to apply consistently at scale |
| Media literacy | Helps people check sources and recognise manipulation | Slow; hard to measure its effect |

Regulation is moving in parallel. The EU AI Act sets transparency obligations for AI-generated content, and the Digital Services Act requires very large platforms to assess and reduce systemic risks, including disinformation. See [Law, Policy & Governance](../governance/index.md) for other jurisdictions.

## Connections

- Psychological research on repetition, emotion and trust explains why false claims persist (see [Psychology & AI](../../brain-mind/psychology/index.md)).
- Misinformation overlaps with [Ethics & Fairness](../ethics/index.md), where it is treated as a harm to a shared information environment.
- Creative and political uses of synthetic media are covered in [Creative AI](../../applications/creative/index.md) and [Social Science](../../applications/social-science/index.md).

## Applications

- **Fact-checking support**: models help find claims worth checking and retrieve prior verifications, with humans making the final call.
- **Provenance tooling** in cameras, editing software and news publishing.
- **Fraud prevention**: banks and call centres use voice and video checks against impersonation.

## Open questions

- Can detection keep pace with generation, or will provenance have to carry the load?
- How large is the real-world effect of AI-generated misinformation compared with human-made content?
- How should platforms balance labelling and removal against free expression?
- How can the liar's dividend be countered without giving cover to false denials?

## References

### Seminal papers

- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science*, 359, 1146–1151. https://www.media.mit.edu/publications/the-spread-of-true-and-false-news-online/ — Compares the spread of true and false stories on Twitter and finds false news travels farther and faster, mainly through human sharing.
- Rössler, A. et al. (2019). FaceForensics++: Learning to detect manipulated facial images. *ICCV*. https://arxiv.org/abs/1901.08971 — Benchmark of facial manipulations with compression variations and a hidden test set for training and evaluating detectors.
- Chesney, B. & Citron, D. (2019). Deep fakes: A looming challenge for privacy, democracy, and national security. *California Law Review*, 107. https://www.californialawreview.org/print/deep-fakes-a-looming-challenge-for-privacy-democracy-and-national-security — Legal analysis of deepfake harms, including the liar's dividend.

### Articles and documentation

- C2PA. *Content Credentials: C2PA Technical Specification*, version 2.0. https://c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html — The open standard for signed provenance metadata, backed by a steering committee of technology and media companies.
- EUR-Lex. *Regulation (EU) 2022/2065 (Digital Services Act)*. https://eur-lex.europa.eu/eli/reg/2022/2065/oj/eng — The official text of the DSA, which sets systemic-risk duties for very large online platforms.
- EUR-Lex. *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng — The official text of the EU AI Act, including transparency rules for AI-generated content.
