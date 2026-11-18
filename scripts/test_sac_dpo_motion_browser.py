#!/usr/bin/env python3
"""Browser integration for bilingual SAC/DPO motion, static fallback and mobile scroll.

Run from the repository root after `python -m playwright install chromium`.
"""
from __future__ import annotations

from pathlib import Path
import json
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
CSS = ROOT / 'docs/stylesheets/concept-motion.css'
JS = ROOT / 'docs/javascripts/concept-motion.js'
TOPICS = ('sac-entropy-temperature', 'dpo-preference-margin')
SVG_NS = '{http://www.w3.org/2000/svg}'
OUT = ROOT/'artifacts/sac-dpo-motion'


def verify_assets():
    for stem in TOPICS:
        for variant in ('motion', 'still'):
            path = ASSETS / f'{stem}-{variant}.svg'
            root = ET.parse(path).getroot()
            assert root.tag == SVG_NS + 'svg'
            assert root.get('viewBox') == '0 0 760 420'
            assert root.find(SVG_NS+'title') is not None
            assert root.find(SVG_NS+'desc') is not None
            nodes = [n for n in root.iter() if n.tag == SVG_NS + 'animate']
            assert bool(nodes) is (variant == 'motion')
            assert all(n.get('repeatCount') == 'indefinite' for n in nodes)
            assert all('://' not in v and not v.startswith(('javascript:', 'data:')) for n in root.iter() for v in n.attrib.values())
        for topic in ('theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/sac/index',
                      'theory/paradigms/reinforcement-learning/learning-from-human-feedback/dpo/index'):
            if stem.startswith(topic.split('/')[-2]) or (stem.startswith('dpo') and '/dpo/' in topic):
                for suffix in ('.md', '.zh-TW.md'):
                    data = (ROOT/'docs'/f'{topic}{suffix}').read_text()
                    assert f'{stem}-motion.svg' in data and f'{stem}-still.svg' in data
                    assert 'CC BY-SA 4.0' in data


def scroll_geometry(page):
    return page.evaluate("""() => {
      const region=document.querySelector('.concept-motion-scroll');
      const host=region.querySelector('.concept-motion-player');const img=region.querySelector('img');
      const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,left:r.left,right:r.right,width:r.width,height:r.height}};
      return {innerWidth,clientWidth:document.documentElement.clientWidth,documentWidth:document.documentElement.scrollWidth,
        region:{...rect(region),clientWidth:region.clientWidth,scrollWidth:region.scrollWidth,scrollLeft:region.scrollLeft},
        host:{...rect(host),maxWidth:getComputedStyle(host).maxWidth,marginLeft:getComputedStyle(host).marginLeft,marginRight:getComputedStyle(host).marginRight},
        img:{...rect(img),naturalWidth:img.naturalWidth}};
    }""")

def assert_scroll_geometry(geometry, viewport):
    assert geometry['innerWidth']==geometry['clientWidth']==viewport, geometry
    assert geometry['documentWidth']<=viewport, geometry
    assert (geometry['region']['scrollWidth']>geometry['region']['clientWidth'])==(viewport<760), geometry

def validate_case_matrix(cases):
    expected={(stem,lang,width,reduced) for stem in TOPICS for lang in ('en','zh')
              for width in (320,360,760,1024) for reduced in (False,True)}
    observed=[(c['stem'],c['lang'],c['viewport'],c['reduced']) for c in cases]
    assert len(observed)==len(set(observed))==32 and set(observed)==expected
    assert all(c['status']=='passed' for c in cases)


def old_host_counterfactual(browser, html, js, handle, record):
    page=browser.new_page(viewport={'width':760,'height':660},reduced_motion='reduce')
    try:
        page.route('https://aiwiki.invalid/assets/concept-animations/*',handle)
        # Restore the original shared 640px centered host by removing only our scoped class.
        page.set_content(html.replace('class="sac-dpo-motion-frame"','class="old-sac-dpo-motion-frame"'),wait_until='load')
        page.add_script_tag(content=js)
        page.locator('.concept-motion-scroll img').evaluate('(el)=>el.decode()')
        geometry=scroll_geometry(page);record['old_host_counterfactual']={'geometry':geometry,'rejected':False}
        page.screenshot(path=str(OUT/(record['id']+'-old-host.png')))
        assert geometry['host']['width']==640 and geometry['img']['width']==760, geometry
        try: assert_scroll_geometry(geometry,760)
        except AssertionError:record['old_host_counterfactual']['rejected']=True
        else:raise AssertionError('Original centered 640px host did not reproduce the 760px boundary failure')
        assert geometry['region']['scrollWidth']>geometry['region']['clientWidth'],geometry
    finally:page.close()


def main():
    verify_assets()
    js = JS.read_text()
    css = CSS.read_text()
    successes=0
    OUT.mkdir(parents=True,exist_ok=True)
    report={"status":"running","cases":[]}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None, args=['--no-sandbox'])
            for stem in TOPICS:
                for lang, alt in [('en', 'Animated SAC or DPO learning diagram'), ('zh', '概念動畫：動作或偏好資料更新')]:
                    for viewport in (320,360,760,1024):
                        for reduced in (False, True):
                            page=browser.new_page(viewport={'width':viewport,'height':660},reduced_motion='reduce' if reduced else 'no-preference')
                            record={"id":f"case-{len(report['cases'])+1:02d}","stem":stem,"lang":lang,"viewport":viewport,"reduced":reduced,"status":"running"}
                            report["cases"].append(record)
                            try:
                                def handle(route):
                                    file_name=route.request.url.rsplit('/',1)[-1]
                                    path=ASSETS/file_name
                                    if path.is_file() and path.name.startswith(stem):
                                        route.fulfill(body=path.read_bytes(),content_type='image/svg+xml',status=200)
                                    else: route.fulfill(status=404,body='not found')
                                page.route('https://aiwiki.invalid/assets/concept-animations/*',handle)
                                url='https://aiwiki.invalid/assets/concept-animations/'
                                html=f'''<html><head><style>body{{margin:0}}{css}</style></head><body><div class="concept-motion-scroll sac-dpo-motion-scroll" style="max-width:100%;overflow-x:auto" tabindex="0"><div class="sac-dpo-motion-frame" style="min-width:760px"><img style="width:760px;min-width:760px;max-width:none" src="{url}{stem}-still.svg" data-motion-src="{url}{stem}-motion.svg" alt="{alt}"></div></div></body></html>'''
                                page.set_content(html,wait_until='load')
                                page.add_script_tag(content=js)
                                img=page.locator('.concept-motion-scroll img')
                                toggle=page.locator('.concept-motion-toggle')
                                assert toggle.count()==1
                                img.evaluate('(el)=>el.decode()')
                                assert ('-still.svg' if reduced else '-motion.svg') in img.get_attribute('src')
                                record['geometry']=scroll_geometry(page)
                                assert page.locator('.concept-motion-scroll').evaluate('(el)=>el.scrollWidth>el.clientWidth') == (viewport < 760), record
                                assert_scroll_geometry(record['geometry'],viewport)
                                if viewport==760:old_host_counterfactual(browser,html,js,handle,record)
                                if not reduced:
                                    toggle.click()
                                    assert '-still.svg' in img.get_attribute('src')
                                    toggle.focus()
                                    toggle.press('Enter')
                                    assert '-motion.svg' in img.get_attribute('src')
                                    toggle.press('Space')
                                    assert '-still.svg' in img.get_attribute('src')
                                else:
                                    toggle.click()
                                    assert '-motion.svg' in img.get_attribute('src')
                                img.evaluate('(el)=>el.decode()')
                                assert img.evaluate('(el)=>el.naturalWidth') == 760
                                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                                if viewport<760:
                                    sc=page.locator('.concept-motion-scroll');sc.focus();page.keyboard.press('ArrowRight');page.wait_for_timeout(80);assert sc.evaluate('e=>e.scrollLeft>0')
                                record["status"]="passed"
                            except Exception as error:
                                record['status']='failed';record['error']=repr(error)
                                try:
                                    record['geometry']=scroll_geometry(page)
                                    page.screenshot(path=str(OUT/(record['id']+'-failure.png')))
                                    (OUT/(record['id']+'-failure.html')).write_text(page.content())
                                except Exception as capture_error:record['capture_error']=repr(capture_error)
                                raise
                            finally:page.close()
                            successes+=1
            browser.close()
        print(f'SAC / DPO SVG, bilingual play/pause, keyboard, reduced-motion, 320–1024px: {successes}/{successes} passed')
        assert successes==32
        validate_case_matrix(report['cases'])
        report['status']='passed'
    except Exception as error:
        report['status']='failed';report['error']=repr(error)
        raise
    finally:(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
