# Imitation Learning

## Idea

Learn a behaviour by **watching an expert** instead of from a reward signal. Useful when good behaviour is easier to demonstrate than to specify as a reward — driving, surgery, folding laundry, writing a helpful answer.

## Approaches

| Approach | How it works | Strengths | Weaknesses |
|---|---|---|---|
| Behavioural cloning (BC) | Supervised learning from state → expert action | Simple, scalable | Compounding errors: small mistakes lead to unfamiliar states (covariate shift) |
| DAgger (Ross et al., 2011) | Run the learner, ask the expert to label the states it visits, aggregate | Fixes covariate shift with theoretical guarantees | Needs an interactive expert |
| Inverse reinforcement learning (IRL) | Infer the reward the expert is optimising, then do RL | Generalises beyond demonstrations; interpretable intent | Ill-posed (many rewards explain the same behaviour); expensive |
| Maximum-entropy IRL | Prefer the least-committed reward consistent with demonstrations | Handles sub-optimal, noisy experts | Still costly |
| Adversarial imitation (GAIL, AIRL) | A discriminator distinguishes expert from learner trajectories; the learner tries to fool it | No explicit reward engineering | GAN-style instability |
| Learning from observation | Imitate from video without action labels | Can use internet video | Must infer actions |
| Diffusion / transformer policies | Model multi-modal action distributions (Diffusion Policy, ACT) | Handles several valid ways to do a task | Data hungry |

### Why naïve behavioural cloning fails

If a policy makes an error with probability ε per step, errors compound so expected total mistakes over horizon T can grow like \(O(\varepsilon T^2)\), versus \(O(\varepsilon T)\) for DAgger-style training (Ross & Bagnell, 2010).

## Imitation learning everywhere

- **Robotics**: teleoperation datasets (ALOHA, Open X-Embodiment) and vision-language-action models are largely behavioural cloning at scale. See [Robotics](../../../applications/robotics/index.md).
- **Autonomous driving**: ALVINN (1989) was behavioural cloning; modern end-to-end planners learn from millions of human driving miles.
- **LLMs**: supervised fine-tuning on human-written answers is behavioural cloning of text; pre-training on human text is imitation of the internet. RLHF exists partly to go beyond imitation.
- **Games**: AlphaGo's first policy network imitated human expert moves; AlphaStar started from human replays.
- **Healthcare**: learning treatment policies from clinician records (with great caution — clinicians are not always optimal).

## Psychology and neuroscience

- **Observational learning**: Bandura's Bobo doll experiments (1961) showed children imitate aggressive models without reinforcement.
- **Over-imitation**: human children copy even causally irrelevant actions, unlike chimpanzees (Horner & Whiten, 2005) — thought to support cultural transmission.
- **Mirror neurons**: neurons in macaque premotor cortex fire both when performing and observing an action (Rizzolatti et al., 1996). Their role in imitation and understanding is debated; strong claims (e.g. explaining empathy or autism) are not well supported.
- **Cultural evolution**: imitation plus selective copying is how humans accumulate knowledge across generations — some argue LLMs are a new channel of cultural transmission.
- **Inverse planning**: humans infer others' goals from actions in a way well described by Bayesian inverse planning (Baker, Saxe & Tenenbaum, 2009) — the cognitive analogue of IRL and a basis of [theory of mind](../../../brain-mind/psychology/index.md).

## Further reading

- Osa et al. (2018), "An Algorithmic Perspective on Imitation Learning"
- Ross, Gordon & Bagnell (2011), DAgger
- Ho & Ermon (2016), GAIL
- Chi et al. (2023), Diffusion Policy
