---
related:
- theory/paradigms/reinforcement-learning/index.md
- applications/robotics
tags:
  - imitation learning
  - DAgger
  - interactive learning
---

# Interactive Imitation Learning

Interactive imitation learning lets the learner query the expert during training. Instead of learning only from a fixed set of demonstrations, the learner runs its own policy, visits the states it actually reaches, and asks the expert what to do there. This fixes the main weakness of [behavioural cloning](../behavioural-cloning/index.md): the training data then matches the distribution the policy will face at test time.

## Overview

The core loop is the same in most methods. The learner rolls out its current policy, the expert labels or corrects the visited states, and the labelled data is added to a growing dataset on which the policy is retrained. Methods differ in who controls the rollout, how the expert intervenes and how the labels are used.

## DAgger

The method has its own page: [DAgger](dagger.md). Dataset Aggregation (DAgger) runs the learner's policy, records the states it visits, labels those states with the expert's actions and aggregates them with all earlier data. Ross, Gordon & Bagnell (2011) show that, for a no-regret online learner, the resulting policy has a performance bound that grows linearly with the horizon rather than quadratically, which is the gap that behavioural cloning leaves open.

Practical variants mix the expert and learner in rollouts, with the expert taking over with some probability that decays over iterations. The main cost is the need for an expert who can label arbitrary states on demand.

## Expert intervention and human-in-the-loop methods

When an expert can only intervene occasionally, the policy can be trained on the intervention data alone. HG-DAgger has a human take over when the policy looks unsafe and then hands control back, so that most labelled data comes from states near the policy's own behaviour (Kelly et al., 2019). Human-gated methods reduce the expert's workload while keeping the coverage benefits of DAgger.

## Noise injection and robustness

The method has its own page: [DART](dart.md). DART injects noise into the expert's own demonstrations so that the recorded data contains recovery behaviour from perturbed states, while the expert's actions remain near-optimal (Laskey et al., 2017). It gives robustness without an online expert, at the cost of extra demonstration effort.

## Learning from reward-based feedback

AggreVaTe and its differentiable successor Deeply AggreVaTeD use a cost-to-go oracle, which can be a learned or simulated critic, in place of direct action labels (Sun et al., 2017). This makes interactive learning possible when the expert gives scores or values rather than demonstrations.

## Connections

Interactive imitation sits between supervised learning and [reinforcement learning](../../reinforcement-learning/index.md). The learner's own rollouts provide the data, as in RL, while the expert's labels provide the supervision, as in [behavioural cloning](../behavioural-cloning/index.md). It is closely related to the [active learning](../../active/index.md) idea of choosing which examples to label.

## Applications

Robot manipulation with human teleoperators who take over during failures, autonomous driving with safety drivers who intervene, and deployment of learned policies that improve from human corrections over time.

## Open questions

Expert effort and the cost of interventions limit scale. Labelling by humans is noisy and inconsistent, and it is unclear how to weight corrections against original demonstrations. Guarantees often assume an expert who can be queried in any state, which is rarely true in practice.

## References

### Seminal papers

- Ross, Gordon & Bagnell (2011), "A reduction of imitation learning and structured prediction to no-regret online learning", AISTATS, [arXiv:1011.0686](https://arxiv.org/abs/1011.0686) — Introduces DAgger and proves its performance bound against behavioural cloning.
- Sun, Venkatraman, Gordon, Boots & Bagnell (2017), "Deeply AggreVaTeD: differentiable imitation learning for sequential prediction", ICML, [arXiv:1703.01030](https://arxiv.org/abs/1703.01030) — Uses a cost-to-go oracle for interactive learning with differentiable policies.
- Laskey, Lee, Fox, Dragan & Goldberg (2017), "DART: noise injection for robust imitation learning", CoRL, [arXiv:1703.09327](https://arxiv.org/abs/1703.09327) — Injects noise into demonstrations to gather recovery data without an online expert.
- Kelly, Sidrane, Driggs-Campbell & Kochenderfer (2019), "HG-DAgger: interactive imitation learning with human experts", ICRA, [arXiv:1810.02890](https://arxiv.org/abs/1810.02890) — A human-gated variant in which the expert takes over only when the policy looks unsafe.

### Surveys and textbooks

- Osa et al. (2018), "An algorithmic perspective on imitation learning", [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — Survey that places interactive methods alongside other imitation approaches.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Ross & Bagnell (2010), "Efficient reductions for imitation learning", AISTATS, https://proceedings.mlr.press/v9/ross10a.html — Earlier analysis of compounding errors that motivates interactive methods.
