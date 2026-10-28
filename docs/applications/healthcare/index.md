---
related:
- theory/models/computer-vision
- theory/models/llm
- applications/life-science
- applications/mental-health
- society/governance
aliases:
  - 醫療保健
  - 醫療
---

# Healthcare

## Landscape

| Area | Examples | Maturity |
|---|---|---|
| Medical imaging | Detection and triage in radiology (chest X-ray, CT, mammography), pathology slides, dermatology, ophthalmology (diabetic retinopathy) | Most mature; the majority of regulator-cleared AI devices |
| Clinical documentation | Ambient AI scribes that listen to visits and draft notes; summarising records | Rapidly deployed since 2023 |
| Clinical decision support | Sepsis and deterioration alerts, risk scores, drug-interaction checking, differential diagnosis with LLMs | Mixed evidence; several high-profile failures |
| Patient communication | Drafting replies to patient messages, triage chatbots, patient-education material | Growing |
| Operations | Scheduling, bed management, coding and billing, prior authorisation | Widespread, less visible |
| Signals and wearables | ECG arrhythmia detection, atrial fibrillation on smartwatches, continuous glucose monitoring | Mature in specific uses |
| Genomics and precision medicine | Variant interpretation, polygenic risk, cancer subtyping | See [Life Sciences](../life-science/index.md) |
| Surgery and robotics | Surgical video analysis, skill assessment, autonomous suturing research | Early |

## Landmark results

- **Diabetic retinopathy**: IDx-DR (2018) was the first FDA-authorised autonomous AI diagnostic system — it makes a screening decision without a clinician reading the image (Abràmoff et al., 2018)
- **Dermatology**: CNNs matched dermatologists on skin-lesion classification (Esteva et al., 2017)
- **Mammography**: in a large Swedish randomised trial (MASAI), AI-supported screen reading was compared with standard double reading for safety and screening accuracy (Lång et al., 2023)
- **Medical LLMs**: Med-PaLM reached passing-level scores on licensing-exam-style questions (Singhal et al., 2023); exam performance does not equal clinical safety

## Cautionary tales

- **Epic Sepsis Model**: external validation found it missed most sepsis cases and generated many alerts (Wong et al., 2021, *JAMA Internal Medicine*)
- **Shortcut learning**: COVID-19 chest X-ray models learned hospital-specific artefacts; reviews found almost none of hundreds of published models clinically usable (Roberts et al., 2021)
- **Bias**: a widely used algorithm used healthcare *costs* as a proxy for *need*, under-referring Black patients (Obermeyer et al., 2019, *Science*); pulse oximeters and some imaging models perform worse for darker skin
- **IBM Watson for Oncology**: high expectations, limited clinical adoption

## Methods and data

- Imaging: CNNs and ViTs, self-supervised pre-training on unlabelled scans, foundation models for pathology (e.g. UNI, Virchow, Prov-GigaPath) and radiology
- EHR: sequence models over visits, LLMs over clinical notes
- Multimodal: combining images, notes, labs and genomics
- Privacy-preserving training: [federated learning](../../theory/paradigms/federated/index.md)
- Datasets: MIMIC (ICU records), CheXpert and MIMIC-CXR, UK Biobank, The Cancer Genome Atlas, PhysioNet

## Evaluation that matters

1. **External validation** on other hospitals and populations
2. **Prospective and randomised trials**, not only retrospective AUC
3. **Calibration** and subgroup performance
4. **Clinical utility**: does it change decisions and outcomes?
5. **Human–AI teaming**: clinicians with AI vs clinicians alone vs AI alone — the combination doesn't always win
6. Reporting guidelines: TRIPOD+AI, CONSORT-AI, SPIRIT-AI, DECIDE-AI, CLAIM

## Regulation

- **US FDA**: Software as a Medical Device; predetermined change control plans let cleared models be updated
- **EU**: Medical Device Regulation plus the AI Act (most medical AI is "high-risk")
- Clinical responsibility generally remains with the clinician; liability for AI errors is unsettled

## Key methods

Three methods underlie most of the systems above. Each links to the page that explains it.

- [ResNet](../../theory/models/cnn/backbones-and-scaling/resnet/index.md): residual convolutional networks, a common backbone for medical image classifiers and detectors (He et al., 2016).
- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md): self-attention over token sequences (Vaswani et al., 2017). It underlies the clinical language models above and transformer-based vision encoders.
- [InstructGPT and RLHF](../../theory/models/llm/instructgpt-rlhf/index.md): instruction tuning on human preference feedback, which turns a pretrained language model into a dialogue assistant (Ouyang et al., 2022). Many chat-style assistants, including those for patient communication, are built on this recipe.

## References

### Seminal papers

- He, K. et al. (2016). Deep Residual Learning for Image Recognition. CVPR. https://doi.org/10.1109/CVPR.2016.90 — Residual connections that make very deep CNNs trainable.
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, built on multi-head self-attention.
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT, instruction tuning from human preference feedback.
- Esteva, A. et al. (2017). Dermatologist-level classification of skin cancer with deep neural networks. *Nature*. https://doi.org/10.1038/nature21056 — A CNN trained on dermatology images and compared with board-certified dermatologists.
- Abràmoff, M. D. et al. (2018). Pivotal trial of an autonomous AI-based diagnostic system for detection of diabetic retinopathy in primary care offices. *npj Digital Medicine*. https://doi.org/10.1038/s41746-018-0040-6 — Pivotal trial of IDx-DR, the autonomous screening system described above.
- Obermeyer, Z. et al. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*. https://doi.org/10.1126/science.aax2342 — Shows how using health costs as a proxy for need disadvantaged Black patients.
- Wong, A. et al. (2021). External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. *JAMA Internal Medicine*. https://doi.org/10.1001/jamainternmed.2021.2626 — External validation of the Epic Sepsis Model, which missed most sepsis cases.
- Roberts, M. et al. (2021). Common pitfalls and recommendations for using machine learning to detect and prognosticate for COVID-19 using chest radiographs and CT scans. *Nature Machine Intelligence*. https://doi.org/10.1038/s42256-021-00307-0 — Reviews published COVID-19 chest imaging models and lists common pitfalls and recommendations.
- Lång, K. et al. (2023). Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study. *The Lancet Oncology*. https://doi.org/10.1016/s1470-2045(23)00298-x — Randomised trial comparing AI-supported screen reading with standard double reading.
- Singhal, K. et al. (2023). Large language models encode clinical knowledge. *Nature*. https://doi.org/10.1038/s41586-023-06291-2 — Med-PaLM, evaluated on medical licensing-style questions.
- Liu, X. et al. (2020). Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension. *Nature Medicine*. https://doi.org/10.1038/s41591-020-1034-x — The CONSORT-AI reporting checklist for trials of AI interventions.

### Surveys and textbooks

- Rajpurkar, P. et al. (2022). AI in health and medicine. *Nature Medicine*. https://doi.org/10.1038/s41591-021-01614-0 — Reviews where AI works in clinical practice and what is still unproven.

## Further learning

- [MONAI](https://monai.io/) — Open-source framework for training and deploying medical imaging models.
