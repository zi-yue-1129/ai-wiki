#!/usr/bin/env python3
"""Actual built bilingual policy-credit labs, not an injected standalone fixture."""
import json
import os
from pathlib import Path
from urllib.parse import urljoin, urldefrag
from playwright.sync_api import sync_playwright, expect
from test_built_motion_browser import serve_site, check_math_rendering, assert_document_fits

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(os.environ.get('POLICY_CREDIT_SITE_DIR', ROOT / 'site'))
OUT = ROOT / 'artifacts/policy-credit-labs'
CHAPTER = 'theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/'


def slider(locator, value):
    locator.evaluate('(e,v)=>{e.value=String(v);e.dispatchEvent(new Event("input",{bubbles:true}));}', value)



ORIGINAL_INLINE_UPDATE = r'\theta \leftarrow \theta + \alpha \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\,(G_t - b)'


def check_320_update_negative(page):
    """Restore the original real MathJax inline update, require overflow, restore."""
    result = page.evaluate(r'''async (tex) => {
      const item = Array.from(document.querySelectorAll('.md-content__inner ol > li'))
        .find(e => e.textContent.trim().startsWith('Update:'));
      if (!item) throw new Error('REINFORCE update list item not found');
      const saved = Array.from(item.childNodes);
      const wrapper = document.createElement('span');
      wrapper.className = 'arithmatex';
      wrapper.textContent = '\\(' + tex + '\\)';
      try {
        // Recreate the original Markdown-generated inline wrapper in situ.
        // Standalone tex2chtmlPromise uses different layout metrics and bypasses
        // the page's arithmatex processing class, so it is not the old DOM.
        item.replaceChildren(document.createTextNode('Update '), wrapper,
                             document.createTextNode('.'));
        await MathJax.startup.promise;
        await MathJax.typesetPromise([wrapper]);
        const rendered = wrapper.querySelector('mjx-container');
        if (!rendered) throw new Error('Original inline formula was not typeset');
        await document.fonts.ready;
        await new Promise(requestAnimationFrame);
        return {inner:innerWidth,width:document.documentElement.scrollWidth,
                itemWidth:item.getBoundingClientRect().width,
                mathRight:rendered.getBoundingClientRect().right,
                wrapper:wrapper.outerHTML,
                fontSize:getComputedStyle(wrapper).fontSize};
      } finally {
        MathJax.typesetClear([wrapper]);
        item.replaceChildren(...saved);
      }
    }''', ORIGINAL_INLINE_UPDATE)
    assert result['width'] > 320, ('original inline regression must overflow', result)
    assert_document_fits(page, {'width':320})
    return dict(status='passed', original_inline_rejected=result)


def failure_evidence(page, case):
    folder = OUT / 'failure-diagnostics'
    folder.mkdir(exist_ok=True)
    try:
        case['overflow_diagnostics'] = page.evaluate('''() => ({
          inner:innerWidth, width:document.documentElement.scrollWidth,
          elements:Array.from(document.querySelectorAll('.md-content__inner *'))
            .map(e=>({tag:e.tagName,cls:String(e.className),text:e.textContent.slice(0,180),
              left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right,
              client:e.clientWidth,scroll:e.scrollWidth,
              overflow:getComputedStyle(e).overflowX}))
            .filter(e=>e.right>innerWidth || e.left<0 || e.scroll>e.client+1)
        })''')
        page.screenshot(path=str(folder/'failure.png'), full_page=True)
    except Exception as diagnostic_error:
        case['diagnostic_error'] = str(diagnostic_error)
    (folder/'case.json').write_text(json.dumps(case,ensure_ascii=False,indent=2))



def same_document_url(actual, expected):
    """Only a fragment difference is permitted, never another page or origin."""
    return urldefrag(actual).url == urldefrag(expected).url


def history_policy_lab(page, url, topic, width):
    """Require real history, destination DOM uniqueness, and a stationary reset.

    Material may restore the destination in the same document without load.
    Waiting for commit does not excuse a stale URL, missing/duplicate controls,
    failed math, overflow, or a timer that survives reset.
    """
    page.evaluate('history.back()')
    # Material restores the in-page scroll anchor in the real history entry.
    # Ignore only that fragment; origin, path and query remain exact.
    page.wait_for_url(lambda actual: same_document_url(actual, url), wait_until='commit')
    host = page.locator(f'[data-policy-lab="{topic}"]')
    expect(host).to_have_count(1)
    expect(host).to_be_visible()
    for selector in ('.pcl-panel', '.pcl-controls'):
        expect(host.locator(selector)).to_have_count(1)
    buttons = host.locator('.pcl-controls button')
    expect(buttons).to_have_count(4)
    controls = [buttons.nth(i) for i in range(4)] + [host.locator(s) for s in ('.pcl-seek', '.pcl-rate', '.pcl-preset')]
    for control in controls:
        expect(control).to_have_count(1)
        expect(control).to_be_visible()
    controls[3].click()
    seek = controls[4]
    expect(seek).to_have_value('0')
    expect(controls[5]).to_have_value('1')
    expect(controls[1]).to_have_attribute('aria-pressed', 'false')
    before = seek.input_value()
    page.wait_for_timeout(1100)  # Exceeds the default 950 ms tick after Reset.
    assert seek.input_value() == before == '0', 'history reset timer kept moving'
    check_math_rendering(page)
    assert_document_fits(page, {'width':width})
    return host



def validate_complete_cases(cases):
    expected={(t,l,w,r) for t in ('reinforce','grpo') for l in ('en','zh-TW') for w in (320,360,390,720,1024,1280) for r in (False,True)}
    observed=[(c['topic'],c['lang'],c['width'],c['reduced']) for c in cases]
    assert len(observed)==48 and len(set(observed))==48 and set(observed)==expected, 'Missing, duplicate or unexpected policy lab case'
    assert all(c.get('status')=='passed' and not c.get('errors') for c in cases), 'Policy lab case failed'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'status': 'running', 'cases': []}
    try:
        with serve_site(SITE.resolve(), 'https://zi-yue-1129.github.io/ai-wiki/') as base, sync_playwright() as p:
            browser = p.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
            try:
                for topic in ('reinforce', 'grpo'):
                    for lang in ('en', 'zh-TW'):
                        for width in (320, 360, 390, 720, 1024, 1280):
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
                                if topic == 'reinforce' and lang == 'en' and width == 320 and not reduced:
                                    case['update_320_negative_canary'] = check_320_update_negative(page)
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
                                # Leave with a live timer so history reset is not a vacuous stationary check.
                                play.click()
                                expect(play).to_have_attribute('aria-pressed', 'true')
                                # Exercise actual MkDocs cross-page navigation and Back with a single lab instance.
                                other='grpo' if topic=='reinforce' else 'reinforce'
                                link=page.locator(f'.md-content__inner a[href="../{other}/"]').first
                                assert link.count()
                                link.click();page.wait_for_url(urljoin(base,prefix+CHAPTER+other+'/'), wait_until='commit')
                                page.locator(f'[data-policy-lab="{other}"] .pcl-panel').wait_for()
                                history_policy_lab(page, url, topic, width)
                                case['history'] = {'back':url,'unique_controls':True,'reset_stationary':True}
                                assert_document_fits(page, {'width':width})
                                assert not case['errors'],case
                                case['status']='passed'
                                page.close()
            except Exception as error:
                if report['cases']:
                    case = report['cases'][-1]
                    case['status'] = 'failed'
                    case['error'] = str(error)
                    if 'page' in locals():
                        failure_evidence(page, case)
                raise
            browser.close()
        validate_complete_cases(report['cases'])
        report['status']='passed'
    except Exception as error:
        report['status'] = 'failed'
        report['error'] = str(error)
        if report['cases']:
            case = report['cases'][-1]
            case['status'] = 'failed'
            case['error'] = str(error)
        raise
    finally:
        (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(f'Policy credit: {len(report["cases"])} actual built bilingual cases passed')


if __name__ == '__main__':
    main()
