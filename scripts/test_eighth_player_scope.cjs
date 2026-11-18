/* Cross-topic integration: keep old and new player focus scopes disjoint. */
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const source=fs.readFileSync('docs/javascripts/concept-motion.js','utf8');
const families=[
 ['kalman-gain-fusion',null],['particle-weight-resampling',null],['unrelated-topic',null],
 ['ucb1-optimism-switch',null],['gqa-head-sharing',null],
 ['paged-block-mapping','concept-motion-inference'],['expert-cache-miss','concept-motion-inference'],
 ['strips-state-effects','concept-motion-wide'],['graphplan-layer-extraction','concept-motion-wide'],
 ['layernorm-feature-shift','norm-seq-wide'],['seq2seq-context-handoff','norm-seq-wide'],
 ...['sliding-window-mask','linear-attention-recurrence','sliding-window-depth-reach','linear-attention-work-growth','gqa-cache-growth','global-local-pair-count','flashattention-online-rescale','flashattention-exact-merge','flashattention-causal-tiles','flashattention-backward-remat','flashattention2-query-parallel','flashattention3-load-compute-pipeline'].map(x=>[x,'attention-motion-wide'])
];
function verify(src){
 for(const [stem,scope] of families)for(const reduced of [true,false])for(const zh of [true,false]){
  const all=[];
  class El{constructor(tag){this.tag=tag;this.attrs={};this.dataset={};this.children=[];this.events={};this.className='';this.classList={add:n=>this.className+=' '+n};all.push(this)}setAttribute(k,v){this.attrs[k]=v}getAttribute(k){return this.attrs[k]??null}append(x){this.children.push(x)}before(x){this.host=x}addEventListener(k,f){this.events[k]=f}}
  const img=new El('img');img.attrs.src=`/assets/concept-animations/${stem}-still.svg?v=1#example`;img.dataset.motionSrc=img.attrs.src.replace('-still.svg','-motion.svg');img.dataset.stillSrc=img.attrs.src;img.alt=zh?'教學圖':'Teaching diagram';
  const document={readyState:'complete',querySelectorAll:()=>[img],createElement:t=>new El(t)};
  vm.runInNewContext(src,{document,window:{matchMedia:()=>({matches:reduced,addEventListener(){}})}});
  assert.equal(img.dataset.conceptMotionEnhanced,'yes');assert.equal(img.host.tabIndex,scope?0:undefined,stem+' focus scope');
  assert.equal(img.host.attrs.role,scope?'region':undefined,stem+' region scope');
  if(scope){assert.ok(img.host.className.split(/\s+/).includes(scope));assert.ok(img.host.attrs['aria-label']);}
  assert.equal(img.attrs.src,reduced?img.dataset.stillSrc:img.dataset.motionSrc);
  const toggle=all.find(e=>e.tag==='button');toggle.events.click();assert.equal(img.attrs.src,reduced?img.dataset.motionSrc:img.dataset.stillSrc);
 }
}
verify(source);
const marker="host.className = 'concept-motion-player';";assert.ok(source.includes(marker));
assert.throws(()=>verify(source.replace(marker,marker+'host.tabIndex=0;')),/focus scope/);
console.log(`${families.length*4} actual shared-player topic/locale/motion cases plus global-focus mutation PASS`);
