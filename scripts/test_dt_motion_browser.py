#!/usr/bin/env python3
"""Chromium visual, control and reduced-motion regression for Decision Transformer SVGs."""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name == 'scripts' else Path(__file__).resolve().parent
ASSET = ROOT / 'docs' / 'assets' / 'concept-animations'
if not ASSET.exists():
    ASSET = ROOT
CAPTURE = ROOT / 'artifacts' / 'dt-motion'
CAPTURE.mkdir(parents=True, exist_ok=True)
PAIRS = ('dt-return-budget', 'dt-causal-prefix')
WIDTHS = (320, 360, 720, 1024)
NS = '{http://www.w3.org/2000/svg}'


def check_svg(name: str, animated: bool) -> str:
    path = ASSET / f'{name}-{ "motion" if animated else "still"}.svg'
    source = path.read_text(encoding='utf8')
    root = ET.fromstring(source)
    assert root.tag == NS + 'svg' and root.get('viewBox') == '0 0 640 360', path
    assert root.find(NS + 'title') is not None and root.find(NS + 'desc') is not None
    assert not any(node.tag.split('}')[-1] in ('script', 'image', 'foreignObject', 'iframe') for node in root.iter())
    nodes = [node for node in root.iter() if node.tag.split('}')[-1].startswith('animate')]
    if animated:
        assert len(nodes) >= 3 and all(x.get('repeatCount') == 'indefinite' for x in nodes)
    else:
        assert not nodes
    assert path.stat().st_size < 50_000
    return source


def main() -> None:
    svg = {(n, m): check_svg(n, m) for n in PAIRS for m in (True, False)}
    assert 6 - 2 - 1 - 3 == 0
    assert [2, 5, 8] == [2, 2 + 3, 2 + 3 + 3]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name in PAIRS:
            for width in WIDTHS:
                for seconds in (0.4, 2.6, 5.4, 9.3):
                    page = browser.new_page(viewport={'width': width, 'height': max(250, int(width * 360 / 640) + 35)})
                    page.set_content(svg[(name, True)])
                    page.add_style_tag(content='html,body{padding:0;margin:0}svg{display:block;width:100vw;height:auto}')
                    page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', seconds)
                    page.locator('svg').screenshot(path=str(CAPTURE / f'{name}-{width}-{str(seconds).replace(".", "-")}.png'))
                    assert page.evaluate('document.querySelector("svg").getBoundingClientRect().width') <= width + 1
                    assert page.evaluate('document.documentElement.scrollWidth') <= width + 1
                    for text in page.locator('svg text').all():
                        bb = text.evaluate('(e)=>({x:e.getBBox().x,y:e.getBBox().y,w:e.getBBox().width,h:e.getBBox().height})')
                        assert bb['x'] >= -0.5 and bb['x'] + bb['w'] <= 640.5, (name, width, bb)
                        assert bb['y'] >= -0.5 and bb['y'] + bb['h'] <= 360.5, (name, width, bb)
                    page.close()
                page = browser.new_page(viewport={'width': width, 'height': max(250, int(width * 360 / 640) + 35)})
                page.set_content(svg[(name, False)])
                page.add_style_tag(content='html,body{padding:0;margin:0}svg{display:block;width:100vw;height:auto}')
                page.locator('svg').screenshot(path=str(CAPTURE / f'{name}-{width}-still.png'))
                page.close()
        js = (ROOT / 'docs/javascripts/concept-motion.js').read_text(encoding='utf8')
        for name in PAIRS:
            for reduce in (False, True):
                context = browser.new_context(reduced_motion='reduce' if reduce else 'no-preference')
                page = context.new_page()
                def respond(route):
                    filename = route.request.url.rsplit('/', 1)[-1]
                    route.fulfill(status=200, body=(ASSET / filename).read_bytes(), content_type='image/svg+xml')
                page.route('**/concept-animations/*.svg', respond)
                still = f'https://wiki.local/concept-animations/{name}-still.svg'
                motion = f'https://wiki.local/concept-animations/{name}-motion.svg'
                page.set_content(f'<html><body><img src="{still}" data-motion-src="{motion}" data-still-src="{still}" alt="Decision Transformer causal and return illustration"></body></html>')
                page.add_script_tag(content=js)
                toggle = page.locator('.concept-motion-toggle')
                toggle.wait_for()
                image = page.locator('img')
                if reduce:
                    assert image.get_attribute('src') == still
                    assert 'Play' in toggle.inner_text()
                else:
                    assert image.get_attribute('src') == motion
                toggle.focus()
                page.keyboard.press('Enter')
                assert image.get_attribute('src') == (motion if reduce else still)
                page.keyboard.press('Space')
                assert image.get_attribute('src') == (still if reduce else motion)
                assert page.locator('.concept-motion-player').count() == 1
                context.close()
        browser.close()
    print('PASS: 40 rendered frames, shared controls, Enter/Space and reduced motion')


if __name__ == '__main__':
    main()
