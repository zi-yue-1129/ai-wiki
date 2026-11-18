# Browser regression for built opt-in motion images

This separate check browses the real strict MkDocs output. It does not replace
the existing animation-semantic tests or the whole-site built-asset URL checker.

```sh
python -m pip install -r requirements.txt 'playwright==1.55.0'
python -m playwright install --with-deps chromium
# On Ubuntu, also install fonts-noto-cjk for Traditional Chinese screenshots.
python scripts/test_built_motion_discovery.py
mkdocs build --strict
python scripts/test_built_motion_browser.py
```

The dedicated `Built motion browser regression` workflow uses Ubuntu 24.04 and
uploads `built-motion-browser-review`, including PNG screenshots and
`report.json`, even after a test failure. It also runs the available
`test_*motion_semantics.py` numerical regressions before the build. Download that artifact to review the
actual page layout. Screenshots are evidence for human review, not a pixel-diff
baseline or proof of animation mathematics.

## Coverage

- Find real marked HTML images in Markdown source, before
  `data-source-asset-urls` is removed by the build hook. Fenced examples and
  comments are excluded. No page-name allowlist needs updating when another
  English or zh-TW page opts in.
- Use the installed MkDocs and suffix-i18n URL generator and configuration to
  locate output HTML, including nested/index pages and translated output.
- Verify every opted-in `src`, `data-motion-src`, and `data-still-src` against
  the expected source asset before starting Chromium.
- Serve the built site under its configured deployment path, currently
  `/ai-wiki/`, and load its real HTML, CSS and JavaScript without synthetic
  `set_content` fixtures or replacement player code.
- Test desktop 1280×900 and touch/mobile 390×844 viewports in each motion mode.
  Check the actual viewport width, document language, decoded image dimensions,
  and whole-document horizontal overflow. Scrolling inside a visual's own
  container is intentionally allowed.
- Check normal initial motion and reduced-motion initial still state, then
  pause to the still asset and replay to the motion asset. Reduced-motion cases
  explicitly play once before pausing. Replay uses keyboard Enter.
- Save actual viewport screenshots for initial, paused and replayed states,
  scrolled to each visual, plus failure screenshots when possible. The report
  records page paths, asset URLs, image decode state, viewport dimensions,
  screenshot directories and diagnostic JavaScript/network errors. Unrelated
  external-request failures are diagnostic, not assertions about image loading.

At introduction there are four source pages (temperature scaling and conformal
prediction, each in English and zh-TW), yielding 16 browser cases and 48 normal
screenshots. New marked motion images are included automatically. Pages without
this opt-in marker and missing-translation fallback copies are outside this
focused check. The shared player must have a distinct `-motion.svg`/`-still.svg`
pair (or explicit `data-still-src`) and unique alt text on that page.

For a browser-free wiring check after a strict build:

```sh
python scripts/test_built_motion_browser.py --discover-only
```

That validates discovery and built HTML attributes only; it is **not** a browser
or screenshot pass. `--site-dir`, `--output`, and a local
`--executable-path /path/to/chromium` are also available. CI deliberately uses
Playwright's bundled browser. Browser startup failures fail the run and are
recorded in `report.json`; they are never treated as skipped successes.
