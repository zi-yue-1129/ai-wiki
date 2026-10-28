---
status: draft
last_reviewed: 2026-10-28
tags:
  - evaluation
  - psychology
aliases:
  - 自動化面試分析
  - 面試表現預測
  - 影片面試
---

# Automated Interview Analysis (Naim et al. 2015)

Automated interview analysis predicts how an interviewer will rate a candidate from the recorded behaviour of the interview: what is said, how it is said and what the face does. Naim et al. (2015) built a framework of this kind from videos of 138 interview sessions, and showed that ratings of traits such as engagement could be predicted with high correlation. It is one of the two landmark methods on the parent page [Human Resources and Recruiting](../index.md).

## Overview

Interviews are among the most consequential steps in many hiring processes, and their judgements are notoriously inconsistent. Two interviewers can rate the same answer differently, and the first minutes often colour the rest. Automated analysis promises a more consistent measure: the same features are extracted from every recording, and the same model scores every candidate.

The method does not measure ability directly. It learns to reproduce human ratings from observable behaviour. That distinction matters, because the quality of the prediction depends on the quality of the ratings, and on whether the observable behaviour is related to the job at all.

## Key concepts

- **Lexical features**: measures of the words a candidate uses, such as their number, their variety and the topics they touch on.
- **Prosodic features**: properties of speech sound, such as pitch, intonation, pauses and fluency.
- **Facial features**: measures from video, such as smiles, head movements and the positions of tracked facial points.
- **Ground truth from raters**: the target the model learns. Here it is a weighted average of nine independent judges' ratings of each interview.
- **Feature weights**: the relative contribution of each feature group in the trained regression, which the authors use to suggest what speakers should change.

## How it works

The framework follows a supervised pipeline. The steps below describe the design as summarised in the abstract; the exact feature sets and regression choices are in the paper.

1. **Record and transcribe.** Each candidate answers interview questions on video, and the speech is transcribed.
2. **Extract features.** Three groups are computed: lexical features from the transcript, prosodic features from the audio, and facial features from the video.
3. **Build the target.** Nine judges rate each interview. Their ratings are combined into a weighted average, the ground-truth score for training.
4. **Train a regression.** A regression model learns to predict the ground-truth ratings from the features, for overall performance and for traits such as excitement, friendliness and engagement.
5. **Read the weights.** Because the model is linear in its feature groups, the learned weights show which signals matter. The authors use them to suggest that speakers speak more fluently, use fewer filler words, say "we" rather than "I", use more distinct words and smile more.

The method is not a pure black box: the feature weights are the basis of the advice it gives, and that advice is only as sound as the features and the ratings behind it.

## Results

The abstract reports that the framework predicts ratings of traits such as excitement, friendliness and engagement with correlation coefficients of 0.75 or higher. It also reports that it can quantify the relative importance of prosody, language and facial expression. The authors observe that candidates rated highly on the first interview question were also rated highly overall. The study used 138 interview sessions with 69 undergraduates at the Massachusetts Institute of Technology, and the authors state that their dataset will be made available to other researchers. The evidence comes from a study of students, not from real hiring decisions.

## Limitations

- **Research setting.** Students answering questions for a research study do not face the same stakes as applicants for jobs, so the results may not transfer to real hiring.
- **Rating-based targets.** The model reproduces the judges' ratings. If the judges were biased, or the traits they rated are not job-relevant, the model learns that bias.
- **Face and voice features.** Facial and vocal signals differ across cultures, languages, disabilities and accents. A model trained on one group may misjudge others, and the abstract does not report a fairness analysis.
- **Advice is not causal.** Feature weights show association in the training data, not that changing a feature would improve a real interview outcome.

Later work has pressed these points. Hickman et al. (2022) found that personality assessments from mock video interviews had mixed reliability, and that they were more valid when trained on interviewer ratings than on self-reports.

## Open questions

- Does automated scoring predict later job performance, rather than interview ratings?
- Which features remain predictive across demographic groups, and which should be excluded as irrelevant to the job?
- Can the ratings used as targets be made more reliable, for example through structured interviews with explicit rubrics?

## References

### Seminal papers

- Naim, I., Tanveer, M. I., Gildea, D. & Hoque, M. E. (2015). *Automated Analysis and Prediction of Job Interview Performance*. arXiv preprint. https://arxiv.org/abs/1504.03425 — The original paper, which predicts interviewer ratings of MIT interview videos from language, facial and prosodic features.

### Surveys and textbooks

- Mehrabi, N. et al. (2019). *A Survey on Bias and Fairness in Machine Learning*. arXiv preprint. https://arxiv.org/abs/1908.09635 — Survey of how bias enters learned systems, which applies directly to models trained on human ratings.

### Articles and documentation

- Hickman, L. et al. (2022). Automated video interview personality assessments: Reliability, validity, and generalizability investigations. *Journal of Applied Psychology*. https://doi.org/10.1037/apl0000695 — Tests machine-learning personality assessments from mock video interviews across three samples, and finds reliability evidence mixed.
- Raghavan, M. et al. (2020). *Mitigating Bias in Algorithmic Hiring: Evaluating Claims and Practices*. FAT* 2020. https://arxiv.org/abs/1906.09208 — Reviews what vendors of video and other assessment tools disclose about validation and bias testing.
- Groves, L. et al. (2024). *Auditing Work: Exploring the New York City algorithmic bias audit regime*. FAccT 2024. https://arxiv.org/abs/2402.08101 — Interview study of New York City's bias-audit requirement for automated hiring tools, relevant to how interview tools would be audited.
