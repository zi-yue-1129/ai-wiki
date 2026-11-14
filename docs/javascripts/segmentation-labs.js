/* Original CC BY-SA 4.0 educational simulations: not model inference. */
(() => {
  'use strict';
  const lang = (el) => el.dataset.lang === 'zh' ? 'zh' : 'en';
  const T = {
    en: {previous:'Previous',next:'Next',play:'Play',pause:'Pause',reset:'Reset',speed:'Speed',step:'Step',x:'Sample x',y:'Sample y',nearest:'Nearest',bilinear:'Bilinear',value:'Value',difference:'Difference',weights:'Corner weights',stage:['Sample','Four neighbours','Interpolate','Compare'],point:'Point only',box:'Point + box',candidate:'Candidate',whole:'Whole',part:'Part',subpart:'Subpart',mask:'Toy mask',allowed:'Possible masks',constrained:'Box-filtered mask',all:'All 3 plausible masks',single:'One constructed match',roiNote:'Synthetic feature values, not measured Mask R-CNN activations. Nearest-grid read is only a quantisation analogy.',samNote:'Constructed mask candidates and box filtering, not trained SAM predictions or confidence scores.'},
    zh: {previous:'上一步',next:'下一步',play:'播放',pause:'暫停',reset:'重設',speed:'速度',step:'步驟',x:'取樣 x',y:'取樣 y',nearest:'最近格點',bilinear:'雙線性插值',value:'數值',difference:'差距',weights:'四角權重',stage:['定位取樣點','取得四角','計算插值','比較結果'],point:'單點提示',box:'點提示＋框提示',candidate:'候選遮罩',whole:'整體',part:'部分',subpart:'子部分',mask:'人工遮罩',allowed:'可能的遮罩',constrained:'受框條件限制的遮罩',all:'三個合理候選',single:'人工規則選取一個',roiNote:'人工特徵值，非 Mask R-CNN 實測活化；最近格點取樣僅用於說明座標量化。',samNote:'人工遮罩候選與框條件篩選，非 SAM 模型推論或信心分數。'}
  };
  const grid = [
    [0.08,0.25,0.55,0.75],
    [0.15,0.40,0.68,0.85],
    [0.20,0.60,0.78,0.90],
    [0.35,0.55,0.72,0.95]
  ];
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  const fmt=v=>Number(v).toFixed(3);
  const mark=(t,attr='')=>`<text ${attr}>${t}</text>`;
  function controls(type,t) {
    return `<div class="seg-lab-controls"><button data-action="prev">${t.previous}</button><button data-action="toggle">${t.play}</button><button data-action="next">${t.next}</button><label>${t.step} <input data-action="seek" type="range" min="0" max="3" step="1" value="0"></label><label>${t.speed} <select data-action="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label><button data-action="reset">${t.reset}</button></div>`;
  }
  function surface(type, t) {
    if(type==='roi') return `<div class="seg-lab-options"><label>${t.x} <input data-axis="x" type="range" min="0.1" max="2.9" step="0.1" value="1.3"><output data-out="x">1.3</output></label><label>${t.y} <input data-axis="y" type="range" min="0.1" max="2.9" step="0.1" value="1.6"><output data-out="y">1.6</output></label></div>`;
    return `<div class="seg-lab-options"><label>${t.candidate} <select data-pick="mask"><option value="0">${t.whole}</option><option value="1">${t.part}</option><option value="2">${t.subpart}</option></select></label><label>${t.box} <input data-pick="box" type="checkbox"></label></div>`;
  }
  function roiState(x,y) {
    const x0=Math.floor(x),y0=Math.floor(y),u=x-x0,v=y-y0;
    const corners=[[x0,y0,(1-u)*(1-v)],[x0+1,y0,u*(1-v)],[x0,y0+1,(1-u)*v],[x0+1,y0+1,u*v]];
    const bi=corners.reduce((s,[cx,cy,w])=>s+grid[cy][cx]*w,0);
    const near=grid[Math.round(y)][Math.round(x)];
    return {corners,bi,near,x,y};
  }
  function roiSVG(st,step,t){
    const originX=46,originY=56,cell=76;
    let cells='';
    for(let j=0;j<4;j++)for(let i=0;i<4;i++){
      const shade=Math.round(244-grid[j][i]*105);
      const weight=st.corners.find(c=>c[0]===i&&c[1]===j)?.[2]||0;
      const stroke=step>=1&&weight>0?'#f59e0b':'#b3c9d8';
      cells+=`<rect x="${originX+i*cell}" y="${originY+j*cell}" width="${cell}" height="${cell}" fill="rgb(${shade},${shade+3},250)" stroke="${stroke}" stroke-width="${step>=1&&weight>0?3:1}"/>`;
      cells+=mark(grid[j][i].toFixed(2),`x="${originX+i*cell+11}" y="${originY+j*cell+22}" fill="#1f3548" font-size="15" text-anchor="start"`);
    }
    const px=originX+cell/2+st.x*cell,py=originY+cell/2+st.y*cell;
    let rings='';
    if(step>=1) for(const [cx,cy,w] of st.corners){
      const tx=originX+cell/2+cx*cell,ty=originY+cell/2+cy*cell;
      rings+=`<line x1="${px}" y1="${py}" x2="${tx}" y2="${ty}" stroke="#dd7c16" stroke-dasharray="4 4" stroke-width="2" opacity=".85"/>`;
      rings+=`<circle cx="${tx}" cy="${ty}" r="${4+9*Math.sqrt(w)}" fill="none" stroke="#de831f" stroke-width="2"/>`;
    }
    const bar=(name,val,y,color)=>`<text x="416" y="${y-13}" font-size="16" fill="#294356">${name} ${fmt(val)}</text><rect x="416" y="${y}" width="234" height="19" rx="5" fill="#e6eef4"/><rect x="416" y="${y}" width="${234*val}" height="19" rx="5" fill="${color}"/>`;
    const sums=st.corners.map(([cx,cy,w])=>fmt(w)).join(' · ');
    return `<svg viewBox="0 0 690 435" role="img" aria-label="Bilinear interpolation sample with four neighbours"><rect width="690" height="435" rx="14" fill="#f9fbff"/>${mark('Feature grid', 'x="46" y="31" font-size="19" font-weight="600" fill="#263c52"')}${cells}${rings}<circle cx="${px}" cy="${py}" r="9" fill="#fb8a1d" stroke="white" stroke-width="3"/><text x="416" y="62" fill="#263c52" font-size="18" font-weight="600">${T.en.stage[step]}</text>${bar('Nearest',st.near,126,'#64748b')}${step>=2?bar('Bilinear',st.bi,210,'#0b8b9b'):''}${step>=3?mark('Δ '+fmt(Math.abs(st.near-st.bi)),'x="416" y="295" font-size="19" fill="#d06415"'):''}${step>=1?mark('w: '+sums,'x="416" y="362" font-size="14" fill="#39536b"'):''}<text x="416" y="401" font-size="14" fill="#64748b">x=${st.x.toFixed(1)}  y=${st.y.toFixed(1)}</text></svg>`;
  }
  const sets=[
    Array.from({length:8},(_,r)=>Array.from({length:8},(_,c)=> (c-3.5)**2/15+(r-3.5)**2/15<1.0)),
    Array.from({length:8},(_,r)=>Array.from({length:8},(_,c)=> (c-3.5)**2/8+(r-3.5)**2/8<1.0)),
    Array.from({length:8},(_,r)=>Array.from({length:8},(_,c)=> (c-3.5)**2/3+(r-3.5)**2/3<1.0))
  ];
  function samSVG(s,step,t){
    const candidateColors=['#0c8795','#c07829','#7460b6'];
    let g='';
    for(let r=0;r<8;r++)for(let c=0;c<8;c++){
      const cell=35, cx=42+c*cell,cy=60+r*cell;
      g+=`<rect x="${cx}" y="${cy}" width="${cell}" height="${cell}" fill="${sets[s.mask][r][c]?'#59bcb4':'#e7eef6'}" stroke="white" stroke-width="2"/>`;
    }
    let candidates='';
    for(let i=0;i<3;i++){
      const x=388+i*92, y=144, selected=s.mask===i;
      candidates+=`<rect x="${x}" y="${y}" width="74" height="74" rx="10" fill="${selected?'#eaf9fa':'#f4f5fa'}" stroke="${selected?'#0c8795':'#bdc9d5'}" stroke-width="${selected?3:1}"/>`;
      candidates+=`<circle cx="${x+37}" cy="${y+37}" r="${[28,21,12][i]}" fill="${candidateColors[i]}" opacity="${s.box&&i!==s.mask&&step>=2?'.18':'.8'}"/>`;
      candidates+=mark(['Whole','Part','Subpart'][i],`x="${x+37}" y="${y+95}" text-anchor="middle" font-size="13" fill="#344b60"`);
      if(s.box&&step>=2&&i!==s.mask)candidates+=`<line x1="${x+10}" y1="${y+62}" x2="${x+64}" y2="${y+13}" stroke="#c55050" stroke-width="2"/>`;
    }
    const bbox=s.box&&step>=2?`<rect x="${42+[0,1,2][s.mask]*32}" y="${60+[0,1,2][s.mask]*32}" width="${280-[0,1,2][s.mask]*64}" height="${280-[0,1,2][s.mask]*64}" fill="none" stroke="#db8b26" stroke-width="4" stroke-dasharray="8 5"/>`:'';
    const count=sets[s.mask].flat().filter(Boolean).length;
    return `<svg viewBox="0 0 690 420" role="img" aria-label="Nested synthetic masks and point box prompts"><rect width="690" height="420" rx="14" fill="#f9fbff"/>${mark('Toy image','x="42" y="34" font-size="18" font-weight="600" fill="#294358"')}${g}${step>=1?`<circle cx="182" cy="200" r="7" fill="#fc8c17" stroke="white" stroke-width="3"/>`:''}${bbox}${mark('Candidate masks','x="388" y="111" font-size="18" font-weight="600" fill="#294358"')}${candidates}${mark((s.box&&step>=2?'Point + box':'Point'), 'x="388" y="304" font-size="17" fill="#2f5c65"')}${mark('Cells: '+count,'x="388" y="339" font-size="16" fill="#425b6f"')}${step>=3?mark(s.box?'1 toy match':'3 plausible masks','x="388" y="372" font-size="17" font-weight="600" fill="#c07829"'):''}</svg>`;
  }
  function attach(host){
    if(host.dataset.segReady)return;host.dataset.segReady='yes';
    const type=host.dataset.segLab, t=T[lang(host)],state={step:0,speed:1,x:1.3,y:1.6,mask:0,box:false};
    host.innerHTML=`<div class="seg-lab-frame"><div class="seg-lab-scroll" tabindex="0" role="region" aria-label="${type==='roi'?'Bilinear interpolation':'Mask candidates'}"><div class="seg-lab-art" data-art></div></div>${surface(type,t)}${controls(type,t)}<output class="seg-lab-readout" data-readout aria-live="polite"></output><p class="seg-lab-note">${type==='roi'?t.roiNote:t.samNote}</p></div>`;
    let timer=null;
    const $=s=>host.querySelector(s);
    function stop(){if(timer!==null){clearInterval(timer);timer=null;}}
    function draw(){
      const lab=type==='roi'?roiState(state.x,state.y):state;
      $('[data-art]').innerHTML=type==='roi'?roiSVG(lab,state.step,t):samSVG(lab,state.step,t);
      const read=type==='roi'?`${t.stage[state.step]} · (${state.x.toFixed(1)}, ${state.y.toFixed(1)}) · ${t.nearest}: ${fmt(lab.near)} · ${t.bilinear}: ${fmt(lab.bi)} · ${t.difference}: ${fmt(Math.abs(lab.near-lab.bi))}`:`${t.stage[state.step]} · ${state.box?t.single:t.all} · ${[t.whole,t.part,t.subpart][state.mask]}`;
      $('[data-readout]').textContent=read;
      $('[data-action="seek"]').value=String(state.step);
      $('[data-action="toggle"]').textContent=timer===null?t.play:t.pause;
      host.querySelectorAll('[data-axis]').forEach(n=>{const o=$(`[data-out="${n.dataset.axis}"]`);o.textContent=state[n.dataset.axis].toFixed(1);});
    }
    function advance(){state.step=(state.step+1)%4;draw();}
    function start(){if(window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;stop();timer=setInterval(advance,1300/state.speed);draw();}
    host.addEventListener('input',e=>{
      const axis=e.target.dataset.axis,action=e.target.dataset.action;
      if(axis){state[axis]=Number(e.target.value);stop();draw();}
      if(action==='seek'){state.step=Number(e.target.value);stop();draw();}
    });
    host.addEventListener('change',e=>{
      const pick=e.target.dataset.pick,action=e.target.dataset.action;
      if(pick){state[pick]=pick==='box'?e.target.checked:Number(e.target.value);stop();draw();}
      if(action==='speed'){state.speed=Number(e.target.value);if(timer!==null)start();}
    });
    host.addEventListener('click',e=>{
      const a=e.target.closest('button[data-action]')?.dataset.action;
      if(!a)return;
      if(a==='toggle'){if(timer!==null)stop();else start();}
      else {stop();if(a==='next')state.step=Math.min(3,state.step+1);if(a==='prev')state.step=Math.max(0,state.step-1);if(a==='reset'){
        Object.assign(state,{step:0,speed:1,x:1.3,y:1.6,mask:0,box:false});
        host.querySelectorAll('[data-axis]').forEach(n=>n.value=String(state[n.dataset.axis]));
        if($('[data-pick="mask"]'))$('[data-pick="mask"]').value='0';
        if($('[data-pick="box"]'))$('[data-pick="box"]').checked=false;
        $('[data-action="speed"]').value='1';
      }}draw();
    });
    document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();draw();}});
    draw();
  }
  function init(){document.querySelectorAll('[data-seg-lab]').forEach(attach);}
  if(typeof document$!=='undefined'&&document$?.subscribe)document$.subscribe(init);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
