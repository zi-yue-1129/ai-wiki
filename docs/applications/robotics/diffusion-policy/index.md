---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
aliases:
  - Diffusion Policy
  - 擴散策略
---

# Diffusion Policy (Chi et al. 2023)

Chi and colleagues proposed generating robot behaviour with a denoising diffusion model. Instead of predicting one action from an observation, the policy turns noise into a sequence of actions, guided by what the robot sees. This page covers that paper; the parent topic is [Robotics](../index.md).

## Problem

Robot action prediction is hard for three reasons, which the paper lists as multimodal action distributions, sequential correlation, and the need for high precision (Sec. 1). A regression policy that predicts a single action averages over the demonstrated choices, and the average can be a poor action. Energy-based implicit policies handle multimodality, but they need negative sampling to estimate a normalisation constant, which makes training unstable (Sec. 1, Sec. 4.4, Fig. 6).

## Core idea

The paper models the visuomotor policy as a conditional denoising diffusion process over action sequences, p(A_t | O_t) (Sec. 2.3, Eqs. 4–5). Observations condition the denoiser but are not themselves denoised. Starting from Gaussian noise, the model repeatedly removes noise, and each step sees the current observations. The sampled action sequence stays close to one of the demonstrated modes rather than their average.

## Procedure

1. **Demonstrations:** collect demonstrations, pairing each observation window with the action sequence that follows it.
2. **Training:** train a noise-prediction network on the demonstrated action sequences, conditioned on the observations. The denoising procedure is the one from [diffusion models](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/index.md).
3. **Inference:** sample an action sequence from noise with the denoising steps, then execute only part of it. This is receding-horizon control: the policy predicts a sequence, runs its first actions, and predicts again.

Table 7 gives the CNN variant's horizons for most simulated tasks as an observation horizon of 2, a prediction horizon of 16 and an execution horizon of 8. The paper finds an execution horizon of 8 best for most tasks, which trades temporal consistency against responsiveness (Sec. 5.3, Fig. 5).

## Architectures

- **CNN:** a 1D temporal convolutional network with FiLM conditioning on the observation and denoising step (Sec. 3.1). The paper recommends starting here.
- **Transformer:** a minGPT-style decoder with causal attention, where observations enter through cross-attention (Sec. 3.1). It performs better when actions change quickly, but it is more sensitive to hyperparameters.
- **Vision encoder:** ResNet-18 without pretraining, with spatial softmax in place of global average pooling and GroupNorm in place of BatchNorm, trained end to end (Sec. 3.2).

## Results

The paper reports an average improvement of 46.9% over the baselines, computed with the best checkpoint per task (Sec. 5, App. B.2). The paper evaluates 15 tasks across simulation and the real world (Sec. 10). Selected visual-policy results from Table 2, against the best LSTM-GMM variant as the baseline:

| Task | LSTM-GMM | Diffusion Policy |
|---|---|---|
| Square (proficient human) | 0.82 | 0.98 |
| Transport (proficient human) | 0.88 | 1.00 |
| Transport (multi-human) | 0.44 | 0.89 |
| ToolHang (proficient human) | 0.68 | 0.95 |
| Push-T (proficient human) | 0.69 | 0.91 |

On the real robot (Sec. 6–7), Push-T reaches 0.95 success against 0.20 for the best LSTM-GMM variant. Mug flipping reaches 0.90 against 0.0, sauce pouring reaches an IoU of 0.74 against 0.06, and sauce spreading reaches 1.00 against 0.00. Three bimanual tasks (egg beater, mat unrolling and shirt folding) reach 55%, 75% and 75%, and they have no baselines.

The text of Sec. 5.3 gives a 213% improvement on Kitchen p4, but Table 4 gives 0.96 against 0.44 for BET, which is about 118%. The table figures are the ones to quote.

## Limitations

- **Compute and latency:** the paper states that Diffusion Policy "has higher computational costs and inference latency compared to simpler methods like LSTM-GMM" (Sec. 9). The denoising step count also differs between the text (Sec. 3.4) and the tables (Tables 7–8), so the latency figure should be checked against the appendix.
- **Demonstration data:** the policy inherits the limits of behaviour cloning, and performs poorly with inadequate demonstrations (Sec. 9).
- **Control rate:** predicting action sequences "may not suffice for tasks requiring high rate control" (Sec. 9).
- **Architecture choice:** the transformer is harder to tune (Sec. 3.1), and the CNN over-smooths fast velocity signals (Sec. 3.1). Frozen pretrained encoders performed poorly, and training a ViT from scratch was hard with limited data (Sec. 5.4).
- **Sensing:** force and tactile sensing are neither discussed nor tested.
- **Action space:** position control consistently outperforms the velocity-control variant (Sec. 4.2, Sec. 5.3). The authors attribute this to compounding error, which they present as a hypothesis.

## Connections

- The imitation-learning setting is covered in [Imitation Learning](../../../theory/paradigms/imitation/index.md).
- The method it builds on is [diffusion models](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/index.md).
- A transformer-based policy for similar bimanual tasks is [ALOHA and ACT](../aloha/index.md).

## References

### Seminal papers

- Chi, C. et al. (2023). Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. arXiv. https://arxiv.org/abs/2303.04137 — Models a visuomotor policy as conditional denoising diffusion over action sequences, with results on 15 tasks across simulation and the real world.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. arXiv. https://arxiv.org/abs/2006.11239 — The denoising diffusion probabilistic model whose training and sampling procedure the policy builds on.
- Zhao, T. Z. et al. (2023). Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. arXiv. https://arxiv.org/abs/2304.13705 — The ACT policy, a transformer-based competing approach for bimanual manipulation.

### Surveys and textbooks

- Hussein, A. et al. (2017). Imitation Learning: A Survey of Learning Methods. *ACM Computing Surveys* 50(2). https://doi.org/10.1145/3054912 — Survey of imitation learning methods, the setting that demonstration-based policies such as Diffusion Policy belong to.
- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — Survey of reinforcement learning applied to robots.
