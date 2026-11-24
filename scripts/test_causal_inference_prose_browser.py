"""Real built MathJax/layout evidence: six causal prose pages at 320/390/1280."""
import argparse,json,os
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from test_built_prose_browser import target
from test_built_motion_browser import serve_site,check_math_rendering,assert_document_fits
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[f'docs/theory/causal-inference/{stem}{lang}.md' for stem in ['index','double-machine-learning','causal-forests'] for lang in ['', '.zh-TW']]
WIDTHS=(320,390,1280)
def main():
 p=argparse.ArgumentParser();p.add_argument('--site-dir',type=Path,default=ROOT/'site');p.add_argument('--output',type=Path,default=ROOT/'artifacts/causal-prose');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 report={'status':'running','cases':[]}
 try:
  with serve_site(a.site_dir.resolve(),'https://zi-yue-1129.github.io/ai-wiki/') as base,sync_playwright() as pw:
   browser=pw.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
   for source in SOURCES:
    lang,relative=target(source)
    for width in WIDTHS:
     folder=a.output/(source.replace('/','__').removesuffix('.md')+f'-{width}');folder.mkdir(exist_ok=True)
     case={'source':source,'lang':lang,'width':width,'status':'running','errors':[],'screenshots':[]};report['cases'].append(case)
     page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce');page.on('pageerror',lambda e,c=case:c['errors'].append(str(e)))
     try:
      response=page.goto(urljoin(base,relative),wait_until='load');assert response and response.ok
      assert page.locator('html').get_attribute('lang')==lang
      case['math']=check_math_rendering(page);page.evaluate('document.fonts.ready');case['layout']=assert_document_fits(page,{'width':width})
      assert page.locator('.md-content__inner h1').count()==1
      if 'index' not in source:assert page.locator('.md-content__inner mjx-container').count()>0
      page.screenshot(path=str(folder/'top.png'));case['screenshots'].append('top.png')
      for n,el in enumerate(page.locator('.md-content__inner h1, .md-content__inner h2, .md-content__inner h3, .md-content__inner mjx-container[display="true"]').all()):
       el.scroll_into_view_if_needed();assert_document_fits(page,{'width':width});name=f'section-{n:02}.png';page.screenshot(path=str(folder/name));case['screenshots'].append(name)
      assert not case['errors'];case['status']='passed'
     except Exception as e:
      case.update(status='failed',error=str(e));page.screenshot(path=str(folder/'failure.png'));case['diagnostics']=page.evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,wide:[...document.querySelectorAll(".md-content__inner *")].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>({tag:e.tagName,text:e.textContent.slice(0,150),right:e.getBoundingClientRect().right}))})');raise
     finally:page.close()
   browser.close()
  assert len(report['cases'])==18 and all(c['status']=='passed' for c in report['cases']);report['status']='passed'
 except Exception as e:report.update(status='failed',error=str(e));raise
 finally:(a.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
