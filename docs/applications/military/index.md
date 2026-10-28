---
related:
- society/governance
- society/safety-alignment
- theory/models/computer-vision
- theory/paradigms/reinforcement-learning
aliases:
  - 軍事
  - 國防
  - Defence
---

# Military and Defence

AI is used in defence for intelligence analysis, logistics, planning, simulation and training, and increasingly for autonomy in platforms and weapons. Most of the public debate is about the last item, but the bulk of military AI spending goes to the first few.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Intelligence, surveillance and reconnaissance (ISR) | Computer vision and multi-sensor fusion over satellite, drone and radar imagery; anomaly detection on signals | Analysts face far more data than they can review; detection quality and false alarms drive value |
| Logistics and maintenance | Demand forecasting, predictive maintenance on vehicles and aircraft | Less visible, often the first large deployments |
| Planning and decision support | Optimisation, simulation, language models that summarise reports | Human review is the norm; the risk is over-trust |
| Training and simulation | Reinforcement learning in simulators, synthetic environments | Sim-to-real transfer is the main gap |
| Cyber defence | Intrusion detection, malware classification, automated response | Overlaps with [Cybersecurity](../cybersecurity/index.md) |
| Autonomous platforms | Navigation, target recognition and control for drones, ground vehicles and ships | The most contested area: see the policy section |

## Why defence is different

- **Adversaries adapt.** A system trained on yesterday's tactics can be defeated by a deliberate change in behaviour, which is a harder version of distribution shift.
- **Scarce data.** Real combat data is rare and classified, so systems are often trained on simulation or on data from other domains.
- **Consequences are severe and sometimes irreversible.** Errors in targeting or escalation carry a higher cost than errors in most other applications, which is why the evaluation standards matter so much.
- **Dual use.** Methods and models built for civilian purposes move quickly into military use, and the same techniques appear on both sides of a conflict.

## Autonomy and the law of armed conflict

The central policy question is how much human judgement must remain over the use of force. Two positions are widely cited:

- The **International Committee of the Red Cross (ICRC)** calls for expressly ruling out unpredictable autonomous weapon systems, whose effects cannot be sufficiently understood, predicted and explained, and for a prohibition on autonomous weapon systems designed or used to apply force against persons. Its position rests on International Humanitarian Law.
- The **United States** does not ban autonomous weapons. Its 2023 directive (DoD Directive 3000.09, effective 25 January 2023) requires that autonomous and semi-autonomous weapon systems be designed to allow "appropriate levels of human judgment over the use of force", and that autonomous weapon systems receive senior review both before formal development and again before fielding. Some systems are exempt from that review.

Civilian AI regulation often leaves military use out. The EU AI Act states that it does not apply to AI systems used exclusively for military, defence or national security purposes (Article 2(3)).

## Strategic competition

Governments see AI as a source of military advantage, and that competition drives investment. Horowitz (2018) argues that AI is a general-purpose, enabling technology. Its effect on military power depends less on the technology itself than on how militaries organise to adopt it, and spread through commercial research can narrow the gap between states. Races between states can reduce the time and care spent on testing, which is one reason arms-control proposals focus on verification and norms as well as on the technology itself.

## Key methods

Four method families carry most of the work. Each links to the page that explains it.

- [Computer vision](../../theory/models/computer-vision/index.md): detection and tracking in imagery; the basis of most ISR and target-recognition pipelines.
- [Reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md): learning control policies and planning in simulated environments, used for training and autonomy research.
- [Anomaly detection](../../theory/paradigms/unsupervised/anomaly-detection/index.md): flagging unusual activity in sensor and network data, used in cyber defence and surveillance triage.
- [Domain adaptation](../../theory/paradigms/transfer/domain-adaptation/index.md): transferring models from simulation or civilian data to operational conditions, where labelled military data is scarce.

## Connections

The civilian counterparts of these systems are described in [Autonomous Driving & Transport](../autonomous-driving/index.md) and [Cybersecurity](../cybersecurity/index.md). The governance and safety questions are treated in [Law, Policy & Governance](../../society/governance/index.md) and [Safety & Alignment](../../society/safety-alignment/index.md).

## Applications

- Automated analysis of satellite and drone imagery for mapping and damage assessment, a use that also appears in humanitarian work.
- Predictive maintenance of military vehicles and aircraft, where downtime has direct operational cost.
- Language models used to summarise reports and to search large document collections, with human review of the output.

## Open questions

- Can meaningful human control be defined in a way that can be checked in practice, not only in policy text?
- How should systems be tested when the adversary's behaviour is unknown and real data is scarce?
- Can international norms on autonomy be verified without revealing sensitive technical detail?
- Will the military exclusion in civilian AI law leave a gap in accountability?

## References

### Seminal papers

- Horowitz, M. C. (2018). Artificial Intelligence, International Competition, and the Balance of Power. *Texas National Security Review*, 1(3). https://tnsr.org/2018/05/artificial-intelligence-international-competition-and-the-balance-of-power/ — Argues that AI is an enabling technology whose effect on military power depends on how militaries adopt it, and considers how commercial research spreads it.

### Articles and documentation

- Boulanin, V. & Verbruggen, M. (2017). *Mapping the Development of Autonomy in Weapon Systems*. SIPRI. https://www.sipri.org/publications/2017/other-publications/mapping-development-autonomy-weapon-systems — An independent study of how autonomy is developing in weapon systems and the policy issues it raises.
- International Committee of the Red Cross (2021). *ICRC position on autonomous weapon systems*. https://www.icrc.org/en/document/icrc-position-autonomous-weapon-systems — The ICRC's position on the legal limits needed for autonomous weapons under International Humanitarian Law.
- U.S. Department of Defense (2023). *DoD Directive 3000.09, Autonomy in Weapon Systems*. https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodd/300009p.PDF — The current U.S. policy on human judgement over the use of force, and the senior review required before formal development and again before fielding.
- European Union (2024). *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*, Article 2(3). https://eur-lex.europa.eu/eli/reg/2024/1689/oj — The legal text that excludes AI systems used exclusively for military, defence or national security purposes.
