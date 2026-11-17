#!/usr/bin/env python3
"""Check built HTML image/motion URLs against files in a deployed site tree.

Standard library only. Run after MkDocs; see README-built-asset-urls.md.
This checks URL/file existence, not image validity, animation or rendering.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit


@dataclass(frozen=True)
class Reference:
    line: int
    attribute: str
    value: str | None


@dataclass(frozen=True)
class Violation:
    page: str
    reference: Reference
    resolved_url: str
    reason: str

    def __str__(self) -> str:
        ref = self.reference
        return (f"{self.page}:{ref.line}: {ref.attribute}={ref.value!r}: "
                f"{self.reason}; resolved URL: {self.resolved_url}")


@dataclass
class CheckResult:
    pages: int = 0
    local_references: int = 0
    skipped_references: int = 0
    violations: list[Violation] = field(default_factory=list)


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[Reference] = []
        self.base: Reference | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in ("img", "base") and not any(
            name in ("data-motion-src", "data-still-src") for name, _ in attrs
        ):
            return
        # Browsers use the first duplicate attribute, not the last.
        attributes: dict[str, str | None] = {}
        for name, value in attrs:
            attributes.setdefault(name, value)
        line = self.getpos()[0]
        if tag == "base" and "href" in attributes and self.base is None:
            self.base = Reference(line, "base href", attributes["href"])
        for name, value in attributes.items():
            if (tag == "img" and name == "src") or name in (
                "data-motion-src", "data-still-src"
            ):
                self.references.append(Reference(line, name, value))


def resolve_url(base: str, value: str) -> str:
    """Resolve HTTP references, including URL-encoded dot segments.

    Unlike filesystem joins, URL joins respect the document's trailing slash.
    HTTP URL parsing treats backslashes as slashes and ignores embedded ASCII
    tabs/newlines. Normalize dot segments even for absolute URLs (urljoin alone
    does not do that), without decoding filenames or query/fragment delimiters.
    """
    value = value.strip("".join(chr(i) for i in range(33)))
    value = value.translate(str.maketrans("", "", "\t\r\n")).replace("\\", "/")
    parts = urlsplit(urljoin(base, value))
    if parts.scheme.lower() not in ("http", "https"):
        return parts.geturl()
    segments: list[str] = []
    for segment in parts.path.split("/"):
        dot = re.sub("%2e", ".", segment, flags=re.IGNORECASE)
        if dot == "..":
            if len(segments) > 1:
                segments.pop()
        elif dot != ".":
            segments.append(segment)
    if re.sub("%2e", ".", parts.path.rsplit("/", 1)[-1], flags=re.IGNORECASE) in (".", ".."):
        segments.append("")
    return urlunsplit(parts._replace(path="/".join(segments) or "/"))


def origin(url: str) -> tuple[str, str | None, int | None]:
    parts = urlsplit(url)
    return (parts.scheme.lower(), parts.hostname,
            parts.port if parts.port is not None else
            {"http": 80, "https": 443}.get(parts.scheme.lower()))


def deployment_url(value: str) -> str:
    parts = urlsplit(value)
    if (parts.scheme not in ("http", "https") or not parts.hostname
            or parts.username is not None or parts.password is not None
            or parts.query or parts.fragment):
        raise ValueError("--site-url must be an absolute HTTP(S) URL without credentials, query or fragment")
    origin(value)  # Validate port syntax before scanning.
    return resolve_url(value, value.rstrip("/") + "/")


def document_url(site_url: str, relative_page: Path) -> str:
    path = relative_page.as_posix()
    if relative_page.name == "index.html":
        path = path[:-len("index.html")]
    return urljoin(site_url, quote(path, safe="/"))


def check_site(site_dir: Path, site_url: str) -> CheckResult:
    site_dir = site_dir.resolve()
    site_url = deployment_url(site_url)
    if not site_dir.is_dir():
        raise ValueError(f"site directory does not exist: {site_dir}")
    pages = sorted(site_dir.rglob("*.html"))
    if not pages:
        raise ValueError(f"no built HTML files found in {site_dir}")
    mount = unquote(urlsplit(site_url).path, errors="strict")
    result = CheckResult()
    for page in pages:
        relative_page = page.relative_to(site_dir)
        page_url = document_url(site_url, relative_page)
        parser = AssetParser()
        html = page.read_text(encoding="utf-8")
        result.pages += 1
        # Most pages have no images. Avoid parsing their large navigation trees;
        # this is only a prefilter, never the source of parsed attribute values.
        lower_html = html.lower()
        if not any(token in lower_html for token in ("<img", "data-motion-src", "data-still-src")):
            continue
        parser.feed(html)
        parser.close()
        base_url = page_url
        if parser.base is not None:
            try:
                base_url = resolve_url(page_url, parser.base.value or "")
            except ValueError as exc:
                result.violations.append(Violation(str(relative_page), parser.base,
                                                   page_url, f"invalid base URL: {exc}"))
        for ref in parser.references:
            resolved = page_url
            try:
                if ref.value is None or not ref.value.strip():
                    raise ValueError("empty asset URL")
                resolved = resolve_url(base_url, ref.value)
                parts = urlsplit(resolved)
                if origin(resolved) != origin(site_url):
                    result.skipped_references += 1
                    continue
                result.local_references += 1
                # Decode only the path. A '?' or '#' inside a filename must be
                # percent-encoded; actual queries/fragments are not filenames.
                path = unquote(parts.path, errors="strict")
                if not path.startswith(mount):
                    raise ValueError(f"same-origin URL is outside deployment path {mount}")
                target = (site_dir / path[len(mount):]).resolve()
                if path.endswith("/"):
                    target = (target / "index.html").resolve()
                if not target.is_relative_to(site_dir):
                    raise ValueError("asset path escapes the built site directory")
                if not target.is_file():
                    raise ValueError(f"missing built file {target.relative_to(site_dir)}")
            except (ValueError, OSError) as exc:
                result.violations.append(Violation(str(relative_page), ref, resolved, str(exc)))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("site"),
                        help="MkDocs output directory (default: site)")
    parser.add_argument("--site-url", required=True,
                        help="deployment URL, matching site_url in mkdocs.yml")
    args = parser.parse_args(argv)
    try:
        result = check_site(args.site_dir, args.site_url)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for violation in result.violations:
        print(f"ERROR: {violation}", file=sys.stderr)
    print(f"Checked {result.pages} HTML files, {result.local_references} local asset URLs; "
          f"skipped {result.skipped_references} external/inline URLs; "
          f"{len(result.violations)} violation(s)")
    return 1 if result.violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
