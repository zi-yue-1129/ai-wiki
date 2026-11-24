"""Real browser regression for CTDE learning sources; run alongside built-site CI."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';OUT=R/'artifacts/marl-source'
css=(R/'docs/stylesheets/concept-motion.css').read_text();js=(R/'docs/javascripts/concept-motion.js').read_text()

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 count=0;report={"status":"running","cases":[]}
 try:
  with sync_playwright() as p:
   b=p.chromium.launch(headless=True)
   for stem in ['maddpg-actor-gradient','maddpg-joint-bootstrap','mappo-shared-advantage','mappo-backward-gae']:
    size=640
    for lang in ['en','zh']:
     for width in [320,390,1024]:
      for reduced in ['reduce','no-preference']:
       page=b.new_page(viewport={'width':width,'height':650},reduced_motion=reduced)
       record={"stem":stem,"lang":lang,"width":width,"reduced":reduced,"status":"running"};report["cases"].append(record)
       try:
        page.route('**/assets/concept-animations/*.svg',lambda route:route.fulfill(content_type='image/svg+xml',body=(A/route.request.url.split('/')[-1]).read_text()))
        alt='集中訓練與分散執行' if lang=='zh' else 'Centralized training and decentralized execution'
        page.set_content(f'<style>body{{margin:0}}{css}</style><main class="md-typeset"><div class="marl-source-scroll" tabindex="0" style="max-width:100%;overflow-x:auto"><img src="https://wiki.example/assets/concept-animations/{stem}-still.svg" data-motion-src="https://wiki.example/assets/concept-animations/{stem}-motion.svg" data-still-src="https://wiki.example/assets/concept-animations/{stem}-still.svg" alt="{alt}" style="width:{size}px;min-width:{size}px;max-width:none;height:auto"></div></main>')
        page.wait_for_function(f'document.querySelector("img").naturalWidth==={size}')
        assert page.evaluate('document.documentElement.scrollWidth')==width
        page.add_script_tag(content=js);button=page.locator('button');assert button.count()==1
        assert page.locator('img').get_attribute('src').endswith('-still.svg' if reduced=='reduce' else '-motion.svg')
        button.press('Enter');button.press('Space')
        if width<size:
         page.locator('.marl-source-scroll').focus();page.keyboard.press('ArrowRight');page.wait_for_function('document.querySelector(".marl-source-scroll").scrollLeft>0')
        assert page.evaluate('document.documentElement.scrollWidth')==width
        page.screenshot(path=str(OUT/f'{stem}-{lang}-{width}-{reduced}.png'));count+=1
        record["status"]="passed"
       except Exception as error:
        record.update(status="failed",error=repr(error))
        try:
         record["dom"]=page.evaluate('() => ({readyState:document.readyState,images:[...document.images].map(i=>({src:i.src,naturalWidth:i.naturalWidth,enhanced:i.dataset.conceptMotionEnhanced||null})),eligible:document.querySelectorAll(\'img[src*="concept-animations/"]\').length,buttons:document.querySelectorAll("button").length})')
         page.screenshot(path=str(OUT/f"{stem}-{lang}-{width}-{reduced}-failure.png"))
         (OUT/f"{stem}-{lang}-{width}-{reduced}-failure.html").write_text(page.content())
        except Exception as capture:record["capture_error"]=repr(capture)
        raise
       finally:page.close()
   b.close()
  expected={(s,l,w,r)for s in ['maddpg-actor-gradient', 'maddpg-joint-bootstrap', 'mappo-shared-advantage', 'mappo-backward-gae'] for l in ('en','zh')for w in (320,390,1024)for r in ('reduce','no-preference')}
  observed=[(c['stem'],c['lang'],c['width'],c['reduced'])for c in report['cases']]
  assert count==len(observed)==len(set(observed))==48 and set(observed)==expected
  assert all(c['status']=='passed'for c in report['cases'])
  report['status']='passed'
  print(f'PASS {count} bilingual/reduced/mobile/keyboard cases')
 except Exception as error:
  report.update(status='failed',error=repr(error));raise
 finally:(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
