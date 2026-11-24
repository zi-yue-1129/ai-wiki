// Execute actual lab code in structural DOM; no native rendering claim.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
let scenarios=0;
for(const kind of ['rnd','icm'])for(const locale of ['en','zh-TW'])for(const reduce of [false,true]){
 class El{constructor(){this.dataset={};this.attrs={};this.children=[];this.style={};this.events={};this.classList={add:()=>{}};}append(...x){this.children.push(...x);}replaceChildren(...x){this.children=x;}setAttribute(k,v){this.attrs[k]=v;}addEventListener(k,f){this.events[k]=f;}}
 const host=new El();host.dataset={curiosityLab:kind,locale};let sub;const doc={readyState:'complete',hidden:false,querySelectorAll:()=>[host],createElement:()=>new El(),addEventListener:()=>{}};
 let source=fs.readFileSync('docs/javascripts/curiosity-labs.js','utf8');
 source=source.replace('  function enhance(){','  globalThis.math={distribution,svg,outcomes};\n  function enhance(){');
 source=source.replace('      set(0);','      host.probe={set,drawSamples,resetSamples,trajectory,plot,seek,play,biasInput,skewInput,transferInput,get:()=>({sampleCount,sampleSum,sampleTrace,sampleCounts})};\n      set(0);');
 const ctx={document:doc,window:{document$:{subscribe:f=>sub=f}},matchMedia:()=>({matches:reduce,addEventListener:()=>{}}),setInterval:()=>1,clearInterval:()=>{}};vm.runInNewContext(source,ctx);
 assert.equal(host.dataset.labReady,'yes');const h=host.probe;assert.equal(h.play.disabled,reduce);const children=host.children.length;sub();assert.equal(host.children.length,children);
 for(let skew=-60;skew<=60;skew+=10){const d=ctx.math.distribution(skew);assert(Math.abs(d.weights.reduce((a,b)=>a+b,0)-1)<1e-12);
  for(let bias=-40;bias<=40;bias+=10){const errors=ctx.math.outcomes.map(([x,y])=>(x-d.center[0]-bias)**2+(y-d.center[1])**2);const mse=errors.reduce((s,x,i)=>s+d.weights[i]*x,0);assert(Math.abs(mse-d.variance-bias*bias)<1e-9);assert(mse<6000);assert(Math.max(...errors)<16000);
   const svg=ctx.math.svg('icm',3,locale==='zh-TW',bias,0,skew);const widths=[...svg.matchAll(/data-contribution="\d"[^>]*width="([\d.]+)"/g)].map(m=>+m[1]);assert.equal(widths.length,3);assert(Math.abs(widths.reduce((a,b)=>a+b,0)-mse*344/6000)<.016);
  }
 }
 if(kind==='icm'){
  h.set(3);h.drawSamples(20);let state=h.get();assert.equal(state.sampleCount,20);assert.equal(state.sampleCounts.reduce((a,b)=>a+b,0),20);assert(Math.abs(state.sampleTrace.at(-1)-state.sampleSum/20000)<1e-12);
  const d=ctx.math.distribution(0),loss=ctx.math.outcomes.map(([x,y])=>((x-d.center[0])**2+(y-d.center[1])**2)/1000),mu=d.variance/1000,sd=Math.sqrt(loss.reduce((s,x,i)=>s+d.weights[i]*(x-mu)**2,0));assert(Math.abs(+h.trajectory.dataset.standardError-sd/Math.sqrt(20))<1e-12);
  h.drawSamples(121);state=h.get();assert.equal(state.sampleCount,141);assert.equal(state.sampleTrace.length,120);assert.equal(h.trajectory.dataset.windowStart,'22');assert(Math.abs(+h.trajectory.dataset.standardError-sd/Math.sqrt(141))<1e-12);
  h.biasInput.value='40';h.biasInput.events.input();assert.equal(h.get().sampleCount,0);
 }else{h.set(4);h.transferInput.value='100';h.transferInput.events.input();assert(h.plot.innerHTML.includes('width="0.00"'));}
 scenarios++;
}
console.log(`PASS ${scenarios} actual lab DOM cases, dense bias/weight geometry, Monte Carlo prefix means/analytic SE/reset/reentry.`);
