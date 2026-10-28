---
status: draft
last_reviewed: 2026-10-28
tags:
  - retrieval
  - fairness
aliases:
  - PJFNN
  - 人職適配
  - 人崗適配
  - 人職匹配
---

# Person-Job Fit (Zhu et al. 2018)

Person-Job Fit is the task of deciding how well a candidate's qualifications match a job, and the Person-Job Fit Neural Network (PJFNN) of Zhu et al. (2018) is an early deep-learning answer to it. The model learns joint representations of candidates and job requirements from historical applications, and it can say which requirement items a candidate meets. It is one of the two landmark methods on the parent page [Human Resources and Recruiting](../index.md).

## Overview

Résumé screening is a matching problem. A recruiter reads a job posting, lists its requirements, and checks each candidate's profile against them. Early automated systems matched keywords, which misses synonyms and skills described in different words. Zhu et al. propose to learn the match from data: past applications show which candidates were a fit for which jobs, and a neural network can learn the link between the two texts from those examples.

The paper treats fit as a joint property of a person and a job, not a score for the person alone. This makes the output more useful: the model can point to the requirements a candidate satisfies, rather than returning one number with no explanation.

## Key concepts

- **Bipartite network**: a network with two input sides, one for the candidate and one for the job, that meet in a shared representation.
- **Joint representation**: a vector space in which a candidate and a job can be compared directly, so that closeness means fit.
- **Requirement items**: the separate statements in a job posting, such as a skill, a qualification or a years-of-experience requirement, each represented on its own.
- **Hierarchical representation**: a layered design in which the model first represents small units of text, then combines them into a representation of the whole profile or posting.

## How it works

The abstract describes a model whose parts can be summarised as follows. The steps are a plain-language reading of the design; the exact layer sizes and equations are in the paper and should be checked there.

1. **Encode the job.** Each requirement item in a posting is turned into a vector with a convolutional network, which slides learned filters over the words of the text and pools the results.
2. **Encode the candidate.** The candidate's qualifications, taken from the résumé, are encoded in the same hierarchical way, so that the two sides can be compared item by item.
3. **Learn the joint space.** The bipartite network is trained on historical applications, where each example pairs a candidate with a job and records the outcome. The network learns a joint representation of the two sides.
4. **Score fit and requirements.** The overall fit is estimated from the joint representation. For each requirement item, the distance between its vector and the matching candidate representation indicates whether the requirement is satisfied.

The design is end-to-end: the text encoders and the matching network are trained together, rather than engineered separately.

## Results

The authors report extensive experiments on a large real-world dataset of job applications, which they say validate the model's performance at predicting fit. They also show visualisations of job and talent benchmarks learned by the model. The abstract gives no figures, so this page quotes none. Readers who need the comparison with baseline models should read the experiments section of the paper.

## Limitations

- **Target bias.** The labels are past decisions. A model trained on them learns the decisions, including any discrimination in them, as the Amazon case shows (see [Algorithmic Bias Case Studies](../../../society/ethics/bias-case-studies.md)).
- **Text only.** The model reads what is written in a résumé and posting. It cannot see skills that a candidate has but does not write down, and it may reward candidates whose résumés are written in the house style of past hires.
- **Dated architecture.** Convolutional encoders have since been overtaken by transformer language models such as BERT (Devlin et al. 2019), which are the usual starting point for newer text-matching work (see [Transformers](../../../theory/models/transformer/index.md)).
- **Requirement-level explanations.** The explanation is only as good as the posting. Vague or inflated requirements produce vague explanations.

## Open questions

- Would a model trained on outcomes that a fairness review has corrected (for instance, performance rather than hiring) learn a better notion of fit?
- How do requirement-level scores hold up across languages and occupations, and against adversarial résumés written to match the posting?
- How should a fit score be presented to a recruiter so that it supports a decision rather than replacing one (see [Human-AI Interaction](../../../society/human-ai-interaction/index.md))?

## References

### Seminal papers

- Zhu, C. et al. (2018). *Person-Job Fit: Adapting the Right Talent for the Right Job with Joint Representation Learning*. arXiv preprint. https://arxiv.org/abs/1810.04040 — The original paper, introducing the bipartite, hierarchical PJFNN for matching candidates to job requirements.
- Kim, Y. (2014). *Convolutional Neural Networks for Sentence Classification*. arXiv preprint. https://arxiv.org/abs/1408.5882 — Shows that a simple convolutional network over word embeddings works well for sentence classification, the family of text encoders used for postings and résumés.
- Devlin, J. et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv preprint (2018); NAACL 2019. https://arxiv.org/abs/1810.04805 — Pre-trained bidirectional Transformer encoder that replaced task-specific convolutional encoders in many text-matching systems.

### Surveys and textbooks

- Mehrabi, N. et al. (2019). *A Survey on Bias and Fairness in Machine Learning*. arXiv preprint. https://arxiv.org/abs/1908.09635 — Survey of sources of bias and fairness definitions, relevant to any model trained on historical hiring decisions.

### Articles and documentation

- Decorte, J.-J. et al. (2021). *JobBERT: Understanding Job Titles through Skills*. arXiv preprint. https://arxiv.org/abs/2109.09605 — Represents job titles through the skills in vacancies, a companion approach to matching requirements with candidates.
- Wilson, K. & Caliskan, A. (2024). *Gender, Race, and Intersectional Bias in Resume Screening via Language Model Retrieval*. arXiv preprint. https://arxiv.org/abs/2407.20371 — Audit showing that learned résumé-to-job matching can systematically favour some names over others.
- Raghavan, M. et al. (2020). *Mitigating Bias in Algorithmic Hiring: Evaluating Claims and Practices*. FAT* 2020. https://arxiv.org/abs/1906.09208 — Reviews what vendors of algorithmic assessments disclose about validation and bias testing.
