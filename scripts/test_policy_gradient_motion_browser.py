#!/usr/bin/env python3
"""Real Chromium visual and bilingual player checks for REINFORCE / GRPO."""
import json
import os
import traceback
import time
from pathlib import Path
from shutil import which
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
JS = ROOT / "docs/javascripts/concept-motion.js"
CSS = ROOT / "docs/stylesheets/concept-motion.css"
STEMS = ["reinforce-return-credit", "grpo-group-advantages"]
OUT = Path(os.environ.get("POLICY_GRADIENT_MOTION_OUTPUT", ROOT / "artifacts/policy-gradient-motion"))
TIMES = [0, 2, 4, 6, 9, 11]

def cases():
    result = []
    for stem in STEMS:
        for kind in ("motion", "still"):
            result.append(dict(stem=stem, kind=kind, test="svg", times=TIMES if kind=="motion" else [0]))
        for lang in ("en", "zh"):
            for width in (320, 360, 720, 1024):
                result.append(dict(stem=stem, test="player", lang=lang, width=width, reduced=False))
            result.append(dict(stem=stem, test="player", lang=lang, width=320, reduced=True))
    return result

# Shared pure checker retains original bounds and overlap arithmetic unchanged.
from policy_glyph_contract import check_boxes, validate_glyph_sample
from policy_line_clearance import check_return_credit_clearance

def shot(page, record, name):
    path = OUT / record["id"] / (name + ".png")
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(path), full_page=True, animations="allow")
    record.setdefault("screenshots", []).append(str(path.relative_to(OUT)))

def check_svg(page, stem, kind, record):
    page.set_content((ASSETS / f"{stem}-{kind}.svg").read_text(encoding="utf-8"),
                     wait_until="domcontentloaded")
    for t in (TIMES if kind == "motion" else [0]):
        if kind == "motion":
            page.evaluate('(t) => { const s=document.querySelector("svg"); s.pauseAnimations(); s.setCurrentTime(t); }', t)
        boxes = page.evaluate("""() => Array.from(document.querySelectorAll('svg text')).map(e => {
          const b=e.getBBox(); return {label:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height};
        })""")
        canvas = page.evaluate("() => { const b=document.querySelector('svg').viewBox.baseVal; return [b.x,b.y,b.width,b.height]; }")
        sample = dict(time=t, canvas=canvas, boxes=boxes)
        record.setdefault("samples", []).append(sample)
        shot(page, record, "time-"+str(t))
        validate_glyph_sample(sample, stem, kind, t)
        if stem == "reinforce-return-credit":
            geometry = page.evaluate("""() => {
              const label = Array.from(document.querySelectorAll('svg text')).find(e => e.textContent === 'Reward-to-go');
              const paths = Array.from(document.querySelectorAll('svg path')).filter(e => e.getAttribute('stroke') === '#d46a3a');
              if (!label || paths.length !== 1) throw new Error('Missing or ambiguous reward-to-go geometry');
              const box = e => { const b=e.getBBox(); return {x:b.x,y:b.y,w:b.width,h:b.height}; };
              return {text:box(label),line:box(paths[0]),stroke:Number.parseFloat(getComputedStyle(paths[0]).strokeWidth)};
            }""")
            clearance = dict(time=t, geometry=geometry)
            record.setdefault('line_clearance', []).append(clearance)
            clearance['gap'] = check_return_credit_clearance(geometry['text'], geometry['line'], geometry['stroke'])

IMAGE_READY = """expected => {const i=document.querySelector('img');return !!i && i.getAttribute('src')===expected && i.currentSrc===expected && i.complete && i.naturalWidth===760 && i.naturalHeight===400 && i.isConnected;}"""
IMAGE_STATE = """i => ({src:i.getAttribute('src'),currentSrc:i.currentSrc,complete:i.complete,width:i.naturalWidth,height:i.naturalHeight,connected:i.isConnected})"""

IMAGE_DECODE = """(i, timeout) => {
  let timer;
  return Promise.race([
    Promise.resolve().then(()=>i.decode()),
    new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error('Image decode timeout')),timeout);})
  ]).finally(()=>clearTimeout(timer));
}"""

def validate_image_state(state, expected):
    assert state['src']==state['currentSrc']==expected, state
    assert state['complete'] is True and state['connected'] is True, state
    assert state['width']==760 and state['height']==400, state

def ready_image(page, img, expected, record, stage):
    """Controls are synchronous; an exact newly selected resource must also decode."""
    sample=dict(stage=stage,expected=expected,time=time.monotonic(),before=img.evaluate(IMAGE_STATE))
    record.setdefault('image_states',[]).append(sample)
    try:
        assert img.count()==1
        page.wait_for_function(IMAGE_READY,arg=expected,timeout=5000)
        img.evaluate(IMAGE_DECODE,5000)
        sample['after']=img.evaluate(IMAGE_STATE)
        validate_image_state(sample['after'],expected)
        sample['status']='passed'
    except Exception as error:
        sample['status']='failed';sample['error']=repr(error)
        sample['failure_state']=img.evaluate(IMAGE_STATE)
        raise

def check_player(browser, stem, lang, width, reduced=False, record=None):
    context=browser.new_context(viewport={"width":width,"height":550},
              reduced_motion="reduce" if reduced else "no-preference")
    page=context.new_page()
    page.on("pageerror", lambda e: record["page_errors"].append(str(e)))
    def failed(request):
        record['failed_requests'].append(request.url)
        record.setdefault('request_failures',[]).append(dict(url=request.url,reason=request.failure,time=time.monotonic()))
    page.on("requestfailed",failed)
    page.on('response',lambda response:record.setdefault('responses',[]).append(dict(url=response.url,status=response.status,time=time.monotonic())))
    base="https://aiwiki.test/assets/concept-animations/"
    def route_svg(route):
        name=route.request.url.split("/")[-1]
        assert name in (f"{stem}-still.svg",f"{stem}-motion.svg"), name
        route.fulfill(status=200, content_type="image/svg+xml", body=(ASSETS/name).read_bytes())
    page.route("https://aiwiki.test/assets/concept-animations/*",route_svg)
    alt=("回報與群組優勢動畫" if lang=="zh" else "Policy gradient animation")
    html=f"""<main style="max-width:100%;padding:8px">
    <div role="region" tabindex="0" aria-label="Scroll horizontally to inspect"
         style="max-width:100%;overflow-x:auto">
      <img style="width:760px;max-width:none;height:auto"
           src="{base}{stem}-still.svg"
           data-motion-src="{base}{stem}-motion.svg"
           data-still-src="{base}{stem}-still.svg" alt="{alt}">
    </div></main>"""
    page.set_content(html,wait_until="domcontentloaded")
    img=page.locator("img")
    ready_image(page,img,base+stem+"-still.svg",record,"initial-still-before-enhancement")
    page.add_style_tag(content=CSS.read_text(encoding="utf-8"))
    page.add_script_tag(content=JS.read_text(encoding="utf-8"))
    img=page.locator("img")
    button=page.locator("button.concept-motion-toggle")
    button.wait_for(timeout=5000)
    ready_image(page,img,base+stem+("-still.svg" if reduced else "-motion.svg"),record,"enhanced")
    assert img.evaluate("(i)=>i.complete && i.naturalWidth===760")
    assert button.count()==1
    assert img.get_attribute("src").endswith("-still.svg" if reduced else "-motion.svg")
    region=page.locator('[role=region]')
    dimensions=region.evaluate("(e)=>({client:e.clientWidth,scroll:e.scrollWidth})")
    if width<=360:
        assert dimensions["scroll"]>=760 and dimensions["scroll"]>dimensions["client"], dimensions
        region.focus()
        region.evaluate("(e)=>{e.scrollLeft=e.scrollWidth-e.clientWidth}")
        assert region.evaluate("(e)=>e.scrollLeft>0")
    shot(page, record, "initial")
    button.click()
    assert img.get_attribute("src").endswith("-motion.svg" if reduced else "-still.svg")
    ready_image(page,img,base+stem+("-motion.svg" if reduced else "-still.svg"),record,"clicked")
    shot(page, record, "clicked")
    button.focus()
    page.keyboard.press("Enter")
    assert img.get_attribute("src").endswith("-still.svg" if reduced else "-motion.svg")
    ready_image(page,img,base+stem+("-still.svg" if reduced else "-motion.svg"),record,"entered")
    shot(page, record, "entered")
    button.focus()
    page.keyboard.press("Space")
    assert img.get_attribute("src").endswith("-motion.svg" if reduced else "-still.svg")
    ready_image(page,img,base+stem+("-motion.svg" if reduced else "-still.svg"),record,"spaced")
    shot(page, record, "spaced")
    if not img.get_attribute("src").endswith("-still.svg"):
        button.click()
    assert img.get_attribute("src").endswith("-still.svg")
    ready_image(page,img,base+stem+"-still.svg",record,"final-still")
    assert img.evaluate("(i)=>i.complete && i.naturalWidth===760")
    shot(page, record, "final-still")
    context.close()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"status": "running", "original_source": "PR1124@e552657b72201fd94907effba63d5d0b31d1a874", "cases": cases()}
    for i, record in enumerate(report["cases"]):
        record.update(id=f"case-{i+1:02}", status="pending", page_errors=[], failed_requests=[])
    def save():
        (OUT/"report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    save()
    browser = None
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_EXECUTABLE") or which("chromium") or None)
            for record in report["cases"]:
                record["status"]="running"; save()
                def watch(page):
                    page.on("pageerror", lambda e: record["page_errors"].append(str(e)))
                    page.on("requestfailed", lambda request: record["failed_requests"].append(request.url))
                try:
                    if record["test"] == "svg":
                        page=browser.new_page(viewport={"width":760,"height":400})
                        watch(page)
                        check_svg(page, record["stem"], record["kind"], record)
                    else:
                        check_player(browser, record["stem"], record["lang"], record["width"], record["reduced"], record)
                    assert not record["page_errors"], record["page_errors"]
                    assert not record["failed_requests"], record["failed_requests"]
                    record["status"]="passed"
                except Exception:
                    record["status"]="failed";record["error"]=traceback.format_exc()
                    for context in browser.contexts:
                        for page in context.pages:
                            try:
                                shot(page, record, "failure")
                                (OUT/record['id']/'failure.html').write_text(page.content(),encoding='utf-8')
                            except Exception as exc: record.setdefault("screenshot_errors",[]).append(str(exc))
                finally:
                    for context in browser.contexts: context.close()
                    save()
            browser.close()
            report["status"]="passed" if all(c["status"]=="passed" for c in report["cases"]) else "failed"
    except Exception:
        report["status"]="failed";report["error"]=traceback.format_exc()
        for record in report["cases"]:
            if record["status"] in ("pending","running"):record["status"]="blocked"
    finally: save()
    print(f"Policy-gradient motion Chromium checks: {sum(c['status']=='passed' for c in report['cases'])}/24 successful cases")
    return 0 if report["status"]=="passed" else 1

if __name__=="__main__":
    raise SystemExit(main())
