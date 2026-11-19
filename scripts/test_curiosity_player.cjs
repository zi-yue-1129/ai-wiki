// Actual shared-player JS with a structural DOM. No computed layout or native-key claim.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
// Also works after commit, independent of git diff.
const topics=['theory/paradigms/reinforcement-learning/exploration/rnd/index','theory/paradigms/reinforcement-learning/exploration/icm/index'];
let count=0;const observed=[];
for(const topic of topics)for(const lang of ['', '.zh-TW']){
 const source=fs.readFileSync('docs/'+topic+lang+'.md','utf8');
 for(const regionSource of source.matchAll(/<div style="max-width:100%;overflow-x:auto"[^>]*>[\s\S]*?<\/div>/g))for(const reduce of [false,true])for(const width of [390,640,641,1280])for(const suffix of ["","?v=1","#sample"]){
  const narrow=width<=640;
  const raw=regionSource[0].match(/<img\b[^>]*data-source-asset-urls[^>]*>/);
  const made=[];class El{
   constructor(tag){this.tag=tag;this.attrs={};this.dataset={};this.children=[];this.events={};made.push(this);}
   setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return this.attrs[k]??null;}
   append(...xs){for(const x of xs){if(x.parent){x.parent.children=x.parent.children.filter(y=>y!==x);}x.parent=this;this.children.push(x);}}
   before(x){let p=this.parent;p.children.splice(p.children.indexOf(this),0,x);x.parent=p;}
   addEventListener(k,f){this.events[k]=f;}
  }
  const region=new El('div');for(const m of regionSource[0].split('>')[0].matchAll(/([\w-]+)="([^"]*)"/g))region.setAttribute(m[1],m[2]);
  assert(region.attrs.style.includes('overflow-x:auto'));
  const img=new El('img');for(const m of raw[0].matchAll(/([\w-]+)="([^"]*)"/g)){img.attrs[m[1]]=m[2];if(m[1].startsWith('data-'))img.dataset[m[1].slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=m[2];}
  for(const key of ['src','data-motion-src','data-still-src']) if(img.attrs[key]){img.attrs[key]+=suffix;if(key.startsWith('data-'))img.dataset[key.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=img.attrs[key];}
  img.alt=img.attrs.alt;const inner=new El('div');inner.setAttribute('style','width:720px');region.append(inner);inner.append(img);
  const red={matches:reduce,addEventListener:(k,f)=>red.change=f};const viewport={matches:narrow,addEventListener:(k,f)=>viewport.change=f};let sub;
  const document={readyState:'complete',querySelectorAll:selector=>require('./concept_motion_fixture_selector.cjs')(selector,[img]),createElement:t=>new El(t)};
  vm.runInNewContext(fs.readFileSync('docs/javascripts/concept-motion.js','utf8'),{document,window:{matchMedia:q=>q.includes("max-width")?(assert.equal(q,"(max-width: 640px)"),viewport):red,document$:{subscribe:f=>sub=f}}});
  assert.equal(img.parent.parent,inner);assert.equal(region.attrs.tabindex,'0');assert.equal(region.attrs.role,'group');assert.equal(img.attrs.tabindex,undefined);
  observed.push({width,base:img.attrs[reduce?'data-still-src':'data-motion-src'],actual:img.attrs.src});
  const button=made.find(x=>x.tag==='button');assert(button);assert(img.attrs.src.split(/[?#]/)[0].endsWith(reduce?'-still.svg':'-motion.svg'));button.events.click();assert(img.attrs.src.split(/[?#]/)[0].endsWith(reduce?'-motion.svg':'-still.svg'));
  const n=made.length;sub();assert.equal(made.length,n);assert.equal(img.parent.parent,inner);const mobile=/\/(?:rnd-state-novelty|icm-predictable-stochastic)-/.test(img.attrs['data-motion-src']);
  assert.equal(img.attrs.src.includes('-mobile-'),mobile&&narrow);
  if(mobile){viewport.matches=!narrow;viewport.change();assert.equal(img.attrs.src.includes('-mobile-'),!narrow);}
  count++;
 }
}
assert.equal(count,864); if(process.env.REPORT_RESPONSIVE)console.log(JSON.stringify(observed));console.log(`PASS ${count} actual shared-player structural DOM cases; focusable ancestor preserved, bilingual/reduced/toggle/reentry. Not a browser layout test.`);
