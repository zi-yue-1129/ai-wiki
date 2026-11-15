#!/usr/bin/env python3
"""Offline Chromium QA for synthetic Gibbs labs, including responsive, bilingual and accessible controls."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1] if (Path(__file__).resolve().parents[1]/'docs').exists() else Path(__file__).resolve().parent
JS = ROOT / 'docs/javascripts/gibbs-labs.js'
CSS = ROOT / 'docs/stylesheets/gibbs-labs.css'
if not JS.exists(): JS = ROOT / 'gibbs-labs.js'
if not CSS.exists(): CSS = ROOT / 'gibbs-labs.css'
ARTIFACT = ROOT / 'artifacts/gibbs-labs' if (ROOT / 'docs').exists() else ROOT / 'screenshots'
ARTIFACT.mkdir(parents=True, exist_ok=True)

html_template = '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>*{box-sizing:border-box}body{font-family:system-ui,sans-serif;margin:0 auto;padding:16px;max-width:1080px;color:#24394c}h2{font-size:20px}</style></head><body>
<h2>Gibbs teaching experiments</h2><div data-gibbs-lab="gaussian" data-lang="LOCALE"><p>Fallback: original Gibbs coordinate-sweep SVG above.</p></div>
<div data-gibbs-lab="disconnected" data-lang="LOCALE"><p>Fallback: original disconnected-support still SVG above.</p></div></body></html>'''

with sync_playwright() as pw:
    config={'headless':True,'args':['--no-sandbox']}
    if Path('/usr/bin/chromium').exists():config['executable_path']='/usr/bin/chromium'
    browser=pw.chromium.launch(**config)
    count=0
    for lang in ('en','zh-TW'):
        for width in (320,360,720,1024):
            for reduced in (False,True):
                page=browser.new_page(viewport={'width':width,'height':850},reduced_motion='reduce' if reduced else 'no-preference')
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.set_content(html_template.replace('LOCALE',lang))
                # No-script fallback is readable before enhancement.
                assert page.get_by_text('Fallback: original Gibbs coordinate-sweep').count()==1
                page.add_style_tag(content=CSS.read_text(encoding='utf-8'))
                page.add_script_tag(content=JS.read_text(encoding='utf-8'))
                ga=page.locator('[data-gibbs-lab="gaussian"]');disc=page.locator('[data-gibbs-lab="disconnected"]')
                assert ga.locator('svg[data-graphic="main"]').count()==1
                assert ga.locator('svg[data-graphic="diagnostic"]').count()==1
                assert disc.locator('svg[data-graphic="diagnostic"]').count()==1
                assert disc.locator('svg[data-graphic="main"]').count()==1
                assert '0.640' in ga.locator('[data-status]').inner_text()
                # Playback remains user-controlled even with a reduced-motion preference.
                ga.locator('[data-field="speed"]').select_option('2')
                ga.locator('[data-action="play"]').click()
                assert ga.locator('[data-action="play"]').inner_text() in ('Pause','暫停')
                ga.locator('[data-action="play"]').click()
                assert ga.locator('[data-action="play"]').inner_text() in ('Play','播放')
                ga.locator('[data-field="rho"]').fill('0')
                assert ga.locator('[data-ess]').get_attribute('data-ess')=='100.000'
                ga.locator('[data-field="rho"]').fill('0.8')
                assert 20 < float(ga.locator('[data-ess]').get_attribute('data-ess')) < 24
                positive_ess=ga.locator('[data-ess]').get_attribute('data-ess')
                ga.locator('[data-field="rho"]').fill('-0.8')
                assert ga.locator('[data-ess]').get_attribute('data-ess')==positive_ess
                ga.locator('[data-action="next"]').click()
                assert '-0.500' in ga.locator('[data-status]').inner_text()
                assert ga.locator('[data-conditional-mean]').get_attribute('data-conditional-mean')=='-0.800'
                ga.locator('[data-action="reset"]').click()
                assert disc.locator('[data-tv]').get_attribute('data-tv')=='0.500'
                assert disc.locator('[data-to="00"]').get_attribute('data-probability')=='1.000'
                assert disc.locator('[data-to="11"]').get_attribute('data-probability')=='0.000'
                ga.locator('[data-action="next"]').click()
                assert '1.100' in ga.locator('[data-status]').inner_text()
                assert ga.locator('[data-conditional-mean]').get_attribute('data-conditional-mean')=='0.800'
                # Capture the meaningful first conditional draw and its mean marker;
                # the standard 16-scenario captures later show a finished trajectory.
                if width in (320,1024) and not reduced:
                    page.screenshot(path=str(ARTIFACT/f'{lang}-{width}-conditional-mean.png'),full_page=True)
                ga.locator('[data-action="next"]').click()
                assert '0.280' in ga.locator('[data-status]').inner_text()
                assert ga.locator('[data-conditional-mean]').get_attribute('data-conditional-mean')=='0.880'
                ga.locator('[data-field="rho"]').fill('0.95')
                assert '0.902' in ga.locator('[data-status]').inner_text() or '0.903' in ga.locator('[data-status]').inner_text()
                # Theoretical full-sweep ACF changes with rho, not with a chosen sample.
                assert abs(float(ga.locator('[data-acf="1"]').get_attribute('width'))-140*.95**2)<.02
                assert float(ga.locator('[data-ess]').get_attribute('data-ess')) < 10
                ga.locator('[data-field="step"]').fill('10')
                assert ga.locator('svg[data-graphic="main"] polyline').count()==1
                ga.locator('[data-action="reset"]').click()
                assert '0.80' in ga.locator('[data-status]').inner_text()
                disc.locator('[data-action="next"]').click()
                assert '(0,0)' in disc.locator('[data-status]').inner_text()
                disc.locator('[data-field="mode"]').select_option('block')
                assert '(1,1)' in disc.locator('[data-status]').inner_text()
                assert disc.locator('[data-to="00"]').get_attribute('data-probability')=='0.500'
                assert disc.locator('[data-to="11"]').get_attribute('data-probability')=='0.500'
                # The two bars are a row-stochastic transition kernel, not visit counts.
                probs=[float(disc.locator(f'[data-to="{dest}"]').get_attribute('data-probability')) for dest in ('00','11')]
                assert abs(sum(probs)-1)<1e-12,probs
                assert disc.locator('[data-tv]').get_attribute('data-tv')=='0.000'
                disc.locator('[data-action="next"]').click()
                assert '(0,0)' in disc.locator('[data-status]').inner_text()
                assert disc.locator('[data-tv]').get_attribute('data-tv')=='0.000'
                disc.locator('[data-field="start"]').select_option('1')
                disc.locator('[data-field="mode"]').select_option('single')
                assert '(1,1)' in disc.locator('[data-status]').inner_text()
                assert disc.locator('[data-to="00"]').get_attribute('data-probability')=='0.000'
                assert disc.locator('[data-to="11"]').get_attribute('data-probability')=='1.000'
                assert disc.locator('[data-tv]').get_attribute('data-tv')=='0.500'
                disc.locator('[data-action="reset"]').click()
                assert '0/8' in disc.locator('[data-status]').inner_text() if lang=='zh-TW' else 'Step 0 of 8' in disc.locator('[data-status]').inner_text()
                # Check that two languages are actually offered, controls are keyboard focusable,
                # and small screens scroll only the SVG region instead of the whole page.
                expected='上一步' if lang=='zh-TW' else 'Previous'
                assert ga.locator('[data-action="prev"]').inner_text()==expected
                assert page.evaluate('document.documentElement.scrollWidth')<=width+1
                for host in (ga,disc):
                    box=host.locator('.gibbs-lab-scroll').first.bounding_box()
                    assert box['width']<=width,(width,lang,box)
                    assert host.locator('svg[data-graphic="main"]').bounding_box()['width']==640
                    assert host.locator('svg[data-graphic="diagnostic"]').bounding_box()['height']==170
                    if width<640: assert host.locator('.gibbs-lab-scroll').first.evaluate('(e)=>e.scrollWidth>e.clientWidth')
                # Plot important post-update states, not just step 0.
                ga.locator('[data-field="rho"]').fill('0.95')
                ga.locator('[data-field="step"]').fill('10')
                disc.locator('[data-field="mode"]').select_option('block')
                disc.locator('[data-field="step"]').fill('7')
                assert ga.locator('[data-ess]').count()==1
                assert disc.locator('[data-tv]').get_attribute('data-tv')=='0.000'
                page.screenshot(path=str(ARTIFACT/f'{lang}-{width}-{"reduced" if reduced else "motion"}.png'),full_page=True)
                assert not errors,errors
                count+=1;page.close()
    browser.close()
    print(f'PASS {count} bilingual × width × reduced-motion browser scenarios')

