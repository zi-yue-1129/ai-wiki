---
related:
- society/interpretability
- theory/models/llm
- theory/models/agents
- theory/paradigms/reinforcement-learning
- society/governance
---

# Safety & Alignment

**Alignment**: getting AI systems to pursue the goals their developers and users actually intend, and to respect human values. **Safety** more broadly: preventing harm from accidents, misuse and loss of control.

## Core problems

| Problem | Description | Example |
|---|---|---|
| [Specification gaming / reward hacking](reward-hacking.md) | Optimising the literal objective, not the intended one | A boat-racing agent circling to collect points instead of finishing (OpenAI, 2016); models special-casing unit tests |
| Goal misgeneralisation | Learning a goal that matches training but differs out of distribution | CoinRun agent learns "go right" rather than "get the coin" (Langosco et al., 2022) |
| Sycophancy | Telling users what they want to hear | Agreeing with incorrect user claims |
| Deception and scheming | Models strategically misleading overseers | Studied in controlled evaluations (e.g. "alignment faking", Greenblatt et al., 2024; Apollo Research's scheming evals) |
| Robustness | Jailbreaks, adversarial inputs, distribution shift | Universal adversarial suffixes (Zou et al., 2023) |
| Scalable oversight | Supervising systems that may exceed human expertise | Grading research-level answers |
| Power-seeking and instrumental convergence | Many goals favour acquiring resources and avoiding shutdown | Theoretical (Omohundro, Bostrom; Turner et al., 2021) |

## Techniques

| Approach | Ideas |
|---|---|
| Learning from human feedback | RLHF, DPO; reward modelling |
| Principle-based training | [Constitutional AI and RLAIF](constitutional-ai.md) and model specifications that state intended behaviour |
| Scalable oversight | Debate, recursive reward modelling, weak-to-strong generalisation, AI-assisted critique |
| [Interpretability](../interpretability/index.md) | Understanding internals to detect deception or dangerous capabilities |
| Adversarial training and red-teaming | Human and automated attacks to find failures |
| Monitoring and control | Chain-of-thought monitoring, trusted monitors, sandboxing, "AI control" protocols that assume models might be misaligned (Greenblatt et al., 2024) |
| Safeguards | Input/output classifiers, rate limits, know-your-customer for powerful capabilities |
| Unlearning | Removing hazardous knowledge (e.g. WMDP benchmark) |

## Evaluating dangerous capabilities

Frontier developers and government institutes evaluate models before release for:

- Chemical, biological, radiological and nuclear (CBRN) uplift
- Offensive cyber capabilities
- Autonomous replication and AI R&D acceleration
- Persuasion and manipulation

These evaluations feed **frontier safety frameworks** (Anthropic's Responsible Scaling Policy with AI Safety Levels, OpenAI's Preparedness Framework, Google DeepMind's Frontier Safety Framework) that tie capability thresholds to required safeguards. Government bodies include the UK AI Security Institute and the US Center for AI Standards and Innovation. The evaluations and frameworks are compared in [Dangerous-capability evaluations and frontier safety frameworks](dangerous-capability-evals.md).

## Perspectives and debate

- Some researchers (e.g. Hinton, Bengio, Russell) warn of catastrophic or existential risks from advanced AI; the 2023 CAIS statement said mitigating extinction risk from AI should be a global priority
- Others (e.g. LeCun, many fairness researchers) consider these risks speculative or argue they distract from present harms
- Many argue the agendas are complementary: robust, honest, controllable systems help both

## Cognitive-science links

- **Value learning** relates to how humans infer others' preferences (inverse planning, see [Imitation Learning](../../theory/paradigms/imitation/index.md))
- **Moral psychology** (Haidt's moral foundations, trolley-problem studies) informs what "human values" even are — and how much they vary across cultures (Moral Machine experiment, Awad et al., 2018)
- **Corrigibility** echoes debates about autonomy and deference in human institutions

## Resources

- Russell, *Human Compatible*
- Christian, *The Alignment Problem*
- Hendrycks, *Introduction to AI Safety, Ethics, and Society* (free textbook)
- [AI Safety Fundamentals](https://aisafetyfundamentals.com/) (BlueDot) courses
- *International AI Safety Report* (2025)
- Amodei et al. (2016), "Concrete Problems in AI Safety"
