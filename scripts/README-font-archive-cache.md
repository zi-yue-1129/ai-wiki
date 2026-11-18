# Verified CJK font archive cache

This caches only the official `fonts-noto-cjk` download, not installed files or
APT databases. An observed CI run spent 18m16s downloading its 61.2 MB archive.
The existing browser dependencies, strict build, all browser/semantic/lab tests,
and 50-minute browser timeout remain unchanged.

## Trust boundary

`install-cjk-font` first refreshes APT indexes with `Error-Mode=any`. The system
Python's APT bindings resolve the current Ubuntu candidate and its SHA256/size.
Candidates with untrusted or non-Ubuntu downloadable origins are rejected. Neither
metadata nor keys are restored from cache. A restored payload is opened without
following symlinks, checked for regular-file type, link count, size and SHA256,
and copied into a fresh root-owned temporary APT archive directory. Extra cache
entries are rejected. This matters because APT can accept an existing archive
based on its size alone; calling `apt-get install` is not sufficient validation
of restored bytes.

On a miss or invalid cache, APT downloads normally. The downloaded font is also
independently hashed before the normal package-name APT installation. No `dpkg -i`,
unsigned repositories, disabled signature checks or restored system state are
used. A cache restore failure is non-fatal; APT update/authentication/install
failures are fatal. The script verifies the installed version and Traditional
Chinese font match. Archive files are never executed except through the normal
APT installation of authenticated package contents.

The normal PR workflow is restore-only. Production saving is restricted to
`push`/manual dispatch on `main`, after the safety matrix succeeds. The cache key
includes Ubuntu release, runner architecture, authenticated package SHA256 and
validator source hash. There are no broad restore keys. Security updates thus
get a new key without accepting obsolete bytes.

The validation workflow uses a separate run-specific cache namespace, including
PR-scoped writes solely to test actual service miss/hit behavior. These cannot
seed sibling PRs. The `corrupt` case flips one byte while retaining size; the
`fallback` case simulates a failing cache transport step, not a real GitHub outage.
The disabled case never restores. All run on fresh Ubuntu runners and require
the same installed version/font checks and installed font-file SHA256 as the cold seed.
The matrix runs font installation and `fc-match` checks, not the full browser suite
in every mode. The full existing browser suite runs
separately on the same commit; the safety matrix does not replace or skip it.

## Verification

- `python scripts/test_ci_font_archive.py`: offline payload, metadata and retained
  workflow coverage regressions; no privileged operations.
- `Font archive cache safety`: real cold seed plus fresh-runner hit, miss,
  disabled, same-size corruption and simulated transport-failure cases. Reports
  contain metadata, result, installed version, font match and elapsed seconds.
- `Built motion browser regression`: unchanged full coverage plus safety tests
  and a dependency report.
- After merging: confirm a trusted main seed completes, then an independent PR
  restores its production key. Same-PR hits do **not** prove cross-PR reuse.

Do not claim a latency improvement until comparing real reports. Cache service
errors still permit cold installation, but cold network latency can still exhaust
job budgets. Browser binaries and other OS dependencies are intentionally outside
this first change.

References:
- https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
- https://github.com/actions/cache
- https://manpages.ubuntu.com/manpages/noble/man8/apt-get.8.html
- https://apt-team.pages.debian.net/python-apt/library/apt.package.html
- https://raw.githubusercontent.com/Debian/apt/main/apt-pkg/acquire-item.cc
