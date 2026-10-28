# Contributing to AI Wiki

Thanks for helping build an open, comprehensive wiki of artificial intelligence.

The full guide is on the site: **[Contributing](https://zi-yue-1129.github.io/ai-wiki/reference/contributing/)** (source: [`docs/reference/contributing/index.md`](docs/reference/contributing/index.md)). The short version:

- **Small fix?** Use the ✏️ button on any page and open a pull request.
- **Error or missing topic?** Open an issue with one of the [templates](https://github.com/zi-yue-1129/ai-wiki/issues/new/choose).
- **Writing a page?** Pick a topic from the [Roadmap](docs/reference/roadmap/index.md), start from [`templates/page-template.md`](templates/page-template.md), and follow the [Style Guide](docs/reference/style-guide/index.md).
- English pages are `topic.md`; Traditional Chinese translations are `topic.zh-TW.md`.
- Before opening a PR, run `mkdocs build --strict` and `python scripts/wiki_status.py --check`.
- Search is built by Pagefind after MkDocs: run `npx pagefind --site site` on the built site to test the search box locally. Without that step the search box reports that the index is not built.

Content is licensed CC BY-SA 4.0; write in your own words and cite your sources.
