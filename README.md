<div align="center">

# 🧠 AI Wiki

**An open, comprehensive wiki of artificial intelligence.**

Theory · Models · Brain & Cognition · Applications · Engineering · Society

[![Deploy site](https://github.com/zi-yue-1129/ai-wiki/actions/workflows/deploy.yml/badge.svg)](https://github.com/zi-yue-1129/ai-wiki/actions/workflows/deploy.yml)
[![Maintenance](https://github.com/zi-yue-1129/ai-wiki/actions/workflows/maintenance.yml/badge.svg)](https://github.com/zi-yue-1129/ai-wiki/actions/workflows/maintenance.yml)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/license-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Last commit](https://img.shields.io/github/last-commit/zi-yue-1129/ai-wiki)](https://github.com/zi-yue-1129/ai-wiki/commits)
[![Stars](https://img.shields.io/github/stars/zi-yue-1129/ai-wiki?style=social)](https://github.com/zi-yue-1129/ai-wiki/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Built with MkDocs Material](https://img.shields.io/badge/built%20with-MkDocs%20Material-526CFE?logo=materialformkdocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

[🌐 **Read the site**](https://zi-yue-1129.github.io/ai-wiki/) · [📚 Learning paths](https://zi-yue-1129.github.io/ai-wiki/start/learning-paths/) · [🤝 Contribute](CONTRIBUTING.md)

</div>

---

## 📖 Overview

AI Wiki maps the landscape of artificial intelligence in one place: from the mathematics and machine learning behind modern systems, to how neuroscience, cognitive science, and psychology inspire AI (and how AI is changing those sciences), to how AI is applied across medicine, science, education, finance, law, and robotics, and finally the engineering practice and societal questions that surround it.

The wiki is written in English and includes Traditional Chinese (繁體中文) translations of many pages. Pages without a translation fall back to English.

## 🗂️ Sections

| | Section | What it covers |
|:-:|---|---|
| 🧭 | [**Start**](docs/start/index.md) | Learning paths, open-source resource survey, history of AI |
| 📐 | [**Theory**](docs/theory/index.md) | Mathematics, machine learning, deep learning, reinforcement learning, probabilistic, symbolic, and evolutionary approaches |
| 🤖 | [**Models**](docs/theory/models/index.md) | Transformers, large language models, generative models, vision, NLP, speech, multimodal, graph neural networks, agents, world models |
| 🧠 | [**Brain & Mind**](docs/brain-mind/index.md) | Neuroscience, computational neuroscience, NeuroAI, spiking neural networks, memory, cognitive science, psychology, consciousness, brain-computer interfaces |
| 🏥 | [**Applications**](docs/applications/index.md) | AI in healthcare, science, education, finance, law, robotics, cybersecurity, agriculture, and more |
| 🛠️ | [**Engineering**](docs/engineering/index.md) | Frameworks, data, training, prompting, RAG, evaluation, MLOps, hardware |
| ⚖️ | [**Society**](docs/society/index.md) | Safety, interpretability, ethics, governance, economics, philosophy |
| 📚 | [**Reference**](docs/reference/index.md) | Glossary, landmark papers, courses and books, datasets, roadmap, style guide |

Start with the [Glossary](docs/reference/glossary/index.md) if a term is unfamiliar, or the [Learning Paths](docs/start/learning-paths/index.md) if you want a guided route.

## 🛠️ Local preview

Requires Python 3.12 or newer.

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open http://127.0.0.1:8000/ in your browser.

## 🚀 Deployment

Every push to `main` runs `mkdocs build --strict` and deploys the site to GitHub Pages through [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml). Pull requests are built to catch broken links and anything that would fail the strict build, but they are not deployed.

A [maintenance workflow](.github/workflows/maintenance.yml) checks page structure on every pull request and publishes a weekly wiki health report as an issue.

## 🤝 Contributing

Contributions are welcome, whether you are fixing a typo, correcting a fact, adding a translation, or writing a new page.

- **Small fix:** use the ✏️ edit button on any page and open a pull request.
- **Error or missing topic:** [open an issue](https://github.com/zi-yue-1129/ai-wiki/issues/new/choose) using one of the templates.
- **New page:** pick a topic from the [Roadmap](docs/reference/roadmap/index.md), start from [`templates/page-template.md`](templates/page-template.md), and follow the [Style Guide](docs/reference/style-guide/index.md).

Read the full [Contributing guide](docs/reference/contributing/index.md) before opening a pull request. The short version is in [CONTRIBUTING.md](CONTRIBUTING.md).

## 📜 License

- **Content:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
- **Code snippets:** [MIT](https://opensource.org/licenses/MIT).

You are free to share and adapt the material, including commercially, as long as you give appropriate credit and distribute your contributions under the same license.
