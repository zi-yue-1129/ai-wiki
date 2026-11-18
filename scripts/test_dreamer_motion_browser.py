#!/usr/bin/env python3
"""Chromium regression for Dreamer prior/posterior and lambda-return motion.

Requires Playwright and its Chromium browser. Use ANIMATION_ASSETS_DIR for local QA.
"""
from __future__ import annotations

import os
import json
from xml.etree import ElementTree as ET
from pathlib import Path
from math import isclose
from playwright.sync_api import sync_playwright

ASSETS = Path(os.environ.get('ANIMATION_ASSETS_DIR', 'docs/assets/concept-animations'))
ARTIFACTS = Path('artifacts/dreamer-motion')
STEMS = ('dreamer-posterior-prior', 'dreamer-lambda-bootstrap')
WIDTHS = (320, 360, 720, 1024)
TIMES = (0, 2, 2.5, 2.9, 5, 5.5, 8, 8.1, 10.6)


def inline_svg(source):
    root = ET.fromstring(source)
    if root.tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError('Expected SVG namespace root')
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    return ET.tostring(root, encoding='unicode')


MOUNT_SVG_JS = r"""source => {
    const xml = new DOMParser().parseFromString(source, 'image/svg+xml');
    if (xml.querySelector('parsererror')) throw new Error('Invalid SVG XML');
    const root = xml.documentElement;
    if (root.localName !== 'svg' || root.namespaceURI !== 'http://www.w3.org/2000/svg')
        throw new Error('Expected one SVG namespace root');
    document.body.replaceChildren(document.importNode(root, true));
}"""


def mount(page, source: str):
    try:
        page.set_content('<!DOCTYPE html><html><body style="margin:0"></body></html>')
        page.evaluate(MOUNT_SVG_JS, inline_svg(source))
        assert page.locator('svg').count() == 1
        assert page.locator('svg').evaluate("s=>s.namespaceURI") == 'http://www.w3.org/2000/svg'
    except Exception as error:
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        (ARTIFACTS / 'mount-failure.json').write_text(json.dumps({'status': 'failed', 'error': repr(error), 'source_prefix': source[:200], 'viewport': page.viewport_size}))
        (ARTIFACTS / 'mount-failure.html').write_text(page.content())
        page.screenshot(path=str(ARTIFACTS / 'mount-failure.png'))
        raise


def namespace_canary(page):
    # The original XML-prefix/HTML-parser mismatch must really reproduce in Chromium.
    source = '<ns0:svg xmlns:ns0="http://www.w3.org/2000/svg" viewBox="0 0 640 360"><ns0:text x="10" y="20">Namespace canary</ns0:text></ns0:svg>'
    page.set_content('<!doctype html><body>' + source)
    assert page.locator('svg').count() == 0, 'Old prefixed HTML fixture unexpectedly mounted'
    mount(page, source)
    assert page.locator('svg text').count() == 1
    assert page.locator('svg').evaluate("s=>typeof s.setCurrentTime") == 'function'
    (ARTIFACTS / 'namespace-canary.json').write_text(json.dumps({'status': 'passed', 'old_html_svg_count': 0, 'xml_import_svg_count': 1, 'native_smil_api': True}))
    page.screenshot(path=str(ARTIFACTS / 'namespace-canary.png'))


def bad_text_bounds(root):
    return root.evaluate("""(s)=>Array.from(s.querySelectorAll('text')).filter(t=>{
      const b=t.getBBox();return b.x<-1||b.y<-1||b.x+b.width>641||b.y+b.height>361
    }).map(t=>t.textContent)""")


def collisions(root):
    return root.evaluate("""(s)=>{
      let texts=[...s.querySelectorAll('text')].map(e=>[e.textContent.trim(),e.getBBox()]);
      let pairs=[];
      for(let i=0;i<texts.length;i++) for(let j=i+1;j<texts.length;j++){
        let a=texts[i][1], b=texts[j][1];
        const dx=Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x);
        const dy=Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y);
        if(dx>2 && dy>2) pairs.push([texts[i][0],texts[j][0]]);
      }
      return pairs;
    }""")


def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        args = {'headless': True}
        if os.getenv('PLAYWRIGHT_CHROMIUM_EXECUTABLE'):
            args['executable_path'] = os.getenv('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
            args['args'] = ['--no-sandbox']
        browser = playwright.chromium.launch(**args)
        canary = browser.new_page()
        try:
            namespace_canary(canary)
        finally:
            canary.close()
        for stem in STEMS:
            motion = (ASSETS / f'{stem}-motion.svg').read_text(encoding='utf-8')
            still = (ASSETS / f'{stem}-still.svg').read_text(encoding='utf-8')
            for width in WIDTHS:
                height = int(width * 360 / 640) + 8
                page = browser.new_page(viewport={'width': width, 'height': height})
                mount(page, motion)
                svg = page.locator('svg')
                svg.evaluate('(s)=>s.pauseAnimations()')
                for i, t in enumerate(TIMES):
                    svg.evaluate('(s,t)=>s.setCurrentTime(t)', t)
                    # Read actual Chromium SMIL opacity, not just source keyTimes.
                    state = svg.evaluate("""(s)=>({
                      rings:[...s.querySelectorAll('[data-arrival]')].map(e=>({arrival:Number(e.dataset.arrival),opacity:Number(getComputedStyle(e).opacity)})),
                      masks:[...s.querySelectorAll('[data-return-mask]')].map(e=>({index:Number(e.dataset.returnMask),opacity:Number(getComputedStyle(e).opacity)}))
                    })""")
                    for ring in state['rings']:
                        if t / 12 < ring['arrival']:
                            assert ring['opacity'] < .001, (stem, width, t, 'early state highlight', ring)
                    for mask in state['masks']:
                        arrival = (3.1 + (2-mask['index'])*3) / 12
                        if t / 12 < arrival:
                            assert mask['opacity'] > .999, (stem, width, t, 'early return', mask)
                        elif arrival + .025 <= t / 12 <= .95:
                            assert mask['opacity'] < .001, (stem, width, t, 'missing completed return', mask)
                    assert not bad_text_bounds(svg), (stem, width, t, 'off canvas')
                    svg.screenshot(path=str(ARTIFACTS / f'{stem}-{width}-{i}.png'))
                svg.evaluate('(s)=>s.setCurrentTime(4)')
                old_time = svg.evaluate('(s)=>s.getCurrentTime()')
                page.wait_for_timeout(120)
                assert isclose(old_time, svg.evaluate('(s)=>s.getCurrentTime()'), abs_tol=.05)
                svg.evaluate('(s)=>s.unpauseAnimations()')
                page.wait_for_timeout(180)
                assert svg.evaluate('(s)=>s.getCurrentTime()') > old_time + .06
                mount(page, still)
                assert not bad_text_bounds(page.locator('svg'))
                assert not collisions(page.locator('svg')), (stem, width, 'text overlap')
                page.locator('svg').screenshot(path=str(ARTIFACTS / f'{stem}-{width}-still.png'))
                page.close()
                reduced = browser.new_page(viewport={'width': width, 'height': height}, reduced_motion='reduce')
                mount(reduced, motion)
                reduced.locator('svg').evaluate('(s)=>{s.pauseAnimations();s.setCurrentTime(8)}')
                reduced_png = reduced.locator('svg').screenshot()
                mount(reduced, still)
                still_png = reduced.locator('svg').screenshot()
                assert reduced_png == still_png, (stem, width, 'reduced-motion differs from still')
                reduced.close()
        browser.close()
    print('Dreamer Chromium QA: 80 stage/still screenshots, pause/resume/seek, '
          'text geometry, 8 exact reduced-motion fallback matches: PASS')


if __name__ == '__main__':
    main()
