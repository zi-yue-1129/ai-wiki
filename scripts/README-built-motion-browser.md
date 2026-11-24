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

## Full-coverage four-way sharding candidate

The candidate workflow partitions **every discovered case**, never only changed
pages. Case IDs are canonical JSON tuples of source path, viewport width/height,
and reduced-motion mode. Sorted IDs are assigned by `index % 4`; each shard still
checks the built mapping of every discovered page before launching Chromium.
No image, screenshot stage, prose suite, mobile preflight or calculator lab is
removed. The old single-job workflow is preserved as a non-executing comparison
fixture at `scripts/fixtures/built-motion-browser-unsharded-reference.yml`.

All four browser shards and the separate support job build the same checkout.
The final required-check job, `built-motion-browser`, independently builds it again
and reconstructs discovery and built URL mapping. Six builds cost more runner
minutes, but avoid transferring a roughly 1 GiB site artifact five times. At the 222-page snapshot, the four shards contain 222 cases each, but equal counts
are **not** equal runtimes. With four cases per page, sorted `index % 4` assigns
each shard a fixed viewport/motion combination. Mobile or reduced-motion work can
therefore be slower. The observed 888-case/24-minute serial phase is only a
baseline; no 6–8 minute shard runtime or wall-time saving is claimed before a real
full CI run measures every shard, support job, gate and artifact upload. Cold
dependencies can dominate. Full-motion shard jobs retain 50-minute budgets;
the complete support-browser job has a 100-minute budget, because it also runs
all numerical semantics, all registered bilingual browser support suites, and
lossless evidence packaging. This does not skip any required check.

The always-running gate rejects a missing/cancelled/skipped producer, missing or
extra shard, duplicate/missing/extra case, incomplete image states, failed case,
wrong discovery digest, wrong actual checkout/tree/event head, or wrong run/attempt.
The PR event head is **not** assumed equal to GitHub's synthetic merge checkout.
All receipt/group names contain both run ID and attempt. Consequently **rerun all
jobs**, not just failed jobs: successful evidence from an earlier attempt is
intentionally not reused to make a later attempt green.

Every PNG and JSON stays in the existing lossless <=100 MiB groups. The gate only
downloads small receipts; they contain the full case reports and original packaging
manifests. Exact-attempt producer success plus the run's server-side artifact
inventory proves every expected group was uploaded and is unexpired. This gate
checks report hashes against the packaging manifest and screenshot references
against its complete file list. It does **not** redownload/re-hash every image from
GitHub; local packaging already verifies every copied byte and SHA256. Human QA
can download only the named bounded groups it needs. No monolithic site or PNG
archive is introduced.

### Extending support coverage

`fixtures/browser-support-suites.json` is the exact-tree, versioned support
registry. Its hash is recorded in execution receipts. Append a suite with a unique
`id` (also its artifact root), exact Python `command`, optional `env`, and a coverage
contract. The runner executes all entries, even after a previous entry fails, and
packaging roots are generated from the same registry. A new or unknown contract
cannot silently pass.

- `motion-preflight`: specifies the exact bilingual topic set/source count and
  viewport bound, and requires every initial/paused/replayed screenshot.
- `prose`: specifies sources (or a source manifest), widths, successful case tuples,
  and per-case top screenshots.
- `legacy-lab`: preserves the original scripts' asserted complete control scenarios
  and declares every existing required screenshot, including real built pages.
- `report-cases`: for new labs, specifies `case_fields`, exact `expected_cases`
  (arrays in field order), `expected_pngs`, and `report_trailing_newline`.
  Reports must contain `status: passed`, successful `cases`, and normally an
  `identity` object. Set `require_identity: false` only for an existing lab report
  whose execution receipt already binds it to this exact checkout; the gate still
  validates its packed report hash, complete cases, and screenshots.

This candidate is based on PR #1195 snapshot
`e8c53bce4b3eba9a168144f3daae3a64ef047b11`. It retains the closest-player harness
and all eight original screenshot roots. The registry already includes the
policy-credit suite (24 cases at widths 320/390/1280, each `boundary.png`) and the unchanged
built planning/evolution suite (32 cases, each `initial.png` and
`numeric-final.png`). Their existing reports have no identity field, so these two
entries explicitly use `require_identity: false`; their report hashes and complete
case/screenshot sets are still bound by the support execution receipt's exact
checkout/tree/event head/run/attempt. Independent tests derive their 24/32 expected
case tuples from the original scripts' loop domains.

The #1195 snapshot discovers 266 bilingual pages, 420 images and 1,064 full browser
cases. Four shards contain 266 cases each, again one viewport/motion combination
per shard, so runtime balance is unmeasured. Future support coverage extends this
registry and its expected tuples, not a fixed seven-suite allowlist. Do not remove
or move the source-specific concept-animation workflow; this candidate only
changes the full built-motion regression workflow.


### Renderer and complete local-scroll evidence (new-base port)

The source snapshot is `e8c53bce4b3eba9a168144f3daae3a64ef047b11`.
The complete mobile preflight now includes Shampoo: seven bilingual topics,
14 pages and 28 cases. Every full shard and the preflight must independently
pass the disposable actual MathJax valid → undefined environment rejected →
valid cleared canary. Its separate JSON and negative-output PNG must be packed;
it is not a formal page case and never contributes to full-case counts.
For each discovered overflowing figure ancestor, the gate requires positive
keyboard movement, arrival at the right edge, and a distinct packed right-edge
PNG. Initial, paused and replayed images remain mandatory and unchanged.
Regions are discovered by computed overflow, not by a CSS class allowlist.

Every full shard and mobile preflight also runs the isolated native lazy-image
canary: an image below a 20,000px spacer is undecoded before scroll, decodes to
640×360 after scroll, and a broken SVG is rejected by timeout. The gate requires
passed status, those exact observations, `lazy-image-canary/report.json` bound
by digest, and `lazy-image-canary/loaded-after-scroll.png` in the lossless pack.
The negative fixture is not a formal page case. Missing or inconsistent lazy
proof fails closed, including in the support job.

The source's 75-minute monolithic transitional budget is superseded here by
50-minute full-shard jobs, a 100-minute complete support job and a 30-minute
independent strict-build gate.
Tests parse the actual job budgets numerically; the original full coverage and
all support suites remain. The unsharded reference fixture is historical only.

### DDIM schedule prose coverage

The support registry additionally requires `ddim-prose`: the English and Traditional Chinese DDIM chapters at 390 and 1280 pixels. It uses the real built prose harness and `ddim-prose-pages.json`, with a required `schedule.png` for the schedule-dependent stochasticity section in every case. The gate rejects a missing suite, page, section screenshot, or capture claim; the original seven support suites remain intact. Packaging retains the ninth `ddim-prose` root.

### Support-job timeout regression (2026-11-19)

The support job in [run 44540063208](https://github.com/zi-yue-1129/ai-wiki/actions/runs/44540063208)
started at 14:05 UTC and was cancelled by its 50-minute timeout at 14:56 UTC,
during the real planning/evolution browser suite, **after all four full-motion
shards succeeded**. Its subsequent lossless pack detected source files changing
during cancellation; the exact-attempt receipt was unavailable, so the gate
correctly failed closed. This was a **runtime budget failure**, not evidence of a
visual-content pass or an excuse to ignore missing suites.

The support job now permits 100 minutes. Coverage, exact-attempt artifact
integrity, lossless packaging, required Chromium interactions, and independent
gate assertions are unchanged. The workflow regression asserts that the support
budget stays within 90–120 minutes while retaining all four 50-minute motion
shards and the 30-minute gate. A new run must still finish successfully before
the complete browser regression can be reported green.
