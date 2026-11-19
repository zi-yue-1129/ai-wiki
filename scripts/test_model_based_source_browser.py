#!/usr/bin/env python3
"""Chromium regression for PETS/MBPO concept motion and shared bilingual controls.

Run after: python -m pip install playwright; python -m playwright install chromium.
All assets are served in-memory; no external network or third-party assets.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
PLAYER = ROOT / 'docs/javascripts/concept-motion.js'
TOPICS = ('pets-ensemble-particles','pets-cem-refit','mbpo-short-branches','mbpo-horizon-error')
WIDTHS = (320, 360, 720, 1024)
OUT = ROOT / 'artifacts/model-based-source-browser'


def validate_image_state(state, expected):
    assert state['src'] == expected and state['currentSrc'] == expected, state
    assert state['complete'] and state['naturalWidth'] > 0 and state['naturalHeight'] > 0, state
    assert state['viewBox'] == [0, 0, 640, 360], state
    assert abs(state['width'] - 640) < .1 and abs(state['height'] - 360) < .1, state


def wait_for_image(page, expected, timeout=30000):
    # Intrinsic fallback size for an SVG with only viewBox is not CSS geometry.
    page.wait_for_function("""expected => {
      const i=document.querySelector('img'); return i && i.src===expected &&
      i.currentSrc===expected && i.complete && i.naturalWidth>0 && i.naturalHeight>0;
    }""", arg=expected, timeout=timeout)
    state = page.locator('img').evaluate(r"""async i => {
      const response=await fetch(i.currentSrc); if(!response.ok) throw Error('SVG HTTP failure');
      const doc=new DOMParser().parseFromString(await response.text(),'image/svg+xml');
      const svg=doc.documentElement;
      if(svg.namespaceURI!=='http://www.w3.org/2000/svg' || svg.localName!=='svg' || doc.querySelector('parsererror')) throw Error('Invalid SVG');
      const b=i.getBoundingClientRect();
      return {src:i.src,currentSrc:i.currentSrc,complete:i.complete,naturalWidth:i.naturalWidth,
        naturalHeight:i.naturalHeight,width:b.width,height:b.height,
        viewBox:(svg.getAttribute('viewBox')||'').trim().split(/\s+/).map(Number)};
    }""")
    validate_image_state(state, expected)
    return state


def save_failure(page, name):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / (name+'-failure.html')).write_text(page.content(), encoding='utf-8')
    state=page.locator('img').evaluate("""i=>({src:i.src,currentSrc:i.currentSrc,complete:i.complete,
      naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight,rect:i.getBoundingClientRect().toJSON()})""")
    (OUT / (name+'-failure.json')).write_text(json.dumps(state,indent=2), encoding='utf-8')
    page.screenshot(path=str(OUT / (name+'-failure.png')), full_page=True)


def check(browser, stem, width, chinese, reduced):
    context = browser.new_context(viewport={'width': width, 'height': 510}, reduced_motion='reduce' if reduced else 'no-preference')
    context.route('**/concept-animations/*.svg', lambda route: route.fulfill(
        status=200, content_type='image/svg+xml', headers={'Access-Control-Allow-Origin':'*'}, body=(ASSETS / route.request.url.rsplit('/', 1)[-1]).read_bytes()
    ))
    page = context.new_page()
    lang = 'zh-TW' if chinese else 'en'
    src = f'https://wiki.test/assets/concept-animations/{stem}-motion.svg'
    alt = '教學概念動畫' if chinese else 'Instructional concept animation'
    states=[]
    try:
        page.set_content(f'''<!doctype html><html lang="{lang}"><style>body{{margin:0;padding:8px}}img{{width:640px;min-width:640px;max-width:none;height:auto}}#scroll{{max-width:100%;overflow-x:auto}}button:focus-visible{{outline:3px solid #168b82}}</style><body><main><div id="scroll" tabindex="0" role="region" aria-label="Scrollable figure"><img alt="{alt}" src="{src.replace('-motion.svg','-still.svg')}" data-motion-src="{src}" data-still-src="{src.replace('-motion.svg','-still.svg')}"></div></main></body></html>''')
        page.add_script_tag(content=PLAYER.read_text(encoding='utf-8'))
        button = page.locator('button.concept-motion-toggle')
        assert button.count() == 1, f'{stem}: missing shared Play/Pause control'
        image = page.locator('img')
        states.append(wait_for_image(page, src.replace('-motion.svg', ('-still.svg' if reduced else '-motion.svg'))))
        assert image.get_attribute('src').endswith(('-still.svg' if reduced else '-motion.svg'))
        assert (('播放' if reduced else '暫停') in button.inner_text()) if chinese else (('Play' if reduced else 'Pause') in button.inner_text())
        assert button.get_attribute('aria-label')
        button.focus()
        assert button.evaluate('(b)=>document.activeElement===b'), 'button not focusable'
        page.keyboard.press('Enter')
        assert image.get_attribute('src').endswith(('-motion.svg' if reduced else '-still.svg')), f'{stem}: keyboard Enter failed'
        states.append(wait_for_image(page, src.replace('-motion.svg', ('-motion.svg' if reduced else '-still.svg'))))
        page.keyboard.press('Space')
        assert image.get_attribute('src').endswith(('-still.svg' if reduced else '-motion.svg')), f'{stem}: keyboard Space failed'
        states.append(wait_for_image(page, src.replace('-motion.svg', ('-still.svg' if reduced else '-motion.svg'))))
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{stem}: document overflow at {width}px'
        scroller = page.locator('#scroll')
        scroller.focus()
        assert scroller.evaluate('(e)=>document.activeElement===e')
        if width < 656:
            page.keyboard.press('ArrowRight')
            page.wait_for_function("document.querySelector('#scroll').scrollLeft>0")
            scroller.evaluate('(e)=>e.scrollLeft=e.scrollWidth')
            page.wait_for_timeout(150)
            assert scroller.evaluate('(e)=>Math.abs(e.scrollLeft-(e.scrollWidth-e.clientWidth))<2')
            OUT.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(OUT / f'{stem}-{width}-{lang}-{reduced}-right.png'))
            scroller.evaluate('(e)=>e.scrollLeft=0')
        OUT.mkdir(parents=True, exist_ok=True)
        image.screenshot(path=str(OUT / f'{stem}-{width}-{lang}-{("reduced" if reduced else "play")}.png'))
        (OUT / f'{stem}-{width}-{lang}-{reduced}-geometry.json').write_text(json.dumps(states,indent=2))
    except Exception:
        try:
            save_failure(page, f'{stem}-{width}-{lang}-{reduced}')
        except Exception as capture_error:
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / f'{stem}-{width}-{lang}-{reduced}-capture-error.json').write_text(json.dumps({'capture_error':repr(capture_error)}))
        raise
    finally:
        context.close()


def native_contract_negatives(browser):
    context=browser.new_context(viewport={'width':720,'height':510})
    page=context.new_page()
    svg=(ASSETS / (TOPICS[0]+'-still.svg')).read_bytes()
    context.route('**/fixture/*.svg',lambda route:route.fulfill(status=200,content_type='image/svg+xml',headers={'Access-Control-Allow-Origin':'*'},body=svg))
    expected='https://wiki.test/fixture/expected.svg'
    rows=[]
    try:
        for mode in ['valid','wrong-src','wrong-geometry','incomplete-load']:
            url=expected if mode!='wrong-src' else 'https://wiki.test/fixture/other.svg'
            if mode=='incomplete-load':
                # Retain the pending request without fulfilling it until teardown.
                context.route('**/fixture/pending.svg',lambda route:None)
                url='https://wiki.test/fixture/pending.svg'
            page.set_content(f'<img style="width:{639 if mode=="wrong-geometry" else 640}px;height:auto" src="{url}">',wait_until='domcontentloaded')
            failed=False
            try:wait_for_image(page, url if mode=='incomplete-load' else expected, timeout=1000)
            except Exception as error:
                if mode == 'wrong-geometry':
                    assert isinstance(error, AssertionError), repr(error)
                    assert abs(page.locator('img').bounding_box()['width']-639)<.1
                elif mode in ('wrong-src','incomplete-load'):
                    assert isinstance(error, PlaywrightTimeoutError), repr(error)
                    if mode == 'wrong-src':
                        assert page.locator('img').evaluate('(i)=>i.src') != expected
                    else:
                        assert page.locator('img').evaluate('(i)=>!i.complete')
                else:
                    raise
                failed=True
                save_failure(page,'contract-'+mode)
            assert failed == (mode!='valid'), mode
            rows.append({'mode':mode,'rejected':failed})
        (OUT/'contract-report.json').write_text(json.dumps(rows,indent=2))
    finally:context.close()


def main():
    assert PLAYER.is_file(), 'shared concept-motion.js missing'
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, **({'executable_path': '/usr/bin/chromium'} if Path('/usr/bin/chromium').is_file() else {}), args=['--no-sandbox'])
        for stem in TOPICS:
            for width in WIDTHS:
                for chinese in (False, True):
                    for reduced in (False, True):
                        check(browser, stem, width, chinese, reduced)
        native_contract_negatives(browser)
        browser.close()
    print('PETS/MBPO: 64 Chromium SVG/player checks (English, zh-TW, reduced motion), keyboard Enter/Space, source-owned focusable local scroll and whole-document bounds: PASS')


if __name__ == '__main__':
    main()
