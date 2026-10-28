---
related:
- society/safety-alignment
- theory/models/agents
- applications/software
- applications/finance
---

# Cybersecurity

AI cuts both ways in security: it strengthens defence, empowers attackers, and creates a new attack surface of its own.

## AI for defence

| Area | Examples |
|---|---|
| Threat detection | Anomaly detection on network and endpoint telemetry, malware classification, phishing detection |
| Security operations (SOC) | LLM copilots that summarise alerts, write queries, triage incidents |
| Vulnerability discovery | ML-guided fuzzing; LLM agents finding real bugs (Google's Big Sleep found an exploitable SQLite bug in 2024); DARPA's AI Cyber Challenge (2025) systems found and patched vulnerabilities automatically |
| Code security | Static analysis with ML, automatic patch generation |
| Identity and fraud | Behavioural biometrics, account-takeover detection |
| Threat intelligence | Extracting indicators from reports, clustering campaigns |

## AI-enabled attacks

- **Phishing and social engineering** at scale, personalised and fluent in any language
- **Voice and video deepfakes** for fraud (e.g. a 2024 Hong Kong case where a deepfaked video call led to a ~US$25 million transfer)
- **Malware development assistance** and faster exploit development
- **Agentic offensive operations**: AI developers have reported disrupting state-linked actors using AI models to assist and partially automate intrusion campaigns (2025)
- **Password guessing** and CAPTCHA solving

## Securing AI systems

| Threat | Description | Defences |
|---|---|---|
| Prompt injection | Instructions hidden in web pages, emails or documents hijack an LLM agent | Privilege separation, treating external content as data, human confirmation for sensitive actions, monitoring |
| Jailbreaks | Prompts that bypass safety training | Adversarial training, classifiers, layered safeguards |
| Data poisoning | Malicious training data plants backdoors; small numbers of poisoned documents can suffice | Data provenance, filtering, anomaly detection |
| Model extraction | Stealing a model via queries | Rate limits, watermarking |
| Training-data extraction | Recovering memorised private data | Deduplication, differential privacy |
| Adversarial examples | Perturbations that fool classifiers | Adversarial training, certified robustness |
| Supply chain | Malicious model files (pickle), compromised packages, poisoned plugins/MCP servers | Safe formats (safetensors), signing, sandboxing |

Frameworks: [OWASP Top 10 for LLM Applications](https://genai.owasp.org/), [MITRE ATLAS](https://atlas.mitre.org/), NIST AI 100-2 (adversarial ML taxonomy).

## Resources

- [OWASP GenAI Security Project](https://genai.owasp.org/)
- Greshake et al. (2023), "Not what you've signed up for: indirect prompt injection"
- Carlini et al., work on adversarial examples and data extraction
- UK AISI and US CAISI cyber-capability evaluations of frontier models
