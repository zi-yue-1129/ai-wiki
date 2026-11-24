#!/usr/bin/env python3
"""Full eight-page prose matrix with rendered formula/scroll evidence."""
from pathlib import Path
import json,os
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from test_built_motion_browser import serve_site,assert_document_fits,check_math_rendering
ROOT=Path(__file__).resolve().parents[1]
SOURCES=tuple('docs/theory/models/time-series/'+s+l for s in ['index','deepar','n-beats','informer'] for l in ['.md','.zh-TW.md'])
WIDTHS=(320,390,1280)
def target(source):
 source=source.removeprefix('docs/');lang='zh-TW' if source.endswith('.zh-TW.md') else 'en';stem=source.removesuffix('.md').removesuffix('.zh-TW');path=stem.removesuffix('index') if stem.endswith('/index') else stem+'/'
 return lang,('' if lang=='en' else 'zh-TW/')+path

def validate_coverage(cases):
 expected={(s,target(s)[0],w) for s in SOURCES for w in WIDTHS}
 keys=[(c['source'],c['lang'],c['width']) for c in cases]
 assert len(keys)==len(set(keys))==24 and set(keys)==expected,'missing, duplicate or unexpected prose case'
 assert all(c.get('status')=='passed' and not c.get('errors') for c in cases),'failed or incomplete prose case'

def validate_formula(m):
 assert not m.get('error'),m
 assert m['width']>0 and m['mathWidth']>0,m
 if m['overflow']:
  assert m['display'] and m['overflowX'] in ('auto','scroll'),m
  assert m['scrollWidth']>m['clientWidth']+1,m
  assert m['after']>0 and abs(m['after']-m['maxScroll'])<=1,m
  assert m['mathRight']<=m['clipRight']+1 and m['mathRight']>=m['clipLeft']-1,m
  assert m['clipLeft']>=-1 and m['clipRight']<=m['width']+1,m
 else:assert m['mathLeft']>=-1 and m['mathRight']<=m['width']+1,m

MEASURE_FORMULA=r'''async (node) => {
 const math=node.querySelector('mjx-math')||node.querySelector('svg')||node;
 const display=node.getAttribute('display')==='true';
 const box=math.getBoundingClientRect();
 let scroller=null;
 for(let e=node;e && !e.classList.contains('md-content__inner');e=e.parentElement){
   const style=getComputedStyle(e);
   if(e.scrollWidth>e.clientWidth+1 && ['auto','scroll','hidden','clip'].includes(style.overflowX)){scroller=e;break;}
 }
 const result={display,width:innerWidth,mathWidth:box.width,mathLeft:box.left,mathRight:box.right,overflow:!!scroller};
 if(scroller){
   result.overflowX=getComputedStyle(scroller).overflowX;
   result.scrollWidth=scroller.scrollWidth;result.clientWidth=scroller.clientWidth;
   result.maxScroll=scroller.scrollWidth-scroller.clientWidth;result.before=scroller.scrollLeft;
   node.__qaScroll={element:scroller,left:scroller.scrollLeft};
   scroller.scrollLeft=result.maxScroll;
   await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
   const edge=scroller.getBoundingClientRect(),final=math.getBoundingClientRect();
   result.after=scroller.scrollLeft;result.mathLeft=final.left;result.mathRight=final.right;
   result.clipLeft=edge.left+scroller.clientLeft;result.clipRight=result.clipLeft+scroller.clientWidth;
 }
 // Reject clipping by any non-scrollable ancestor, even when document width fits.
 for(let e=node.parentElement;e && !e.classList.contains('md-content__inner');e=e.parentElement){
   if(e===scroller)continue;
   const x=getComputedStyle(e).overflowX,r=e.getBoundingClientRect(),m=math.getBoundingClientRect();
   if(['hidden','clip'].includes(x) && (m.left<r.left-1 || m.right>r.right+1))result.error='formula clipped by ancestor';
 }
 return result;
}'''
RESET_FORMULA='''node=>{if(node.__qaScroll){node.__qaScroll.element.scrollLeft=node.__qaScroll.left;delete node.__qaScroll;}}'''

def main():
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--sources',nargs='+');p.add_argument('--manifest',type=Path);p.add_argument('--site-dir',type=Path,default=ROOT/'site');p.add_argument('--output',type=Path,default=ROOT/'artifacts/time-series-prose');args=p.parse_args()
 entries=json.loads(args.manifest.read_text()) if args.manifest else (args.sources or SOURCES);entries=[{'source':x} if isinstance(x,str) else x for x in entries]
 args.output.mkdir(parents=True,exist_ok=True);report={'status':'running','cases':[]}
 try:
  assert len(entries)==8 and {e['source'] for e in entries}==set(SOURCES),'full source matrix required'
  with serve_site(args.site_dir.resolve(),'https://zi-yue-1129.github.io/ai-wiki/') as base,sync_playwright() as p:
   browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
   for entry in entries:
    source=entry['source'];lang,relative=target(source)
    for width in WIDTHS:
     case={'source':source,'lang':lang,'width':width,'status':'running','errors':[],'formulas':[],'screenshots':[]};report['cases'].append(case)
     folder=args.output/(source.replace('/','__').removesuffix('.md')+f'-{width}');folder.mkdir(exist_ok=True)
     page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce');page.on('pageerror',lambda e,c=case:c['errors'].append(str(e)))
     def shot(name):page.screenshot(path=str(folder/name));case['screenshots'].append(name)
     try:
      url=urljoin(base,relative)
      if entry.get('overview'):
       from posixpath import relpath
       _,overview=target(entry['overview']);response=page.goto(urljoin(base,overview),wait_until='load');assert response and response.ok
       link=page.locator(f'.md-content__inner a[href="{relpath(relative,overview)+"/"}"]').first;assert link.count()==1;link.click();page.wait_for_url(url,wait_until='commit')
      else:
       response=page.goto(url,wait_until='load');assert response and response.ok
      assert page.locator('html').get_attribute('lang')==lang
      case['math']=check_math_rendering(page);page.evaluate('document.fonts.ready');case['layout']=assert_document_fits(page,{'width':width})
      assert page.locator('.md-content__inner h1').count()==1;shot('top.png')
      for name,selector in [('math','.md-content__inner mjx-container'),('table','.md-content__inner table')]:
       el=page.locator(selector).first
       if el.count():el.scroll_into_view_if_needed();shot(name+'.png')
      formulas=page.locator('.md-content__inner mjx-container').all();assert formulas,'expected rendered formulas'
      for i,el in enumerate(formulas):
       el.scroll_into_view_if_needed();shot(f'equation-{i:02d}.png')
       try:
        m=el.evaluate(MEASURE_FORMULA);case['formulas'].append(m);validate_formula(m)
        assert_document_fits(page,{'width':width})
        if m['overflow']:
         name=f'equation-{i:02d}-right.png';shot(name);m['rightEdgeScreenshot']=name
       finally:el.evaluate(RESET_FORMULA)
      assert not case['errors'];case['status']='passed'
     except Exception as e:
      case.update(status='failed',error=str(e))
      try:shot('failure.png');case['diagnostics']=page.evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,wide:[...document.querySelectorAll(".md-content__inner *")].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>({tag:e.tagName,right:e.getBoundingClientRect().right,text:e.textContent.slice(0,120)}))})')
      except Exception as diagnostic_error:case['diagnostic_error']=str(diagnostic_error)
      raise
     finally:page.close()
   browser.close()
  validate_coverage(report['cases']);report['status']='passed'
 except Exception as e:report.update(status='failed',error=str(e));raise
 finally:(args.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print('24 bilingual time-series prose cases passed; horizontal scrolling tested programmatically, not by keyboard')
if __name__=='__main__':main()
