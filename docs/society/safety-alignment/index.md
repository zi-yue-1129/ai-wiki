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
| [Deception and scheming](deceptive-alignment.md) | Models strategically misleading overseers | Studied in controlled evaluations (e.g. "alignment faking", Greenblatt et al., 2024; Apollo Research's scheming evals) |
| Robustness | Jailbreaks, adversarial inputs, distribution shift | Universal adversarial suffixes (Zou et al., 2023) |
| [Scalable oversight](scalable-oversight.md) | Supervising systems that may exceed human expertise | Grading research-level answers |
| Power-seeking and instrumental convergence | Many goals favour acquiring resources and avoiding shutdown | Theoretical (Omohundro, Bostrom; Turner et al., 2021) |

## Techniques

| Approach | Ideas |
|---|---|
| Learning from human feedback | RLHF, DPO; reward modelling |
| Principle-based training | [Constitutional AI](constitutional-ai.md) and [model specifications](model-specs.md) that state intended behaviour |
| [Scalable oversight](scalable-oversight.md) | Debate, recursive reward modelling, weak-to-strong generalisation, AI-assisted critique |
| [Interpretability](../interpretability/index.md) | Understanding internals to detect deception or dangerous capabilities |
| Adversarial training and red-teaming | Human and automated attacks to find failures |
| Monitoring and control | Chain-of-thought monitoring, trusted monitors, sandboxing, "AI control" protocols that assume models might be misaligned (Greenblatt et al., 2024) |
| Safeguards | Input/output classifiers, rate limits, know-your-customer for powerful capabilities |
| Unlearning | Removing hazardous knowledge (e.g. WMDP benchmark) |

## Evaluating dangerous capabilities

The detailed page is [dangerous-capability evaluations](dangerous-capability-evals.md).

Frontier developers and government institutes evaluate models before release for:

- Chemical, biological, radiological and nuclear (CBRN) uplift
- Offensive cyber capabilities
- Autonomous replication and AI R&D acceleration
- Persuasion and manipulation

These evaluations feed **frontier safety frameworks** (Anthropic's Responsible Scaling Policy with AI Safety Levels, OpenAI's Preparedness Framework, Google DeepMind's Frontier Safety Framework) that tie capability thresholds to required safeguards. Government bodies include the UK AI Security Institute and the US Center for AI Standards and Innovation.

## Detailed pages

- [Reward hacking and specification gaming](reward-hacking.md): optimising a proxy reward until it diverges from the goal.
- [Scalable oversight](scalable-oversight.md): debate, decomposition and weak-to-strong generalisation.
- [AI debate](debate.md): two debaters argue opposing answers while a judge decides, and the evidence from human-judge studies.
- [Debate cross-examination](debate-cross-examination.md): questioning saved copies of debaters to stop ambiguous claims from shifting.
- [Constitutional AI and RLAIF](constitutional-ai.md): principle-guided self-critique and AI preference labels.
- [RLAIF](rlaif.md): training a reward model on preference labels from a language model, compared with RLHF.
- [Model specifications](model-specs.md): written statements of intended behaviour, instruction hierarchies and auditing.
- [Deceptive alignment and sleeper agents](deceptive-alignment.md): the deceptive-alignment argument and the experimental evidence.
- [Sleeper agents](sleeper-agents.md): backdoors that survive standard safety training, and what the experiments do and do not show.
- [Dangerous-capability evaluations](dangerous-capability-evals.md): pre-deployment tests and frontier safety frameworks.

## Perspectives and debate

- Some researchers (e.g. Hinton, Bengio, Russell) warn of catastrophic or existential risks from advanced AI; the 2023 CAIS statement said mitigating extinction risk from AI should be a global priority
- Others (e.g. LeCun, many fairness researchers) consider these risks speculative or argue they distract from present harms
- Many argue the agendas are complementary: robust, honest, controllable systems help both

## Cognitive-science links

- **Value learning** relates to how humans infer others' preferences (inverse planning, see [Imitation Learning](../../theory/paradigms/imitation/index.md))
- **Moral psychology** (Haidt's moral foundations, trolley-problem studies) informs what "human values" even are — and how much they vary across cultures (Moral Machine experiment, Awad et al., 2018)
- **Corrigibility** echoes debates about autonomy and deference in human institutions

## References

- Amodei, D. et al. (2016). *Concrete Problems in AI Safety*. arXiv:1606.06565. https://arxiv.org/abs/1606.06565 — Lists practical accident risks for machine-learning systems, including side effects, reward hacking and unsafe exploration.
- Christiano, P. et al. (2017). Deep Reinforcement Learning from Human Preferences. *NeurIPS 2017*. https://arxiv.org/abs/1706.03741 — Learns a reward model from human pairwise comparisons, the basis of later RLHF methods.
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS 2022*. https://arxiv.org/abs/2203.02155 — Applies reward-model RLHF to make a language model follow user instructions more reliably.
- Hubinger, E. et al. (2019). *Risks from Learned Optimization in Advanced Machine Learning Systems*. arXiv:1906.01820. https://arxiv.org/abs/1906.01820 — Introduces mesa-optimisation, the risk that a learned system pursues objectives different from its training signal.
- Ngo, R., Chan, L. & Mindermann, S. (2022). *The Alignment Problem from a Deep Learning Perspective*. arXiv:2209.00626. https://arxiv.org/abs/2209.00626 — Argues that capable deep-learning systems may develop goals and situational awareness that make misalignment hard to detect.

## Further learning

- [AI Safety Fundamentals](https://aisafetyfundamentals.com/) (BlueDot) — introductory course with curated readings on alignment and safety.
