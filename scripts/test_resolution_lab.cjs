'use strict';
const fs=require('node:fs'), vm=require('node:vm'), assert=require('node:assert/strict'), path=require('node:path');
const file=process.argv[2] || path.join(__dirname,'../docs/javascripts/symbolic-proof-labs.js');
let code=fs.readFileSync(file,'utf8');
const marker="  if(document.readyState==='loading')";
assert(code.includes(marker));
code=code.replace(marker,'  globalThis.__resolutionTest={resolve,setupResolution,proofResults};\n'+marker);
class El {
 constructor(tag){this.tagName=tag;this.children=[];this.listeners={};this.className='';this.isConnected=true;this._text='';this.classList={add:(s)=>{this.className+=' '+s;}};}
 set textContent(s){this._text=String(s);this.children=[];}
 get textContent(){return this._text+this.children.map(c=>c.textContent).join('');}
 append(...cs){this.children.push(...cs);}
 replaceChildren(...cs){this._text='';this.children=cs;}
 setAttribute(k,v){this[k]=String(v);}
 addEventListener(k,f){this.listeners[k]=f;}
 fire(k){if(!this.disabled)this.listeners[k]?.({target:this});}
 all(cls){return [this,...this.children.flatMap(c=>c.all(cls))].filter(e=>e.className.split(' ').includes(cls));}
}
let timers=new Map(), next=0, mediaHandlers=[];const docListeners={};
const document={readyState:'loading',hidden:false,createElement:t=>new El(t),createTextNode:s=>{const e=new El('#text');e.textContent=s;return e;},addEventListener:(n,f)=>docListeners[n]=f};
const window={matchMedia:()=>({addEventListener:(n,f)=>mediaHandlers.push(f)}),setInterval:(f,ms)=>{timers.set(++next,{f,ms});return next;},clearInterval:i=>timers.delete(i)};
const ctx={document,window,console};vm.runInNewContext(code,ctx);const api=ctx.__resolutionTest;
const normalized=x=>JSON.parse(JSON.stringify(x));
assert.deepEqual(normalized(api.proofResults),[['Q','R'],['R'],[]]);
assert.deepEqual(normalized(api.resolve(['P','¬P'],['¬P'],'P')),['¬P']);
assert.deepEqual(normalized(api.resolve(['¬P','Q'],['P','R'],'P')),['Q','R']);
assert.throws(()=>api.resolve(['P'],['Q'],'P'));
for(const lang of ['en','zh']){
 const root=new El('root');api.setupResolution(root,lang);
 const buttons=root.all('sp-lab-btn'),[back,play,forward,reset]=buttons;
 const slider=root.all('sp-lab-seek')[0],select=root.all('sp-lab-select')[0];
 const counter=()=>root.all('sp-lab-counter')[0].textContent;
 const done=()=>root.all('sp-proof-done').length;
 assert.equal(counter(),'1 / 4');assert.equal(done(),0);assert(!root.textContent.includes('□'));
 forward.fire('click');assert.equal(done(),1);assert(!root.textContent.includes('□'));assert(root.all('sp-res-row')[0].textContent.includes('Q ∨ R'));
 forward.fire('click');assert.equal(done(),2);assert(!root.textContent.includes('□'));
 forward.fire('click');assert.equal(done(),3);assert(root.textContent.includes('□'));assert(forward.disabled);
 forward.fire('click');assert.equal(counter(),'4 / 4');
 back.fire('click');assert.equal(counter(),'3 / 4');assert(!root.textContent.includes('□'));
 reset.fire('click');reset.fire('click');assert.equal(counter(),'1 / 4');assert(!root.textContent.includes('□'));
 play.fire('click');assert.equal(timers.size,1);play.fire('click');assert.equal(timers.size,0);
 play.fire('click');select.value='2';select.fire('change');assert.equal(timers.size,1);assert.equal([...timers.values()][0].ms,500);
 [...timers.values()][0].f();assert.equal(counter(),'2 / 4');
 slider.value='3';slider.fire('input');assert.equal(counter(),'4 / 4');assert.equal(timers.size,0);
 play.fire('click');assert.equal(counter(),'1 / 4');assert.equal(timers.size,1);
 for(let i=0;i<3;i++) [...timers.values()][0].f();assert.equal(counter(),'4 / 4');assert.equal(timers.size,0);
 play.fire('click');document.hidden=true;docListeners.visibilitychange();assert.equal(timers.size,0);document.hidden=false;
 play.fire('click');mediaHandlers.at(-1)({matches:true});assert.equal(timers.size,0);
 play.fire('click');root.isConnected=false;[...timers.values()][0].f();assert.equal(timers.size,0);
}
console.log('PASS resolution inference semantics and bilingual repeated controls/seek/playback lifecycle');
