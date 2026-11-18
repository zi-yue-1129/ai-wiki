// Actual shared-player JS with a structural DOM. No computed layout or native-key claim.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
// Also works after commit, independent of git diff.
const topics=['theory/math/calculus/lagrange-multipliers','theory/math/calculus/newtons-method','theory/math/probability-statistics/maximum-a-posteriori','theory/math/probability-statistics/maximum-likelihood','theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction','theory/paradigms/probabilistic/uncertainty-calibration/temperature-scaling','theory/paradigms/unsupervised/clustering/k-means'];
let count=0;
for(const topic of topics)for(const lang of ['', '.zh-TW']){
 const source=fs.readFileSync('docs/'+topic+lang+'.md','utf8');
 for(const regionSource of source.matchAll(/<div class="reviewed-motion-scroll"[^>]*>[\s\S]*?<\/div>/g))for(const reduce of [false,true]){
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
  img.alt=img.attrs.alt;region.append(img);
  const red={matches:reduce,addEventListener:(k,f)=>red.change=f};let sub;
  const document={readyState:'complete',querySelectorAll:selector=>require('./concept_motion_fixture_selector.cjs')(selector,[img]),createElement:t=>new El(t)};
  vm.runInNewContext(fs.readFileSync('docs/javascripts/concept-motion.js','utf8'),{document,window:{matchMedia:()=>red,document$:{subscribe:f=>sub=f}}});
  assert.equal(img.parent.parent,region);assert.equal(region.attrs.tabindex,'0');assert.equal(region.attrs.role,'region');assert.equal(img.attrs.tabindex,undefined);
  const button=made.find(x=>x.tag==='button');assert(button);assert(img.attrs.src.endsWith(reduce?'-still.svg':'-motion.svg'));button.events.click();assert(img.attrs.src.endsWith(reduce?'-motion.svg':'-still.svg'));
  const n=made.length;sub();assert.equal(made.length,n);assert.equal(img.parent.parent,region);count++;
 }
}
assert.equal(count,40);console.log(`PASS ${count} actual shared-player structural DOM cases; focusable ancestor preserved, bilingual/reduced/toggle/reentry. Not a browser layout test.`);
