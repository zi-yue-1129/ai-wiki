---
status: draft
last_reviewed: 2026-10-28
related:
  - society/misinformation
  - society/governance
  - society/ethics
tags:
  - elections
  - democracy
  - persuasion
aliases:
  - 選舉與民主
  - 人工智慧與選舉
  - 政治廣告
  - Political persuasion
---

# AI, elections and democracy

Generative AI can write persuasive political messages, produce convincing synthetic media and help campaigns target voters at scale. These capabilities raise questions about whether elections are fair, whether voters can form their own judgements, and who is accountable when a campaign uses AI. This page covers the democratic stakes. The mechanics of false content are covered in [Misinformation and deepfakes](../misinformation/index.md).

## Overview

Democracy depends on voters being able to learn about candidates, debate issues and trust that the information they receive is honest. AI changes three things. It lowers the cost of producing political text and images. It makes personalised messages cheap. And it makes it harder for voters to tell authentic content from fabricated content. The research so far shows that these concerns are real, but it does not yet show that AI reliably changes election outcomes.

## Key concepts

- **Microtargeting**: tailoring a political message to a specific person or small group, using their data.
- **Persuasion**: a change in a person's attitude or stated intention caused by a message.
- **Liar's dividend**: the ability of a public figure to dismiss real evidence as fake because fakes exist.
- **Political advertising rules**: legal duties on campaigns and platforms, such as disclosure and limits on targeting.

## How it works

A campaign can use an AI system to draft many variants of a message, test them and deliver those that perform best. Personalised content goes further, since a system can adapt the message to a voter's stated views or demographics. Synthetic video and audio can be used to mislead, but research suggests that the more common effect is uncertainty. Vaccari and Chadwick found that people are more likely to feel uncertain about a deepfake than to be misled by it, and that this uncertainty reduces trust in news shared on social media [(Vaccari and Chadwick, 2020)](https://doi.org/10.1177/2056305120903408).

Text raises a separate question. Kreps, McCain and Brundage ran three experiments on whether AI-generated news text is credible and whether it can influence opinions, including opinions on foreign policy [(Kreps, McCain and Brundage, 2020)](https://doi.org/10.1017/XPS.2020.37).

## What the evidence shows on persuasion

A preregistered experiment is the most direct test of the microtargeting worry. Hackenburg and Margetts built a web application that fed each participant's demographic and political data into GPT-4 prompts. In a randomised experiment with 8,587 participants, the messages were broadly persuasive, in some cases raising support for a policy stance by up to 12 percentage points. However, the persuasive impact of microtargeted messages was not statistically different from that of non-microtargeted messages (4.83 vs 6.20 percentage points, P = 0.226). The authors conclude that the influence of current LLMs may come from the general persuasiveness of their text, not from their ability to tailor it to each person [(Hackenburg and Margetts, 2024)](https://doi.org/10.1073/pnas.2403116121).

The public reaction to AI labels matters too. Altay and Gilardi found that people are sceptical of headlines labelled as AI-generated, even when the content is true or was written by humans, because they assume the labelled piece was fully automated [(Altay and Gilardi, 2024)](https://doi.org/10.1093/pnasnexus/pgae403). Labelling can therefore affect trust in accurate content as well as inaccurate content.

## Responses

The EU AI Act requires that deployers of AI systems that generate or manipulate deepfakes disclose that the content is artificially generated, with exceptions for some creative and artistic work [(Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj). Platform policies on political content add further constraints, and their rules differ widely across services and countries.

## Connections

The persuasion research links to the cognitive science and psychology side of the wiki, where belief change and source trust are long-standing topics. The governance questions are on [Law, policy and governance](index.md). The mechanics of false content are on [Misinformation and deepfakes](../misinformation/index.md).

## Applications

Campaigns use AI for content drafting, translation, volunteer outreach and voter data analysis. Election authorities and fact-checkers use detection tools and rapid-response monitoring. Platforms apply labelling and ad-transparency rules to political content.

## Open questions

- Do AI-generated messages change votes, as opposed to attitudes or stated intentions, and how large is any such effect in real campaigns?
- Will uncertainty about authenticity, rather than deception, become the main democratic harm?
- Who should be accountable when a campaign uses AI to produce misleading content: the campaign, the tool provider or the platform?
- How can transparency about AI use in campaigns be required without chilling legitimate uses?

## References

### Seminal papers

- Kreps, McCain and Brundage, *All the News That's Fit to Fabricate: AI-Generated Text as a Tool of Media Misinformation*, Journal of Experimental Political Science (2020). https://doi.org/10.1017/XPS.2020.37 — Three experiments on the credibility of AI-generated news text and its effect on opinions.
- Vaccari and Chadwick, *Deepfakes and Disinformation: Exploring the Impact of Synthetic Political Video on Deception, Uncertainty, and Trust in News*, Social Media + Society (2020). https://doi.org/10.1177/2056305120903408 — Experimental evidence that deepfakes mainly cause uncertainty, which reduces trust in news.
- Hackenburg and Margetts, *Evaluating the persuasive influence of political microtargeting with large language models*, Proceedings of the National Academy of Sciences (2024). https://doi.org/10.1073/pnas.2403116121 — A preregistered experiment with 8,587 participants finding that GPT-4 messages are persuasive and that microtargeting adds no significant effect.
- Altay and Gilardi, *People are skeptical of headlines labeled as AI-generated, even if true or human-made, because they assume full AI automation*, PNAS Nexus (2024). https://doi.org/10.1093/pnasnexus/pgae403 — Shows that AI labels reduce trust in headlines, including accurate ones.

### Articles and documentation

- European Union, *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*, Official Journal of the European Union (2024). https://eur-lex.europa.eu/eli/reg/2024/1689/oj — Sets deepfake disclosure duties for deployers.
