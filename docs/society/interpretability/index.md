---
related:
- theory/models/transformer
- brain-mind/neuroai
- brain-mind/computational-neuroscience
- society/safety-alignment
---

# Interpretability

Understanding *why* a model produces its outputs — for debugging, trust, science, regulation and safety.

## Two traditions

| | Explainable AI (XAI) | Mechanistic interpretability |
|---|---|---|
| Goal | Explain individual predictions to users and auditors | Reverse-engineer the algorithms learned inside networks |
| Methods | Feature attribution, surrogate models, counterfactuals | Circuits, features, causal interventions |
| Typical models | Tabular models, image classifiers | Transformers, LLMs |

## Explainable AI methods

| Method | Idea |
|---|---|
| Inherently interpretable models | Linear models, small trees, rule lists, GAMs (EBMs) — Rudin (2019) argues to prefer them for high-stakes decisions |
| Permutation importance | Drop in performance when a feature is shuffled |
| LIME | Fit a local linear surrogate around one prediction |
| SHAP | Shapley-value attributions with game-theoretic properties |
| Saliency / Grad-CAM / Integrated Gradients | Which pixels or tokens drove the output |
| Counterfactual explanations | Smallest change that would flip the decision |
| Concept-based (TCAV) | Sensitivity to human-defined concepts |

Caution: attribution maps can be unfaithful or fail sanity checks (Adebayo et al., 2018), and explanations can increase over-trust.

Two method pages go deeper: [Feature attribution: SHAP, LIME and saliency](feature-attribution.md) and [Probing classifiers and representation analysis](probing.md). Each named method has its own page: [Saliency maps](saliency-maps.md), [Integrated gradients](integrated-gradients.md), [LIME](lime.md), [SHAP](shap.md), [Linear probes](linear-probes.md), [Control tasks and selectivity](control-tasks.md) and [Representational similarity analysis](representational-similarity-analysis.md).

## Mechanistic interpretability

- **[Circuits](mechanistic-interpretability.md)**: small subnetworks implementing identifiable algorithms — curve detectors in vision models, induction heads in Transformers, indirect-object identification circuits
- **Superposition**: networks represent more features than they have neurons by using overlapping directions (Elhage et al., 2022), making single neurons polysemantic
- **[Sparse autoencoders (SAEs)](sparse-autoencoders.md) and dictionary learning** extract millions of more interpretable features from LLM activations (Anthropic's "Scaling Monosemanticity", 2024; similar work at OpenAI and Google DeepMind's Gemma Scope)
- **Attribution graphs / circuit tracing**: tracing how features interact to produce outputs, e.g. revealing multi-step reasoning and planning ahead in rhymes (Anthropic, 2025)
- **Causal interventions**: activation patching, causal tracing (locating factual recall, Meng et al., 2022), steering vectors
- **Probing**: linear classifiers that read information from activations — e.g. truthfulness directions, board state in Othello-GPT
- **Chain-of-thought faithfulness**: whether a model's stated reasoning reflects its actual computation — often only partially

## Detailed pages

- [Mechanistic interpretability and circuits](mechanistic-interpretability.md): circuits, induction heads, factual recall and superposition.
- [Sparse autoencoders and feature dictionaries](sparse-autoencoders.md): dictionary learning on activations, scaling and known failure modes.
- [k-sparse autoencoders](k-sparse-autoencoders.md): enforcing sparsity by keeping the k largest activations.
- [JumpReLU sparse autoencoders](jumprelu-sae.md): per-feature thresholds that improve reconstruction at a given sparsity.

## The neuroscience parallel

Interpretability researchers face the problems neuroscientists have faced for decades — but with perfect access to every "neuron":

| Neuroscience | Interpretability |
|---|---|
| Single-unit tuning curves | Neuron and feature visualisation |
| "Grandmother cells" and concept cells | Monosemantic features |
| Mixed selectivity in prefrontal cortex | Polysemantic neurons, superposition |
| Lesions and optogenetics | Ablations, activation patching |
| Population coding and neural manifolds | Linear representations, low-dimensional structure |
| Connectomics | Weights and attribution graphs |

"Could a neuroscientist understand a microprocessor?" (Jonas & Kording, 2017) showed standard neuroscience methods struggle even on a known chip — a cautionary tale for both fields. Methods now flow both ways: representational similarity analysis and dimensionality reduction from neuroscience; SAEs and causal patching back into neural data analysis.

## Uses

- Debugging spurious correlations and shortcuts
- Auditing for bias and regulatory explanation requirements (GDPR, credit regulations, EU AI Act)
- Detecting deception or hidden objectives (auditing games)
- Steering behaviour without retraining
- Scientific discovery: learning new concepts from superhuman models (e.g. chess concepts from AlphaZero, Schut et al., 2023)

## References

- Ribeiro, M. T., Singh, S. & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *Proceedings of KDD 2016*. https://arxiv.org/abs/1602.04938 — Introduces LIME, which explains one prediction by fitting a simple surrogate model around that input.
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017*. https://arxiv.org/abs/1705.07874 — SHAP: attributes a prediction to its input features using Shapley values from cooperative game theory.
- Bau, D. et al. (2017). Network Dissection: Quantifying Interpretability of Deep Visual Representations. *CVPR 2017*. https://arxiv.org/abs/1704.05796 — Measures how well individual hidden units align with human-labelled visual concepts.
- Olah, C. et al. (2020). Zoom In: An Introduction to Circuits. *Distill*. https://doi.org/10.23915/distill.00024.001 — Argues that features and the connections between them in a vision network can be studied as circuits.
- Elhage, N. et al. (2021). A Mathematical Framework for Transformer Circuits. *Transformer Circuits Thread*. https://transformer-circuits.pub/2021/framework/index.html — Frames attention and MLP components of small transformers as linear algebra on the residual stream.

## Further learning

- [Transformer Circuits Thread](https://transformer-circuits.pub/) — ongoing series of mechanistic interpretability papers.
- [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) — open-source library for inspecting transformer activations.
- [Captum](https://captum.ai/) and [SHAP](https://github.com/shap/shap) — open-source attribution libraries for PyTorch and general models.
