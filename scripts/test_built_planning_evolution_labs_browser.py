#!/usr/bin/env python3
"""Real MkDocs planning/evolution lab integration; never inject JS, CSS or HTML.

The original component fixtures remain complementary tests. Reduced motion means
no spontaneous playback; evolution permits an explicit Play request, whereas
planning refuses it. Visibility interruption below is a labelled synthetic event.
"""
import json
import os
from pathlib import Path
from urllib.parse import urljoin, urldefrag
from playwright.sync_api import sync_playwright, expect
from test_built_motion_browser import (serve_site, check_math_rendering,
                                       assert_document_fits, settled_scroll_left)

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(os.environ.get('PLANNING_EVOLUTION_SITE_DIR', ROOT / 'site'))
OUT = ROOT / 'artifacts/built-planning-evolution-labs'
TOPICS = {
    'strips': ('planning', 'theory/paradigms/symbolic-ai/planning/strips/', 'graphplan'),
    'graphplan': ('planning', 'theory/paradigms/symbolic-ai/planning/graphplan/', 'strips'),
    'ga': ('evolution', 'theory/paradigms/evolutionary/genetic-algorithms/', 'map'),
    'map': ('evolution', 'theory/paradigms/evolutionary/map-elites/', 'ga'),
}


def change(control, value):
    control.evaluate('(e,v)=>{e.value=String(v);e.dispatchEvent(new Event("input",{bubbles:true}));}', value)


def controls(host, family):
    if family == 'planning':
        return {name: host.locator(f'[data-a={name}]') for name in ('prev','play','next','seek','speed','reset')}
    buttons = host.locator('.evo-timeline button')
    return dict(prev=buttons.nth(0), play=buttons.nth(1), next=buttons.nth(2),
                speed=buttons.nth(3), reset=buttons.nth(4), seek=host.locator('.evo-timeline input'))


def same_document_url(actual, expected):
    """Only a fragment difference is permitted, never another page or origin."""
    return urldefrag(actual).url == urldefrag(expected).url


def history_lab(page, url, topic, *, forward=False):
    """Exercise browser history without demanding a new document load event.

    Material instant navigation may restore history in the current document.
    The URL transition AND exact destination lab/control DOM must settle; neither
    a stale lab nor a duplicate re-initialization is accepted as navigation.
    """
    family, _, _ = TOPICS[topic]
    page.evaluate('history.forward()' if forward else 'history.back()')
    # Material restores the in-page scroll anchor in the real history entry.
    # Ignore only that fragment; origin, path and query remain exact.
    page.wait_for_url(lambda actual: same_document_url(actual, url), wait_until='commit')
    host = page.locator(f'[data-{family}-lab="{topic}"]')
    expect(host).to_have_count(1)
    expect(host).to_be_visible()
    group = host.locator('.planning-controls' if family == 'planning' else '.evo-timeline')
    expect(group).to_have_count(1)
    current = controls(host, family)
    for control in current.values():
        expect(control).to_have_count(1)
        expect(control).to_be_visible()
    current['reset'].click()
    expect(current['seek']).to_have_value('0')
    stationary(page, current['seek'])
    return host


def stationary(page, seek, duration=1100):
    # Exceed the default 850ms tick: a label-only Pause must not falsely pass.
    # Explicit 650ms checks occur only after setting 2x speed (425ms per tick).
    value=seek.input_value();page.wait_for_timeout(duration)
    assert seek.input_value()==value, 'Paused/interrupted timeline kept moving'


def numerical(host, topic, c):
    seek=c['seek']; change(seek,4)
    if topic=='strips':
        assert 'At(B)' in host.locator('.planning-status').inner_text()
        host.locator('[data-p=atA]').uncheck()
        assert 'not applied' in host.locator('svg').text_content()
        assert 'At(B)' not in host.locator('.planning-status').inner_text()
        c['reset'].click(); host.locator('[data-p=charged]').uncheck();change(seek,4)
        assert 'Charged' not in host.locator('.planning-status').inner_text()
    elif topic=='graphplan':
        assert 'Move(A,B)' in host.locator('.planning-status').inner_text()
        host.locator('[data-p=goal]').select_option('AB')
        assert any(x in host.locator('.planning-status').inner_text() for x in ('mutex','互斥'))
    elif topic=='ga':
        inputs=host.locator('.evo-parameters input');canvas=host.locator('.evo-canvas')
        assert host.locator('.evo-bit').count()==24
        change(inputs.nth(0),4);change(inputs.nth(1),7);change(seek,9)
        assert canvas.get_attribute('data-child')=='11010111'
        change(inputs.nth(0),5);change(seek,9)
        assert canvas.get_attribute('data-child')=='11011111'
    else:
        inputs=host.locator('.evo-parameters input');canvas=host.locator('.evo-canvas')
        assert host.locator('.evo-niche').count()==24
        assert canvas.get_attribute('data-coverage')=='5'
        change(inputs.nth(0),.95);change(seek,2)
        assert canvas.get_attribute('data-coverage')=='4'
        assert canvas.get_attribute('data-last-decision') in ('Replace','取代')
        change(seek,3)
        assert canvas.get_attribute('data-last-decision') in ('Reject','拒絕')
        change(inputs.nth(0),.82);change(seek,2)
        assert canvas.get_attribute('data-last-decision') in ('Reject','拒絕')
    c['reset'].click(); c['reset'].click()
    assert seek.input_value()=='0'
    if topic=='strips':
        assert host.locator('[data-p=atA]').is_checked() and host.locator('[data-p=charged]').is_checked()
    elif topic=='graphplan': assert host.locator('[data-p=goal]').input_value()=='C'
    elif topic=='ga': assert host.locator('.evo-canvas').get_attribute('data-child')=='11010101'
    else: assert host.locator('.evo-canvas').get_attribute('data-coverage')=='3'


def exercise(page, base, topic, lang, width, reduced, folder, record):
    family,path,other=TOPICS[topic];prefix='' if lang=='en' else 'zh-TW/'
    url=urljoin(base,prefix+path);selector=f'[data-{family}-lab="{topic}"]'
    response=page.goto(url,wait_until='load');assert response and response.ok
    assert page.locator('html').get_attribute('lang')==lang
    record['math']=check_math_rendering(page);page.evaluate('document.fonts.ready')
    host=page.locator(selector);host.locator('button').first.wait_for()
    assert host.count()==1
    c=controls(host,family);seek=c['seek'];canvas=host.locator('.planning-canvas' if family=='planning' else '.evo-canvas')
    assert canvas.get_attribute('tabindex')=='0'
    assert_document_fits(page,{'width':width})
    # Verify real linked scripts/styles were fetched by MkDocs, not a test fixture.
    for suffix in (f'javascripts/{family}-labs.js',f'stylesheets/{family}-labs.css'):
        assert page.evaluate('(s)=>performance.getEntriesByType("resource").some(r=>r.name.split("?")[0].endsWith(s))',suffix),suffix
    assert seek.input_value()=='0';stationary(page,seek)
    host.scroll_into_view_if_needed();page.screenshot(path=str(folder/'initial.png'))
    numerical(host,topic,c)
    # Native Enter/Space, arrow-key range input and repeated Reset.
    c['next'].focus();page.keyboard.press('Enter');assert seek.input_value()=='1'
    c['prev'].focus();page.keyboard.press('Space');assert seek.input_value()=='0'
    seek.focus();page.keyboard.press('ArrowRight');assert seek.input_value()=='1'
    c['reset'].click()
    if width<600:
        assert canvas.evaluate('e=>e.scrollWidth>e.clientWidth+2')
        canvas.focus();page.keyboard.press('ArrowRight')
        page.wait_for_function('e=>e.scrollLeft>0',arg=canvas.element_handle(),timeout=2000)
        assert settled_scroll_left(canvas)>0
        canvas.evaluate('e=>{e.blur();e.scrollTo({left:0,behavior:"instant"})}')
        assert settled_scroll_left(canvas)==0
    # Respect actual component contract for explicit playback under reduction.
    c['play'].click()
    if reduced and family=='planning':
        assert c['play'].get_attribute('aria-pressed')=='false';stationary(page,seek)
    else:
        page.wait_for_function('e=>e.value!=="0"',arg=seek.element_handle(),timeout=5000)
        c['play'].click();stationary(page,seek)
    c['reset'].click()
    page.emulate_media(reduced_motion='no-preference')
    page.wait_for_function('!matchMedia("(prefers-reduced-motion: reduce)").matches')
    if family=='planning':c['speed'].select_option('2')
    else:
        c['speed'].click()  # First speed change: default 1x -> 2x.
        assert '2×' in c['speed'].inner_text()
    c['play'].click()
    page.wait_for_function('e=>e.value!=="0"',arg=seek.element_handle(),timeout=5000)
    page.emulate_media(reduced_motion='reduce')
    page.wait_for_function('matchMedia("(prefers-reduced-motion: reduce)").matches')
    page.wait_for_function('e=>!/(Pause|暫停)/.test(e.textContent)',arg=c['play'].element_handle())
    stationary(page,seek,650)
    c['reset'].click();page.emulate_media(reduced_motion='no-preference')
    page.wait_for_function('!matchMedia("(prefers-reduced-motion: reduce)").matches')
    c['play'].click()
    page.evaluate('''() => {Object.defineProperty(document,'hidden',{configurable:true,value:true});
      document.dispatchEvent(new Event('visibilitychange'));delete document.hidden;}''')
    stationary(page,seek,650);record['visibility']='synthetic visibility event, not physical tab focus'
    c['reset'].click();change(seek,4 if topic!='ga' else 9)
    host.scroll_into_view_if_needed();page.screenshot(path=str(folder/'numeric-final.png'))
    # Full real-document navigation while a timer is active, then history Back/Forward.
    c['reset'].click();c['play'].click()
    otherfamily,otherpath,_=TOPICS[other];otherurl=urljoin(base,prefix+otherpath)
    response=page.goto(otherurl,wait_until='load');assert response and response.ok
    page.locator(f'[data-{otherfamily}-lab="{other}"] button').first.wait_for()
    history_lab(page, url, topic)
    history_lab(page, otherurl, other, forward=True)
    record['history'] = {'back': url, 'forward': otherurl, 'reset_and_unique_controls': True}
    assert_document_fits(page,{'width':width})


def main():
    OUT.mkdir(parents=True,exist_ok=True);report={'status':'running','cases':[]}
    try:
        with serve_site(SITE.resolve(),'https://zi-yue-1129.github.io/ai-wiki/') as base,sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
            for topic in TOPICS:
                for lang in ('en','zh-TW'):
                    for width in (320,1280):
                        for reduced in (False,True):
                            case=dict(topic=topic,lang=lang,width=width,reduced=reduced,errors=[]);report['cases'].append(case)
                            folder=OUT/f'{topic}-{lang}-{width}-{reduced}';folder.mkdir(exist_ok=True)
                            context=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce' if reduced else 'no-preference')
                            page=context.new_page();page.on('pageerror',lambda e,c=case:c['errors'].append(str(e)))
                            try:
                                exercise(page,base,topic,lang,width,reduced,folder,case)
                                assert not case['errors'],case['errors'];case['status']='passed'
                            except Exception as exc:
                                case['status']='failed';case['failure']=str(exc)
                                try:page.screenshot(path=str(folder/'failure.png'))
                                except Exception as shot_error:case['screenshot_error']=str(shot_error)
                            finally:context.close()
                            print(case['status'],topic,lang,width,reduced,flush=True)
            browser.close()
        report['status']='failed' if any(c['status']!='passed' for c in report['cases']) else 'passed'
    finally:(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    assert report['status']=='passed',f"Built planning/evolution: {sum(c['status']!='passed' for c in report['cases'])} failures"
    print(f'Built planning/evolution: {len(report["cases"])} cases passed')


if __name__=='__main__':main()
