const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('docs/javascripts/t5-deit-labs.js','utf8');
class El{constructor(value=''){this.value=value;this.events={};this.dataset={};this.nextElementSibling={};}addEventListener(k,f){this.events[k]=f}emit(k){this.events[k]?.({target:this})}}
function setup(mode,lang){let map={},ranges=[],timers=new Map(),n=0,scan,reduce;const root={id:`td-${mode}-${lang}`,dataset:{lab:mode,lang},isConnected:true,set innerHTML(s){this.html=s;map={};for(const key of ['.td-art','.td-state','.td-seek','.td-speed','.td-params select'])map[key]=new El(key==='.td-speed'?'1':'0');ranges=Array.from({length:mode==='t5'?4:2},()=>new El());for(const a of ['prev','next','play','reset']){const e=new El();e.dataset.action=a;map[`[data-action="${a}"]`]=e}},querySelector:k=>map[k],querySelectorAll:k=>k==='.td-params input'?ranges:Object.values(map).filter(e=>e.dataset.action)};
 const document={documentElement:{lang},readyState:'complete',hidden:false,querySelectorAll:()=>[root],addEventListener(){}};const window={document$:{subscribe:f=>scan=f},matchMedia:()=>({addEventListener:(_,f)=>reduce=f})};vm.runInNewContext(source,{window,document,setInterval:f=>{timers.set(++n,f);return n},clearInterval:i=>timers.delete(i)});
 return{root,map,ranges,timers,scan,reduce:()=>reduce({matches:true}),param:(i,v)=>{ranges[i].value=String(v);ranges[i].emit('input')},seek:n=>{map['.td-seek'].value=String(n);map['.td-seek'].emit('input')},click:a=>map[`[data-action="${a}"]`].emit('click'),svg:()=>map['.td-art'].innerHTML};}
let count=0;
for(const lang of ['en','zh'])for(const mode of ['t5','deit']){
 const h=setup(mode,lang),original=h.map['.td-art'];h.scan();assert.equal(h.map['.td-art'],original);
 if(mode==='t5')assert.ok(!h.svg().includes('4/10'));else{assert.ok(h.svg().includes('M168 85H217 M190 85V192H217'));assert.ok(!h.svg().includes('>B</text>'));}
 const ids=[...h.root.html.matchAll(/<input id="([^"]+)"/g)].map(m=>m[1]);assert.equal(new Set(ids).size,mode==='t5'?4:2);
 if(mode==='t5'){
 for(let a=1;a<=4;a++)for(let l=1;l<=3;l++)for(let b=7;b<=9;b++)for(let k=1;k<=2;k++){
 h.param(0,a);h.param(1,l);h.param(2,b);h.param(3,k);const start2=Math.max(b-1,a-1+l+1,6);const tokens='ABCDEFGHIJ'.split('');const enc=[...tokens.slice(0,a-1),'S0',...tokens.slice(a-1+l,start2),'S1',...tokens.slice(start2+k)],target=['S0',...tokens.slice(a-1,a-1+l),'S1',...tokens.slice(start2,start2+k),'S2'];
 for(let step=0;step<4;step++){h.seek(step);const svg=h.svg(),status=h.map['.td-state'].textContent;assert.equal(svg.includes('data-length="Encoder"'),step>=2);assert.equal(svg.includes('data-length="Target"'),step>=3);assert.equal(status.includes('Encoder:'),step>=2);assert.equal(status.includes('Target:'),step>=3);if(step>=2){assert.ok(status.includes(enc.join(' ')));assert.ok(svg.includes(`data-count="${12-l-k}"`));}if(step>=3){assert.ok(status.includes(target.join(' ')));assert.ok(svg.includes(`data-count="${l+k+3}"`));}count++;}
 }
 }else{
 for(let p=1;p<=19;p++)for(let d=1;d<=19;d++)for(const teacher of ['A','B']){h.param(0,p/20);h.param(1,d/20);h.map['.td-params select'].value=teacher;h.map['.td-params select'].emit('change');h.seek(3);const loss=(-Math.log(p/20)-Math.log(teacher==='A'?d/20:1-d/20))/2;assert.ok(h.svg().includes(`L ${loss.toFixed(3)}`));h.seek(4);assert.ok(h.svg().includes(`P(A) ${(100*(p+d)/40).toFixed(1)}%`));count++;}
 }
 h.click('reset');h.click('play');assert.equal(h.timers.size,1);h.reduce();assert.equal(h.timers.size,0);h.click('play');h.root.isConnected=false;[...h.timers.values()][0]();assert.equal(h.timers.size,0);h.root.isConnected=true;h.click('play');for(let i=0;i<5&&h.timers.size;i++)[...h.timers.values()][0]();assert.equal(h.timers.size,0);assert.equal(+h.map['.td-seek'].value,mode==='t5'?3:4);h.click('play');assert.equal(+h.map['.td-seek'].value,0);h.click('reset');
 if(process.env.TD_RENDER_DIR){fs.mkdirSync(process.env.TD_RENDER_DIR,{recursive:true});for(let i=0;i<=(mode==='t5'?3:4);i++){h.seek(i);fs.writeFileSync(`${process.env.TD_RENDER_DIR}/${mode}-${lang}-${i}.svg`,h.svg().replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" '));}}
}
console.log(`PASS ${count} actual JS numeric/stage cases, distinct bilingual IDs, lifecycle, restart and final hold`);
