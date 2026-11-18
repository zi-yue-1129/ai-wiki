// Execute the actual lab against a small DOM model; real layout is tested separately.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('docs/javascripts/evolution-labs.js','utf8');
class Element {
 constructor(tag){this.tag=tag;this.children=[];this.events={};this.dataset={};this.className='';this.isConnected=true;this.style={setProperty(){}};this.classList={add:c=>{this.className+=' '+c}};}
 append(...items){for(const x of items){if(x.parent)x.parent.children=x.parent.children.filter(v=>v!==x);x.parent=this;this.children.push(x)}}
 replaceChildren(...items){this.children=[];this.append(...items)}
 setAttribute(k,v){this[k]=v}addEventListener(k,fn){(this.events[k]??=[]).push(fn)}
 emit(k){for(const fn of this.events[k]??[])fn()}
 all(){return this.children.flatMap(x=>[x,...x.all()])}
 querySelector(s){if(s.startsWith('.evo-timeline'))return this.all().find(x=>x.className==='evo-timeline').children.filter(x=>x.tag==='button').at(-1);throw Error(s)}
}
function setup(kind,lang){const root=new Element('div');root.dataset={evolutionLab:kind,lang};const timers=new Map();let id=0,enhance;
 const document={readyState:'complete',createElement:t=>new Element(t),querySelectorAll:()=>[root],addEventListener(){}};
 vm.runInNewContext(source,{document,window:{matchMedia:()=>({addEventListener(){}}),setInterval:f=>{timers.set(++id,f);return id},clearInterval:i=>timers.delete(i),document$:{subscribe:f=>{enhance=f}}}});
 const inputs=()=>root.all().filter(x=>x.tag==='input');const buttons=()=>root.all().filter(x=>x.tag==='button');
 const input=(i,v)=>{const e=inputs()[i];e.value=String(v);e.emit('input')};const seek=v=>input(2,v);const canvas=()=>root.all().find(x=>x.className==='evo-canvas');
 return {root,inputs,buttons,input,seek,canvas,timers,enhance};}
for(const lang of ['en','zh']){
 const h=setup('ga',lang);assert.equal(h.root.all().filter(x=>x.className==='evo-timeline').length,1);h.enhance();assert.equal(h.root.all().filter(x=>x.className==='evo-timeline').length,1);
 for(let cut=1;cut<=7;cut++)for(let flip=1;flip<=8;flip++){
  h.input(0,cut);h.input(1,flip);const raw='11011010'.slice(0,cut)+'00100101'.slice(cut);
  for(let n=0;n<=9;n++){h.seek(n);const shown=h.canvas().children[2].children[1].children.map(x=>x.textContent).join('');const final=raw.slice(0,flip-1)+(raw[flip-1]==='1'?'0':'1')+raw.slice(flip);assert.equal(shown,n===9?final:raw.slice(0,n)+'·'.repeat(8-n));}
 }
 h.buttons()[4].emit('click');assert.equal(h.inputs()[0].value,'4');assert.equal(h.inputs()[1].value,'7');assert.equal(h.canvas().dataset.step,'0');
 h.buttons()[1].emit('click');assert.equal(h.timers.size,1);[...h.timers.values()][0]();assert.equal(h.canvas().dataset.step,'1');h.buttons()[1].emit('click');assert.equal(h.timers.size,0);
 h.buttons()[1].emit('click');h.root.isConnected=false;[...h.timers.values()][0]();assert.equal(h.timers.size,0);
 const m=setup('map',lang);for(const rival of [0,.61,.82,.93,.95,1])for(const replacement of [0,.82,.93,.95,1]){
  m.input(0,rival);m.input(1,replacement);let best=.82;
  for(let n=0;n<=4;n++){m.seek(n);if(n===2)best=Math.max(best,rival);if(n===3)best=Math.max(best,replacement);assert.equal(+m.canvas().dataset.coverage,n===0?3:n===4?5:4);const cells=m.canvas().children[0].children;if(n>0)assert.equal(cells[9].textContent,best.toFixed(2));
   const expected=1.71+(n>0?best:0)+(n===4?.75:0);assert.ok(m.root.all().find(x=>x.className==='evo-numeric').textContent.endsWith(expected.toFixed(2)));
  }
 }
 m.input(0,.82);m.seek(2);assert.equal(m.canvas().dataset.lastDecision,lang==='zh'?'拒絕':'Reject');m.buttons()[4].emit('click');assert.equal(m.canvas().dataset.coverage,'3');
}
console.log('PASS actual evolution JS: 112 crossover/mutation combinations × 10 states, 60 archive scenarios × 5 events, equality, quality sums, reset, repeat init, pause and detached-page timer cleanup');
