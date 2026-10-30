#!/usr/bin/env python3
"""Render and exercise original GPipe/FSDP motion pairs in real Chromium.

Requires playwright and installed Chromium. Set CHROMIUM_EXECUTABLE for system Chrome.
"""
from __future__ import annotations

import os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
ASSETS = DOCS / 'assets' / 'concept-animations'
STEMS = ('gpipe-fill-drain', 'fsdp-gather-scatter')
OUT = ROOT / 'distributed-motion-screenshots'
NS = '{http://www.w3.org/2000/svg}'


def validate_structure():
    for stem in STEMS:
        for kind in ('motion', 'still'):
            p = ASSETS / f'{stem}-{kind}.svg'
            assert p.is_file(), p
            assert p.stat().st_size < 50 * 1024, p
            svg = ET.parse(p).getroot()
            assert svg.tag == NS + 'svg' and svg.get('viewBox') == '0 0 640 360'
            assert svg.find(NS + 'title') is not None and svg.find(NS + 'desc') is not None
            motions = [n for n in svg.iter() if n.tag.split('}')[-1] in ('animate', 'animateTransform', 'animateMotion')]
            assert bool(motions) == (kind == 'motion'), (p, len(motions))
            for node in svg.iter():
                tag = node.tag.split('}')[-1]
                assert tag not in {'script', 'foreignObject', 'iframe', 'image'}
                assert not any(k.split('}')[-1].startswith('on') for k in node.attrib)
                if tag in ('animate', 'animateTransform', 'animateMotion'):
                    assert node.get('repeatCount') == 'indefinite'
        for lang in ('.md', '.zh-TW.md'):
            page = DOCS / 'engineering' / 'distributed-training' / ('gpipe' if stem.startswith('gpipe') else 'fsdp')
            content = page.with_suffix(lang).read_text(encoding='utf-8')
            assert f'{stem}-motion.svg' in content and f'{stem}-still.svg' in content
            assert 'CC BY-SA 4.0' in content


def main():
    validate_structure()
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        launch = {'headless': True, 'args': ['--no-sandbox']}
        if os.environ.get('CHROMIUM_EXECUTABLE'):
            launch['executable_path'] = os.environ['CHROMIUM_EXECUTABLE']
        browser = pw.chromium.launch(**launch)
        for stem in STEMS:
            for width in (360, 900):
                for reduce in (False, True):
                    context = browser.new_context(viewport={'width': width, 'height': 550}, reduced_motion='reduce' if reduce else 'no-preference')
                    page = context.new_page()
                    def handle(route):
                        name = route.request.url.split('/')[-1]
                        route.fulfill(status=200, content_type='image/svg+xml', body=(ASSETS / name).read_bytes())
                    page.route('**/concept-animations/*.svg', handle)
                    css = (DOCS / 'stylesheets' / 'concept-motion.css').read_text() + '\n' + (DOCS / 'stylesheets' / 'extra.css').read_text()
                    html = f'<html><head><style>body{{margin:12px;max-width:800px}}{css}</style></head><body><img alt="{stem} animation" src="https://example.invalid/concept-animations/{stem}-motion.svg"></body></html>'
                    page.set_content(html)
                    page.add_script_tag(content=(DOCS / 'javascripts' / 'concept-motion.js').read_text())
                    button = page.locator('.concept-motion-toggle')
                    assert button.count() == 1, stem
                    img = page.locator('.concept-motion-player img')
                    expected = 'still' if reduce else 'motion'
                    assert f'-{expected}.svg' in img.get_attribute('src')
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (stem,width,'overflow')
                    if width == 360:
                        assert page.evaluate("document.querySelector('.concept-motion-player').scrollWidth >= 640")
                    page.screenshot(path=str(OUT / f'{stem}-{width}-reduced-{reduce}.png'))
                    button.focus()
                    page.keyboard.press('Space')
                    expected = 'motion' if reduce else 'still'
                    assert f'-{expected}.svg' in img.get_attribute('src'), (stem,reduce)
                    page.close()
                    context.close()
            # Inline SVG permits direct geometry and actual animation-timeline checks.
            page = browser.new_page(viewport={'width': 900, 'height': 550})
            markup = (ASSETS / f'{stem}-motion.svg').read_text()
            page.set_content('<style>svg{width:640px;height:360px}</style>'+markup)
            bad = page.evaluate("""() => [...document.querySelectorAll('svg text')].filter(el => {let b=el.getBBox();return b.x < 0 || b.y < 0 || b.x+b.width > 640 || b.y+b.height > 360}).map(el=>el.textContent)""")
            assert not bad, (stem,bad)
            if stem.startswith('gpipe'):
                first = page.evaluate("document.querySelector('#elapsed rect').width.animVal.value")
                page.wait_for_timeout(600)
                later = page.evaluate("document.querySelector('#elapsed rect').width.animVal.value")
                assert later > first + 10, (first,later)
            else:
                assert page.locator('svg animateTransform').count() >= 3
                # A full-shard unit gathers for forward and backward, but
                # must release temporary copies between the two phases.
                for t, present in ((0.2, False), (2.8, True), (4.5, False), (6.6, True), (8.1, False)):
                    opacity = page.evaluate("""t => { const s=document.querySelector('svg'); s.setCurrentTime(t); return +getComputedStyle(s.querySelector('g[opacity]')).opacity }""", t)
                    assert (opacity > .9) == present, (t, opacity)
                scatter = page.evaluate("""() => +getComputedStyle(document.querySelectorAll('svg circle')[2]).opacity""")
                assert scatter > .5, scatter
            page.close()
            print(f'{stem}: structure, motion, 360/900px, keyboard and reduced-motion checks passed')
        browser.close()


if __name__ == '__main__':
    main()
