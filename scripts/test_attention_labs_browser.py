#!/usr/bin/env python3
"""Chromium QA for exact causal-window counts and normalised scalar recurrence."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT/'docs/javascripts/attention-variant-labs.js').read_text()
CSS = (ROOT/'docs/stylesheets/attention-variant-labs.css').read_text()
OUT = ROOT/'artifacts/attention-variant-labs'
OUT.mkdir(parents=True, exist_ok=True)

def html(lang):
    return ('<!doctype html><html lang="'+lang+'"><head><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<style>*{box-sizing:border-box}body{margin:0;padding:16px;font-family:Arial,sans-serif;max-width:100vw}'+CSS+'</style></head><body>'
            '<div class="attention-lab" data-lab="window" data-lang="'+lang+'">Static window preview is available above.</div>'
            '<div class="attention-lab" data-lab="linear" data-lang="'+lang+'">Static recurrence preview is available above.</div></body></html>')

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    checks=0
    for lang in ('en','zh'):
        for width in (320,360,768,1024):
            for reduced in ('reduce','no-preference'):
                page=browser.new_page(viewport={'width':width,'height':850},reduced_motion=reduced)
                page.set_content(html(lang))
                page.add_script_tag(content=JS)
                assert page.locator('.attention-lab[data-ready="yes"]').count()==2
                assert page.locator('.attention-lab-stage svg').count()==2
                assert page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth'),(lang,width)
                assert page.locator('.attention-lab-stage').first.evaluate('(e)=>e.scrollWidth>e.clientWidth')==(width<680)
                a=page.locator('.attention-lab[data-lab="window"]')
                b=page.locator('.attention-lab[data-lab="linear"]')
                assert '42 / 78' in a.locator('.attention-lab-stats').inner_text()
                a.locator('[data-range="factor"]').fill('2')
                assert '23 / 78' in a.locator('.attention-lab-stats').inner_text()
                a.locator('[data-range="step"]').fill('2')
                assert '1–2' in a.locator('.attention-lab-stats').inner_text()
                a.locator('[data-act="next"]').click()
                assert '2–3' in a.locator('.attention-lab-stats').inner_text()
                a.locator('[data-act="reset"]').click()
                assert '42 / 78' in a.locator('.attention-lab-stats').inner_text()
                b.locator('[data-range="step"]').fill('4')
                assert 'S=8, z=6, y=1.333' in b.locator('.attention-lab-stats').inner_text()
                b.locator('[data-range="factor"]').fill('5')
                assert 'S=10, z=6, y=1.667' in b.locator('.attention-lab-stats').inner_text()
                b.locator('[data-act="reset"]').click()
                b.locator('[data-act="next"]').focus()
                page.keyboard.press('Enter')
                assert 'S=1, z=1, y=1' in b.locator('.attention-lab-stats').inner_text()
                b.locator('[data-act="speed"]').click()
                assert '2×' in b.locator('[data-act="speed"]').inner_text()
                b.locator('[data-act="play"]').click()
                assert b.locator('[data-act="play"]').get_attribute('aria-pressed')=='true'
                b.locator('[data-act="play"]').click()
                assert b.locator('[data-act="play"]').get_attribute('aria-pressed')=='false'
                if width in (360,1024) and reduced=='reduce':
                    page.screenshot(path=str(OUT/(lang+'-'+str(width)+'.png')),full_page=True)
                checks+=1
                page.close()
        page=browser.new_page()
        page.set_content(html(lang))
        assert page.locator('.attention-lab[data-ready="yes"]').count()==0
        assert page.get_by_text('Static').count()==2
        checks+=1
        page.close()
    browser.close()
print('PASS:',checks,'bilingual Chromium viewports/reduced-motion/no-JS cases')
