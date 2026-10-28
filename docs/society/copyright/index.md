---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/creative
  - society/privacy
  - society/governance
  - society/economics
tags:
  - copyright
  - intellectual property
  - training data
aliases:
  - 著作權
  - 智慧財產權
  - 版權
  - Copyright
---

# Copyright and Intellectual Property

AI systems are trained on books, images, music, code and web pages that people created and, in most cases, own. Copyright and related rights decide whether that use needs permission, whether generated output can infringe, and who owns what the system produces. These questions are being settled now, through courts, legislatures and licensing deals, and the answers differ by country.

## Overview

Copyright protects original works of authorship, not ideas or facts. It grants the owner exclusive rights to copy, adapt and distribute a work, subject to exceptions. AI raises three separate questions:

1. **Training**: is copying works into a training set permitted, and under which exception?
2. **Output**: can a model reproduce protected material, and is a similar output an infringement?
3. **Authorship**: who, if anyone, owns a work generated mainly by a machine?

The three questions have different answers, and debates often mix them up. A model can be lawfully trained and still produce infringing output if it memorised specific works.

## Key concepts

- **Training data copying**: storing and processing works to fit model parameters. Whether this is a copy in the legal sense is contested.
- **Text and data mining (TDM)**: automated analysis of works. Many laws create exceptions for it, sometimes only for research or only where rights holders have not opted out.
- **Fair use and fair dealing**: flexible exceptions in US and UK-style law. Their application to AI training is being decided case by case.
- **Memorisation and replication**: a model reproducing a training work closely. This is the most direct route to infringing output.
- **Authorship**: copyright generally requires a human author. Works produced with AI assistance are judged by how much human creative control they show.

## How it works

Training copies works into a dataset, then a model adjusts its weights to predict the data. The model does not usually store files, but it can retain patterns that reproduce specific works, particularly when a work appears many times in the training set. Two outcomes matter for rights holders. A model may output close copies of training works, and it may produce a new work in the style or manner of an artist, which is generally not infringement on its own, although how far a style can be protected is unsettled.

Rights holders have responded in several ways: lawsuits, opt-out signals that tell crawlers not to use their content, and licensing deals with AI developers. Developers respond with dataset filtering, deduplication and output filters.

## Key methods

### Somepalli et al. (2022), data replication in diffusion models

- **Problem:** do image diffusion models copy their training images, or do they generalise?
- **Core idea:** generate images from prompts tied to training captions, then search the training set for close matches to the generated images, using similarity measures on image features.
- **Equation or algorithm:** retrieval of nearest training images for each generated image, followed by a similarity threshold and manual inspection of matches.
- **Results:** the abstract says that some diffusion models, including Stable Diffusion, can "blatantly copy" from their training data in specific cases, and that replication depends on factors such as training set size and duplication. It gives no overall replication rate.
- **Limitations:** the abstract does not quantify how often replication occurs, and it does not say how far the results extend beyond the datasets tested (including Oxford flowers, CelebA, ImageNet and LAION subsets).

### Carlini et al. (2023), extracting training data from diffusion models

- **Problem:** can an outside user extract training images from a trained diffusion model?
- **Core idea:** a generate-and-filter pipeline. Sample many images from the model, then filter out the candidates that look like copies of training images.
- **Equation or algorithm:** generation, then filtering on similarity to training examples, with candidates checked against the source data.
- **Results:** the abstract reports that the pipeline extracts "over a thousand training examples from state-of-the-art models". It does not give separate counts per model.
- **Limitations:** the abstract gives no counts per model and does not say how many generated images were examined, so extraction rates cannot be compared directly across settings.

Somepalli et al. report that duplication and training set size affect replication. This makes deduplication a practical safeguard, and also a privacy measure (see [Privacy and Data Protection](../privacy/index.md)).

## Law and regulation

- **EU**: Directive (EU) 2019/790 on copyright in the Digital Single Market, adopted 17 April 2019, contains text and data mining exceptions, including a general one that rights holders can opt out of. Whether an opt-out made in a machine-readable form covers AI training is a current question.
- **EU AI Act**: Regulation (EU) 2024/1689 requires providers of general-purpose AI models to have a copyright policy and to publish a summary of the training content. It applies on top of the copyright rules and does not settle them.
- **Elsewhere**: countries take different positions on training exceptions, and courts in several countries are deciding AI cases. Outcomes are changing quickly, so check current rulings before relying on any one position. For national approaches, see [Law, Policy & Governance](../governance/index.md).

## Connections

- Generative creative tools are where the output questions appear most directly (see [Creative AI](../../applications/creative/index.md)).
- Memorisation links copyright to privacy: the same mechanism that reproduces a copyrighted image can reproduce personal data (see [Privacy and Data Protection](../privacy/index.md)).
- The economic case for creators depends on how licensing and compensation develop (see [Economics & Work](../economics/index.md)).

## Applications

- **Licensed training data**: stock image libraries, music catalogues and publishers that license their archives to AI developers.
- **Collective licensing**: rights organisations that offer blanket licences for AI use of their members' works.
- **Provenance and attribution**: tools that record where a work came from, so that creators can be credited (see [Misinformation and Deepfakes](../misinformation/index.md) for provenance standards).

## Open questions

- Is copying a work into a training set a reproduction under copyright law, or is it an allowed analysis of the work?
- If a model memorises a work, who is liable: the developer, the deployer or the user who prompted it?
- Can an opt-out signal be respected in practice across the web and across jurisdictions?
- Should creators receive compensation for training use, and how should it be shared?

## References

### Seminal papers

- Somepalli, G., Singla, V., Goldblum, M., Geiping, J. & Goldstein, T. (2022). Diffusion art or digital forgery? Investigating data replication in diffusion models. arXiv:2212.03860. https://arxiv.org/abs/2212.03860 — Shows that some diffusion models copy training images in specific cases, and that replication depends on training set size and duplication.
- Carlini, N. et al. (2023). Extracting training data from diffusion models. arXiv:2301.13188. https://arxiv.org/abs/2301.13188 — Extracts over a thousand training examples from state-of-the-art image models with a generate-and-filter pipeline.
- Carlini, N. et al. (2021). Extracting training data from large language models. *USENIX Security Symposium*. https://arxiv.org/abs/2012.07805 — The text-model counterpart, showing that memorised training sequences can be extracted verbatim.

### Articles and documentation

- EUR-Lex. *Directive (EU) 2019/790 on copyright and related rights in the Digital Single Market*. https://eur-lex.europa.eu/eli/dir/2019/790/oj/eng — The official text of the EU copyright directive with its text and data mining exceptions.
- EUR-Lex. *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng — The official text of the AI Act, including the copyright-policy and training-summary duties for general-purpose models.
