#!/usr/bin/env python3
"""Exercise opt-in motion images on real, already-built MkDocs pages.

Run after `mkdocs build --strict`; see README-built-motion-browser.md.
Discovery uses source HTML because the URL-rewriting hook removes its marker.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import posixpath
import re
import tempfile
from threading import Thread
from urllib.parse import quote, unquote, urljoin, urlsplit

from markdown import Markdown
from mkdocs.config import load_config
from mkdocs.structure.files import File
from mkdocs_static_i18n.suffix import create_i18n_file

ROOT = Path(__file__).resolve().parents[1]
MARKER = "data-source-asset-urls"
ATTRIBUTES = ("src", "data-motion-src", "data-still-src")
VIEWPORTS = {"desktop": {"width": 1280, "height": 900},
             "mobile": {"width": 390, "height": 844}}


class Images(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.images = []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            image = {}
            for key, value in attrs:
                image.setdefault(key, value)
            self.images.append(image)


@dataclass
class MotionPage:
    source: str
    locale: str
    url: str
    output: str
    images: list[dict]


def discover_pages(config):
    """Use the installed MkDocs/i18n URL generator, not Markdown-depth guesses."""
    i18n = config.plugins["i18n"].config
    assert i18n.docs_structure == "suffix", "Update discovery for the new i18n layout"
    languages = {lang["locale"]: lang for lang in i18n.languages}
    default = next(lang["locale"] for lang in i18n.languages if lang["default"])
    pages = []
    for source in sorted(Path(config.docs_dir).rglob("*.md")):
        text = source.read_text(encoding="utf-8")
        if MARKER not in text.lower():
            continue
        # Rendering Markdown avoids treating fenced examples as actual images.
        html = Markdown(extensions=config.markdown_extensions,
                        extension_configs=config.mdx_configs).convert(text)
        images = [img for img in Images(html).images if MARKER in img and (
            img.get("data-motion-src") or re.search(r"-motion\.svg(?:[?#]|$)", img.get("src") or ""))]
        if not images:
            continue
        uri = source.relative_to(config.docs_dir).as_posix()
        locale = next((lang for lang in languages if source.stem.endswith("." + lang)), default)
        if not languages[locale]["build"]:
            continue
        file = create_i18n_file(File(uri, config.docs_dir, config.site_dir,
                                     config.use_directory_urls),
                                locale, default, list(languages), config)
        pages.append(MotionPage(uri, locale, file.url, file.dest_uri, images))
    assert pages, "No marked motion images discovered; refusing a vacuous browser pass"
    return pages


def source_asset_url(base_url, source, value):
    """Independent expected URL for source-relative, shared docs/assets files."""
    parts = urlsplit(value)
    assert not parts.scheme and not parts.netloc and not parts.path.startswith("/"), value
    path = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(parts.path)))
    assert path.startswith("assets/"), (source, value, path)
    return urljoin(base_url, quote(path, safe="/")) + (
        "?" + parts.query if parts.query else "") + ("#" + parts.fragment if parts.fragment else "")


def check_built_page(site, target, base_url):
    """Fail before launch if a marked image disappeared or a built attribute is wrong."""
    output = site / target.output
    assert output.is_file(), f"Missing built page: {output}; run mkdocs build --strict"
    built = Images(output.read_text(encoding="utf-8")).images
    expected = []
    for source in target.images:
        alt = source.get("alt")
        assert alt, f"{target.source}: marked motion image needs alt text"
        matches = [img for img in built if img.get("alt") == alt]
        assert len(matches) == 1, f"{target.source}: expected one built image with alt {alt!r}"
        image = matches[0]
        assert MARKER not in image, f"{target.source}: source URL hook did not run"
        for attribute in ATTRIBUTES:
            if attribute in source:
                actual = urljoin(urljoin(base_url, target.url), image.get(attribute) or "")
                wanted = source_asset_url(base_url, target.source, source[attribute])
                assert actual == wanted, (target.source, attribute, actual, wanted)
        motion = source.get("data-motion-src") or source["src"]
        still = source.get("data-still-src") or re.sub(r"-motion\.svg(?=[?#]|$)", "-still.svg", motion)
        assert still != motion, f"{target.source}: no distinct still fallback"
        expected.append({"alt": alt,
                         "motion": source_asset_url(base_url, target.source, motion),
                         "still": source_asset_url(base_url, target.source, still)})
    return expected


@contextmanager
def serve_site(site, site_url):
    # Serve at the production mount (/ai-wiki/), including on translated pages.
    # This catches URLs that accidentally work only when the site is at '/'.
    mount = unquote(urlsplit(site_url).path).strip("/")
    assert ".." not in mount.split("/"), "Invalid site_url mount"
    with tempfile.TemporaryDirectory(prefix="built-motion-") as directory:
        root = Path(directory)
        if mount:
            link = root / mount
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(site, target_is_directory=True)
        else:
            root = site

        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, *_args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(root)))
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}/" + (quote(mount, safe="/") + "/" if mount else "")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


def assert_document_fits(page, viewport):
    size = page.evaluate("""() => ({inner: innerWidth,
        client: document.documentElement.clientWidth,
        width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)})""")
    assert size["inner"] == viewport["width"], ("actual viewport mismatch", size, viewport)
    # Scrolling *inside* a figure is intentional. Only whole-document overflow fails.
    assert size["width"] <= size["client"] + 1, ("whole-document horizontal overflow", size)
    return size


def check_math_rendering(page):
    """Wait for real MathJax output and reject re-typeset accessibility MathML."""
    page.evaluate("""async () => {
        let timer;
        try {
            await Promise.race([window.MathJax.startup.promise, new Promise((_, reject) => {
                timer = setTimeout(() => reject(new Error('MathJax startup did not settle')), 15000);
            })]);
        } finally { clearTimeout(timer); }
    }""")
    state = page.evaluate("""() => {
        const article = document.querySelector('.md-content__inner');
        const roots = Array.from(article.querySelectorAll('.arithmatex'));
        return {
            sourceRoots: roots.length,
            unrendered: roots.filter(node => !node.querySelector('mjx-container')).length,
            containers: article.querySelectorAll('mjx-container').length,
            nestedAssistive: article.querySelectorAll('mjx-assistive-mml mjx-container').length,
            assistiveMathML: article.querySelectorAll('mjx-assistive-mml > math').length,
            trackedItems: MathJax.startup.document.getMathItemsWithin(article).length
        };
    }""")
    assert state["unrendered"] == 0, ("unrendered math source", state)
    assert state["nestedAssistive"] == 0, ("assistive MathML was typeset again", state)
    assert state["assistiveMathML"] == state["containers"], ("missing assistive MathML", state)
    assert state["trackedItems"] == state["containers"], ("rendered MathItems were forgotten", state)
    return state


OVERFLOW_DIAGNOSTICS_JS = r"""() => {
    const root = document.documentElement;
    const limit = root.clientWidth;
    const rect = r => ({left: r.left + scrollX, right: r.right + scrollX,
                       top: r.top + scrollY, bottom: r.bottom + scrollY,
                       width: r.width, height: r.height});
    const selector = element => {
        const parts = [];
        for (let node = element; node && parts.length < 6; node = node.parentElement) {
            let part = node.localName;
            if (node.id) { parts.unshift(part + '#' + node.id); break; }
            part += Array.from(node.classList || []).map(name => '.' + name).join('');
            if (node.parentElement) {
                part += ':nth-child(' + (Array.from(node.parentElement.children).indexOf(node) + 1) + ')';
            }
            parts.unshift(part);
        }
        return parts.join(' > ');
    };
    const style = element => {
        const s = getComputedStyle(element);
        return {overflowX: s.overflowX, overflowY: s.overflowY, position: s.position,
                display: s.display, visibility: s.visibility, opacity: s.opacity,
                transform: s.transform, contain: s.contain, whiteSpace: s.whiteSpace,
                overflowWrap: s.overflowWrap, wordBreak: s.wordBreak,
                fontFamily: s.fontFamily, fontSize: s.fontSize};
    };
    const clipping = element => {
        const clips = [];
        for (let node = element; node; node = node.parentElement) {
            const s = getComputedStyle(node);
            if (s.overflowX !== 'visible' || /(?:paint|strict|content)/.test(s.contain)) {
                clips.push({selector: selector(node), rect: rect(node.getBoundingClientRect()),
                            clientWidth: node.clientWidth, scrollWidth: node.scrollWidth,
                            overflowX: s.overflowX, contain: s.contain});
            }
        }
        return clips;
    };
    const outside = r => r.width > 0 && r.height > 0 &&
        (r.right > limit + 0.01 || r.left < -0.01);
    const describe = (element, r, clipStart) => {
        const clips = clipping(clipStart);
        // Bounds after ancestor clipping are diagnostic estimates, not a pass rule.
        const clippedLeft = Math.max(r.left, ...clips.map(clip => clip.rect.left));
        const clippedRight = Math.min(r.right, ...clips.map(clip => clip.rect.right));
        return {selector: selector(element), text: (element.textContent || '').trim().slice(0, 180),
                rect: r, style: style(element), clientWidth: element.clientWidth,
                scrollWidth: element.scrollWidth, clippingAncestors: clips,
                estimatedClippedBounds: {left: clippedLeft, right: clippedRight},
                estimatedOutsideAfterClipping: clippedRight > clippedLeft &&
                    (clippedRight > limit + 0.01 || clippedLeft < -0.01)};
    };
    const elements = [];
    for (const element of document.querySelectorAll('*')) {
        const r = rect(element.getBoundingClientRect());
        if (outside(r)) elements.push(describe(element, r, element.parentElement));
    }
    const textRanges = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.textContent.trim()) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        for (const clientRect of range.getClientRects()) {
            const r = rect(clientRect);
            if (outside(r)) textRanges.push({...describe(node.parentElement, r, node.parentElement),
                                            text: node.textContent.trim().slice(0, 240)});
        }
    }
    return {
        innerWidth, outerWidth, scrollX, scrollY, devicePixelRatio,
        screen: {width: screen.width, height: screen.height, availWidth: screen.availWidth},
        visualViewport: visualViewport ? {width: visualViewport.width, height: visualViewport.height,
            scale: visualViewport.scale, offsetLeft: visualViewport.offsetLeft,
            pageLeft: visualViewport.pageLeft} : null,
        viewportMeta: Array.from(document.querySelectorAll('meta[name="viewport"]')).map(e => e.content),
        documentElement: {clientWidth: root.clientWidth, scrollWidth: root.scrollWidth,
                          rect: rect(root.getBoundingClientRect())},
        body: {clientWidth: document.body.clientWidth, scrollWidth: document.body.scrollWidth,
               rect: rect(document.body.getBoundingClientRect())},
        fontsStatus: document.fonts.status,
        mathJax: {present: !!window.MathJax, containers: document.querySelectorAll('mjx-container').length},
        motionContainers: Array.from(document.querySelectorAll('.concept-motion-scroll, .concept-motion-player'))
            .map(element => describe(element, rect(element.getBoundingClientRect()), element.parentElement)),
        overflowingElements: elements, overflowingTextRanges: textRanges
    };
}"""


def record_failure_diagnostics(page, output, result):
    """Preserve failure evidence without altering layout, assertions, or the failure."""
    try:
        diagnostics = page.evaluate(OVERFLOW_DIAGNOSTICS_JS)
        name = "overflow-diagnostics.json"
        (output / name).write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")
        result["overflow_diagnostics"] = name
    except Exception as error:
        result["overflow_diagnostics_error"] = str(error)


def check_image(page, image, url):
    # complete alone also becomes true for broken images, so check decoded size too.
    page.wait_for_function("""({alt, url}) => {
        const img = Array.from(document.images).find(img => img.alt === alt);
        return img && img.src === url && img.complete && img.naturalWidth > 0 && img.naturalHeight > 0;
    }""", arg={"alt": image.get_attribute("alt"), "url": url})
    assert image.is_visible(), ("image hidden", url)
    return image.evaluate("img => ({src: img.src, complete: img.complete, naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight})")


def settled_scroll_left(region):
    """Wait for native key-scroll animation to finish, not merely its first frame."""
    return region.evaluate("""(e) => new Promise((resolve, reject) => {
      let last = e.scrollLeft, stableSince = performance.now();
      const started = stableSince;
      function frame(now) {
        const current = e.scrollLeft;
        if (current !== last) { last = current; stableSince = now; }
        if (now - stableSince >= 180) { resolve(current); return; }
        if (now - started > 3000) { reject(new Error('Native scroll did not settle')); return; }
        requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    })""")


def check_keyboard_scrollers(page):
    """Measure native keyboard scrolling, then restore the screenshot position."""
    measured = []
    regions = page.locator('.concept-motion-scroll[tabindex="0"]')
    for index in range(regions.count()):
        region = regions.nth(index)
        if not region.is_visible():
            continue
        bounds = region.evaluate('(e) => ({clientWidth: e.clientWidth, scrollWidth: e.scrollWidth})')
        if bounds['scrollWidth'] <= bounds['clientWidth'] + 2:
            continue
        region.evaluate('(e) => e.scrollTo({left: 0, behavior: "instant"})')
        region.focus()
        assert region.evaluate('(e) => document.activeElement === e'), 'Scroll region cannot receive focus'
        region.press('ArrowRight')
        page.wait_for_function('(e) => e.scrollLeft > 0', arg=region.element_handle(), timeout=2000)
        bounds['afterArrowRight'] = settled_scroll_left(region)
        assert bounds['afterArrowRight'] > 0, 'Keyboard scroll did not remain moved'
        region.evaluate('(e) => { e.blur(); e.scrollTo({left: 0, behavior: "instant"}); }')
        assert settled_scroll_left(region) == 0, 'Scroll region did not reset'
        measured.append(bounds)
    return measured


def exercise_page(browser, target, expected, base_url, viewport, reduced, output, result):
    from playwright.sync_api import expect

    context = browser.new_context(viewport=viewport, device_scale_factor=1,
                                  is_mobile=viewport["width"] < 600,
                                  has_touch=viewport["width"] < 600,
                                  reduced_motion="reduce" if reduced else "no-preference",
                                  color_scheme="light")
    page = context.new_page()
    page.set_default_timeout(15000)
    result["page_errors"] = []
    result["failed_requests"] = []
    page.on("pageerror", lambda error: result["page_errors"].append(str(error)))
    page.on("requestfailed", lambda request: result["failed_requests"].append(
        {"url": request.url, "failure": request.failure}))
    try:
        response = page.goto(urljoin(base_url, target.url), wait_until="load", timeout=45000)
        assert response and response.ok, f"Built page returned {response.status if response else 'no response'}"
        assert page.locator("html").get_attribute("lang") == target.locale
        assert page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches") == reduced
        result["math_rendering"] = check_math_rendering(page)
        # Wait for font layout before judging bounds or taking the review screenshots.
        page.evaluate("document.fonts.ready")
        result['keyboard_scroll'] = check_keyboard_scrollers(page)
        # These diagrams intentionally preserve a 640px reading width on phones.
        topic = target.source.rsplit('/', 1)[-1].removesuffix('.md').removesuffix('.zh-TW')
        if viewport['width'] < 600 and topic in {'t-sne', 'umap', 'minhash-deduplication', 'data-programming'}:
            assert any(r['scrollWidth'] >= 640 and r['afterArrowRight'] > 0
                       for r in result['keyboard_scroll']), 'Readable mobile diagram scroller is missing'
        result["images"] = []
        for index, asset in enumerate(expected, 1):
            image = page.get_by_alt_text(asset["alt"], exact=True)
            expect(image).to_have_count(1)
            expect(image).to_have_attribute("data-concept-motion-enhanced", "yes")
            host = image.locator("xpath=parent::*")
            toggle = host.locator(".concept-motion-toggle").first
            chinese = bool(re.search(r"[\u3400-\u9fff]", asset["alt"]))
            play = "播放概念動畫" if chinese else "Play concept animation"
            pause = "暫停概念動畫" if chinese else "Pause concept animation"
            record = {"alt": asset["alt"], "states": {}}
            result["images"].append(record)

            def capture(stage, state, label):
                expect(toggle).to_have_attribute("aria-label", label)
                record["states"][stage] = check_image(page, image, asset[state])
                record["states"][stage]["document"] = assert_document_fits(page, viewport)
                image.scroll_into_view_if_needed()
                screenshot = output / f"image-{index}-{stage}.png"
                # Viewport screenshot, not set_content or an enlarged image-only viewport.
                page.screenshot(path=str(screenshot))
                record["states"][stage]["screenshot"] = screenshot.name

            capture("initial", "still" if reduced else "motion", play if reduced else pause)
            if reduced:
                # Reduced motion must start still, but deliberate playback remains usable.
                toggle.click()
                expect(toggle).to_have_attribute("aria-label", pause)
                check_image(page, image, asset["motion"])
            toggle.click()
            capture("paused", "still", play)
            # Keyboard activation also proves that the real control is operable.
            toggle.focus()
            page.keyboard.press("Enter")
            capture("replayed", "motion", pause)
        result["status"] = "passed"
    except Exception:
        record_failure_diagnostics(page, output, result)
        try:
            page.screenshot(path=str(output / "failure.png"))
        except Exception:
            pass
        raise
    finally:
        context.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "mkdocs.yml")
    parser.add_argument("--site-dir", type=Path, help="Already-built site (defaults to mkdocs.yml)")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/built-motion-browser")
    parser.add_argument("--keyboard-preflight", action="store_true",
                        help="Check the four keyboard-scroll topics on mobile before the separate full suite")
    parser.add_argument("--discover-only", action="store_true", help="Validate discovery and built attributes without Chromium")
    parser.add_argument("--executable-path", help="Optional local Chromium; CI uses Playwright's pinned browser")
    args = parser.parse_args()
    config = load_config(config_file=str(args.config.resolve()))
    site = (args.site_dir or Path(config.site_dir)).resolve()
    targets = discover_pages(config)
    if args.keyboard_preflight:
        names = {'t-sne', 'umap', 'minhash-deduplication', 'data-programming'}
        targets = [t for t in targets if t.source.rsplit('/', 1)[-1].removesuffix('.md').removesuffix('.zh-TW') in names]
        assert len(targets) == 8, 'Keyboard preflight requires all four bilingual topics'
    report = {"pages": [asdict(target) for target in targets], "cases": [],
              "scope": "keyboard-preflight" if args.keyboard_preflight else "full"}
    args.output.mkdir(parents=True, exist_ok=True)
    try:
        for target in targets:
            check_built_page(site, target, config.site_url)
        print(f"Discovered {len(targets)} marked pages, {sum(len(t.images) for t in targets)} motion images")
        if args.discover_only:
            report["status"] = "discovery-only; browser checks not run"
            return 0
        from playwright.sync_api import sync_playwright

        with serve_site(site, config.site_url) as base_url, sync_playwright() as playwright:
            browser = playwright.chromium.launch(**({"executable_path": args.executable_path}
                                                     if args.executable_path else {}))
            try:
                for target in targets:
                    expected = check_built_page(site, target, base_url)
                    for name, viewport in VIEWPORTS.items():
                        if args.keyboard_preflight and viewport["width"] >= 600:
                            continue
                        for reduced in (False, True):
                            mode = "reduce" if reduced else "no-preference"
                            output = args.output / Path(target.source).with_suffix("") / f"{name}-{mode}"
                            output.mkdir(parents=True, exist_ok=True)
                            result = {"source": target.source, "url": urljoin(base_url, target.url),
                                      "viewport": viewport, "reduced_motion": mode,
                                      "artifact_directory": output.relative_to(args.output).as_posix()}
                            report["cases"].append(result)
                            try:
                                exercise_page(browser, target, expected, base_url, viewport, reduced, output, result)
                            except Exception as error:
                                result.update(status="failed", error=str(error))
                            print(f"{result['status'].upper()}: {target.source} {name} {mode}", flush=True)
            finally:
                browser.close()
        failures = [case for case in report["cases"] if case["status"] != "passed"]
        report["status"] = "failed" if failures else "passed"
        print(f"Built-page browser checks: {len(report['cases'])} cases, {len(failures)} failures")
        for failure in failures:
            print(f"{failure['source']}: {failure['error']}")
        return 1 if failures else 0
    except Exception as error:
        report.update(status="blocked-or-failed", error=str(error))
        raise
    finally:
        (args.output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
