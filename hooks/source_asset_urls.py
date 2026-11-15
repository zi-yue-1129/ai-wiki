"""Resolve explicitly marked raw-image URLs from source to built-page paths.

Raw HTML is not rewritten by MkDocs' Markdown image handling. An <img> may
opt in with data-source-asset-urls so its relative src/data-motion-src/
data-still-src can remain readable on GitHub. Unmarked HTML is left untouched.
"""
from html import escape
from html.parser import HTMLParser
import posixpath
from urllib.parse import unquote, urlsplit, urlunsplit


MARKER = "data-source-asset-urls"
ASSET_ATTRIBUTES = {"src", "data-motion-src", "data-still-src"}


def built_asset_url(value, page, files):
    parts = urlsplit(value)
    # The opt-in convention only changes source-relative paths, not external,
    # root-relative or fragment-only references.
    if parts.scheme or parts.netloc or not parts.path or parts.path.startswith("/"):
        return value
    source = posixpath.normpath(posixpath.join(
        posixpath.dirname(page.file.src_uri), unquote(parts.path, errors="strict")
    ))
    if not source.startswith("assets/"):
        raise ValueError(f"{page.file.src_uri}: marked image URL {value!r} must resolve under docs/assets/")
    asset = files.get_file_from_path(source)
    if asset is None:
        raise ValueError(f"{page.file.src_uri}: marked image URL {value!r} has no built asset: {source}")
    # Use the actual output URL, including the locale directory, rather than
    # assuming the Markdown filename and deployed page have identical depth.
    relative = posixpath.relpath(asset.url, posixpath.dirname(page.url) or ".")
    return urlunsplit(("", "", relative, parts.query, parts.fragment))


class SourceAssetParser(HTMLParser):
    def __init__(self, html, page, files):
        super().__init__(convert_charrefs=True)
        self.html = html
        self.page = page
        self.files = files
        self.offsets = [0]
        # HTMLParser's line counter advances on '\n', not every Unicode line
        # separator accepted by str.splitlines().
        for index, character in enumerate(html):
            if character == "\n":
                self.offsets.append(index + 1)
        self.replacements = []

    def handle_starttag(self, tag, attrs):
        if tag != "img" or not any(name == MARKER for name, _ in attrs):
            return
        attributes = {}
        for name, value in attrs:
            attributes.setdefault(name, value)
        del attributes[MARKER]
        for name, value in attributes.items():
            if name in ASSET_ATTRIBUTES:
                if value is None or not value.strip():
                    raise ValueError(f"{self.page.file.src_uri}: marked image has empty {name}")
                attributes[name] = built_asset_url(value, self.page, self.files)
        serialized = "".join(
            f" {name}" if value is None else f' {name}="{escape(value, quote=True)}"'
            for name, value in attributes.items()
        )
        raw = self.get_starttag_text()
        closing = " />" if raw.endswith("/>") else ">"
        line, column = self.getpos()
        start = self.offsets[line - 1] + column
        self.replacements.append((start, start + len(raw), f"<img{serialized}{closing}"))


def on_page_content(html, page, config, files, **kwargs):
    if MARKER not in html.lower():
        return html
    parser = SourceAssetParser(html, page, files)
    parser.feed(html)
    parser.close()
    for start, end, replacement in reversed(parser.replacements):
        html = html[:start] + replacement + html[end:]
    return html
