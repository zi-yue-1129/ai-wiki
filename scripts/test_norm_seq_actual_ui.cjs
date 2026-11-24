const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
class El{
 constructor(tag='div'){this.tag=tag;this.attrs={};this.children=[];this.dataset={};this.events={};this.isConnected=true;this.className='';this.textContent='';this._html='';this.classList={add:(s)=>this.className+=' '+s};}
 setAttribute(k,v){this.attrs[k]=v;if(k==='class')this.className=v;if(k==='value')this.value=String(v);}
 append(...e){for(const a of e){a.parent=this;this.children.push(a);}}
 replaceChildren(...e){this.children=[];this.append(...e);}
 before(e){const p=this.parent;e.parent=p;p.children.splice(p.children.indexOf(this),0,e);}
 addEventListener(k,f){this.events[k]=f;}
 set innerHTML(s){this._html=s;if(s.includes('ns-dynamic')){this.dynamic=new El('g');this.dynamic.className='ns-dynamic';}}
 get innerHTML(){return this._html;}
 querySelector(s){if(s==='.ns-dynamic')return this.dynamic;return this.all().find(e=>e.className.split(' ').includes(s.slice(1)));}
 all(){return this.children.flatMap(e=>[e,...e.all()]);}
}
let roots=[],timers=new Map(),tid=0,sub,events={},red={matches:false,addEventListener:(k,f)=>red.change=f};
const document={hidden:false,readyState:'complete',createElement:t=>new El(t),querySelectorAll:()=>roots,addEventListener:(k,f)=>events[k]=f};
for(const lang of ['en','zh'])for(const topic of ['layernorm','seq2seq']){const r=new El();r.dataset={lang,normSeqLab:topic};roots.push(r);}
vm.runInNewContext(fs.readFileSync('docs/javascripts/norm-seq-labs.js','utf8'),{document,window:{matchMedia:()=>red,document$:{subscribe:f=>sub=f}},setInterval:f=>{timers.set(++tid,f);return tid;},clearInterval:id=>timers.delete(id)});
const out=process.env.NORM_SEQ_RENDER_DIR;if(out)fs.mkdirSync(out,{recursive:true});
function save(r,suffix){if(!out)return;const graph=r.all().find(e=>e.dynamic);let svg=graph.innerHTML.replace('<g class="ns-dynamic"></g>','<g>'+graph.dynamic.innerHTML+'</g>');svg=svg.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ').replace('<title>','<style>'+fs.readFileSync('docs/stylesheets/norm-seq-labs.css','utf8')+'</style><title>');fs.writeFileSync(`${out}/${r.dataset.normSeqLab}-${r.dataset.lang}-${suffix}.svg`,svg);}
for(const r of roots){assert(r.className.includes('ns-lab'));save(r,'initial');const all=r.all(),inputs=all.filter(e=>e.tag==='input'),buttons=all.filter(e=>e.tag==='button');
 if(r.dataset.normSeqLab==='layernorm'){for(const [i,v] of [[0,'4'],[1,'3']]){inputs[i].value=v;inputs[i].events.input();}save(r,'perturbed');buttons[0].events.click();assert.equal(inputs[0].value,'2');assert.equal(inputs[1].value,'0');}
 else {inputs[0].value='4';inputs[0].events.input();save(r,'handoff');inputs[0].value='6';inputs[0].events.input();save(r,'decoder');buttons[3].events.click();buttons[1].events.click();assert.equal(timers.size,1);[...timers.values()][0]();assert.equal(inputs[0].value,'1');document.hidden=true;events.visibilitychange();assert.equal(timers.size,0);document.hidden=false;buttons[1].events.click();red.matches=true;red.change();assert.equal(timers.size,0);red.matches=false;buttons[1].events.click();r.isConnected=false;sub();assert.equal(timers.size,0);r.isConnected=true;}
}
sub();assert.equal(roots[0].all().filter(e=>e.tag==='input').length,2);console.log('PASS actual bilingual DOM render, numerical inputs/reset, timer visibility/reduced/disconnect cleanup and duplicate initialization');
