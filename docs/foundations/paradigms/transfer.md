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

See [Training & Fine-tuning](../../engineering/training.md).

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

## Further reading

- Pan & Yang (2010), "A Survey on Transfer Learning"
- Howard & Ruder (2018), ULMFiT
- Ganin et al. (2016), "Domain-Adversarial Training of Neural Networks"
- Koh et al. (2021), WILDS benchmark of in-the-wild distribution shifts
