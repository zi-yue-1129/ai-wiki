const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const source=fs.readFileSync('docs/javascripts/semi-supervised-process-labs.js','utf8');
function setup(kind,lang){
 const all=[],listeners={},timers=new Map();let seq=0,nav;
 class El{constructor(tag){this.tag=tag;this.attrs={};this.dataset={};this.children=[];this.events={};this.value='';this.textContent='';this.isConnected=true;all.push(this)}setAttribute(k,v){this.attrs[k]=String(v);if(k==='value')this.value=String(v)}append(e){this.children.push(e)}replaceChildren(...xs){this.children=xs}addEventListener(k,f){this.events[k]=f}}
 const host=new El('div');host.dataset={kind,lang};const doc={readyState:'complete',hidden:false,querySelectorAll:()=>host.dataset.ready?[]:[host],createElement:t=>new El(t),createElementNS:(n,t)=>{assert.equal(n,'http://www.w3.org/2000/svg');return new El(t)},addEventListener:(k,f)=>listeners[k]=f};
 vm.runInNewContext(source,{document:doc,document$:{subscribe:f=>{nav=f;f()}},window:{matchMedia:()=>({addEventListener:(k,f)=>listeners.media=f})},setInterval:(f,ms)=>{timers.set(++seq,{f,ms});return seq},clearInterval:i=>timers.delete(i)});
 const control=k=>all.find(e=>e.attrs['data-act']===k),params=all.filter(e=>e.tag==='input'&&!e.attrs['data-act']),read=all.find(e=>e.attrs.class==='semi-read'),svg=all.find(e=>e.tag==='svg');
 return{host,all,doc,listeners,timers,read,svg,control,params,nav,click:k=>control(k).events.click(),set:(i,v)=>{params[i].value=String(v);params[i].events.input()},seek:t=>{control('seek').value=String(t);control('seek').events.input()},tick:()=>[...timers.values()].forEach(o=>o.f())};
}
function serialize(e){const esc=x=>String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');return '<'+e.tag+(e.tag==='svg'?' xmlns="http://www.w3.org/2000/svg"':'')+Object.entries(e.attrs).map(([k,v])=>' '+k+'="'+esc(v)+'"').join('')+'>'+esc(e.textContent)+e.children.map(serialize).join('')+'</'+e.tag+'>'}
for(const lang of ['en','zh'])for(const kind of ['fixmatch','teacher']){
 const h=setup(kind,lang);assert.equal(h.timers.size,0);const count=h.all.length;h.nav();assert.equal(h.all.length,count);
 if(kind==='fixmatch'){
  for(const weak of [.5,.9,.95,.99])for(const gate of [.6,.9,.95,.99])for(const strong of [.1,.5,.62,.99]){
   h.set(0,weak);h.set(1,gate);h.set(2,strong);h.seek(3);const want=weak>=gate?-Math.log(strong):0;
   assert.ok(h.read.textContent.endsWith(want.toFixed(3)));assert.ok(h.svg.children.some(e=>e.textContent===(weak>=gate?'PASS':'SKIP')));
  }
  h.seek(0);assert.ok(h.read.textContent.endsWith('—'));h.set(0,.9);h.set(1,.85);h.set(2,.5);h.seek(3);assert.ok(h.read.textContent.endsWith('0.693'));
 }else{
  const st=[.15,.85,.35,.95,.5,.72];
  for(const alpha of [.5,.75,.9,.99]){h.set(0,alpha);let prev=.15;
   for(let t=0;t<6;t++){if(t)prev=alpha*prev+(1-alpha)*st[t];h.seek(t);assert.ok(h.read.textContent.includes((lang==='zh'?'教師':'Teacher')+' = '+prev.toFixed(3)));const paths=h.svg.children.filter(e=>e.tag==='polyline');assert.equal(paths.length,2);assert.equal(paths[1].attrs.points.split(' ').length,t+1);const point=paths[1].attrs.points.split(' ').at(-1).split(',').map(Number);assert.ok(Math.abs(point[1]-(247-176*prev))<1e-10);}
  }
 }
 h.click('reset');assert.equal(h.control('seek').value,'0');h.click('next');h.click('prev');assert.equal(h.control('seek').value,'0');h.click('play');h.tick();assert.equal(h.control('seek').value,'1');h.control('speed').value='2';h.control('speed').events.change();assert.equal(h.timers.size,1);assert.equal([...h.timers.values()][0].ms,425);h.doc.hidden=true;h.listeners.visibilitychange();assert.equal(h.timers.size,0);
 h.click('play');h.listeners.media({matches:true});assert.equal(h.timers.size,0);h.click('play');h.host.isConnected=false;h.tick();assert.equal(h.timers.size,0);h.host.isConnected=true;h.click('reset');h.click('play');for(let i=0;i<6;i++)h.tick();assert.equal(h.timers.size,0);h.click('play');assert.equal(h.control('seek').value,'0');h.click('play');assert.equal(h.timers.size,0);
 if(process.argv[2]){for(const step of [0,1,kind==='teacher'?5:3]){h.seek(step);fs.mkdirSync(process.argv[2],{recursive:true});fs.writeFileSync(`${process.argv[2]}/${kind}-${lang}-${step}.svg`,serialize(h.svg));}}
}
console.log('Actual semi-process JS: 128 threshold/CE cases, 48 EMA stages, reveal geometry, controls/navigation/media/hidden/detached PASS');
