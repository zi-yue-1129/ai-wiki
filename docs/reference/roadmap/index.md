---
references: not-required  # lists and meta pages cite through their entries
---

# Roadmap & Coverage

The goal of this wiki is **complete coverage of artificial intelligence**: how it works, how it relates to the brain and mind, and how every field uses it. This page tracks how far we are and what is still missing.

- **Coverage status** below is generated automatically from the pages themselves on every deploy.
- **Open chapters** are tracked as GitHub issues with the `chapter` label. Each missing topic and each unfinished page has one issue. Anyone can propose a topic with a [topic request](https://github.com/zi-yue-1129/ai-wiki/issues/new?template=topic-request.yml); accepted requests become chapter issues.

To pick something up, see [Contributing](../contributing/index.md).

## Coverage status

--8<-- "includes/status.md"

## Open chapters

The issues are the list, so this page does not repeat them. A pull request that says `Closes #n` in its description closes the chapter when it is merged.

| Priority | Open chapter issues |
|---|---|
| ★★★ core | [Core chapters](https://github.com/zi-yue-1129/ai-wiki/issues?q=is%3Aissue+is%3Aopen+label%3Achapter+label%3Apriority%3Acore) |
| ★★ important | [Important chapters](https://github.com/zi-yue-1129/ai-wiki/issues?q=is%3Aissue+is%3Aopen+label%3Achapter+label%3Apriority%3Aimportant) |
| ★ nice to have | [Nice-to-have chapters](https://github.com/zi-yue-1129/ai-wiki/issues?q=is%3Aissue+is%3Aopen+label%3Achapter+label%3Apriority%3Anice) |
| Unranked: drafts and stubs to finish | [Drafts and stubs](https://github.com/zi-yue-1129/ai-wiki/issues?q=is%3Aissue+is%3Aopen+label%3Achapter+-label%3Apriority%3Acore+-label%3Apriority%3Aimportant+-label%3Apriority%3Anice) |
| Finished | [Closed chapters](https://github.com/zi-yue-1129/ai-wiki/issues?q=is%3Aissue+is%3Aclosed+label%3Achapter) |

## How the wiki is maintained

| What | How | Where |
|---|---|---|
| New topics | Topic request issue → chapter issue → page written in a PR that says `Closes #n` | [Issues](https://github.com/zi-yue-1129/ai-wiki/issues) |
| Corrections | Correction issue, or an edit PR via the ✏️ button on any page | [Issues](https://github.com/zi-yue-1129/ai-wiki/issues) |
| Build and internal links | `mkdocs build --strict` and `scripts/wiki_status.py --check` on every PR | GitHub Actions |
| External links | Weekly link check | Weekly health report issue |
| Stale pages | Pages not reviewed for 12 months are listed for review | Weekly health report issue |
| Translations | zh-TW pages older than their English page are flagged | Status above, weekly report |
