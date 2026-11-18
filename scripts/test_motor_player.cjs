const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const src=fs.readFileSync('docs/javascripts/concept-motion.js','utf8');
for(const stem of ['forward-prediction-correction','ofc-selective-feedback','some-other'])for(const reduced of [true,false])for(const zh of [true,false]){
 const all=[],listeners=[];let nav;
 class El{constructor(tag){this.tag=tag;this.attrs={};this.dataset={};this.children=[];this.events={};this.className='';this.classList={add:n=>this.className+=' '+n};all.push(this)}setAttribute(k,v){this.attrs[k]=v}getAttribute(k){return this.attrs[k]??null}append(x){this.children.push(x);x.parentElement=this}before(x){this.host=x}addEventListener(k,f){this.events[k]=f}}
 const img=new El('img'),original=`/assets/concept-animations/${stem}-${stem==='some-other'?'motion':'still'}.svg?v=1#figure`;img.attrs.src=original;if(stem!=='some-other'){img.dataset.motionSrc=original.replace('-still.svg','-motion.svg');img.dataset.stillSrc=original;}img.alt=zh?'示意動畫':'Illustrative animation';
 const media={matches:reduced,addEventListener:(k,f)=>listeners.push(f)},document={readyState:'complete',querySelectorAll:()=>[img],createElement:t=>new El(t)};
 vm.runInNewContext(src,{document,window:{matchMedia:()=>media,document$:{subscribe:f=>nav=f}}});
 const host=img.host,toggle=all.find(e=>e.tag==='button'),animated=original.replace('-still.svg','-motion.svg'),still=animated.replace('-motion.svg','-still.svg');
 assert.equal(img.attrs.src,reduced?still:animated);assert.equal(img.dataset.conceptMotionEnhanced,'yes');
 const viewport=all.find(e=>e.className==='concept-motion-viewport');if(stem==='some-other'){assert.equal(viewport,undefined);assert.equal(img.parentElement,host);assert.ok(host.children.includes(img));assert.ok(!host.className.includes('motor'))}else{assert.equal(viewport.tabIndex,0);assert.equal(img.parentElement,viewport);assert.equal(viewport.parentElement,host);assert.match(host.className,/concept-motion-motor/);assert.match(viewport.attrs['aria-label'],zh?/捲動/:/Scrollable/)}
 const count=all.length;nav();assert.equal(all.length,count,'instant navigation does not double enhance');
 listeners.forEach(f=>f({matches:!reduced}));assert.equal(img.attrs.src,!reduced?still:animated);
 toggle.events.click();assert.equal(img.attrs.src,reduced?still:animated);listeners.forEach(f=>f({matches:reduced}));assert.equal(img.attrs.src,reduced?still:animated,'manual preference wins');
 toggle.events.click();toggle.events.click();assert.equal(img.attrs.src,reduced?still:animated);
}
console.log('12 actual-player scenarios: scoped scrolling, source query/hash, repeated controls, media changes and navigation PASS');
