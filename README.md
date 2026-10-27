# AI Wiki

An open, comprehensive wiki of artificial intelligence: foundations, models, brain and cognitive science, applications across fields, engineering practice, and AI & society. Available in English and Traditional Chinese (繁體中文).

**Website:** https://zi-yue-1129.github.io/ai-wiki/

## Structure

```
docs/
  start/         Learning paths, open-source resource survey, history
  foundations/   Math, ML, deep learning, RL, probabilistic, symbolic, evolutionary
  models/        Transformers, LLMs, generative, vision, NLP, speech, multimodal, GNN, agents, world models
  brain-mind/    Neuroscience, computational neuroscience, NeuroAI, SNNs, memory, cognitive science, psychology, consciousness, BCI
  applications/  AI in healthcare, science, education, finance, law, robotics, and more
  engineering/   Frameworks, data, training, prompting, RAG, evaluation, MLOps, hardware
  society/       Safety, interpretability, ethics, governance, economics, philosophy
  reference/     Glossary, papers, courses, datasets, contributing
```

Each page `topic.md` is English; `topic.zh-TW.md` is its Traditional Chinese version. Pages without a translation fall back to English.

## Local preview

```bash
pip install -r requirements.txt
mkdocs serve
```

Every push to `main` builds the site with `mkdocs build --strict` and deploys it to GitHub Pages via `.github/workflows/deploy.yml`. Pull requests are built (to catch broken links) but not deployed.

## Contributing

See [docs/reference/contributing.md](docs/reference/contributing.md).

## License

Text: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Code snippets: MIT.
