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

Full treatment of the attribution methods, with sanity checks and attribution for Transformers: [Feature attribution: SHAP, LIME and saliency](feature-attribution.md).

## Mechanistic interpretability

Full treatment, with the methods compared and the open questions: [Mechanistic interpretability and circuits](mechanistic-interpretability.md).

- **Circuits**: small subnetworks implementing identifiable algorithms — curve detectors in vision models, induction heads in Transformers, indirect-object identification circuits
- **Superposition**: networks represent more features than they have neurons by using overlapping directions (Elhage et al., 2022), making single neurons polysemantic
- **Sparse autoencoders (SAEs) and dictionary learning** extract millions of more interpretable features from LLM activations (Anthropic's "Scaling Monosemanticity", 2024; similar work at OpenAI and Google DeepMind's Gemma Scope). Full treatment: [Sparse autoencoders and feature dictionaries](sparse-autoencoders.md)
- **Attribution graphs / circuit tracing**: tracing how features interact to produce outputs, e.g. revealing multi-step reasoning and planning ahead in rhymes (Anthropic, 2025)
- **Causal interventions**: activation patching, causal tracing (locating factual recall, Meng et al., 2022), steering vectors
- **Probing**: linear classifiers that read information from activations — e.g. truthfulness directions, board state in Othello-GPT. Control tasks and representation analysis are covered in [Probing classifiers and representation analysis](probing.md)
- **Chain-of-thought faithfulness**: whether a model's stated reasoning reflects its actual computation — often only partially

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

## Resources

- Molnar, *Interpretable Machine Learning* (free online)
- [Transformer Circuits Thread](https://transformer-circuits.pub/)
- Neel Nanda's mechanistic interpretability guides; [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens)
- Bereska & Gavves (2024), "Mechanistic Interpretability for AI Safety — A Review"
- [Captum](https://captum.ai/), [SHAP](https://github.com/shap/shap)
