---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 成員推論
  - 成員推論攻擊
  - Membership inference attack
---

# Membership Inference

!!! info "Part of Privacy and Data Protection"
    This method page belongs to [Privacy and Data Protection](index.md). It explains the attack in detail; the parent page compares it with other risks.

A membership inference attack asks whether a particular record was in a model's training set. It needs only the ability to query the model, and it is one of the simplest ways a trained model can reveal information about the people in its data. Shokri et al. (2017) showed the attack against machine-learning services, and later work explained when it succeeds.

## Problem

A model should describe a population, not reveal whether a specific person's record was used to train it. Membership can be sensitive in itself: knowing that someone's medical record was in a training set of patients with a condition reveals a health fact. The problem is to measure how well an attacker can tell members from non-members, using only the model's outputs.

## Core idea

Train the attacker to recognise the difference in how the model responds to members and non-members. Models often produce more confident or lower-loss outputs on examples they were trained on. An attack classifier learns that pattern from models the attacker builds to imitate the target.

## How the attack works

1. **Build shadow models.** Train models on data the attacker controls, with a setup similar to the target.
2. **Collect outputs.** Record each model's output for examples known to be members and non-members of its training set.
3. **Train the attack model.** Learn a classifier that takes an output vector and predicts "member" or "non-member".
4. **Apply to the target.** Query the target model for the record in question and apply the attack model.

Shokri et al. (2017) describe this black-box setting. Yeom et al. (2018) show that overfitting is sufficient for such an attack, and that it is not the only factor. Carlini et al. (2022) argue that the usual evaluation, which reports average accuracy, can hide an attack's real power, and they propose evaluating at very low false-positive rates.

## Results

The abstract of Shokri et al. (2017) reports that models from commercial machine-learning services can be vulnerable to membership inference, and it gives no accuracy figure. The abstract of Carlini et al. (2022) reports that their attack, LiRA, is about ten times more powerful than prior attacks at low false-positive rates, such as below 0.1%. The strength of an attack therefore depends heavily on how it is scored.

## Limitations

- **Setting dependence.** Results depend on the model, its training regime and how much it overfits. A well-regularised model may be much less exposed.
- **Evaluation.** Average accuracy can make an attack look weak even when it reliably identifies some members, which is what matters for privacy.
- **Not the only leak.** Membership is one kind of leak. Attribute inference and extraction can reveal more, and defences against membership inference do not cover them.

## Connections

- The main defence in training is differential privacy. See [Differential Privacy](differential-privacy.md).
- Extraction of training text is a stronger form of leakage that goes beyond yes or no. See [Training Data Extraction](training-data-extraction.md).
- The same risk arises for training images, discussed on the copyright pages in [Copyright & IP](../copyright/index.md).

## Open questions

- Which training practices most reduce membership risk without a large loss of accuracy?
- Should a privacy evaluation of a model use low false-positive rates as the standard measure?
- How should membership risk be communicated to people whose data is in a training set?

## References

### Seminal papers

- Shokri, R., Stronati, M., Song, C. & Shmatikov, V. (2017). Membership inference attacks against machine learning models. *IEEE Symposium on Security and Privacy*. https://arxiv.org/abs/1610.05820 — Introduces the shadow-model attack and shows it against commercial machine-learning services.
- Yeom, S., Giacomelli, I., Fredrikson, M. & Jha, S. (2018). Privacy risk in machine learning: Analyzing the connection to overfitting. arXiv:1709.01604. https://arxiv.org/abs/1709.01604 — Shows that overfitting is sufficient for membership inference, and that it is not required.
- Carlini, N. et al. (2022). Membership inference attacks from first principles. arXiv:2112.03570. https://arxiv.org/abs/2112.03570 — Argues for evaluation at low false-positive rates and proposes the LiRA attack.
- Carlini, N. et al. (2022). Quantifying memorization across neural language models. arXiv:2202.07646. https://arxiv.org/abs/2202.07646 — Shows that memorisation grows with model size, duplication and prompt context.
- Carlini, N. et al. (2021). Extracting training data from large language models. *USENIX Security Symposium*. https://arxiv.org/abs/2012.07805 — Shows that memorised training text can be extracted, a stronger leak than membership alone.
