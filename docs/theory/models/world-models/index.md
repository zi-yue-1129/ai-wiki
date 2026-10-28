---
related:
- applications/robotics
- brain-mind/cognitive-science
- brain-mind/memory-learning
---

# World Models & Embodied AI

## What is a world model?

A **world model** is an agent's internal model of how its environment works — it predicts "if I do *a*, what happens next?". With one, an agent can plan in **imagination** instead of by trial and error in the real world.

The idea comes from psychology: Craik (1943) proposed the mind builds "small-scale models" of external reality; Tolman (1948) showed rats form **cognitive maps** of mazes.

## Technical routes

| Route | Examples | Notes |
|---|---|---|
| Latent dynamics models | World Models (Ha & Schmidhuber, 2018), Dreamer series, MuZero | Predict the future in a compressed latent space for RL planning; DreamerV3 collected diamonds in Minecraft from scratch |
| Video generation as world simulation | Sora, Genie series, Cosmos, etc. | Generate interactive or physically plausible video worlds |
| JEPA | I-JEPA, V-JEPA series | LeCun's proposal: predict in representation space, not pixels |
| Driving world models | GAIA and others | Generate driving scenarios for training and testing |
| LLMs as implicit world models | Othello-GPT | A model trained only on move sequences developed an internal board-state representation (Li et al., 2023) |

## Key methods and sub-topics

Each method has its own page with the detail. This overview only compares them.

| Page | What separates it |
|---|---|
| [Action controllability](action-controllability.md) | Why models can ignore the action input, the shortcuts behind it, and the remedies |
| [Dreamer](dreamer.md) | Reinforcement learning by imagining trajectories inside a latent model, from DreamerV1 to DreamerV3 |
| [DINO-WM](dino-wm.md) | A predictor on frozen DINOv2 patch features, used for zero-shot planning |
| [V-JEPA 2](v-jepa-2.md) | Video pre-training in representation space, then action post-training on robot video |
| [Genie](genie.md) | A generative world that the user controls through latent actions learned without labels |
| [LAPO](lapo.md) | Latent actions learned from action-free video, with a quantised bottleneck against copying |

## Embodied AI

Intelligence arises not only in a brain but in **the interaction of body and environment**.

### Moravec's paradox
What is hard for humans (chess, arithmetic) is easy for computers; what is easy for humans (walking, picking up a cup) is very hard for computers — because sensorimotor skills were optimised by hundreds of millions of years of evolution.

### Robot foundation models

| Type | Examples |
|---|---|
| Vision-language-action models | RT-2, OpenVLA, π0 / π0.5 (Physical Intelligence), Gemini Robotics, GR00T (NVIDIA) |
| Large robot datasets | Open X-Embodiment (dozens of labs, many robot types), DROID |
| [Imitation learning](../../paradigms/imitation/index.md) | ALOHA, Diffusion Policy, Action Chunking Transformer |
| Simulation | Isaac Sim/Lab, MuJoCo, Habitat, Genesis |

See [Robotics](../../../applications/robotics/index.md).

## Neuroscience and cognitive-science foundations

- **The predictive brain**: the cerebellum is thought to contain **forward models** predicting the sensory consequences of movement (Wolpert and others) — which is why you cannot tickle yourself
- **Cognitive maps**: hippocampal **place cells** (O'Keefe, 1971) and entorhinal **grid cells** (the Mosers, 2005) — Nobel Prize 2014. The hippocampal–entorhinal system may map abstract conceptual spaces as well as physical space (Behrens et al., 2018)
- **Mental simulation**: patients with hippocampal damage struggle to imagine new scenarios (Hassabis et al., 2007)
- **Embodied cognition**: understanding depends on sensorimotor systems (Barsalou's perceptual symbol systems; Lakoff's conceptual metaphor)
- **Active inference**: agents act to make sensory input match predictions (Friston) — see [Cognitive Science](../../../brain-mind/cognitive-science/index.md)
- **Developmental psychology**: infants build intuitive physics and object permanence by acting on objects (Spelke's core knowledge)

## Open questions

- Do video models learn physics, or surface statistics?
- How can world models support long-horizon, compositional planning?
- Robot data are tiny compared with web text — how to scale?
- Is embodiment necessary for "understanding"?

## Resources

- Ha & Schmidhuber, "World Models" interactive paper ([worldmodels.github.io](https://worldmodels.github.io/))
- LeCun (2022), "A Path Towards Autonomous Machine Intelligence"
- Hafner et al., DreamerV3
- Pfeifer & Bongard, *How the Body Shapes the Way We Think*
