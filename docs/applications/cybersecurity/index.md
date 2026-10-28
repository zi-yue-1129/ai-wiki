---
related:
- society/safety-alignment
- theory/models/agents
- applications/software
- applications/finance
aliases:
  - 資訊安全
  - 網路安全
---

# Cybersecurity

AI cuts both ways in security: it strengthens defence, empowers attackers, and creates a new attack surface of its own.

## AI for defence

| Area | Examples |
|---|---|
| Threat detection | Anomaly detection on network and endpoint telemetry, malware classification, phishing detection |
| Security operations (SOC) | LLM copilots that summarise alerts, write queries, triage incidents |
| Vulnerability discovery | ML-guided fuzzing; LLM agents that search code for real bugs |
| Code security | Static analysis with ML, automatic patch generation |
| Identity and fraud | Behavioural biometrics, account-takeover detection |
| Threat intelligence | Extracting indicators from reports, clustering campaigns |

## AI-enabled attacks

- **Phishing and social engineering** at scale, personalised and fluent in any language
- **Voice and video deepfakes** for fraud, including impersonation during video calls
- **Malware development assistance** and faster exploit development
- **Password guessing** and CAPTCHA solving

## Securing AI systems

| Threat | Description | Defences |
|---|---|---|
| Prompt injection | Instructions hidden in web pages, emails or documents hijack an LLM agent (Greshake et al., 2023) | Privilege separation, treating external content as data, human confirmation for sensitive actions, monitoring |
| Jailbreaks | Prompts that bypass safety training | Adversarial training, classifiers, layered safeguards |
| Data poisoning | Malicious training data can plant backdoors (Carlini & Terzis, 2021) | Data provenance, filtering, anomaly detection |
| Model extraction | Stealing a model via queries | Rate limits, watermarking |
| Training-data extraction | Recovering memorised private data (Carlini et al., 2020) | Deduplication, differential privacy |
| Adversarial examples | Perturbations that fool classifiers (Szegedy et al., 2013; Goodfellow et al., 2014) | Adversarial training, certified robustness |
| Supply chain | Malicious model files (pickle), compromised packages, poisoned plugins/MCP servers | Safe formats (safetensors), signing, sandboxing |

Frameworks: [OWASP Top 10 for LLM Applications](https://genai.owasp.org/), [MITRE ATLAS](https://atlas.mitre.org/), NIST AI 100-2 (adversarial ML taxonomy).

## Key methods

Three methods cover most of the defensive and attack-surface points above. Each links to the page that explains it.

- [Anomaly detection](../../theory/paradigms/unsupervised/anomaly-detection/index.md): models of normal telemetry that flag deviations, used for intrusion and fraud detection.
- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md): the architecture behind LLM copilots that summarise alerts and write queries (Vaswani et al., 2017).
- [Agents](../../theory/models/agents/index.md): LLM agents that call tools, whose exposure to prompt injection is the central security concern (Greshake et al., 2023).

## References

### Seminal papers

- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, built on multi-head self-attention.
- Greshake et al. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. arXiv. https://arxiv.org/abs/2302.12173 — Shows how instructions hidden in retrieved content can hijack LLM-integrated applications.
- Carlini et al. (2020). Extracting Training Data from Large Language Models. arXiv. https://arxiv.org/abs/2012.07805 — Shows that language models can reproduce memorised training text.
- Szegedy et al. (2013). Intriguing properties of neural networks. arXiv. https://arxiv.org/abs/1312.6199 — Introduces adversarial examples, where small input changes fool neural networks.
- Goodfellow, Shlens & Szegedy (2014). Explaining and Harnessing Adversarial Examples. arXiv. https://arxiv.org/abs/1412.6572 — Explains adversarial vulnerability and introduces the fast gradient sign attack.
- Carlini & Terzis (2021). Poisoning and Backdooring Contrastive Learning. arXiv. https://arxiv.org/abs/2106.09667 — Shows how poisoned training data can backdoor contrastive learning models.
- Vassilev et al. (2025). Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations. NIST AI 100-2e2025. https://doi.org/10.6028/nist.ai.100-2e2025 — NIST taxonomy of attacks on machine learning and their mitigations.
