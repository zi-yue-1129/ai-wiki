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

from motion_shard_contract import case_id, identity, manifest, partition, dpo_mobile

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
        assert alt and alt.strip(), f"{target.source}: marked motion image needs non-whitespace alt text"
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


MOBILE_PREFLIGHT_NAMES = frozenset({'t-sne', 'umap', 'minhash-deduplication',
    'data-programming', 'regularized-evolution', 'asam', 'shampoo'})


def check_math_rendering(page):
    """Reject rendered MathJax errors as well as incomplete/duplicate output."""
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
            trackedItems: MathJax.startup.document.getMathItemsWithin(article).length,
            // Error output still has mjx-container, so container counts alone pass.
            // Inspect rendered DOM/MathML, never prose containing the word "error".
            renderedErrors: Array.from(article.querySelectorAll(
                'mjx-merror, [data-mjx-error], merror, [data-mml-node="merror"]'
            )).map(node => ({
                tag: node.localName,
                message: node.getAttribute('data-mjx-error') || node.getAttribute('title') || node.textContent,
                html: node.outerHTML.slice(0, 1200)
            }))
        };
    }""")
    assert not state["renderedErrors"], ("rendered MathJax error", state)
    assert state["unrendered"] == 0, ("unrendered math source", state)
    assert state["nestedAssistive"] == 0, ("assistive MathML was typeset again", state)
    assert state["assistiveMathML"] == state["containers"], ("missing assistive MathML", state)
    assert state["trackedItems"] == state["containers"], ("rendered MathItems were forgotten", state)
    return state


def check_math_renderer_canary(browser, url, output):
    """Exercise the real site renderer in a disposable context before real cases.

    Valid -> invalid -> valid proves merror rejection even with a rendered
    container and proves the failure is cleared. No fake MathJax or injected
    renderer is used; only isolated TeX input is replaced on a real built page.
    """
    context = browser.new_context()
    page = context.new_page()
    result = {"status": "running", "scope": "isolated actual MathJax renderer canary"}
    render = r"""async tex => {
        const article = document.querySelector('.md-content__inner');
        MathJax.typesetClear([article]);
        const source = document.createElement('div');
        source.className = 'arithmatex';
        source.textContent = tex;
        article.replaceChildren(source);
        MathJax.texReset();
        await MathJax.typesetPromise([source]);
    }"""
    folder = output / 'math-renderer-canary'
    folder.mkdir(parents=True, exist_ok=True)
    try:
        response = page.goto(url, wait_until='load', timeout=45000)
        assert response and response.ok, 'Renderer canary built page unavailable'
        check_math_rendering(page)  # Also bounds startup settling before typesetPromise.
        page.evaluate(render, r'\[x^2 + 1\]')
        result['valid'] = check_math_rendering(page)
        assert result['valid']['containers'] == 1
        page.evaluate(render, r'\[\begin{definitelyUndefinedWikiAuditEnvironment}x\end{definitelyUndefinedWikiAuditEnvironment}\]')
        try:
            check_math_rendering(page)
        except AssertionError as error:
            if 'rendered MathJax error' not in str(error):
                raise
            invalid = error.args[0][1]
            assert invalid['containers'] > 0, 'Negative canary did not produce a rendered container'
            assert invalid['renderedErrors'], 'Negative canary did not produce a rendered error node'
            result['invalid_rejected'] = invalid
            page.screenshot(path=str(folder / 'invalid-rendered-error.png'))
        else:
            raise AssertionError('Invalid TeX renderer canary was incorrectly accepted')
        page.evaluate(render, r'\[\frac{1}{2} + x\]')
        result['cleared'] = check_math_rendering(page)
        assert result['cleared']['containers'] == 1
        result['status'] = 'passed'
        return result
    except Exception as error:
        result.update(status='failed', error=str(error))
        raise
    finally:
        try:
            (folder / 'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        finally:
            context.close()  # Never reuse the invalid-input document for real cases.


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


def responsive_asset_url(url, viewport):
    """Independent exact counterpart of the two production mobile variants."""
    if viewport['width'] <= 640:
        return re.sub(r'(?<=/)(icm-predictable-stochastic|rnd-state-novelty)-(motion|still)\.svg(?=$|[?#])',
                      r'\1-mobile-\2.svg', url)
    return url


def check_image(page, image, url):
    # Native lazy images must approach the viewport before waiting for decoding.
    # Do not rely on unrelated keyboard-scroller coverage to load later images.
    image.scroll_into_view_if_needed()
    # complete alone also becomes true for broken images, so check decoded size too.
    page.wait_for_function("""({alt, url}) => {
        const img = Array.from(document.images).find(img => img.alt === alt);
        return img && img.src === url && img.complete && img.naturalWidth > 0 && img.naturalHeight > 0;
    }""", arg={"alt": image.get_attribute("alt"), "url": url})
    assert image.is_visible(), ("image hidden", url)
    return image.evaluate("img => ({src: img.src, complete: img.complete, naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight})")


def check_co_design_timeline(page, image, host, output, index, record, viewport):
    """Inspect the visible, controllable SVG in a real built MkDocs page.

    The original image remains in the DOM as a no-script fallback but is
    intentionally hidden while the interactive SVG object is active. Unlike
    legacy GIF/SVG players, the visible state must be inspected via the object
    and its controls, not by scrolling the hidden fallback image into view.
    """
    from playwright.sync_api import expect

    frame = host.locator('object.distributed-motion-frame')
    expect(frame).to_have_count(1)
    expect(frame).to_be_visible()
    expect(image).to_be_hidden()
    assert frame.get_attribute('aria-label') == image.get_attribute('alt')
    fallback = frame.locator('img')
    expect(fallback).to_have_count(1)
    assert fallback.get_attribute('alt') == ''
    assert fallback.get_attribute('aria-hidden') == 'true'
    assert fallback.get_attribute('role') == 'presentation'
    assert page.get_by_alt_text(image.get_attribute('alt'), exact=True).count() == 1
    assert frame.get_attribute('data').endswith('-motion.svg')
    page.wait_for_function(
        '(el) => !!el.contentDocument?.documentElement?.getCurrentTime',
        arg=frame.element_handle(), timeout=15000)
    region = host.locator(
        "xpath=ancestor::*[contains(concat(' ', normalize-space(@class), ' '), ' concept-motion-scroll ')][1]")
    controls = region.locator(
        "xpath=following-sibling::*[contains(concat(' ', normalize-space(@class), ' '), ' co-design-motion-controls ')][1]")
    expect(controls).to_have_count(1)
    expect(controls).to_be_visible()
    expect(host.locator('.concept-motion-controls')).to_be_hidden()
    buttons = controls.locator('button.concept-motion-toggle')
    expect(buttons).to_have_count(4)  # Previous, Play/Pause, Next, Restart
    seek = controls.locator('input.distributed-motion-seek')
    rate = controls.locator('select.distributed-motion-rate')
    expect(seek).to_be_visible()
    expect(rate).to_be_visible()
    get_time = lambda: frame.evaluate(
        'e => e.contentDocument.documentElement.getCurrentTime()')
    assert get_time() < 0.1

    def capture(stage):
        frame.scroll_into_view_if_needed()
        document = assert_document_fits(page, viewport)
        screenshot = output / f'image-{index}-{stage}.png'
        svg_time = get_time()
        page.screenshot(path=str(screenshot))
        record['states'][stage] = {
            'screenshot': screenshot.name, 'document': document, 'svg_time': svg_time,
        }
        return screenshot.name

    # The text companion must explain the *mathematical state*, not only the
    # playback timestamp. The visible paragraph updates each frame, whereas
    # the screen-reader live region speaks only after user-triggered changes.
    interpretation = controls.locator('.distributed-motion-interpretation')
    expect(interpretation).to_be_visible()
    assert interpretation.get_attribute('aria-live') == 'off'
    stem = frame.get_attribute('data').rsplit('/', 1)[-1].removesuffix('-motion.svg')
    initial_tokens = {
        'checkpoint-spacing': ('s=1', '17'),
        'fp16-scaling-window': ('2^0', '1'),
        'gradscaler-feedback': ('t1', '1024'),
    }
    assert stem in initial_tokens, ('unexpected interactive motion asset', stem)
    initial_summary = interpretation.inner_text()
    assert all(token in initial_summary for token in initial_tokens[stem]), (stem, initial_summary)
    capture('initial')
    buttons.nth(2).click()  # Semantic next step
    assert controls.locator('.concept-motion-status').inner_text() == interpretation.inner_text()
    step_time = get_time()
    assert step_time > 0.5, ('next step did not advance SVG', step_time)
    seek.evaluate('e => {e.value = "750"; e.dispatchEvent(new Event("input", {bubbles:true}));}')
    seek_time = get_time()
    assert 8.95 <= seek_time <= 9.05, ('continuous seeking did not advance SVG', seek_time)
    selected_summary = interpretation.inner_text()
    selected_tokens = {
        'checkpoint-spacing': ('s=8', '10'),
        'fp16-scaling-window': ('2^6', '64'),
        'gradscaler-feedback': ('t5', '1024'),
    }
    assert all(token in selected_summary for token in selected_tokens[stem]), (stem, selected_summary)
    assert controls.locator('.concept-motion-status').inner_text() == selected_summary
    rate.select_option('2')
    assert rate.input_value() == '2'
    buttons.nth(1).click()  # Play at 2x
    page.wait_for_timeout(240)
    advanced = get_time()
    assert advanced > seek_time + 0.08, ('SVG timeline did not play', seek_time, advanced)
    buttons.nth(1).click()  # Pause
    paused = get_time()
    page.wait_for_timeout(120)
    assert abs(get_time() - paused) < 0.03, 'SVG timeline moved while paused'
    capture('paused')
    buttons.nth(0).click()  # Previous semantic step
    previous = get_time()
    assert previous < paused - 0.05, ('previous step did not seek backward', paused, previous)
    # Resume through the real keyboard control, and prove this is a new
    # playing state rather than another capture of the paused frame.
    buttons.nth(1).focus()
    page.keyboard.press('Enter')
    page.wait_for_function(
        '([el, start]) => el.contentDocument.documentElement.getCurrentTime() > start + 0.08',
        arg=[frame.element_handle(), previous], timeout=5000)
    replay_screenshot = capture('replayed')
    buttons.nth(1).click()  # Leave the player paused before testing the next image.
    # Restart must reset both the accessible interpretation and SVG position.
    buttons.nth(3).focus()
    page.keyboard.press('Enter')
    reset_time = get_time()
    assert reset_time < 0.08, ('restart did not rewind SVG', reset_time)
    assert seek.input_value() == '0', ('restart did not reset seek', seek.input_value())
    assert controls.locator('.concept-motion-status').inner_text() == interpretation.inner_text()
    # Headless Chromium does not hide background tabs; simulate the DOM
    # visibility transition to exercise its pause and no-auto-resume logic.
    seek.evaluate('e => {e.value = "750"; e.dispatchEvent(new Event("input", {bubbles:true}));}')
    buttons.nth(1).click()
    page.wait_for_timeout(110)
    page.evaluate("""() => {
        Object.defineProperty(document, 'hidden', {configurable:true, get:()=>true});
        document.dispatchEvent(new Event('visibilitychange'));
    }""")
    hidden_pause_time = get_time()
    page.wait_for_timeout(150)
    assert abs(get_time() - hidden_pause_time) < 0.03, 'hidden-tab pause did not hold SVG state'
    assert 'Ⅱ' not in buttons.nth(1).inner_text(), 'backgrounded animation still playing'
    page.evaluate("""() => {
        delete document.hidden;
        document.dispatchEvent(new Event('visibilitychange'));
    }""")
    page.wait_for_timeout(120)
    assert abs(get_time() - hidden_pause_time) < 0.03, 'animation auto-resumed after tab return'
    record['interactive'] = {
        'reset_time': reset_time, 'hidden_pause_time': hidden_pause_time,
        'visible_svg': True, 'hidden_no_script_fallback': True,
        'unique_alt': True, 'step_time': step_time,
        'seek_time': seek_time, 'playing_time': advanced,
        'paused_time': paused, 'previous_time': previous, 'speed': 2,
        'semantic_initial': initial_summary, 'semantic_seek': selected_summary,
        'screenshot': replay_screenshot,
    }


def check_lazy_image_canary(browser, url, output):
    """Prove native lazy loading and broken-image rejection in isolated Chromium."""
    from playwright.sync_api import TimeoutError as BrowserTimeoutError
    context = browser.new_context(viewport=VIEWPORTS['mobile'])
    page = context.new_page()
    folder = output / 'lazy-image-canary'
    folder.mkdir(parents=True, exist_ok=True)
    result = {'status': 'running', 'scope': 'isolated native lazy image canary'}
    try:
        response = page.goto(url, wait_until='load', timeout=45000)
        assert response and response.ok
        image_url = urljoin(url, '__isolated_lazy_canary__.svg')
        broken_url = urljoin(url, '__isolated_broken_canary__.svg')
        page.route(image_url, lambda route: route.fulfill(status=200, content_type='image/svg+xml',
            body='<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360"><rect width="640" height="360" fill="teal"/></svg>'))
        page.route(broken_url, lambda route: route.fulfill(status=200, content_type='image/svg+xml', body='not an SVG'))
        page.evaluate('''src => {
            document.body.replaceChildren();
            const spacer = document.createElement('div'); spacer.style.height = '20000px';
            const img = document.createElement('img'); img.alt = 'Isolated native lazy canary';
            img.loading = 'lazy'; img.width = 320; img.height = 180; img.src = src;
            document.body.append(spacer, img); scrollTo(0, 0);
        }''', image_url)
        image = page.get_by_alt_text('Isolated native lazy canary', exact=True)
        page.wait_for_timeout(250)
        result['before_scroll'] = image.evaluate('img => ({top: img.getBoundingClientRect().top, complete: img.complete, naturalWidth: img.naturalWidth})')
        assert result['before_scroll']['top'] > 10000
        assert result['before_scroll']['naturalWidth'] == 0, 'Negative lazy fixture loaded before scrolling'
        page.set_default_timeout(5000)
        result['after_scroll'] = check_image(page, image, image_url)
        assert result['after_scroll']['naturalWidth'] == 640
        page.screenshot(path=str(folder / 'loaded-after-scroll.png'))
        image.evaluate('(img, src) => img.src = src', broken_url)
        page.set_default_timeout(1000)
        try:
            check_image(page, image, broken_url)
        except BrowserTimeoutError:
            result['broken_rejected'] = True
        else:
            raise AssertionError('Broken image incorrectly accepted')
        result['status'] = 'passed'
        return result
    except Exception as error:
        result.update(status='failed', error=str(error))
        raise
    finally:
        try:
            (folder / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
        finally:
            context.close()


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


MOTION_SCROLL_DISCOVERY_JS = r"""() => {
    const article = document.querySelector('.md-content__inner');
    if (!article) throw new Error('Built article missing during scroll discovery');
    const found = new Set();
    for (const img of article.querySelectorAll('img[data-concept-motion-enhanced="yes"]')) {
        for (let node = img.parentElement; node; node = node.parentElement) {
            const overflow = getComputedStyle(node).overflowX;
            if ((overflow === 'auto' || overflow === 'scroll') && node.scrollWidth > node.clientWidth + 2) {
                found.add(node); // Do not prefilter tabindex: inaccessible regions must fail below.
            }
            if (node === article) break;
        }
    }
    return Array.from(found);
}"""


def check_keyboard_scrollers(page, output=None):
    """Discover actual overflowing ancestors, exercise native keys, retain right edges."""
    measured = []
    array = page.evaluate_handle(MOTION_SCROLL_DISCOVERY_JS)
    try:
        properties = array.get_properties()
        regions = [properties[key].as_element() for key in sorted(properties, key=lambda k: int(k) if k.isdigit() else -1)
                   if key.isdigit()]
        for index, region in enumerate(regions, 1):
            assert region is not None, 'Scroll discovery did not return a DOM element'
            if not region.is_visible():
                continue
            bounds = region.evaluate('(e) => ({clientWidth: e.clientWidth, scrollWidth: e.scrollWidth})')
            if bounds['scrollWidth'] <= bounds['clientWidth'] + 2:
                continue
            assert region.get_attribute('tabindex') == '0', 'Overflowing motion region lacks tabindex=0'
            region.evaluate('(e) => e.scrollTo({left: 0, behavior: "instant"})')
            region.focus()
            assert region.evaluate('(e) => document.activeElement === e'), 'Scroll region cannot receive focus'
            region.press('ArrowRight')
            page.wait_for_function('(e) => e.scrollLeft > 0', arg=region, timeout=2000)
            bounds['afterArrowRight'] = settled_scroll_left(region)
            assert bounds['afterArrowRight'] > 0, 'Keyboard scroll did not remain moved'
            if output is not None:
                region.scroll_into_view_if_needed()
                region.evaluate('(e) => e.scrollTo({left: e.scrollWidth, behavior: "instant"})')
                bounds['rightEdge'] = settled_scroll_left(region)
                assert bounds['rightEdge'] >= bounds['scrollWidth'] - bounds['clientWidth'] - 1, 'Scroll region cannot reach right edge'
                screenshot = output / f'scroll-region-{index}-right.png'
                page.screenshot(path=str(screenshot))
                bounds['rightEdgeScreenshot'] = screenshot.name
            region.evaluate('(e) => { e.blur(); e.scrollTo({left: 0, behavior: "instant"}); }')
            assert settled_scroll_left(region) == 0, 'Scroll region did not reset'
            measured.append(bounds)
    finally:
        array.dispose()
    return measured


DPO_REWARD_SELECTOR_JS = r"""(elements, expected) => {
    const compact = value => value.replace(/\s+/g, '');
    const matches = [];
    elements.forEach((element, index) => {
        const root = element.closest('.arithmatex');
        if (!root) throw new Error('Display lacks its MathJax source wrapper');
        const items = MathJax.startup.document.getMathItemsWithin(root);
        if (items.length === 1 && typeof items[0].math === 'string' && compact(items[0].math) === compact(expected)) matches.push(index);
    });
    if (matches.length !== 1) throw new Error('Missing or ambiguous exact DPO reward identity');
    return matches[0];
}"""


def check_dpo_reward_identity(browser, page, url, viewport, reduced, output, record):
    """Measure the real built MathJax identity and reproduce its old inline overflow.

    Only the four existing bilingual mobile cases call this. Original image-state
    checks and screenshots remain unchanged. The negative page is disposable.
    """
    from motion_shard_contract import DPO_REWARD_TEX, validate_dpo_reward_measurement
    displays=page.locator('.md-content__inner mjx-container[display="true"]')
    reward_index=displays.evaluate_all(DPO_REWARD_SELECTOR_JS, DPO_REWARD_TEX)
    formula=displays.nth(reward_index)
    assert formula.count()==1, 'Missing display reward identity'
    formula.scroll_into_view_if_needed()
    assert formula.is_visible()
    record.update(formula.evaluate("""e => {
      const rect=e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}};
      const root=e.closest('.arithmatex');const items=MathJax.startup.document.getMathItemsWithin(root);
      if(items.length!==1)throw new Error('Ambiguous rendered reward identity');
      return {tex:items[0].math,display:e.getAttribute('display')==='true',visible:!!e.getClientRects().length,
        math:rect(e.querySelector('mjx-math')),article:rect(document.querySelector('.md-content__inner'))};
    }"""))
    record['document']=assert_document_fits(page,viewport)
    record['screenshot']='dpo-reward-identity.png'
    page.screenshot(path=str(output/record['screenshot']))
    context=browser.new_context(viewport=viewport,device_scale_factor=1,is_mobile=True,has_touch=True,
                                reduced_motion='reduce' if reduced else 'no-preference',color_scheme='light')
    negative=context.new_page();errors=[]
    negative.on('pageerror',lambda error:errors.append(str(error)))
    try:
        response=negative.goto(url,wait_until='load',timeout=45000)
        assert response and response.ok
        check_math_rendering(negative);negative.evaluate('document.fonts.ready')
        assert_document_fits(negative,viewport)  # No pre-existing overflow may stand in for this canary.
        old_tex=r'\(r(x, y) = \beta \log(\pi_r(y \mid x)/\pi_{\text{ref}}(y \mid x)) + \beta \log Z(x)\)'
        negative.evaluate(r"""async tex => {
          const article=document.querySelector('.md-content__inner');MathJax.typesetClear([article]);
          const p=document.createElement('p'),span=document.createElement('span');span.className='arithmatex';
          span.textContent=tex;p.append(span);article.replaceChildren(p);MathJax.texReset();await MathJax.typesetPromise([span]);
        }""",old_tex)
        check_math_rendering(negative);negative.evaluate('document.fonts.ready')
        old=negative.evaluate("""() => ({inner:innerWidth,client:document.documentElement.clientWidth,width:document.documentElement.scrollWidth,
          mathRight:document.querySelector('.md-content__inner mjx-math').getBoundingClientRect().right,
          display:document.querySelector('.md-content__inner mjx-container').getAttribute('display')==='true',rejected:false})""")
        record['original_inline']=old
        try:assert_document_fits(negative,viewport)
        except AssertionError:old['rejected']=True
        else:raise AssertionError('Original DPO inline formula did not reproduce viewport overflow')
        assert not errors,errors
        record['old_inline_screenshot']='dpo-original-inline.png'
        negative.screenshot(path=str(output/record['old_inline_screenshot']))
    finally:
        try:
            negative.screenshot(path=str(output/'dpo-original-inline.png'))
            (output/'dpo-reward-measurement.json').write_text(json.dumps(record,indent=2))
        finally:context.close()
    record['status']='passed'
    validate_dpo_reward_measurement(record,viewport)
    (output/'dpo-reward-measurement.json').write_text(json.dumps(record,indent=2))
    return record


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
        if dpo_mobile(target.source, viewport):
            result["dpo_reward_identity"] = {"status":"running"}
            check_dpo_reward_identity(browser, page, urljoin(base_url,target.url), viewport, reduced, output, result["dpo_reward_identity"])
        # Discovery uses enhanced targets; wait for every expected player before
        # enumerating ancestors so delayed initialization cannot yield an empty pass.
        for asset in expected:
            expected_image = page.get_by_alt_text(asset["alt"], exact=True)
            expect(expected_image).to_have_count(1)
            expect(expected_image).to_have_attribute("data-concept-motion-enhanced", "yes")
        result['keyboard_scroll'] = check_keyboard_scrollers(page, output)
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
            host = image.locator("xpath=ancestor::*[contains(concat(' ', normalize-space(@class), ' '), ' concept-motion-player ')][1]")
            # Three co-design diagrams are enhanced into same-origin, seekable
            # SVG objects. Their original <img> is deliberately hidden while
            # playing; the legacy image/toggle contract applies to all other
            # diagrams and to the reduced-motion still-image fallback.
            interactive_names = {
                'checkpoint-spacing-motion.svg',
                'fp16-scaling-window-motion.svg',
                'gradscaler-feedback-motion.svg',
            }
            if not reduced and any(asset['motion'].split('?', 1)[0].endswith(name)
                                   for name in interactive_names):
                record = {'alt': asset['alt'], 'states': {}}
                result['images'].append(record)
                check_co_design_timeline(page, image, host, output, index,
                                         record, viewport)
                continue
            toggle = host.locator(".concept-motion-toggle").first
            chinese = bool(re.search(r"[\u3400-\u9fff]", asset["alt"]))
            play = "播放概念動畫" if chinese else "Play concept animation"
            pause = "暫停概念動畫" if chinese else "Pause concept animation"
            record = {"alt": asset["alt"], "states": {}}
            result["images"].append(record)

            def capture(stage, state, label):
                expect(toggle).to_have_attribute("aria-label", label)
                record["states"][stage] = check_image(page, image, responsive_asset_url(asset[state], viewport))
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
                check_image(page, image, responsive_asset_url(asset["motion"], viewport))
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
                        help="Check seven bilingual keyboard/math topics on mobile before the separate full suite")
    parser.add_argument("--discover-only", action="store_true", help="Validate discovery and built attributes without Chromium")
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--executable-path", help="Optional local Chromium; CI uses Playwright's pinned browser")
    args = parser.parse_args()
    config = load_config(config_file=str(args.config.resolve()))
    site = (args.site_dir or Path(config.site_dir)).resolve()
    targets = discover_pages(config)
    full_manifest = manifest(targets, VIEWPORTS, identity())
    if args.keyboard_preflight and (args.shard_index != 0 or args.shard_count != 1):
        parser.error('Preflight stays complete and cannot be sharded')
    assigned = set(partition(full_manifest['expected_case_ids'], args.shard_index, args.shard_count))
    if args.keyboard_preflight:
        # Retain native-scroll regressions and fail fast on the new formula-overflow pages.
        names = MOBILE_PREFLIGHT_NAMES
        targets = [t for t in targets if t.source.rsplit('/', 1)[-1].removesuffix('.md').removesuffix('.zh-TW') in names]
        assert len(targets) == 14, 'Mobile preflight requires all seven bilingual topics'
    report = {"pages": [asdict(target) for target in targets], "cases": [],
              "scope": "keyboard-preflight" if args.keyboard_preflight else "full",
              "identity": full_manifest['identity'], "manifest_sha256": full_manifest['sha256'],
              "shard_index": args.shard_index, "shard_count": args.shard_count}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "discovery-manifest.json").write_text(json.dumps(full_manifest, ensure_ascii=False, indent=2)+"\n")
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
                report["math_renderer_canary"] = check_math_renderer_canary(
                    browser, urljoin(base_url, targets[0].url), args.output)
                report["lazy_image_canary"] = check_lazy_image_canary(
                    browser, urljoin(base_url, targets[0].url), args.output)
                for target in targets:
                    expected = check_built_page(site, target, base_url)
                    for name, viewport in VIEWPORTS.items():
                        if args.keyboard_preflight and viewport["width"] >= 600:
                            continue
                        for reduced in (False, True):
                            mode = "reduce" if reduced else "no-preference"
                            current_id = case_id(target.source, viewport, mode)
                            if current_id not in assigned:
                                continue
                            output = args.output / Path(target.source).with_suffix("") / f"{name}-{mode}"
                            output.mkdir(parents=True, exist_ok=True)
                            result = {"case_id": current_id, "source": target.source, "url": urljoin(base_url, target.url),
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
        if not args.keyboard_preflight:
            assert {c['case_id'] for c in report['cases']} == assigned, 'Incomplete assigned coverage'
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
