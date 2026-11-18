# Built asset URL checks

Run from the repository root after building:

```sh
python scripts/test_built_asset_urls.py
python scripts/test_source_asset_urls.py
mkdocs build --strict
python scripts/verify_built_asset_urls.py \
  --site-dir site \
  --site-url https://zi-yue-1129.github.io/ai-wiki/
```

`--site-url` must match `site_url` in `mkdocs.yml`. It is explicit so a change
between a project deployment (`/ai-wiki/`) and a root deployment (`/`) cannot
silently use the wrong mount point. No third-party Python packages or network
requests are needed by either script.

The checker reads **built HTML**, including translated pages, and resolves
`img[src]`, `data-motion-src`, and `data-still-src` from each page's served URL.
For example, `chapter/index.html` is served at `chapter/`, whereas `chapter.html`
retains its filename. The first `<base href>` is respected. Same-origin absolute
and root-relative URLs must stay within the deployment path. URL-encoded
filenames are decoded after query strings and fragments have been separated.
External origins, data URLs, and other non-HTTP URLs are skipped, not verified.

Every failure reports the built page, line, attribute, resolved URL and missing
file (or deployment-path error). Exit codes are 0 for success, 1 for asset URL
violations and 2 for input/read errors, including an absent or empty build.

The two regression fixtures capture path-depth failures seen in PR #1031 (raw
HTML uses three parent segments where the built URL needs four) and PR #1035
(the translated Markdown `src` is rewritten to five parent segments while its
custom data attributes retain four). Tests require both the broken fixture to
fail and its corrected version to pass. A source-level file check alone can
miss these failures.

### Initial baseline

The strict build of main commit `f3b42e789abb45e4e2ae2ce9b5b559914e582188`
contained **1,921 HTML files, 175 local asset references, and 8 violations**.
They were the `src` and `data-motion-src` attributes on the English and zh-TW
`conformal-prediction` and `temperature-scaling` pages under
`theory/paradigms/probabilistic/uncertainty-calibration/`.
Raw source-relative `../../../../assets/` resolved to `theory/assets/` in English
and `zh-TW/theory/assets/` in zh-TW, instead of the built root's `assets/`.
The unit tests retain this original failure mode. The initial checker-only
commit changed no existing page, asset, animation validator or workflow.

## Explicit raw HTML support

The four affected source images now opt in with `data-source-asset-urls`.
`hooks/source_asset_urls.py` resolves their relative `src`, `data-motion-src`
and `data-still-src` from the Markdown source file to the asset's registered
output URL, then makes that URL relative to the actual built page (including
`zh-TW/`). The source-relative paths stay intact for GitHub. No SVG, player
JavaScript, styles or unmarked image markup is changed.

Use this marker only when **all relative asset attributes on the raw image are
source-relative**. Do not put it on Markdown images whose `src` MkDocs already
rewrites, or on mixed source/built-relative attribute conventions. The hook
requires local targets under `docs/assets/`, leaves absolute/external references
alone, and removes the marker from its output to avoid a second rewrite.

```sh
python scripts/test_source_asset_urls.py
```

## CI integration

The scoped repair was verified with the same 1,921-page / 175-reference scan:
**zero violations**. `.github/workflows/deploy.yml` now runs both unit suites
before the build and the checker immediately after `mkdocs build --strict`,
before search indexing and artifact upload. The deployment URL is read through
MkDocs' config loader so it stays in sync with `mkdocs.yml` (which also contains
Python-tagged extension settings). The gate runs on both pull requests and
deployment builds; there is no baseline allowlist suppressing broken images.

This check does **not** validate image decoding, MIME types, visual correctness,
animation semantics, JavaScript-generated URLs, `srcset`, CSS resources, or
external URL availability. It supplements rather than replaces image/animation
validators and browser review.
