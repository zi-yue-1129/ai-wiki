---
references: not-required  # lists and meta pages cite through their entries
---

# Roadmap & Coverage

The goal of this wiki is **complete coverage of artificial intelligence**: how it works, how it relates to the brain and mind, and how every field uses it. This page tracks how far we are and what is still missing.

- **Coverage status** below is generated automatically from the pages themselves on every deploy.
- **Missing topics** is a hand-curated backlog. Anyone can propose a topic with a [topic request](https://github.com/zi-yue-1129/ai-wiki/issues/new?template=topic-request.yml); accepted requests are added here.

To pick something up, see [Contributing](../contributing/index.md).

## Coverage status

--8<-- "includes/status.md"

## Missing topics

Topics that do not have a page yet. Tick a box (in the same PR) when its page is merged. Rough priority: ★★★ core, ★★ important, ★ nice to have.

### Foundations

- [ ] ★★★ Optimization (gradient descent variants, convexity, loss landscapes)
- [ ] ★★★ Information theory for ML (entropy, KL divergence, mutual information)
- [ ] ★★ Statistical learning theory (bias–variance, VC dimension, generalization)
- [ ] ★★ Causal inference and causal ML
- [ ] ★★ Kernel methods and support vector machines
- [ ] ★★ Self-supervised and contrastive learning
- [ ] ★★ Continual, meta- and transfer learning
- [ ] ★ Federated and privacy-preserving learning

### Models & Techniques

- [ ] ★★★ Convolutional neural networks
- [ ] ★★★ Recurrent networks and LSTMs
- [ ] ★★★ Diffusion models
- [ ] ★★ Reasoning models and test-time compute
- [ ] ★★ Mixture of experts
- [ ] ★★ State-space models (S4, Mamba) and alternatives to attention
- [ ] ★★ Embeddings and representation learning
- [ ] ★★ Recommender systems
- [ ] ★★ Time-series forecasting
- [ ] ★ Small and efficient models (distillation, pruning)

### Brain & Mind

- [ ] ★★★ Perception and the visual system
- [ ] ★★★ Language in the brain
- [ ] ★★ Predictive coding and the free-energy principle
- [ ] ★★ Decision making, dopamine and reward
- [ ] ★★ Attention in brains and machines
- [ ] ★★ Emotion and affective computing
- [ ] ★★ Neuroimaging and recording methods (EEG, fMRI, electrophysiology)
- [ ] ★ Developmental cognition and how children learn
- [ ] ★ Animal cognition and comparative intelligence

### Applications

- [ ] ★★ Government and public services
- [ ] ★★ Retail, marketing and e-commerce
- [ ] ★★ Journalism and information ecosystems
- [ ] ★★ Accessibility and assistive technology
- [ ] ★★ Linguistics and machine translation
- [ ] ★ Military and defense
- [ ] ★ Space and astronomy
- [ ] ★ Architecture, construction and urban planning
- [ ] ★ Telecommunications

### Engineering

- [ ] ★★★ Inference optimization (quantization, batching, KV caching)
- [ ] ★★ Distributed training
- [ ] ★★ Vector databases and semantic search
- [ ] ★★ LLM application security (prompt injection, data leakage)
- [ ] ★★ Synthetic data
- [ ] ★ On-device and edge AI
- [ ] ★ AI coding assistants in practice

### AI & Society

- [ ] ★★★ Privacy and data protection
- [ ] ★★ Copyright and intellectual property
- [ ] ★★ Misinformation and deepfakes
- [ ] ★★ Environmental impact of AI
- [ ] ★★ Open versus closed models
- [ ] ★ AI in Taiwan: policy, industry and research
- [ ] ★ Children, education policy and AI

### Reference

- [ ] ★★ People and research labs
- [ ] ★★ Frequently asked questions
- [ ] ★ Timeline of models and releases

## How the wiki is maintained

| What | How | Where |
|---|---|---|
| New topics | Topic request issue → added to the backlog above → page written in a PR | [Issues](https://github.com/zi-yue-1129/ai-wiki/issues) |
| Corrections | Correction issue, or an edit PR via the ✏️ button on any page | [Issues](https://github.com/zi-yue-1129/ai-wiki/issues) |
| Build and internal links | `mkdocs build --strict` and `scripts/wiki_status.py --check` on every PR | GitHub Actions |
| External links | Weekly link check | Weekly health report issue |
| Stale pages | Pages not reviewed for 12 months are listed for review | Weekly health report issue |
| Translations | zh-TW pages older than their English page are flagged | Status above, weekly report |
