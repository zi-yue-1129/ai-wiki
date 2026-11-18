#!/usr/bin/env python3
"""Actual built bilingual policy-credit labs, not an injected standalone fixture."""
import json
import os
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from test_built_motion_browser import serve_site, check_math_rendering, assert_document_fits

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(os.environ.get('POLICY_CREDIT_SITE_DIR', ROOT / 'site'))
OUT = ROOT / 'artifacts/policy-credit-labs'
CHAPTER = 'theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/'


def slider(locator, value):
    locator.evaluate('(e,v)=>{e.value=String(v);e.dispatchEvent(new Event("input",{bubbles:true}));}', value)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'status': 'running', 'cases': []}
    try:
        with serve_site(SITE.resolve(), 'https://zi-yue-1129.github.io/ai-wiki/') as base, sync_playwright() as p:
            browser = p.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
            for topic in ('reinforce', 'grpo'):
                for lang in ('en', 'zh-TW'):
                    for width in (320, 1280):
                        for reduced in (False, True):
                            case = dict(topic=topic, lang=lang, width=width, reduced=reduced, errors=[])
                            report['cases'].append(case)
                            page = browser.new_page(viewport={'width':width,'height':900}, reduced_motion='reduce' if reduced else 'no-preference')
                            page.on('pageerror', lambda error,c=case: c['errors'].append(str(error)))
                            prefix = '' if lang == 'en' else 'zh-TW/'
                            url = urljoin(base, prefix + CHAPTER + topic + '/')
                            response = page.goto(url, wait_until='load')
                            assert response and response.ok
                            check_math_rendering(page)
                            host = page.locator(f'[data-policy-lab="{topic}"]')
                            host.locator('.pcl-panel').wait_for()
                            assert host.locator('.pcl-panel').count() == 1
                            assert_document_fits(page, {'width':width})
                            buttons = host.locator('.pcl-controls button')
                            prev, play, nxt, reset = (buttons.nth(i) for i in range(4))
                            seek = host.locator('.pcl-seek')
                            inputs = host.locator('.pcl-fields input[type=range]')
                            assert play.is_disabled() == reduced
                            final = 2 if topic == 'reinforce' else 3
                            # Both preserved source-PR numerical examples, through real controls.
                            host.locator('.pcl-preset').select_option('mixed')
                            read = host.locator('.pcl-read').inner_text()
                            if topic == 'reinforce':
                                assert 'G=[2.620, 1.800, 2.000]' in read and 'G−b=[0.720, -0.100, 0.100]' in read
                            else:
                                assert 'σ=1.118' in read and '[-0.447, 1.342, -1.342, 0.447]' in read
                            reset.click()
                            assert seek.input_value() == '0'
                            assert host.locator('.pcl-preset').input_value() == 'terminal'
                            # Real native keyboard navigation and seek.
                            nxt.focus(); page.keyboard.press('Enter')
                            assert seek.input_value() == '1'
                            prev.focus(); page.keyboard.press('Space')
                            assert seek.input_value() == '0'
                            seek.focus(); page.keyboard.press('ArrowRight')
                            assert seek.input_value() == '1'
                            slider(seek, final)
                            assert nxt.is_disabled()
                            reset.click(); assert prev.is_disabled()
                            # Runtime media preference changes must re-enable Play without another control.
                            page.emulate_media(reduced_motion='reduce')
                            page.wait_for_function('(s)=>document.querySelector(s).disabled',arg=f'[data-policy-lab="{topic}"] .pcl-controls button:nth-child(2)')
                            assert play.is_disabled()
                            page.emulate_media(reduced_motion='no-preference')
                            page.wait_for_function('(s)=>!document.querySelector(s).disabled',arg=f'[data-policy-lab="{topic}"] .pcl-controls button:nth-child(2)')
                            assert play.is_enabled()
                            host.locator('.pcl-rate').select_option('0.5')
                            play.click(); page.wait_for_timeout(700)
                            assert seek.input_value() == '0'
                            play.click(); paused = seek.input_value(); page.wait_for_timeout(550)
                            assert seek.input_value() == paused and play.get_attribute('aria-pressed') == 'false'
                            host.locator('.pcl-rate').select_option('2')
                            play.click()
                            page.wait_for_function('(s)=>document.querySelector(s).value!=="0"', arg=f'[data-policy-lab="{topic}"] .pcl-seek')
                            if play.get_attribute('aria-pressed') == 'true': play.click()
                            reset.click(); reset.click()
                            assert host.locator('.pcl-rate').input_value() == '1'
                            play.click()
                            # Dispatch a deterministic visibility event; this is a handler test,
                            # not a claim that headless Chromium changed real tab focus.
                            page.evaluate('''() => {
                              Object.defineProperty(document,'hidden',{configurable:true,value:true});
                              document.dispatchEvent(new Event('visibilitychange'));
                              delete document.hidden;
                            }''')
                            assert play.get_attribute('aria-pressed') == 'false'
                            frozen=seek.input_value();page.wait_for_timeout(550)
                            assert seek.input_value()==frozen
                            case['visibility_check']='simulated event handler'
                            reset.click()
                            if topic == 'reinforce':
                                slider(inputs.nth(0),4.75);slider(inputs.nth(1),5);slider(inputs.nth(2),0)
                                # Two formerly saturated values must now have distinct proportional heights.
                                bars=host.locator('svg > rect').evaluate_all('xs=>xs.slice(1).map(x=>+x.getAttribute("height"))')
                                assert abs(bars[0]/bars[1]-4.75/5)<1e-10 and bars[0]<bars[1], bars
                                reset.click();slider(inputs.nth(4),4);slider(seek,2)
                                assert 'G−b=[-1.440, -0.800, 0.000]' in host.locator('.pcl-read').inner_text()
                            else:
                                host.locator('.pcl-check input').check();slider(seek,3)
                                text=host.locator('.pcl-read').inner_text()
                                assert 'σ=0.000' in text and '[0.000, 0.000, 0.000, 0.000]' in text
                            folder=OUT/f'{topic}-{lang}-{width}-{reduced}'
                            folder.mkdir(exist_ok=True)
                            host.scroll_into_view_if_needed();page.screenshot(path=str(folder/'boundary.png'))
                            reset.click()
                            # Exercise actual MkDocs cross-page navigation and Back with a single lab instance.
                            other='grpo' if topic=='reinforce' else 'reinforce'
                            link=page.locator(f'.md-content__inner a[href="../{other}/"]').first
                            assert link.count()
                            link.click();page.wait_for_url(urljoin(base,prefix+CHAPTER+other+'/'))
                            page.locator(f'[data-policy-lab="{other}"] .pcl-panel').wait_for()
                            page.go_back(wait_until='load');page.wait_for_url(url)
                            assert page.locator(f'[data-policy-lab="{topic}"] .pcl-panel').count()==1
                            assert_document_fits(page, {'width':width})
                            assert not case['errors'],case
                            case['status']='passed'
                            page.close()
            browser.close()
        report['status']='passed'
    finally:
        (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(f'Policy credit: {len(report["cases"])} actual built bilingual cases passed')


if __name__ == '__main__':
    main()
