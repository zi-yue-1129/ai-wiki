---
related:
- theory/paradigms/semi-supervised
- theory/paradigms/active
- society/ethics
- engineering/evaluation
tags:
- engineering
- data
aliases:
- 資料工程
---

# Data

"Data-centric AI": for most real projects, better data beats a better model.

## Lifecycle

```mermaid
flowchart LR
  C[Collect] --> L[Label / annotate] --> CL[Clean & deduplicate] --> S[Split] --> V[Version & document] --> M[Monitor in production]
  M --> C
```

## Collection

- First-party logs, sensors, records; public datasets; web crawling (respect robots.txt and terms); licensed data; simulation
- Sampling must match the deployment population — think about who is missing
- Consent, privacy and copyright from the start (GDPR, local privacy laws)

## Labelling

| Approach | Notes |
|---|---|
| Expert annotation | Gold standard in medicine, law, science; expensive |
| Crowdsourcing | Scale; needs quality control (redundancy, gold questions, agreement metrics) |
| Weak / programmatic supervision | Labelling functions and a label model; see [Data Programming and Weak Supervision](data-programming.md) |
| Active learning | Label only informative samples ([Active Learning](../../theory/paradigms/active/index.md)) |
| Model-assisted / LLM labelling | Fast; validate against human labels and watch for systematic bias |
| Preference data | Pairwise comparisons for RLHF/DPO |

Write **annotation guidelines** with examples and edge cases; measure inter-annotator agreement (Cohen's / Fleiss' κ, Krippendorff's α).

## Cleaning and quality

- Deduplication (exact and near-duplicate) — critical for LLM pre-training and for avoiding test leakage; see [MinHash Deduplication](minhash-deduplication.md)
- Label-error detection (confident learning / cleanlab); see [Confident Learning](confident-learning.md)
- Outlier and corruption checks, schema validation (Great Expectations, pandera)
- For web text: language ID, quality classifiers, toxicity and PII filtering (e.g. FineWeb, DCLM pipelines)

## Key methods

Each named method has its own page, which covers the problem it solves, the core idea, the algorithm, the reported results and its limitations. The table compares the three methods on this page.

| Method | Problem it solves | Core idea | Main trade-off | Page |
|---|---|---|---|---|
| MinHash deduplication | Near-copies of documents repeat training text | Compact signatures estimate Jaccard similarity; LSH finds candidate pairs | Threshold choice; misses paraphrases | [MinHash Deduplication](minhash-deduplication.md) |
| Confident learning | Label errors in human-labelled sets | Out-of-sample probabilities and the confident joint select likely errors to prune | Needs cross-validated predictions | [Confident Learning](confident-learning.md) |
| Data programming | Labels are expensive, but weak signals are cheap | Labelling functions are combined by a generative label model without ground truth | Quality depends on the functions written | [Data Programming and Weak Supervision](data-programming.md) |

## Splitting without leakage

- Split by **entity** (patient, user, device), by **time**, or by **site** when generalisation across them matters
- Deduplicate across splits
- Keep a locked final test set

## Synthetic data

- Uses: augmentation, rare events, privacy, instruction tuning, reasoning traces, simulation for robotics and driving
- Risks: amplifying model biases; **model collapse** when models are trained recursively on their own outputs without fresh real data (Shumailov et al., 2024, *Nature*); verification needed (e.g. execute generated code, check math answers)

## Documentation and governance

- **Datasheets for Datasets** (Gebru et al.) and **Data Cards**; **Model Cards** for models
- Data versioning: DVC, lakeFS, Hugging Face dataset revisions
- Lineage and access control; retention policies
- Licences and provenance: the Data Provenance Initiative audit reports frequent miscategorisation of dataset licences on widely used hosting sites

## Scale reference points

| Domain | Typical scale |
|---|---|
| ImageNet-1k | 1.28 million labelled images |
| LAION-5B | 5.85 billion image–text pairs; taken offline in 2023 after a study reported links to illegal material, and a cleaned version, Re-LAION-5B, was released in 2024 |
| Open pre-training corpora | Trillions of tokens (Dolma: three trillion) |
| Instruction tuning | Thousands of examples can be enough: LIMA reports strong results from about 1,000 curated examples, so quality matters more than quantity |

## References

### Seminal papers

- Gebru, T. et al. (2018). *Datasheets for Datasets*. arXiv:1803.09010. https://arxiv.org/abs/1803.09010 — Proposes a standard datasheet that documents a dataset's motivation, composition, collection and intended uses.
- Northcutt, C. G., Jiang, L. & Chuang, I. L. (2021). *Confident Learning: Estimating Uncertainty in Dataset Labels*. arXiv:1911.00068. https://arxiv.org/abs/1911.00068 — Estimates and prunes label errors from out-of-sample predicted probabilities.

### Related work

- Northcutt, C. G., Athalye, A. & Mueller, J. (2021). *Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks*. NeurIPS 2021 Datasets and Benchmarks Track. arXiv:2103.14749. https://arxiv.org/abs/2103.14749 — Finds label errors in widely used benchmark test sets and shows that they change model rankings.
- Penedo, G. et al. (2024). *The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale*. arXiv:2406.17557. https://arxiv.org/abs/2406.17557 — A large web-text corpus and the filtering pipeline that produces it.
- Zhou, C. et al. (2023). *LIMA: Less Is More for Alignment*. arXiv:2305.11206. https://arxiv.org/abs/2305.11206 — Shows that a small set of carefully curated instruction examples can give strong instruction-following results.
- Longpre, S. et al. (2023). *The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing & Attribution in AI*. arXiv:2310.16787. https://arxiv.org/abs/2310.16787 — An audit of licences and attribution for widely used AI training datasets.
- Shumailov, I. et al. (2024). *AI models collapse when trained on recursively generated data*. *Nature* 631, 755–759. https://doi.org/10.1038/s41586-024-07566-y — Shows that recursive training on model-generated data loses the tails of the original distribution.

Further reading: [Data-Centric AI resources (MIT course)](https://dcai.csail.mit.edu/).
