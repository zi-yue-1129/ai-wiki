# Applications

How AI is used across fields — what works today, what is emerging, and what goes wrong.

Each page follows the same structure: **landscape** (main use cases), **landmark systems**, **data and methods**, **risks and limits**, and **resources**.

| Field | Highlights |
|---|---|
| [Healthcare](healthcare/index.md) | Medical imaging, clinical decision support, ambient scribes, regulatory approvals |
| [Life Sciences & Drug Discovery](life-science/index.md) | AlphaFold, protein design, genomics, single-cell, drug discovery pipelines |
| [Scientific Discovery](science/index.md) | Weather, materials, math, physics, self-driving labs, AI scientists |
| [AI for AI Research](ai-research/index.md) | Automated literature review, AI scientists, benchmarks of research ability, self-improving agents, the recursive-improvement debate |
| [Mental Health](mental-health/index.md) | Computational psychiatry, digital phenotyping, chatbot therapy evidence and risks |
| [Education](education/index.md) | Intelligent tutoring, LLM tutors, assessment, academic integrity |
| [Finance](finance/index.md) | Fraud, credit, trading, risk, compliance |
| [Insurance & Actuarial Science](insurance/index.md) | Risk pricing, claims triage and fraud detection, telematics, fairness and regulatory scrutiny of pricing models |
| [Law](law/index.md) | Legal research, contract review, hallucinated citations, AI in courts |
| [Human Resources & Recruiting](hr-recruiting/index.md) | Résumé screening, skills matching, interview analysis, bias audits, NYC Local Law 144, EU AI Act high-risk duties |
| [Robotics](robotics/index.md) | Manipulation, locomotion, humanoids, robot foundation models |
| [Autonomous Driving & Transport](autonomous-driving/index.md) | Robotaxis, driver assistance, logistics, traffic |
| [Logistics & Supply Chain](logistics-supply-chain/index.md) | Demand forecasting, vehicle routing, warehouse robots, port operations, shortage prediction |
| [Manufacturing & Industry](manufacturing/index.md) | Visual inspection, predictive maintenance, process optimisation, chip design |
| [Agriculture & Food](agriculture/index.md) | Precision farming, crop monitoring, breeding, food systems |
| [Climate & Energy](climate-energy/index.md) | Forecasting, grids, emissions monitoring, AI's own footprint |
| [Weather Forecasting & Earth Observation](weather-and-earth-observation/index.md) | GraphCast and Pangu-Weather, ML versus numerical forecasts, satellite and remote-sensing models, disaster mapping |
| [Art, Media & Creativity](creative/index.md) | Image, video, music and writing tools; copyright |
| [Games](games/index.md) | Game-playing AI, game development, AI-native games |
| [Sports Analytics & Performance](sports/index.md) | Tracking data, pose estimation, expected goals, injury prediction, officiating technology, scouting and broadcast |
| [Cybersecurity](cybersecurity/index.md) | Detection, vulnerability discovery, AI-enabled attacks, securing AI |
| [Social Sciences & Humanities](social-science/index.md) | Computational social science, digital humanities, simulating societies |
| [Software Development](software/index.md) | Code assistants, coding agents, testing, productivity evidence |
| [Customer Service and Conversational Systems](customer-service/index.md) | Intent classifiers, task-oriented dialogue, LLM agents, deflection and escalation, labour effects |
| [Search & Information Retrieval](search-and-information-retrieval/index.md) | Learning to rank, neural web search, query understanding, answer engines, ads and recommendation ranking |
| [Mathematics & Formal Proof](mathematics/index.md) | Competition mathematics, Lean proofs, AlphaProof and AlphaGeometry, program search for new constructions, mathematicians' workflows |

## Methods behind each field

Each field relies on a few shared methods. The right-hand column lists the pages to read before the field page.

| Field | Methods to read first |
|---|---|
| Healthcare | [Computer Vision](../theory/models/computer-vision/index.md), [Federated Learning](../theory/paradigms/federated/index.md), [Evaluation & Validation](../theory/paradigms/supervised/evaluation-and-validation/index.md) |
| Life Sciences & Drug Discovery | [Graph Neural Networks](../theory/models/gnn/index.md), [Generative Models](../theory/generative/index.md), [Active Learning](../theory/paradigms/active/index.md) |
| Scientific Discovery | [Graph Neural Networks](../theory/models/gnn/index.md), [Active Learning](../theory/paradigms/active/index.md), [Mathematics](../theory/math/index.md) |
| AI for AI Research | [Large Language Models](../theory/models/llm/index.md), [AI Agents](../theory/models/agents/index.md), [Evaluation & Benchmarks](../engineering/evaluation/index.md) |
| Mental Health | [Psychology & AI](../brain-mind/psychology/index.md), [Probabilistic & Bayesian Methods](../theory/probabilistic/index.md) |
| Education | [Large Language Models](../theory/models/llm/index.md), [Evaluation & Benchmarks](../engineering/evaluation/index.md) |
| Finance | [Contextual Bandits](../theory/paradigms/online/contextual-bandits/index.md), [Streaming & Concept Drift](../theory/paradigms/online/streaming-and-concept-drift/index.md), [Probabilistic & Bayesian Methods](../theory/probabilistic/index.md) |
| Insurance & Actuarial Science | [Linear and Generalised Linear Models](../theory/paradigms/supervised/linear-models/index.md), [Trees and Ensembles](../theory/paradigms/supervised/trees-and-ensembles/index.md), [Graph Neural Networks](../theory/models/gnn/index.md) |
| Law | [Retrieval-Augmented Generation](../engineering/rag/index.md), [Interpretability](../society/interpretability/index.md) |
| Human Resources & Recruiting | [Large Language Models](../theory/models/llm/index.md), [Ethics & Fairness](../society/ethics/index.md), [Evaluation & Benchmarks](../engineering/evaluation/index.md) |
| Robotics | [Imitation Learning](../theory/paradigms/imitation/index.md), [Reinforcement Learning](../theory/paradigms/reinforcement-learning/index.md), [World Models & Embodied AI](../theory/models/world-models/index.md), [Hand-eye coordination for grasping](robotics/hand-eye-grasping/index.md) |
| Autonomous Driving & Transport | [Sim-to-Real Transfer](../theory/paradigms/transfer/sim-to-real/index.md), [World Models & Embodied AI](../theory/models/world-models/index.md), [End-to-end steering from pixels](autonomous-driving/end-to-end-steering/index.md) |
| Logistics & Supply Chain | [Reinforcement Learning](../theory/paradigms/reinforcement-learning/index.md), [Recurrent Networks](../theory/models/rnn/index.md), [Automated Planning](../theory/symbolic-ai/planning/index.md) |
| Manufacturing & Industry | [Computer Vision](../theory/models/computer-vision/index.md), [Anomaly Detection](../theory/paradigms/unsupervised/anomaly-detection/index.md) |
| Agriculture & Food | [Computer Vision](../theory/models/computer-vision/index.md), [Domain Adaptation](../theory/paradigms/transfer/domain-adaptation/index.md) |
| Climate & Energy | [Streaming & Concept Drift](../theory/paradigms/online/streaming-and-concept-drift/index.md), [Domain Adaptation](../theory/paradigms/transfer/domain-adaptation/index.md) |
| Weather Forecasting & Earth Observation | [Graph Neural Networks](../theory/models/gnn/index.md), [Computer Vision](../theory/models/computer-vision/index.md), [Masked prediction](../theory/paradigms/self-supervised/masked-prediction/index.md) |
| Art, Media & Creativity | [Generative Models](../theory/generative/index.md), [Multimodal Models](../theory/models/multimodal/index.md) |
| Games | [Reinforcement Learning](../theory/paradigms/reinforcement-learning/index.md), [Symbolic AI, Search & Planning](../theory/symbolic-ai/index.md) |
| Sports Analytics & Performance | [Computer Vision](../theory/models/computer-vision/index.md), [Probabilistic & Bayesian Methods](../theory/probabilistic/index.md), [Evaluation & Validation](../theory/paradigms/supervised/evaluation-and-validation/index.md) |
| Cybersecurity | [Anomaly Detection](../theory/paradigms/unsupervised/anomaly-detection/index.md), [Safety & Alignment](../society/safety-alignment/index.md) |
| Social Sciences & Humanities | [Probabilistic & Bayesian Methods](../theory/probabilistic/index.md), [Ethics & Fairness](../society/ethics/index.md) |
| Software Development | [Large Language Models](../theory/models/llm/index.md), [AI Agents](../theory/models/agents/index.md), [Evaluation & Benchmarks](../engineering/evaluation/index.md) |
| Customer Service and Conversational Systems | [Joint intent detection and slot filling](customer-service/joint-intent-slot-filling/index.md), [SimpleTOD](customer-service/simpletod/index.md), [AI Agents](../theory/models/agents/index.md) |
| Search & Information Retrieval | [Loss Functions, Regularisation and Optimisation](../theory/paradigms/supervised/loss-functions-and-optimization/index.md), [Vector Databases and Semantic Search](../engineering/vector-databases/index.md), [Contextual Bandits](../theory/paradigms/online/contextual-bandits/index.md) |
| Mathematics & Formal Proof | [Mathematics for AI](../theory/math/index.md), [Symbolic AI, Search & Planning](../theory/symbolic-ai/index.md), [Reasoning Models and Test-Time Compute](../theory/models/reasoning/index.md) |

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
