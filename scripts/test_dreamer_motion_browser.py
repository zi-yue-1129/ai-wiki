#!/usr/bin/env python3
"""Chromium regression for Dreamer prior/posterior and lambda-return motion.

Requires Playwright and its Chromium browser. Use ANIMATION_ASSETS_DIR for local QA.
"""
from __future__ import annotations

import os
from pathlib import Path
from math import isclose
from playwright.sync_api import sync_playwright

ASSETS = Path(os.environ.get('ANIMATION_ASSETS_DIR', 'docs/assets/concept-animations'))
ARTIFACTS = Path('artifacts/dreamer-motion')
STEMS = ('dreamer-posterior-prior', 'dreamer-lambda-bootstrap')
WIDTHS = (320, 360, 720, 1024)
TIMES = (0, 2.5, 5, 8, 10.6)


def mount(page, source: str):
    page.set_content('<!DOCTYPE html><html><body style="margin:0">' + source + '</body></html>')
    assert page.locator('svg').count() == 1


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
    print('Dreamer Chromium QA: 48 stage/still screenshots, pause/resume/seek, '
          'text geometry, 8 exact reduced-motion fallback matches: PASS')


if __name__ == '__main__':
    main()
