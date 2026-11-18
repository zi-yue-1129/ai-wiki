const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('docs/javascripts/vq-splat-labs.js','utf8');
class El{constructor(){this.children=[];this.attrs={};this.events={};this.dataset={};}setAttribute(k,v){this.attrs[k]=String(v)}append(e){this.children.push(e)}replaceChildren(){this.children=[]}addEventListener(k,f){this.events[k]=f}emit(k){this.events[k]?.({target:this})}}
function setup(mode,lang){let map={},params=[],outputs=[],timers=new Map(),id=0;const root={dataset:{vqSplatLab:mode,lang},isConnected:true,classList:{add(){}},set innerHTML(s){this.html=s;map={svg:new El(),'[role=status]':new El()};for(const a of ['prev','next','play','seek','speed','reset']){map[`[data-action="${a}"]`]=new El();map[`[data-action="${a}"]`].value=a==='speed'?'1':'0'}params=Array.from({length:mode==='vq'?2:3},(_,i)=>{let e=new El();e.dataset.param=String(i);return e});outputs=params.map(()=>new El())},querySelector(s){if(s.startsWith('[data-value'))return outputs[+s.match(/\d+/)[0]];return map[s]},querySelectorAll(){return params}};
 let enhance,reduce;const window={document$:{subscribe:f=>enhance=f},matchMedia:()=>({addEventListener:(n,f)=>reduce=f})};const document={readyState:'complete',hidden:false,querySelectorAll:()=>[root],createElementNS:(_ns,tag)=>{const el=new El();el.tag=tag;return el},addEventListener(){}};
 vm.runInNewContext(source,{window,document,setInterval:f=>{timers.set(++id,f);return id},clearInterval:i=>timers.delete(i)});
 return{root,map,params,timers,math:window.__vqSplatMath,enhance,reduce:()=>reduce({matches:true}),control:a=>map[`[data-action="${a}"]`],param:(i,v)=>{params[i].value=String(v);params[i].emit('input')},seek:v=>{map['[data-action="seek"]'].value=String(v);map['[data-action="seek"]'].emit('input')}};
}
const C=[[.2,.35],[.75,.35],[.48,.82]],RGB=[[235,93,98],[79,171,223],[239,193,100]],BG=[30,39,60];
const h=setup('splat','en');const M=h.math;
for(let x=0;x<=40;x++)for(let y=0;y<=40;y++){const ds=C.map(([a,b])=>(x/40-a)**2+(y/40-b)**2);assert.equal(M.nearest(x/40,y/40).index,ds.indexOf(Math.min(...ds)));}
assert.equal(M.nearest(.475,.35).index,0);
const linear=c=>c/255<=.04045?c/255/12.92:Math.pow((c/255+.055)/1.055,2.4);
const srgb=c=>Math.round(255*(c<=.0031308?12.92*c:1.055*Math.pow(c,1/2.4)-.055));
for(let a=0;a<=10;a++)for(let b=0;b<=10;b++)for(let c=0;c<=10;c++){
 const aa=[a/10,b/10,c/10],result=M.composite(aa),w=[aa[0],(1-aa[0])*aa[1],(1-aa[0])*(1-aa[1])*aa[2]],T=(1-aa[0])*(1-aa[1])*(1-aa[2]);
 assert.ok(Math.abs(result.weights.reduce((s,x)=>s+x,0)+result.t-1)<1e-12);
 result.weights.forEach((x,i)=>assert.ok(Math.abs(x-w[i])<1e-12));
 assert.equal(JSON.stringify(result.color),JSON.stringify(BG.map((v,ch)=>srgb(w.reduce((s,x,i)=>s+x*linear(RGB[i][ch]),0)+T*linear(v)))));
}
assert.equal(JSON.stringify(M.composite([0,0,0]).color),JSON.stringify(BG));assert.equal(JSON.stringify(M.composite([1,1,1]).color),JSON.stringify(RGB[0]));
for(const lang of ['en','zh'])for(const mode of ['vq','splat']){
 const s=setup(mode,lang),svg=s.map.svg;const original=svg;s.enhance();assert.equal(s.map.svg,original);
 if(mode==='vq'){
  s.param(0,.2);s.param(1,.35);s.seek(5);assert.ok(s.map['[role=status]'].textContent.includes('e1'));
  assert.equal(svg.children.find(x=>x.attrs.x==='425'&&x.attrs.y==='63'&&x.attrs.fill==='#e56f55').attrs.width,'0');
  const circles=svg.children.filter(x=>x.attrs.cx);assert.ok(Math.abs(+circles[1].attrs.cx-+circles[0].attrs.cx-195*(.75-.2))<1e-10);
 }else{
  for(const aa of [[.5,.6,.8],[0,0,0],[1,1,1],[.01,.99,.5]]){
   aa.forEach((a,i)=>s.param(i,a));for(let n=0;n<=3;n++){s.seek(n);const wanted=M.composite(aa.map((a,i)=>i<n?a:0));const patch=svg.children.find(x=>x.attrs.x==='570'&&x.attrs.y==='191');assert.equal(patch.attrs.fill,`rgb(${wanted.color.join(',')})`);}
  }
 }
 s.control('reset').emit('click');assert.equal(s.control('seek').value,'0');s.control('play').emit('click');assert.equal(s.timers.size,1);[...s.timers.values()][0]();assert.equal(s.control('seek').value,'1');s.reduce();assert.equal(s.timers.size,0);s.control('play').emit('click');s.root.isConnected=false;[...s.timers.values()][0]();assert.equal(s.timers.size,0);
}
console.log('PASS actual JS: 1681 nearest points, 1331 opacity triples with linear-light sRGB, four bilingual DOM states, zero-distance bar, metric scale, all partial RGB, reset/reinit/reduced/detached timers. Default sRGB:',M.composite([.5,.6,.8]).color.join(','));

if(process.env.VQ_RENDER_DIR){fs.mkdirSync(process.env.VQ_RENDER_DIR,{recursive:true});for(const mode of ['vq','splat']){const h=setup(mode,'en');for(let i=0;i<=(mode==='vq'?5:3);i++){h.seek(i);const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');const body=h.map.svg.children.map(e=>`<${e.tag} ${Object.entries(e.attrs).map(([k,v])=>`${k}="${escape(v)}"`).join(' ')}>${escape(e.textContent??'')}</${e.tag}>`).join('');fs.writeFileSync(`${process.env.VQ_RENDER_DIR}/${mode}-${i}.svg`,`<svg xmlns="http://www.w3.org/2000/svg" width="720" height="270" viewBox="0 0 720 270">${body}</svg>`);}}}
