---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/education
  - society/privacy
  - society/governance
tags:
  - children
  - education
  - child rights
  - policy
aliases:
  - Children and AI
  - AI and children
  - AI education policy
  - 兒童與 AI
  - 兒童教育政策
---

# Children, Education Policy and AI

Children use AI in schools, at home and on consumer platforms, often before any rules for their age group exist. This page covers the policy questions that follow: which protections apply, how age limits and consent work, and how the design of an AI tool affects what children learn.

## Overview

Policy for children and AI sits where three frameworks meet: child rights, data protection and education. Most recent guidance asks that AI be designed for children's best interests and development, rather than adapted from adult products after release. The guidance is mostly advisory. Binding rules are narrower, and in many places they are still being written.

## Key concepts

- **Child**: the age below which a law gives special protection. Under the US Children's Online Privacy Protection Act, a child is an individual under 13 (15 U.S.C. §6501). Other laws use different ages.
- **Verifiable parental consent**: under the same Act, a reasonable effort, given available technology, to make sure a parent receives notice of an operator's practices and authorises the collection of a child's personal information before it happens.
- **Guardrails**: design features that shape how an AI tool responds, such as prompts that ask a student to reason through a problem rather than giving the answer.

## How it works

Policy affects children through three levers.

1. **Access and age limits.** UNESCO's 2023 guidance recommends setting an age limit for independent conversations with generative AI platforms. It does not say what that age should be.
2. **Data protection.** The same guidance recommends mandating data privacy protection. UNICEF's 2025 guidance lists the protection of children's data and privacy as one of its ten requirements. In the United States, the Children's Online Privacy Protection Act requires verifiable parental consent before collecting personal information from children under 13 on services directed to them.
3. **Design and pedagogy.** Whether a tool gives answers or guides reasoning changes what students learn. In a field study with high-school mathematics students, Bastani et al. (2025) found that generative AI used without guardrails harmed learning, while tutors with guardrails that encouraged reasoning protected student learning and performance.

## Responses

| Approach | What it does | Limits |
|---|---|---|
| Age limits on independent use | Restricts when a child can use a generative AI platform alone | UNESCO does not give an age; checking age can require collecting more data about the child |
| Parental consent and data rules | Requires consent and limits what can be collected from young children | The US rule covers children under 13; other countries have different thresholds and rules |
| Child-centred design requirements | Sets out ten requirements for AI that upholds child rights, from safety to AI skills | Guidance rather than binding law |
| Guardrailed tutor design | Prompts reasoning rather than giving answers | Evidence comes from specific studies, and the effect may vary by subject and age |

## Connections

- Tools used in classrooms, such as tutors and feedback systems, are covered in [Education](../../applications/education/index.md).
- How children's data is protected under privacy law, including for models trained on personal data, is covered in [Privacy & Data Protection](../privacy/index.md).
- The laws and standards that set these duties are compared in [Law, Policy & Governance](../governance/index.md).

## Applications

- **Schools** deciding which AI tools to allow in classrooms and at what age.
- **Parents** deciding whether a child may use an AI service alone.
- **Product teams** building AI for children, who must meet consent and design requirements.
- **Policymakers** setting age limits and consent rules for AI services.

## Open questions

- What age limits are appropriate for independent AI use, and how can age be checked without collecting more personal data?
- Do guardrailed tutors keep their benefits over a longer period and outside mathematics?
- How should children learn AI literacy, which UNICEF's guidance lists as a requirement?

## References

### Seminal papers

- Seßler, K. et al. (2023). ChatGPT for good? On opportunities and challenges of large language models for education. *Learning and Individual Differences*, 103, 102274. https://doi.org/10.1016/j.lindif.2023.102274 — Overview of the opportunities and challenges that large language models present for education, by a multidisciplinary author group.
- Bastani, H. et al. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. *PNAS*. https://doi.org/10.1073/pnas.2422633122 — Field study of high-school mathematics students using generative AI tutors, comparing tutors with and without guardrails that encourage reasoning.

### Articles and documentation

- UNICEF Office of Strategy and Evidence – Innocenti (2025). *Guidance on AI and children*, version 3.0. https://www.unicef.org/innocenti/reports/policy-guidance-ai-children — Ten requirements for AI policies and systems that uphold child rights, covering safety, data protection, fairness, transparency, inclusion and AI skills.
- Miao, F. & Holmes, W. (2023). *Guidance for generative AI in education and research*. UNESCO. https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research — Recommends mandating data privacy protection and an age limit for independent use of generative AI platforms, with an age-appropriate approach to educational design.
- *Children's Online Privacy Protection Act*, 15 U.S.C. §6501 (definitions). https://www.law.cornell.edu/uscode/text/15/6501 — Defines "child" as an individual under 13 and sets out verifiable parental consent. The obligations on operators are in §6502.
