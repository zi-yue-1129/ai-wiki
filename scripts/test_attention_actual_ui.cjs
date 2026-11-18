const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
class El{
 constructor(tag='div'){this.tag=tag;this.attrs={};this.children=[];this.dataset={};this.events={};this.isConnected=true;this.textContent='';}
 setAttribute(k,v){this.attrs[k]=String(v);if(k==='value')this.value=String(v);}
 append(...es){this.children.push(...es);} replaceChildren(...es){this.children=es;this.textContent='';}
 addEventListener(k,f){this.events[k]=f;}
 all(){return this.children.flatMap(e=>[e,...e.all()]);}
 querySelector(s){return this.all().find(e=>s.startsWith('[')?e.attrs[s.slice(1).split('=')[0]]===s.split('="')[1].slice(0,-2):e.tag===s);}
}
const roots=[];for(const lang of ['en','zh'])for(const lab of ['window','linear','gqa','global']){const r=new El();r.dataset={lang,lab};roots.push(r);}
let nextid=0;const timers=new Map(),events={},subs=[],red={matches:false,callbacks:[],addEventListener(k,f){this.callbacks.push(f)}};
const document={hidden:false,readyState:'complete',createElement:t=>new El(t),createElementNS:(_,t)=>new El(t),querySelectorAll:()=>roots,addEventListener:(k,f)=>(events[k]??=[]).push(f)};
vm.runInNewContext(fs.readFileSync('docs/javascripts/attention-variant-labs.js','utf8'),{document,window:{matchMedia:()=>red,document$:{subscribe:f=>subs.push(f)}},setInterval:f=>{timers.set(++nextid,f);return nextid},clearInterval:id=>timers.delete(id)});
const out=process.env.ATTENTION_RENDER_DIR;if(out)fs.mkdirSync(out,{recursive:true});
const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
function serialize(e){return '<'+e.tag+' '+Object.entries(e.attrs).map(([k,v])=>k+'="'+escape(v)+'"').join(' ')+'>'+escape(e.textContent)+e.children.map(serialize).join('')+'</'+e.tag+'>';}
function save(r,phase){if(out)fs.writeFileSync(`${out}/${r.dataset.lab}-${r.dataset.lang}-${phase}.svg`,serialize(r.all().find(e=>e.tag==='svg')).replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" '));}
for(const r of roots){
 const get=(k,v)=>r.all().find(e=>e.attrs[k]===v),set=(key,v)=>{const e=get('data-range',key);e.value=String(v);e.events.input();};
 const stats=()=>get('class','attention-lab-stats').textContent;
 save(r,'initial');assert.equal(get('data-act','play').attrs['aria-pressed'],'false');
 if(r.dataset.lab==='window'){for(let w=1;w<=8;w++)for(let q=1;q<=12;q++){set('factor',w);set('step',q);const n=Array.from({length:12},(_,i)=>Math.min(i+1,w)).reduce((a,b)=>a+b);assert(stats().includes(n+' / 78'));assert(stats().includes(Math.max(1,q-w+1)+'–'+q));}}
 if(r.dataset.lab==='linear'){for(let v=-1;v<=5;v++)for(let t=0;t<=4;t++){set('factor',v);set('step',t);if(t){const ks=[1,2,1,2],vs=[1,0,v,2],S=ks.slice(0,t).reduce((a,k,i)=>a+k*vs[i],0),z=ks.slice(0,t).reduce((a,k)=>a+k,0);assert(stats().includes('S='+S+', z='+z));}}}
 if(r.dataset.lab==='gqa'){for(let j=0;j<4;j++){set('step',j);assert(stats().includes((2**j)+'/8 ('+(12.5*2**j)+'%)'));}}
 if(r.dataset.lab==='global'){for(const active of [true,false]){let e=get('data-toggle','global');e.checked=active;e.events.change();for(let d=0;d<=3;d++){set('step',d);assert(stats().includes(([1,4,12,12][d]-(active?0:([1,4,12,12][d]-[1,3,5,6][d])))+'/12'));}}}
 save(r,'changed');get('data-act','reset').events.click();save(r,'reset');
 get('data-act','play').events.click();assert.equal(timers.size,1);[...timers.values()][0]();save(r,'midplay');document.hidden=true;events.visibilitychange.forEach(f=>f());assert.equal(timers.size,0);document.hidden=false;
 get('data-act','play').events.click();red.matches=true;red.callbacks.forEach(f=>f());assert.equal(timers.size,0);red.matches=false;
 get('data-act','play').events.click();r.isConnected=false;subs.forEach(f=>f());assert.equal(timers.size,0);r.isConnected=true;
 const count=r.all().length;subs.forEach(f=>f());assert.equal(r.all().length,count);
}
console.log('PASS actual JS bilingual DOM, full scalar/window/GQA/reach grids, reset/play, visibility/reduced/disconnect cleanup, no duplicate initialization');
