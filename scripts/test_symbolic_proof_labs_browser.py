#!/usr/bin/env python3
"""Chromium regression for the IDA* / resolution instructional simulators.

Run: python scripts/test_symbolic_proof_labs_browser.py [--local-assets PATH]
By default reads docs/javascripts and docs/stylesheets in a repository checkout.
"""
from __future__ import annotations
import argparse
import html
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright


def run(js_file: Path, css_file: Path, screenshots: Path|None=None) -> None:
    assert js_file.is_file() and css_file.is_file(), "Required repository assets are missing"
    with TemporaryDirectory() as temp:
        pagefile = Path(temp) / 'index.html'
        css_uri = '/symbolic-proof-labs.css'
        js_uri = '/symbolic-proof-labs.js'
        pagefile.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="{html.escape(css_uri)}"></head><body style="margin:0;padding:12px;font-family:Arial,sans-serif;max-width:100vw;">
<div data-aiwiki-lab="ida" data-lang="en"><p>Static figure is available above.</p></div>
<div data-aiwiki-lab="resolution" data-lang="zh-TW"><p>上方保留靜態預覽。</p></div>
<script src="{html.escape(js_uri)}"></script></body></html>''', encoding='utf8')
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,args=['--no-sandbox'])
            for width in (320,360,720,1024):
                page=browser.new_page(viewport={'width':width,'height':880},reduced_motion='reduce')
                page.set_content(pagefile.read_text(encoding='utf8').replace(f'<script src="{html.escape(js_uri)}"></script>', '').replace('data-lang="en"','data-lang="TEMP"' if width in (360,1024) else 'data-lang="en"').replace('data-lang="zh-TW"','data-lang="en"' if width in (360,1024) else 'data-lang="zh-TW"').replace('data-lang="TEMP"','data-lang="zh-TW"'))
                page.add_style_tag(content=css_file.read_text(encoding='utf8'))
                page.add_script_tag(content=js_file.read_text(encoding='utf8'))
                assert page.locator('.sp-lab').count()==2
                assert page.locator('.sp-ida-canvas .sp-node').count()==7
                assert page.locator('.sp-proof-step').count()==3
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), f"Horizontal overflow at {width}"
                assert '4' in page.locator('.sp-lab-metric').first.inner_text()
                assert page.locator('[data-aiwiki-lab="ida"] .sp-lab-counter').inner_text().startswith('1 / ')
                assert page.locator('[data-aiwiki-lab="resolution"] .sp-lab-counter').inner_text()=='1 / 4'
                # Real IDA* DFS: first expanded S, then A cut at bound 4.
                ida=page.locator('[data-aiwiki-lab="ida"]')
                ida.get_by_role('button',name='下一步' if width in (360,1024) else 'Next').click()
                assert 'S' in ida.locator('.sp-lab-live').inner_text()
                ida.get_by_role('button',name='下一步' if width in (360,1024) else 'Next').click()
                assert 'A' in ida.locator('.sp-lab-live').inner_text()
                assert '6' in ida.locator('.sp-lab-metric').nth(4).inner_text()
                assert ida.locator('.sp-cut').count()==1
                # Seek to last step and verify full path and repeated visits.
                ida.locator('input[type=range]').fill(ida.locator('input[type=range]').get_attribute('max'))
                assert 'S → A → C → G' in ida.locator('.sp-lab-wide').inner_text()
                assert ('找到目標' if width in (360,1024) else 'Goal') in ida.locator('.sp-lab-live').inner_text()
                assert int(ida.locator('.sp-lab-metric').nth(3).locator('strong').inner_text())>0
                ida.get_by_role('button',name='重設' if width in (360,1024) else 'Reset').click()
                assert ida.locator('.sp-lab-metric').nth(2).locator('strong').inner_text()=='0'
                # Resolution must derive Q or R -> R -> empty clause.
                res=page.locator('[data-aiwiki-lab="resolution"]')
                res.get_by_role('button',name='Next' if width in (360,1024) else '下一步').click()
                assert res.locator('.sp-proof-done').count()==1
                assert 'Q ∨ R' in ' '.join(res.locator('.sp-res-row').inner_text().split())
                res.get_by_role('button',name='Next' if width in (360,1024) else '下一步').click()
                assert '¬Q' in res.locator('.sp-res-row').inner_text()
                res.get_by_role('button',name='Next' if width in (360,1024) else '下一步').click()
                assert res.locator('.sp-clause-empty').inner_text()=='□'
                assert res.locator('.sp-proof-done').count()==3
                # Keyboard accessibility: native range input responds to ArrowLeft.
                slider=res.locator('input[type=range]')
                slider.focus();slider.press('ArrowLeft')
                assert res.locator('.sp-lab-counter').inner_text()=='3 / 4'
                if screenshots:
                    screenshots.mkdir(parents=True,exist_ok=True)
                    res.get_by_role('button',name='Next' if width in (360,1024) else '下一步').click()
                    page.screenshot(path=str(screenshots/f'symbolic-{width}.png'),full_page=True)
                page.close()
            # Non-script fallback is retained verbatim.
            page=browser.new_page(java_script_enabled=False)
            page.set_content(pagefile.read_text(encoding='utf8').replace(f'<script src="{html.escape(js_uri)}"></script>', ''))
            assert page.locator('.sp-lab').count()==0
            assert 'Static figure' in page.locator('[data-aiwiki-lab="ida"]').inner_text()
            page.close()
            # Playback automatically pauses on the last step, supports speed change.
            page=browser.new_page()
            page.set_content(pagefile.read_text(encoding='utf8').replace(f'<script src="{html.escape(js_uri)}"></script>', ''))
            page.add_style_tag(content=css_file.read_text(encoding='utf8'))
            page.add_script_tag(content=js_file.read_text(encoding='utf8'))
            ida=page.locator('[data-aiwiki-lab="ida"]')
            ida.locator('select').select_option('2')
            ida.get_by_role('button',name='Play').click()
            assert ida.get_by_role('button',name='Pause').count()==1
            ida.get_by_role('button',name='Pause').click()
            assert ida.get_by_role('button',name='Play').count()==1
            browser.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--local-assets',type=Path)
    parser.add_argument('--screenshots',type=Path)
    args=parser.parse_args()
    root=args.local_assets
    if root:
        js=root/'symbolic-proof-labs.js';css=root/'symbolic-proof-labs.css'
    else:
        repo=Path(__file__).resolve().parents[1]
        js=repo/'docs/javascripts/symbolic-proof-labs.js'
        css=repo/'docs/stylesheets/symbolic-proof-labs.css'
    run(js,css,args.screenshots)
    print('PASS: symbolic proof labs, responsive controls, keyboard, reduced motion and fallback')