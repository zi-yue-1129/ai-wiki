---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
  - theory/paradigms/federated
  - society/governance
tags:
  - privacy
  - data protection
aliases:
  - 隱私
  - 資料保護
  - 個人資料保護
---

# Privacy and Data Protection

AI systems learn from information about people, and they can sometimes reveal it again. Privacy work asks which data may be collected and used, what a trained model can leak about its training data, and which legal and technical safeguards keep individuals in control.

## Overview

Modern models are trained on very large collections of text, images and behavioural records, much of it gathered from the web without the knowledge of the people it describes. Privacy problems arise at three points: when data is **collected and used for training**, when a **trained model leaks** what it learned, and when a deployed system **infers sensitive facts** from ordinary inputs. Debates about privacy in AI therefore combine questions of data governance with technical questions about what a model has memorised. For the wider ethical context, see [Ethics & Fairness](../ethics/index.md).

## Key concepts

- **Personal data**: any information relating to an identified or identifiable person, including data that is inferred rather than collected.
- **Memorisation**: a model reproducing specific training examples, sometimes word for word, rather than only general patterns.
- **Membership inference**: deciding whether a given record was in a model's training set.
- **Attribute inference**: predicting a sensitive property, such as health or political views, from data that never stated it.
- **Differential privacy**: a formal guarantee that no single person's data changes the output distribution much. See [Federated & Privacy-Preserving Learning](../../theory/paradigms/federated/index.md).
- **Data minimisation and purpose limitation**: the legal principles that data should be used for a stated purpose and kept no longer than needed.

## How it works

Three mechanisms explain most leakage.

1. **Memorisation.** Large models can store rare or repeated sequences. Carlini et al. (2021) showed that training text can be recovered by sampling from a language model (see [Key methods](#key-methods)). Repeated data is memorised more readily, so deduplication before training lowers the risk.
2. **Membership inference.** A model is often more confident on examples it was trained on. An attacker who can query the model can exploit that gap to separate members from non-members.
3. **Inference from innocuous data.** A model trained on public data can predict private traits from correlated signals such as writing style, purchase history or location. This follows from learning itself, not from a bug, so restricting access to the data does not fully solve it.

**Unlearning**, removing one person's data from a trained model after the fact, is hard. Retraining is expensive, and approximate methods give weaker guarantees that are difficult to check.

## Key methods

### Dwork et al. (2006), differential privacy

- **Problem:** release aggregate statistics from a database without revealing whether any one person is in it.
- **Core idea:** add random noise scaled to how much one record could change the answer (the query's sensitivity), so the output looks almost the same with or without that record.
- **Equation or algorithm:** a randomised mechanism \(M\) is \(\varepsilon\)-differentially private if, for every pair of datasets \(D, D'\) that differ in one record and every set of outputs \(S\), \(\Pr[M(D)\in S] \le e^{\varepsilon}\Pr[M(D')\in S]\). The Laplace mechanism adds noise with scale sensitivity divided by \(\varepsilon\).
- **Results:** a formal guarantee and a recipe for calibrating noise, rather than an empirical benchmark.
- **Limitations:** privacy costs accuracy, and small groups are affected most. Each release uses part of a privacy budget, so repeated queries weaken the guarantee.

### Shokri et al. (2017), membership inference

- **Problem:** can an attacker with only black-box query access to a trained model tell whether a particular record was in its training set?
- **Core idea:** build models that imitate the target's behaviour, then train an attack classifier that learns how the target's predictions differ for members and non-members.
- **Equation or algorithm:** the attack is a binary classifier over the model's output vector, trained on examples whose membership the attacker knows.
- **Results:** the paper reports that models from commercial machine-learning services, including Google and Amazon, can be vulnerable to membership inference.
- **Limitations:** the attack depends on outputs that differ between members and non-members. Defences such as regularisation and differential privacy narrow that gap, usually at some cost in accuracy.

### Carlini et al. (2021), extracting training data from language models

- **Problem:** do large language models memorise training text in a form that an outside user can extract?
- **Core idea:** generate many samples from the model, rank them by signs of memorisation such as unusually high likelihood, and check the top candidates against sources on the web.
- **Equation or algorithm:** (1) sample many continuations; (2) score each by its likelihood, relative to a reference model; (3) keep the highest-scoring candidates; (4) verify each candidate against the training corpus.
- **Results:** the abstract reports that the attack extracts hundreds of verbatim text sequences from the training data of GPT-2.
- **Limitations:** the study targets GPT-2. The authors also report that larger models were more vulnerable than smaller ones, and extraction success depends on how many samples the attacker can afford.

## Protection techniques

| Technique | What it protects | Trade-off |
|---|---|---|
| Deduplication and filtering | Keeps repeated or sensitive strings out of training | Detection is imperfect; may remove useful data |
| Differential privacy in training (DP-SGD) | Limits the influence of any one example | Lower accuracy and slower training |
| Federated learning | Keeps raw data on users' devices | Shared updates can still leak; see [federated learning](../../theory/paradigms/federated/index.md) |
| Access control and minimisation | Limits who sees data and how much is kept | Less data available for learning |
| Machine unlearning | Removes a person's influence after training | Hard to verify; often approximate |

## Law and regulation

- **GDPR**: Regulation (EU) 2016/679, adopted on 27 April 2016, gives individuals rights of access and erasure and requires a lawful basis for processing personal data. Whether a trained model itself counts as personal data is actively debated.
- **EU AI Act**: Regulation (EU) 2024/1689, dated 13 June 2024, takes a risk-based approach and restricts some uses of biometric identification. It applies alongside data-protection law rather than replacing it.
- Other jurisdictions take different approaches. See [Law, Policy & Governance](../governance/index.md) for national and international efforts.

## Connections

- Privacy is one of the shared principles in [Ethics & Fairness](../ethics/index.md), where it is treated mainly as a question of values.
- Neural and brain data are among the most sensitive kinds of personal data. A [brain-computer interface](../../brain-mind/bci/index.md) can record signals that reveal intent or health, which raises the same questions in a new form.
- The technical side of privacy-preserving learning is covered in [Federated & Privacy-Preserving Learning](../../theory/paradigms/federated/index.md).

## Applications

- **Health records**: clinical models need access controls and de-identification before data leaves a hospital.
- **Official statistics and analytics**: statistical agencies and large technology companies release aggregate figures with differential privacy.
- **On-device processing**: keyboards and voice assistants increasingly run models locally, so raw input does not leave the device.

## Open questions

- Does a trained model contain personal data in the legal sense, and if so, how can it be erased?
- How can memorisation be measured reliably as models and training sets grow?
- Differential privacy reduces accuracy most for small groups. How should that trade-off with fairness be decided?
- Is web-scraped data for training covered by consent, legitimate interest or neither?

## References

### Seminal papers

- Dwork, C., McSherry, F., Nissim, K. & Smith, A. (2006). Calibrating noise to sensitivity in private data analysis. *Theory of Cryptography Conference (TCC)*. https://doi.org/10.1007/11681878_14 — Introduces differential privacy and the noise-calibration framework used across the field.
- Shokri, R., Stronati, M., Song, C. & Shmatikov, V. (2017). Membership inference attacks against machine learning models. *IEEE Symposium on Security and Privacy*. https://arxiv.org/abs/1610.05820 — Shows that black-box queries can reveal training-set membership, including against commercial machine-learning services.
- Carlini, N. et al. (2021). Extracting training data from large language models. *USENIX Security Symposium*. https://arxiv.org/abs/2012.07805 — Demonstrates extraction of verbatim training sequences from GPT-2.
- Abadi, M. et al. (2016). Deep learning with differential privacy. *ACM CCS*. https://arxiv.org/abs/1607.00133 — DP-SGD, which clips and adds noise to gradients during training.

### Surveys and textbooks

- Dwork, C. & Roth, A. (2014). *The Algorithmic Foundations of Differential Privacy*. Foundations and Trends in Theoretical Computer Science, 9(3–4). https://doi.org/10.1561/0400000042 — The standard textbook on differential privacy, with the mechanisms and proofs in full.

### Articles and documentation

- EUR-Lex. *Regulation (EU) 2016/679 (General Data Protection Regulation)*. https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng — The official text of the GDPR, the main European law on personal data.
- EUR-Lex. *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng — The official text of the EU AI Act, with its risk-based rules.
