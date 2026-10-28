---
related:
- theory/models/computer-vision
- theory/models/llm
- applications/life-science
- applications/mental-health
- society/governance
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

- **Diabetic retinopathy**: IDx-DR (2018) was the first FDA-authorised autonomous AI diagnostic system — it makes a screening decision without a clinician reading the image
- **Dermatology**: CNNs matched dermatologists on skin-lesion classification (Esteva et al., 2017)
- **Mammography**: in a large Swedish randomised trial (MASAI), AI-supported screening detected more cancers while cutting radiologist workload by about 44% (Lång et al., 2023; 2025)
- **Medical LLMs**: Med-PaLM 2 and later general frontier models exceed passing scores on licensing-exam-style questions; exam performance does not equal clinical safety
- **Regulation volume**: the FDA's public list of AI-enabled medical devices exceeded 1,000 by 2025, roughly three-quarters in radiology

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

## Resources

- Topol, *Deep Medicine*
- Rajpurkar et al. (2022), "AI in health and medicine", *Nature Medicine*
- [FDA list of AI-enabled medical devices](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices)
- Stanford AIMI, MIT Clinical ML group publications
- [MONAI](https://monai.io/) (open medical-imaging framework)
