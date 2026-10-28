---
related:
- engineering/training
---

# Transfer Learning & Domain Adaptation

## Idea

Reuse knowledge learned on a **source** task or domain to do better on a **target** task or domain with less data. Today almost every applied model starts from a pre-trained network.

## Types

| Type | Source vs target | Example |
|---|---|---|
| Inductive transfer (fine-tuning) | Different task, labelled target data | ImageNet model → skin-lesion classifier |
| Transductive / domain adaptation | Same task, different input distribution, few or no target labels | Synthetic → real images; one hospital's scanner → another's |
| Multi-task learning | Several tasks learned jointly | Shared encoder for detection + segmentation |
| Cross-lingual transfer | Train in one language, use in another | Multilingual models answering in low-resource languages |
| Sim-to-real | Simulation → physical world | Robot locomotion trained in simulation |
| Zero-shot transfer | No target training at all | CLIP classifying new categories from text names |

## Fine-tuning strategies

| Strategy | What is trained | When |
|---|---|---|
| Linear probe | Only a new head | Very small data; diagnosing representation quality |
| Full fine-tuning | All weights | Enough data and compute |
| Gradual unfreezing / discriminative learning rates | Later layers first, smaller LR for early layers | ULMFiT-style |
| Parameter-efficient fine-tuning (PEFT) | Adapters, LoRA, prefix/prompt tuning | Large models, many tasks |
| Prompting / in-context learning | Nothing — task specified in the input | Foundation models |

See [Training & Fine-tuning](../../../engineering/training/index.md).

## Domain shift taxonomy

- **Covariate shift**: \(p(x)\) changes, \(p(y\mid x)\) stays.
- **Label (prior) shift**: \(p(y)\) changes (disease prevalence differs between clinics).
- **Concept shift**: \(p(y\mid x)\) changes (what counts as spam evolves).

Domain adaptation methods: importance re-weighting, feature alignment (MMD, CORAL), domain-adversarial training (DANN), self-training on the target, test-time adaptation, data augmentation and domain randomisation.

## Negative transfer

Transfer can hurt when source and target are too dissimilar. Check against a from-scratch baseline, especially in specialised domains (medical, satellite, scientific data), where domain-specific pre-training often beats generic ImageNet or web pre-training.

## Transfer in human cognition

- **Near vs far transfer**: learning transfers readily to similar problems but rarely to distant ones — a robust finding in educational psychology (e.g. brain-training games improve the trained tasks but show little far transfer; Simons et al., 2016).
- **Analogical reasoning** (Gentner's structure-mapping theory) is the cognitive mechanism of far transfer: mapping relational structure from a known domain to a new one.
- **Neural reuse**: brain regions are recycled for new cultural skills — the visual word form area for reading (Dehaene's "neuronal recycling") is a biological analogue of fine-tuning a pre-trained network.

## Subtopics

- [Fine-tuning and adaptation](fine-tuning-and-adaptation/index.md): linear probes, full fine-tuning and parameter-efficient methods such as LoRA.
- [Domain adaptation](domain-adaptation/index.md): aligning source and target features, adversarial and test-time methods.
- [Multi-task learning](multi-task-learning/index.md): shared representations, learned sharing and loss balancing.
- [Sim-to-real transfer](sim-to-real/index.md): domain and dynamics randomisation for robots trained in simulation.
- [Transfer theory](transfer-theory/index.md): divergence bounds on target error and negative transfer.

## Further reading

- Pan & Yang (2010), "A Survey on Transfer Learning"
- Howard & Ruder (2018), ULMFiT
- Ganin et al. (2016), "Domain-Adversarial Training of Neural Networks"
- Koh et al. (2021), WILDS benchmark of in-the-wild distribution shifts

## References

### Seminal papers

- Yosinski, Clune, Bengio & Lipson (2014), "How transferable are features in deep neural networks?", NeurIPS, arXiv:1411.1792 — Measures how generic and task-specific features transfer between tasks in each layer.
- Howard & Ruder (2018), "Universal language model fine-tuning for text classification", ACL, arXiv:1801.06146 — ULMFiT, a practical recipe for fine-tuning pre-trained language models.
- Ganin et al. (2016), "Domain-adversarial training of neural networks", JMLR, arXiv:1505.07818 — DANN, which learns domain-invariant features for adaptation.
- Tobin et al. (2017), "Domain randomization for transferring deep neural networks from simulation to the real world", IROS, arXiv:1703.06907 — Randomised simulation so that real-world data looks like one more sample.
- Ben-David, Blitzer, Crammer, Kulesza, Pereira & Vaughan (2010), "A theory of learning from different domains", Machine Learning. https://doi.org/10.1007/s10994-009-5152-4 — Bounds target error by source error plus a domain divergence.

### Surveys and textbooks

- Pan & Yang (2010), "A survey on transfer learning", IEEE Transactions on Knowledge and Data Engineering. https://www.cse.ust.hk/~qyang/Docs/2009/tkde_transfer_learning.pdf — Survey that defines transfer settings and the taxonomy used across the field.
- Weiss, Khoshgoftaar & Wang (2016), "A survey of transfer learning", Journal of Big Data. https://link.springer.com/10.1186/s40537-016-0043-6 — Survey with a discussion of when transfer fails.
