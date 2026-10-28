# Applications

How AI is used across fields — what works today, what is emerging, and what goes wrong.

Each page follows the same structure: **landscape** (main use cases), **landmark systems**, **data and methods**, **risks and limits**, and **resources**.

| Field | Highlights |
|---|---|
| [Healthcare](healthcare/index.md) | Medical imaging, clinical decision support, ambient scribes, regulatory approvals |
| [Life Sciences & Drug Discovery](life-science/index.md) | AlphaFold, protein design, genomics, single-cell, drug discovery pipelines |
| [Scientific Discovery](science/index.md) | Weather, materials, math, physics, self-driving labs, AI scientists |
| [Mental Health](mental-health/index.md) | Computational psychiatry, digital phenotyping, chatbot therapy evidence and risks |
| [Education](education/index.md) | Intelligent tutoring, LLM tutors, assessment, academic integrity |
| [Finance](finance/index.md) | Fraud, credit, trading, risk, compliance |
| [Law](law/index.md) | Legal research, contract review, hallucinated citations, AI in courts |
| [Robotics](robotics/index.md) | Manipulation, locomotion, humanoids, robot foundation models |
| [Autonomous Driving & Transport](autonomous-driving/index.md) | Robotaxis, driver assistance, logistics, traffic |
| [Manufacturing & Industry](manufacturing/index.md) | Visual inspection, predictive maintenance, process optimisation, chip design |
| [Agriculture & Food](agriculture/index.md) | Precision farming, crop monitoring, breeding, food systems |
| [Climate & Energy](climate-energy/index.md) | Forecasting, grids, emissions monitoring, AI's own footprint |
| [Art, Media & Creativity](creative/index.md) | Image, video, music and writing tools; copyright |
| [Games](games/index.md) | Game-playing AI, game development, AI-native games |
| [Cybersecurity](cybersecurity/index.md) | Detection, vulnerability discovery, AI-enabled attacks, securing AI |
| [Social Sciences & Humanities](social-science/index.md) | Computational social science, digital humanities, simulating societies |
| [Software Development](software/index.md) | Code assistants, coding agents, testing, productivity evidence |
| [Linguistics & Machine Translation](linguistics-translation/index.md) | Neural translation, low-resource languages, corpus linguistics, translator tools |

## Methods behind each field

Each field relies on a few shared methods. The right-hand column lists the pages to read before the field page.

| Field | Methods to read first |
|---|---|
| Healthcare | [Computer Vision](../theory/models/computer-vision/index.md), [Federated Learning](../theory/paradigms/federated/index.md), [Evaluation & Validation](../theory/paradigms/supervised/evaluation-and-validation/index.md) |
| Life Sciences & Drug Discovery | [Graph Neural Networks](../theory/models/gnn/index.md), [Generative Models](../theory/paradigms/unsupervised/density-and-generative-models/generative-models/index.md), [Active Learning](../theory/paradigms/active/index.md) |
| Scientific Discovery | [Graph Neural Networks](../theory/models/gnn/index.md), [Active Learning](../theory/paradigms/active/index.md), [Mathematics](../theory/math/index.md) |
| Mental Health | [Psychology & AI](../brain-mind/psychology/index.md), [Probabilistic & Bayesian Methods](../theory/paradigms/probabilistic/index.md) |
| Education | [Large Language Models](../theory/models/llm/index.md), [Evaluation & Benchmarks](../engineering/evaluation/index.md) |
| Finance | [Contextual Bandits](../theory/paradigms/online/contextual-bandits/index.md), [Streaming & Concept Drift](../theory/paradigms/online/streaming-and-concept-drift/index.md), [Probabilistic & Bayesian Methods](../theory/paradigms/probabilistic/index.md) |
| Law | [Retrieval-Augmented Generation](../engineering/rag/index.md), [Interpretability](../society/interpretability/index.md) |
| Robotics | [Imitation Learning](../theory/paradigms/imitation/index.md), [Reinforcement Learning](../theory/paradigms/reinforcement-learning/index.md), [World Models & Embodied AI](../theory/models/world-models/index.md), [Hand-eye coordination for grasping](robotics/hand-eye-grasping/index.md) |
| Autonomous Driving & Transport | [Sim-to-Real Transfer](../theory/paradigms/transfer/sim-to-real/index.md), [World Models & Embodied AI](../theory/models/world-models/index.md), [End-to-end steering from pixels](autonomous-driving/end-to-end-steering/index.md) |
| Manufacturing & Industry | [Computer Vision](../theory/models/computer-vision/index.md), [Anomaly Detection](../theory/paradigms/unsupervised/anomaly-detection/index.md) |
| Agriculture & Food | [Computer Vision](../theory/models/computer-vision/index.md), [Domain Adaptation](../theory/paradigms/transfer/domain-adaptation/index.md) |
| Climate & Energy | [Streaming & Concept Drift](../theory/paradigms/online/streaming-and-concept-drift/index.md), [Domain Adaptation](../theory/paradigms/transfer/domain-adaptation/index.md) |
| Art, Media & Creativity | [Generative Models](../theory/paradigms/unsupervised/density-and-generative-models/generative-models/index.md), [Multimodal Models](../theory/models/multimodal/index.md) |
| Games | [Reinforcement Learning](../theory/paradigms/reinforcement-learning/index.md), [Symbolic AI, Search & Planning](../theory/paradigms/symbolic-ai/index.md) |
| Cybersecurity | [Anomaly Detection](../theory/paradigms/unsupervised/anomaly-detection/index.md), [Safety & Alignment](../society/safety-alignment/index.md) |
| Social Sciences & Humanities | [Probabilistic & Bayesian Methods](../theory/paradigms/probabilistic/index.md), [Ethics & Fairness](../society/ethics/index.md) |
| Software Development | [Large Language Models](../theory/models/llm/index.md), [AI Agents](../theory/models/agents/index.md), [Evaluation & Benchmarks](../engineering/evaluation/index.md) |
| Linguistics & Machine Translation | [Natural Language Processing](../theory/models/nlp/index.md), [Transformer](../theory/models/transformer/index.md), [Attention in Brains & Machines](../brain-mind/attention-brain-machine/index.md) |

## Cross-cutting patterns

| Pattern | Seen in |
|---|---|
| **Perception at scale** (vision, speech, sensors) | Healthcare imaging, manufacturing inspection, agriculture, driving |
| **Prediction from structured data** | Finance, maintenance, energy, logistics |
| **Generative design** | Proteins, molecules, materials, chips, media |
| **Language interfaces to expertise** | Law, medicine, education, customer service, software |
| **Simulation and surrogate models** | Weather, physics, engineering, robotics |
| **Autonomous agents** | Software engineering, science, operations |

## Common failure modes

1. **Distribution shift**: a model validated in one hospital, country or season fails in another.
2. **Shortcut learning**: models use spurious cues (scanner type, watermark, zip code).
3. **Automation bias**: humans over-trust outputs.
4. **Evaluation on the wrong metric**: accuracy without calibration, retrospective without prospective trials.
5. **Workflow mismatch**: technically good tools that don't fit how people actually work.
6. **Accountability gaps**: unclear responsibility when AI-assisted decisions go wrong.

See [Evaluation & Benchmarks](../engineering/evaluation/index.md), [Ethics & Fairness](../society/ethics/index.md) and [Law, Policy & Governance](../society/governance/index.md).
