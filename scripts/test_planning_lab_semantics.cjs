const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const source=fs.readFileSync('docs/javascripts/planning-labs.js','utf8');
function setup(kind,zh,reduced=false){
 class El{constructor(){this.events={};this.attrs={};this.value='';this.checked=true;this.type='';this.textContent='';this.innerHTML=''}addEventListener(k,f){this.events[k]=f}setAttribute(k,v){this.attrs[k]=v}}
 const controls={};for(const key of ['svg','.planning-parameters','.planning-status','prev','next','play','seek','speed','reset','atA','charged','goal'])controls[key]=new El();
 controls.atA.type=controls.charged.type='checkbox';controls.goal.value='C';controls.speed.value='1';
 const params=kind==='strips'?[controls.atA,controls.charged]:[controls.goal];
 const host={dataset:{planningLab:kind,lang:zh?'zh-TW':'en'},isConnected:true,querySelector:s=>{let k=s.match(/data-[ap]=([^\]]+)/)?.[1]||s;if((kind==='strips'&&k==='goal')||(kind==='graphplan'&&['atA','charged'].includes(k)))return null;return controls[k]},querySelectorAll:()=>params};
 const listeners={},timers=new Map();let id=0;const document={readyState:'complete',hidden:false,querySelectorAll:()=>[host],addEventListener:(k,f)=>listeners[k]=f};
 vm.runInNewContext(source,{document,window:{matchMedia:()=>({matches:reduced,addEventListener:(k,f)=>listeners.media=f})},setInterval:f=>{timers.set(++id,f);return id},clearInterval:i=>timers.delete(i)});
 return {host,controls,document,listeners,timers,click:k=>controls[k].events.click(),seek:n=>{controls.seek.value=String(n);controls.seek.events.input()},change:k=>controls[k].events.change({target:controls[k]}),tick:()=>[...timers.values()].forEach(f=>f())};
}
for(const zh of [false,true]){
 for(const atA of [false,true])for(const charged of [false,true]){
  const h=setup('strips',zh);h.controls.atA.checked=atA;h.controls.charged.checked=charged;h.change('atA');h.seek(4);
  const expected=[...(charged?['Charged']:[]),...(atA?['At(B)']:[])];assert.ok(h.controls['.planning-status'].textContent.endsWith('{'+expected.join(', ')+'}'));
  assert.equal(h.controls.svg.innerHTML.includes('− At(A)'),atA);assert.equal(h.controls.svg.innerHTML.includes('+ At(B)'),atA);
  h.click('reset');assert.equal(h.controls.seek.value,'0');h.click('next');h.click('prev');assert.equal(h.controls.seek.value,'0');h.click('play');h.tick();assert.equal(h.controls.seek.value,'1');h.host.isConnected=false;h.tick();assert.equal(h.timers.size,0);
 }
 const h=setup('graphplan',zh);h.seek(0);assert.match(h.controls['.planning-status'].textContent,/F0=\{At\(A\)\}/);h.seek(1);assert.match(h.controls['.planning-status'].textContent,/F1=\{At\(A\), At\(B\)\}/);h.seek(4);assert.match(h.controls['.planning-status'].textContent,/Move\(A,B\) → Move\(B,C\)/);
 assert.ok(h.controls.svg.innerHTML.includes('M218 75 L296 128'));assert.ok(h.controls.svg.innerHTML.includes('M458 128 L536 181'));
 h.controls.goal.value='AB';h.change('goal');assert.match(h.controls['.planning-status'].textContent,zh?/互斥/:/mutex/);h.click('reset');h.click('play');h.controls.speed.value='2';h.change('speed');assert.equal(h.timers.size,1);h.document.hidden=true;h.listeners.visibilitychange();assert.equal(h.timers.size,0);h.click('play');h.listeners.media({matches:true});assert.equal(h.timers.size,0);
 for(const kind of ['strips','graphplan']){const r=setup(kind,zh,true);r.click('play');assert.equal(r.timers.size,0);r.click('next');assert.equal(r.controls.seek.value,'1')}
}
console.log('Planning actual-JS truth tables, mutex goals, controls, hidden/reduced/detached interruption PASS');
