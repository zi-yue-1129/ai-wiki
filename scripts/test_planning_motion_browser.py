#!/usr/bin/env python3
"""Chromium regression for bilingual STRIPS/Graphplan SVG motion and shared player.

Uses real repository assets and the site's actual concept-motion.js/CSS. The standalone
SVGs are rendered directly (no network); player state transitions are checked in a
controlled HTML fixture, with no claim of publicly deployed-site coverage.
"""
from __future__ import annotations

import os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / 'docs').exists():
    ROOT = Path('/mnt/data/aiwiki_planning_20261113')
ASSETS = ROOT / 'docs/assets/concept-animations'
if not ASSETS.exists():
    ASSETS = ROOT
STEMS = ('strips-state-effects', 'graphplan-layer-extraction')


def test_svg(page, stem):
    raw = (ASSETS / f'{stem}-motion.svg').read_text(encoding='utf-8')
    ET.fromstring(raw)
    page.set_content(raw, wait_until='load')
    assert page.locator('svg').count() == 1
    for second in (0, 2.5, 5, 7.5):
        page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', second)
        page.wait_for_timeout(80)
        bad = page.evaluate('''() => [...document.querySelectorAll('svg text')].map(t => {
          const b=t.getBBox(); return [t.textContent,b.x,b.y,b.x+b.width,b.y+b.height];
        }).filter(b => b[1]<-1 || b[2]<-1 || b[3]>641 || b[4]>361)''')
        assert not bad, f'{stem} at {second}s has clipped text: {bad}'
    if stem.startswith('strips'):
        x0 = page.evaluate('() => {const s=document.querySelector("svg");s.setCurrentTime(0);return document.querySelector("circle").cx.animVal.value}')
        x1 = page.evaluate('() => {const s=document.querySelector("svg");s.setCurrentTime(7.5);return document.querySelector("circle").cx.animVal.value}')
        assert x1 > x0 + 40, (x0, x1)
    else:
        o0 = page.evaluate('() => {document.querySelector("svg").setCurrentTime(0);return parseFloat(getComputedStyle(document.querySelectorAll("g[opacity]")[1]).opacity)}')
        o1 = page.evaluate('() => {document.querySelector("svg").setCurrentTime(7.5);return parseFloat(getComputedStyle(document.querySelectorAll("g[opacity]")[1]).opacity)}')
        assert o1 > o0 + .5, (o0, o1)


def test_player(page, stem, lang, reduced):
    js = (ROOT / 'docs/javascripts/concept-motion.js').read_text(encoding='utf-8')
    css = (ROOT / 'docs/stylesheets/concept-motion.css').read_text(encoding='utf-8')
    alt = ('顯示規劃圖動畫' if lang == 'zh' else 'Planning diagram animation')
    prefix = 'https://fixtures.invalid/docs/assets/concept-animations/'
    html = (f'<html><head><style>{css}</style></head><body><main>'
            f'<img src="{prefix}{stem}-motion.svg" alt="{alt}">'
            f'</main><script>{js}</script></body></html>')
    page.set_content(html, wait_until='domcontentloaded')
    page.wait_for_function("document.querySelector('.concept-motion-toggle') !== null")
    host=page.locator('.concept-motion-wide')
    assert host.count()==1
    assert host.get_attribute('tabindex')=='0'
    img=host.locator('img')
    toggle=host.locator('button')
    if reduced:
        assert img.get_attribute('src').endswith('-still.svg')
        toggle.focus()
        page.keyboard.press('Enter')
        assert img.get_attribute('src').endswith('-motion.svg')
    else:
        assert img.get_attribute('src').endswith('-motion.svg')
        toggle.focus()
        page.keyboard.press('Space')
        assert img.get_attribute('src').endswith('-still.svg')
        toggle.click()
        assert img.get_attribute('src').endswith('-motion.svg')
    if page.viewport_size['width'] < 681:
        left,right=host.evaluate('(e)=>[e.clientWidth,e.scrollWidth]')
        assert right > left + 80, (stem,left,right)
        host.focus()
        page.keyboard.press('ArrowRight')
        page.wait_for_timeout(180)
        assert host.evaluate('(e)=>e.scrollLeft') > 0, stem


def main():
    n=0
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True, args=['--no-sandbox'], executable_path=os.environ.get('CHROMIUM_PATH') or None)
        for stem in STEMS:
            for width in (320, 360, 720, 1024):
                page=browser.new_page(viewport={'width':width,'height':560})
                test_svg(page,stem)
                page.close();n+=1
                if not (ROOT/'docs/javascripts/concept-motion.js').exists():
                    continue
                for lang in ('en','zh'):
                    for reduced in (False,True):
                        page=browser.new_page(viewport={'width':width,'height':560}, reduced_motion='reduce' if reduced else 'no-preference')
                        test_player(page,stem,lang,reduced)
                        page.close();n+=1
        browser.close()
    print(f'planning SVG and bilingual player Chromium cases: {n} passed')


if __name__=='__main__':
    main()
