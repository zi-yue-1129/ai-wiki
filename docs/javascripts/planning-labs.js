/* Original CC BY-SA 4.0 teaching simulations; illustrative propositional planning only. */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const reduce = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const strings = {
    en: {prev:'Previous',next:'Next',play:'Play',pause:'Pause',reset:'Reset',speed:'Speed',step:'Step',
      present:'Initial At(A)',charged:'Initial Charged',goal:'Goal',single:'At(C)',joint:'At(A) + At(B)',
      invalid:'Precondition missing: no successor state',valid:'Precondition satisfied',
      output:'Successor',preview:'Effect preview — the action is atomic',
      reject:'Rejected: the goal facts are mutex',accept:'Extracted: Move(A,B) → Move(B,C)',
      possible:'A fact layer is a union of possibilities, not one state.'},
    zh: {prev:'上一步',next:'下一步',play:'播放',pause:'暫停',reset:'重設',speed:'速度',step:'步驟',
      present:'起始包含 At(A)',charged:'起始包含 Charged',goal:'目標',single:'At(C)',joint:'At(A) + At(B)',
      invalid:'缺少前置條件：不產生後繼狀態',valid:'前置條件成立',
      output:'後繼狀態',preview:'效果預覽：動作語義為原子操作',
      reject:'拒絕：兩個目標事實互斥',accept:'抽取：Move(A,B) → Move(B,C)',
      possible:'事實層是各種可能的聯集，而非單一狀態。'}
  };
  const esc = s => String(s).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const rect = (x,y,w,h,fill,stroke='#cbd5e1',r=12) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`;
  const label = (x,y,s,size=17,color='#233148',anchor='middle') => `<text x="${x}" y="${y}" font-size="${size}" font-family="Arial,sans-serif" font-weight="600" text-anchor="${anchor}" fill="${color}">${esc(s)}</text>`;
  const line = (x1,y1,x2,y2,c='#64748b',dash='') => `<path d="M${x1} ${y1} L${x2} ${y2}" stroke="${c}" stroke-width="3" stroke-linecap="round" ${dash?'stroke-dasharray="6 5"':''} fill="none"/>`;
  const pill = (x,y,t,active,highlight=false) => rect(x,y,122,42,active?'#d5f8e8':'#f0f3f8',active?'#147d62':'#cbd5e1',10)+label(x+61,y+27,t,15,active?'#135f4a':'#64748b');
  const labs = [];
  function init(host) {
    if (host.dataset.planningEnhanced) return;
    host.dataset.planningEnhanced='yes';
    const lang = host.dataset.lang === 'zh-TW' ? 'zh':'en', t=strings[lang];
    const kind=host.dataset.planningLab;
    if (kind!=='strips'&&kind!=='graphplan')return;
    let step=0,playing=false,speed=1,timer=null;
    let atA=true,charged=true,goal='C';
    const max=kind==='strips'?4:4;
    const canvasLabel=lang==='zh'
      ? (kind==='strips'?'STRIPS 互動狀態轉移圖（可水平捲動）':'Graphplan 互動事實層與互斥圖（可水平捲動）')
      : (kind==='strips'?'STRIPS interactive state transition (horizontal scroll)':'Graphplan interactive layers and mutex (horizontal scroll)');
    const svgLabel=lang==='zh'
      ? (kind==='strips'?'STRIPS 狀態更新':'Graphplan 事實層與互斥')
      : (kind==='strips'?'STRIPS state update':'Graphplan layers and mutex');
    host.innerHTML = `<div class="planning-parameters"></div><div class="planning-canvas" tabindex="0" role="region" aria-label="${canvasLabel}"><svg role="img" viewBox="0 0 720 250" xmlns="${NS}" aria-label="${svgLabel}"></svg></div><div class="planning-controls"><button type="button" data-a="prev">${t.prev}</button><button type="button" data-a="next">${t.next}</button><button type="button" data-a="play">${t.play}</button><label>${t.step} <input data-a="seek" type="range" min="0" max="${max}" step="1" value="0"/></label><label>${t.speed} <select data-a="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label><button type="button" data-a="reset">${t.reset}</button></div><p class="planning-status" role="status" aria-live="polite"></p>`;
    const svg=host.querySelector('svg'),params=host.querySelector('.planning-parameters');
    const status=host.querySelector('.planning-status'),play=host.querySelector('[data-a=play]'),seek=host.querySelector('[data-a=seek]');
    if(kind==='strips') params.innerHTML=`<label><input type="checkbox" data-p="atA" checked/> ${t.present}</label><label><input type="checkbox" data-p="charged" checked/> ${t.charged}</label>`;
    else params.innerHTML=`<label>${t.goal} <select data-p="goal"><option value="C">${t.single}</option><option value="AB">${t.joint}</option></select></label>`;
    function stop(){playing=false;clearInterval(timer);timer=null;play.textContent=t.play;play.setAttribute('aria-pressed','false');}
    function renderStrips() {
      const valid=atA;
      const initial=[...(atA?['At(A)']:[]),...(charged?['Charged']:[])];
      // Compute successor using exact STRIPS set difference and union only when applicable.
      const successor=valid?[...new Set([...initial.filter(x=>x!=='At(A)'),'At(B)'])]:initial.slice();
      const pre=step>=1, del=step>=2&&valid,add=step>=3&&valid,final=step>=4;
      let out=rect(15,12,690,226,'#fff','#d3dbea')+label(105,47,'Before',19)+label(612,47,'After',19);
      out+=pill(40,70,'At(A)',atA)+pill(40,126,'Charged',charged);
      out+=line(190,120,515,120,pre?(valid?'#0e9775':'#d64c65'):'#b0bccc');
      out+=label(350,85,'Move(A,B)',21);out+=label(350,154,pre?(valid?'pre ✓':'pre ✕'):'pre ?',17,pre?(valid?'#168364':'#be3455'):'#64748b');
      out+=pill(545,70,'At(B)',final&&successor.includes('At(B)'))+pill(545,126,'Charged',final&&successor.includes('Charged'));
      if(del)out+=label(350,180,'− At(A)',16,'#bd4261');
      if(add)out+=label(350,207,'+ At(B)',16,'#168364');
      out+=label(350,228,final?(valid?'s′ = {'+successor.join(', ')+'}':'s′ = s (not applied)'):(step===0?'s = {'+initial.join(', ')+'}':(valid?'Effects pending':'No effects')),13,'#475569');
      svg.innerHTML=out;
      status.textContent=`${t.step} ${step}/4 · ${pre?(valid?t.valid:t.invalid):'s = {'+initial.join(', ')+'}'} · ${final?t.output+': {'+successor.join(', ')+'}':t.preview}`;
    }
    function renderGraphplan(){
      // Planning-graph fact sets: persistence and two grounded move actions.
      const moves=[['A','B'],['B','C']];let factLayers=[new Set(['A'])];
      for(let i=0;i<2;i++){const next=new Set(factLayers[i]);moves.forEach(([from,to])=>{if(factLayers[i].has(from))next.add(to);});factLayers.push(next);}
      const pairMutex=(a,b)=>a!==b; // single-location invariant in this toy domain
      let out=rect(12,9,696,231,'#fff','#d3dbea');
      const xs=[82,324,566];
      for(let i=0;i<3;i++){
        const shown=i<=Math.min(step,2),x=xs[i];
        out+=label(x+55,40,'F'+i,19,shown?'#1e293b':'#94a3b8');
        const names=['A','B','C'];
        names.forEach((name,j)=>{const avail=shown&&factLayers[i].has(name);out+=pill(x,54+j*53,'At('+name+')',avail);});
        if(shown&&factLayers[i].has('A')&&factLayers[i].has('B'))out+=line(x+132,86,x+132,135,'#d44860',true);
      }
      if(step>=1){out+=line(218,75,296,128,'#2c8b7a');out+=label(257,80,'Move AB',12);}
      if(step>=2){out+=line(458,128,536,181,'#2c8b7a');out+=label(497,130,'Move BC',12);}
      if(step>=3){const rejected=goal==='AB';out+=rect(255,207,210,28,rejected?'#ffe1e6':'#d7f5e6',rejected?'#c54966':'#0d906b',6);out+=label(360,226,rejected?'mutex: A × B':'goal: At(C)',14,rejected?'#9f2949':'#147154');}
      svg.innerHTML=out;
      const current=goal==='AB'?['A','B']:['C'];
      const layer=new Set(factLayers[Math.min(step,2)]),included=current.every(x=>layer.has(x));
      const conflict=current.some((x,i)=>current.slice(i+1).some(y=>pairMutex(x,y)));
      status.textContent=`${t.step} ${step}/4 · F${Math.min(step,2)}={${[...layer].map(x=>'At('+x+')').join(', ')}} · ${step>=3?(conflict?t.reject:included&&step===4?t.accept:t.possible):t.possible}`;
    }
    function render(){seek.value=String(step);if(kind==='strips')renderStrips();else renderGraphplan();}
    function goto(n){step=Math.max(0,Math.min(max,n));render();if(step===max)stop();}
    function start(){if(playing)return;if(step===max)step=0;if(reduce()){render();return;}playing=true;play.textContent=t.pause;play.setAttribute('aria-pressed','true');timer=setInterval(()=>{if(!host.isConnected){stop();return;}goto(step+1);},850/speed);render();}
    host.querySelector('[data-a=prev]').addEventListener('click',()=>{stop();goto(step-1);});
    host.querySelector('[data-a=next]').addEventListener('click',()=>{stop();goto(step+1);});
    play.addEventListener('click',()=>playing?stop():start());
    seek.addEventListener('input',()=>{stop();goto(Number(seek.value));});
    host.querySelector('[data-a=speed]').addEventListener('change',e=>{speed=Number(e.target.value);if(playing){stop();start();}});
    host.querySelector('[data-a=reset]').addEventListener('click',()=>{stop();atA=true;charged=true;goal='C';for(const e of host.querySelectorAll('[data-p]')){if(e.type==='checkbox')e.checked=true;else e.value='C';}step=0;render();});
    host.querySelectorAll('[data-p]').forEach(el=>el.addEventListener('change',()=>{stop();atA=host.querySelector('[data-p=atA]')?.checked??true;charged=host.querySelector('[data-p=charged]')?.checked??true;goal=host.querySelector('[data-p=goal]')?.value??'C';render();}));
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    const media=window.matchMedia('(prefers-reduced-motion: reduce)');
    if(media.addEventListener)media.addEventListener('change',e=>{if(e.matches)stop();});
    labs.push(stop);render();
  }
  const enhance=()=>document.querySelectorAll('[data-planning-lab]').forEach(init);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  // Material for MkDocs instant navigation swaps pages without reloading JS.
  if (window.document$ && typeof window.document$.subscribe==='function') {
    window.document$.subscribe(() => enhance());
  }
})();
